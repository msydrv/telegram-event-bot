from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User, Event, Registration, Moderator, SupportTicket
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

#------------Users

async def get_or_create_user(session: AsyncSession, tg_user) -> User:
    user = await session.get(User, tg_user.id)
    if not user:
        user = User(
            id=tg_user.id,
            username=tg_user.username,
            full_name = None
        )
        session.add(user)
        await session.commit()
    return user

async def set_user_name(session: AsyncSession, user_id: int, full_name: str) -> User:     
    user = await session.get(User, user_id)
    if user:
        user.full_name = full_name
        await session.commit()
    

#-------------Events

async def get_active_events(session: AsyncSession) -> list[Event]:
    result = await session.execute(
        select(Event).where(Event.is_active == True)
    )
    return result.scalars().all()

async def get_event_by_id(session: AsyncSession, event_id: int) -> Event | None:
    return await session.get(Event, event_id)


#--------------registrations

async def get_event_registered_count(
    session: AsyncSession,
    event_id: int
) -> int:
    """Returns number of confirmed (non-waitlist) registrations."""
    result = await session.execute(
        select(Registration).where(
            Registration.event_id == event_id,
            
        )
    )
    return len(result.scalars().all())

async def get_adress(session: AsyncSession, event_id: int) -> str:
    result = await session.execute(select(Event.adress).where(Event.id == event_id))
    return result.scalar_one_or_none()


async def get_waitlist(
    session: AsyncSession,
    event_id: int
) -> list[Registration]:
    """Returns waitlist in order of registration."""
    result = await session.execute(
        select(Registration)
        .where(
            Registration.event_id == event_id,
            Registration.is_waitlist == True
        )
        .options(selectinload(Registration.user))
        .order_by(Registration.registered_at)  # FIFO order
    )
    return result.scalars().all()


async def register_user_for_event(
    session: AsyncSession,
    user_id: int,
    event_id: int,
    username: str | None = None
) -> str:
    """
    Returns:
        'registered'  — successfully registered
        'waitlist'    — added to waitlist (event full)
        'duplicate'   — already registered or on waitlist
    """
    # Check if already registered or on waitlist
    existing = await session.execute(
        select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
    )
    if existing.scalar():
        return "duplicate"

    # Check event capacity
    event = await session.get(Event, event_id)
    if event.capacity is not None:
        confirmed_count = await get_event_registered_count(session, event_id)
        if confirmed_count >= event.capacity:
            # Event is full — add to waitlist
            registration = Registration(
                user_id=user_id,
                event_id=event_id,
                username=username,
                is_waitlist=True
            )
            session.add(registration)
            await session.commit()
            return "waitlist"

    # Spot available — register normally
    registration = Registration(
        user_id=user_id,
        event_id=event_id,
        username=username,
        is_waitlist=False
    )
    session.add(registration)
    await session.commit()
    return "registered"


async def cancel_registration(
    session: AsyncSession,
    user_id: int,
    event_id: int
) -> dict:
    """
    Cancels registration and promotes first person from waitlist if exists.
    Returns dict with 'cancelled' bool and 'promoted' User or None.
    """
    result = await session.execute(
        select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
    )
    registration = result.scalar()
    if not registration:
        return {"cancelled": False, "promoted": None}

    was_confirmed = not registration.is_waitlist

    await session.delete(registration)
    await session.commit()

    # Only promote from waitlist if a confirmed spot was freed
    promoted_user = None
    if was_confirmed:
        waitlist = await get_waitlist(session, event_id)
        if waitlist:
            first_in_line = waitlist[0]
            first_in_line.is_waitlist = False
            await session.commit()

            # Load user for notification
            promoted_user = await session.get(User, first_in_line.user_id)

    return {"cancelled": True, "promoted": promoted_user}

#______________________ 

async def get_user_registrations(
    session: AsyncSession,
    user_id: int
) -> list[Registration]:
    result = await session.execute(
        select(Registration).where(Registration.user_id == user_id).options(selectinload(Registration.event))
    ) 
    return result.scalars().all()



async def is_user_registered(
        session: AsyncSession,
        user_id: int,
        event_id: int
) -> bool:
    result = await session.execute(
        select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
    )
    return result.scalar() is not None


#__________________________Admin_requests_____

async def get_all_registrations(session: AsyncSession) -> list[Registration]:
    result = await session.execute(
        select(Registration)
        .options(
            selectinload(Registration.user),
            selectinload(ReferenceError.event)
        )
    )
    return result.scalars().all()

async def get_all_events(session: AsyncSession) -> list[Event]:
    result = await session.execute(
        select(Event)
    )
    return result.scalars().all()

async def delete_event(session: AsyncSession, event_id: int) -> bool:
    event = await session.get(Event, event_id)
    if not event:
        return False
    
    await session.execute(
        delete(Registration).where(Registration.event_id == event_id)
    )
    await session.delete(event)
    await session.commit()
    return True

async def get_global_statistics(session: AsyncSession) -> dict:
    base = select(Registration).where(
        Registration.registered_at >= datetime.now() - timedelta(days=30)
    )

    users_result = len((await session.execute(select(User))).scalars().all())
    global_regs_result = len((await session.execute(select(Registration))).scalars().all())
    regs_last_month = len((await session.execute(base)).scalars().all())
    visited_last_month = len((await session.execute(
        base.where(
            Registration.attended == True,
            Registration.is_waitlist == False,
        )
    )).scalars().all())

    return {"t_users" : users_result,
            "t_regs" : global_regs_result,
            "t_regs_month" : regs_last_month,
            "t_regs_vis" : visited_last_month }
    

