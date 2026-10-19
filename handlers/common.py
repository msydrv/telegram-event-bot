from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.reply import main_menu
import messages as T
from keyboards.inline import event_keyboard, waitlist_keyboard
from db.models import Registration
from db import requests as db
from db.base import async_session
from sqlalchemy import select
router = Router()

# ___________________________Start___________


from aiogram.fsm.state import State, StatesGroup

class RegistrationForm(StatesGroup):
    waiting_for_name = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    async with async_session() as session:
        user = await db.get_or_create_user(session, message.from_user)

    if not user.full_name:
        await state.set_state(RegistrationForm.waiting_for_name)
        await message.answer(T.WELCOM, parse_mode="MarkdownV2")
    else:
        await message.answer(
            T.COME_BACK, reply_markup=main_menu
        )


@router.message(RegistrationForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    full_name = message.text
    try:
        if not full_name.replace(" ", "").isalpha():
            raise ValueError

    except ValueError:
        await message.answer(
                    T.NAME_INVALID, parse_mode= "MarkdownV2"
                )
        return


    async with async_session() as session:
        await db.set_user_name(session, message.from_user.id, full_name)

    await state.clear()

    await message.answer(
        T.REGISTRATION, reply_markup= main_menu
    )


# ___________________________NextEvent___________

@router.message(F.text == T.BTN_EVENTS)
async def next_events(message: Message):
    async with async_session() as session:
        events = await db.get_active_events(session)

        if not events:
            await message.answer(T.NO_FUTURE_EVENTS)
            return

        await message.answer(T.NEXT_EVENTS)
        for event in events:
            is_registered = await db.is_user_registered(
                session,
                user_id=message.from_user.id,
                event_id=event.id
            )
            confirmed_count = await db.get_event_registered_count(session, event.id)

            # Build capacity string
            if event.capacity:
                spots_left = event.capacity - confirmed_count
                if spots_left > 0:
                    capacity_text = T.CAPACITY_FREE.format(spots=spots_left)
                    keyboard = event_keyboard(event.id, is_registered)
                elif spots_left >= -19:
                    capacity_text = T.CAPACITY_FULL_WAITLIST.format(count=confirmed_count, capacity=event.capacity)
                    keyboard = event_keyboard(event.id, is_registered)
                else:
                    capacity_text = T.CAPACITY_FULL.format(count=confirmed_count, capacity=event.capacity)
                    keyboard = None
            else:
                capacity_text = T.CAPACITY_UNLIMITED.format(count=confirmed_count)

            await message.answer(
                f"🎯 <b>{event.title}</b>\n\n"
                f"📝 {event.description}\n\n"
                f"📆 <b>{event.date.strftime('%d.%m.%Y %H:%M')}</b>\n"
                f"<b>{capacity_text}</b>",
                reply_markup=keyboard,
                parse_mode= "HTML"
            )




#__________________________Event Reg______________

#### Queue for events and notification in case of free place,
### oportunity to cancel registration via button durning notification


@router.callback_query(F.data == "nottrue")
async def confirm_attendance(callback: CallbackQuery):
    await callback.message.answer(T.ATTENDANCE_CONFIRMED)


@router.callback_query(F.data.startswith("register_"))
async def register_for_event(callback: CallbackQuery, bot: Bot):
    event_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        # Check capacity first before registering
        event = await db.get_event_by_id(session, event_id)
        confirmed_count = await db.get_event_registered_count(session, event_id)

        if event.capacity and confirmed_count >= event.capacity:
            # Event is full — ask if they want to join waitlist
            await callback.message.edit_text(
                callback.message.text + "\n\n" + T.EVENT_FULL_ASK_WAITLIST,
                reply_markup=waitlist_keyboard(event_id)
            )
            await callback.answer()
            return

        # Spot available — register normally
        result = await db.register_user_for_event(
            session,
            user_id=callback.from_user.id,
            event_id=event_id,
            username=callback.from_user.username
        )

    if result == "registered":
        await callback.message.edit_text(
            callback.message.text,
            reply_markup=event_keyboard(event_id, is_registered=True)
        )
        await callback.message.answer(T.REGISTERED)
        await callback.message.answer(T.EVENT_LOCATION.format(address=await db.get_adress(session, event_id=event_id)))
    else:
        await callback.message.answer(T.ALREADY_REGISTERED)


# ── WAITLIST CONFIRMATION ─────────────────────────────

@router.callback_query(F.data.startswith("waitlist_yes_"))
async def join_waitlist(callback: CallbackQuery):
    event_id = int(callback.data.split("_")[2])

    async with async_session() as session:
        existing = await session.execute(
            select(Registration).where(
                Registration.user_id == callback.from_user.id,
                Registration.event_id == event_id
            )
        )
        if existing.scalar():
            await callback.message.answer(T.ALREADY_IN_LIST, show_alert=True)
            return

        registration = Registration(
            user_id=callback.from_user.id,
            event_id=event_id,
            username=callback.from_user.username,
            is_waitlist=True
        )
        session.add(registration)
        await session.commit()

    await callback.message.edit_text(T.WAITLIST_JOINED)
    await callback.answer()


@router.callback_query(F.data.startswith("waitlist_no_"))
async def decline_waitlist(callback: CallbackQuery):
    event_id = int(callback.data.split("_")[2])

    # Restore original event message
    await callback.message.edit_text(
        # Remove the waitlist question we added
        callback.message.text.split("\n\n⚠️")[0],
        reply_markup=event_keyboard(event_id, is_registered=False)
    )
    await callback.answer()



@router.callback_query(F.data.startswith("unregister_"))
async def unregister_from_event(callback: CallbackQuery, bot: Bot):
    event_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        result = await db.cancel_registration(
            session,
            user_id=callback.from_user.id,
            event_id=event_id,
        )

    if result["cancelled"]:
        await callback.message.edit_text(
            callback.message.text,
            reply_markup=event_keyboard(event_id, is_registered=False)
        )
        await callback.message.answer(T.REG_CANCELLED)

        # Notify promoted user from waitlist
        if result["promoted"]:
            promoted = result["promoted"]
            async with async_session() as session:
                adress = await db.get_adress(session, event_id=event_id)
            try:
                await bot.send_message(
                    chat_id=promoted.id,
                    text=T.PROMOTED.format(address=adress)
                )
            except Exception as e:
                print(f"Could not notify promoted user {promoted.id}: {e}")
    else:
        await callback.answer(T.NOT_REGISTERED, show_alert=True)


# ___________________________My Events___________

@router.message(F.text == T.BTN_MY_REGS)
async def myEvents(message: Message):
    async with async_session() as session:
        registrations = await db.get_user_registrations(session, message.from_user.id)

    if not registrations:
        await message.answer(T.NO_MY_EVENTS, parse_mode="MarkdownV2")
        return

    for reg in registrations:
        if not reg.event.is_active:
            continue
        else:
            if reg.is_waitlist:
                tmp = T.MY_REG_WAITLIST_NOTE
            else:
                tmp = ""
            await message.answer(f"🎟 <b>{reg.event.title}</b>:  {reg.event.date.strftime('%d.%m.%Y %H:%M')} {tmp}", parse_mode="HTML",
                                reply_markup=event_keyboard(reg.event_id, is_registered=True))
