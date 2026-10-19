from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.base import async_session
from keyboards.inline import notification_keyboard
from db.models import Registration, Event
from asyncio import sleep
import messages as T


async def send_reminders(bot, days_before: int):
    """Sends reminders to all users registered for events happening in X days."""
    now = datetime.now()
    target_date = now + timedelta(days=days_before)

    async with async_session() as session:
        result = await session.execute(
            select(Event)
            .where(
                Event.is_active == True,
                Event.date >= target_date.replace(hour=0, minute=0, second=0),
                Event.date <= target_date.replace(hour=23, minute=59, second=59),
            )
        )
        events = result.scalars().all()
        print(f"DEBUG: Found {len(events)} events")
        if not events:
            return

        for event in events:
            reg_result = await session.execute(
                select(Registration)
                .where(Registration.event_id == event.id)
                .where(Registration.is_waitlist.is_not(True))
                .options(selectinload(Registration.user))
            )
            registrations = reg_result.scalars().all()

            for reg in registrations:
                
                    try:
                        template = T.REMINDER_3_DAYS if days_before == 3 else T.REMINDER_1_DAY
                        text = template.format(
                            title=event.title,
                            date=event.date.strftime('%d.%m.%Y %H:%M')
                        )
                        await sleep(0.05)
                        await bot.send_message(chat_id=reg.user_id, text=text, reply_markup = notification_keyboard(reg.event_id))

                    except Exception as e:
                        print(f"Could not send reminder to {reg.user_id}: {e}")




def setup_scheduler(bot) -> AsyncIOScheduler:
    """SETUP SCHEDULER TO SEND REMAINDERS IN 1 AND 3 DAYS BEFORE EVENT"""
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        send_reminders,
#        DateTrigger(run_date=datetime.now() + timedelta(seconds=10)),  triggers 10 seconds after bot start for tests 
        CronTrigger(hour=10, minute=0),
        args=[bot, 3],
        id="reminder_3_days"
    )

    scheduler.add_job(
        send_reminders,
        CronTrigger(hour=10, minute=0),
        args=[bot, 1],
        id="reminder_1_day"
    )

    return scheduler