async def get_event_stat(session: AsyncSession) -> dict:
  
    # All events with their stats
    events_result = await session.execute(
        select(Event).options(selectinload(Event.registrations))
    )
    events = events_result.scalars().all()

    event_stats = []
    for event in events:
        confirmed = [r for r in event.registrations ] #### if not r.is_waitlist add at the end after waitlist implamantation 
        attended = [r for r in confirmed if r.attended == True]

        event_stats.append({
            "title": event.title,
            "date": event.date,
            "capacity": event.capacity,
            "registered": len(confirmed),
            "attended": len(attended),
            "is_active": event.is_active
        })

    return {
        
        "events": event_stats
    }

async def get_users_stat(session: AsyncSession):
    res = await session.execute(select(User.id ,User.username, User.full_name, func.count(Registration.user_id).label("attendance"))
                                  .join(Registration, Registration.user_id == User.id)
                                  .group_by(User.id, User.full_name)
                                    .where(
                                    Registration.is_waitlist == False
                                    )
                                  .having(func.count(Registration.user_id)>=2)
                                  .order_by(func.count().desc()))
    stats = res.all()

    result = []
    for us in stats:
        result.append({
            "username" : us.username,
            "full_name" : us.full_name,
            "attendance" : us.attendance,
        })

    return result

async def get_user_stat(session: AsyncSession, username: str) -> dict:
    user = (await session.execute(select(User.full_name, User.username, User.created_at)
                                  .where(User.username == username))).first()

    if user == None: 
        return None

    regs = (await session.execute(
        select(Event.title, Event.date)
        .join(Registration, Registration.event_id == Event.id)
        .where(Registration.username == username)
        .order_by(Event.date)
    )).all()
    
    return {
        "full_name" : user[0],
        "username" : user[1],
        "created_at" : user[2],
        "regs" : [tuple(r) for r in regs]
    }


# ── MODERATORS ──────────────────────────────────────

async def add_moderator(session: AsyncSession, user_id: int) -> bool:
    existing = await session.execute(
        select(Moderator).where(Moderator.user_id == user_id)
    )
    if existing.scalar():
        return False
    mod = Moderator(user_id=user_id)
    session.add(mod)
    await session.commit()
    return True

async def remove_moderator(session: AsyncSession, user_id: int) -> bool:
    result = await session.execute(
        select(Moderator).where(Moderator.user_id == user_id)
    )
    mod = result.scalar()
    if not mod:
        return False
    await session.delete(mod)
    await session.commit()
    return True

async def get_all_moderators(session: AsyncSession) -> list[Moderator]:
    result = await session.execute(
        select(Moderator).options(selectinload(Moderator.user))
    )
    return result.scalars().all()

async def is_moderator(session: AsyncSession, user_id: int) -> bool:
    result = await session.execute(
        select(Moderator).where(Moderator.user_id == user_id)
    )
    return result.scalar() is not None

async def get_moderator_ids(session: AsyncSession) -> list[int]:
    result = await session.execute(select(Moderator.user_id))
    return list(result.scalars().all())

# ── SUPPORT TICKETS ─────────────────────────────────

async def create_ticket(
    session: AsyncSession,
    user_id: int,
    question: str
) -> SupportTicket:
    ticket = SupportTicket(user_id=user_id, question=question)
    session.add(ticket)
    await session.commit()
    return ticket

async def get_open_tickets(session: AsyncSession) -> list[SupportTicket]:
    result = await session.execute(
        select(SupportTicket)
        .where(SupportTicket.is_answered == False)
        .options(selectinload(SupportTicket.user))
    )
    return result.scalars().all()

async def get_ticket_by_id(
    session: AsyncSession,
    ticket_id: int
) -> SupportTicket | None:
    result = await session.execute(
        select(SupportTicket)
        .where(SupportTicket.id == ticket_id)
        .options(selectinload(SupportTicket.user))
    )
    return result.scalar()

async def answer_ticket(
    session: AsyncSession,
    ticket_id: int,
    answer: str
) -> bool:
    ticket = await session.get(SupportTicket, ticket_id)
    if not ticket:
        return False
    ticket.answer = answer
    ticket.is_answered = True
    await session.commit()
    return True


async def is_answered(session: AsyncSession, ticket_id: int) -> bool:
    res = await session.execute(select(SupportTicket).where(SupportTicket.id == ticket_id))
    return res.scalar().is_answered

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(
        select(User).where(User.username == username)
    )
    return result.scalar()

# _______________________

async def deactivate_event(session: AsyncSession, event_id: int) -> bool:
    event = await session.get(Event, event_id)
    if not event:
        return False
    event.is_active = False
    await session.commit()
    return True



async def get_event_registrations(
    session: AsyncSession,
    event_id: int
) -> list[Registration]:
    result = await session.execute(
        select(Registration)
        .where(Registration.event_id == event_id)
        .options(selectinload(Registration.user))
    )
    return result.scalars().all()

async def mark_attendance(
    session: AsyncSession,
    registration_id: int,
    attended: bool
) -> bool:
    reg = await session.get(Registration, registration_id)
    if not reg:
        return False
    reg.attended = attended
    await session.commit()
    return True

#__________________________________Change Event_____
async def change_capacity(
    session: AsyncSession,
    event_id: int,
    new_capacity: int
) -> bool:
    event = await session.get(Event, event_id)
    if not event:
        return False
    event.capacity = new_capacity
    await session.commit()
    return True

async def change_name(
    session: AsyncSession,
    event_id: int,
    name: str
) -> bool:
    event = await session.get(Event, event_id)
    if not event:
        return False
    event.title = name
    await session.commit()
    return True

async def change_description(
        session : AsyncSession,
        event_id: int,
        description: str
) -> bool:
    event = await session.get(Event, event_id)
    if not event:
        return False
    event.description = description
    await session.commit()
    return True