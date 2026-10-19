from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from db.base import async_session
from db import requests as db
from config import ADMIN_IDS
from keyboards.inline import attendance_keyboard
from keyboards.reply import staff_menu, main_menu, MENU_BUTTONS, admin_menu
import messages as T

router = Router()


# ── FSM ──────────────────────────────────────────────

class StaffForm(StatesGroup):
    waiting_for_event_id = State()


# ── ACCESS CHECK ─────────────────────────────────────

async def is_staff(user_id: int) -> bool:
    if user_id in ADMIN_IDS:
        return True
    async with async_session() as session:
        return await db.is_moderator(session, user_id)


# ── ALL REGISTRATIONS ────────────────────────────────

@router.message(Command("mod"))
async def mod_panel(message: Message):
    await message.answer(T.MOD_MENU_OPENED, reply_markup=staff_menu)




BACK_TEXTS = {T.BTN_BACK, T.BTN_MAIN_MENU}

@router.message(F.text.in_(BACK_TEXTS))
async def return_to_menu(message: Message, state: FSMContext):
    await state.clear()
    menu = admin_menu if message.from_user.id in ADMIN_IDS else main_menu
    await message.answer(T.MAIN_MENU_OPENED, reply_markup=menu)

@router.message(F.text == T.BTN_ALL_REGS)
async def ask_event_id(message: Message, state: FSMContext):
    if not await is_staff(message.from_user.id):
        return

    async with async_session() as session:
        events = await db.get_all_events(session)


    if not events:
        await message.answer(T.NO_EVENTS)
        return
    events.sort(key=lambda e: e.id)
    text = T.CHOOSE_EVENT_ID
    for event in events:
        regs = await db.get_event_registrations(session, event.id)
        text += f"ID: {event.id} — {event.title} ({event.date.strftime('%d.%m.%Y')}) - {len(regs)}/{event.capacity}\n"


    await state.set_state(StaffForm.waiting_for_event_id)
    await message.answer(text)


@router.message(StaffForm.waiting_for_event_id)
async def show_registrations(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer(T.INVALID_EVENT_ID)
        return


    event_id = int(message.text)
    await state.clear()
    async with async_session() as session:
        event = await db.get_event_by_id(session, event_id)
        if not event:
            await message.answer(T.EVENT_NOT_FOUND.format(event_id=event_id))
            return

        registrations = await db.get_event_registrations(session, event_id)

    if not registrations:
        await message.answer(T.NO_REGISTRATIONS.format(title=event.title))
        return

    await message.answer(
        T.REGISTRATIONS_HEADER.format(
            title=event.title,
            date=event.date.strftime('%d.%m.%Y %H:%M'),
            count=len(registrations)
        )
    )

    # Send each participant as a separate message with attendance buttons
    registrations.sort(key=lambda x: x.registered_at)
    for reg in registrations:
        if reg.attended is True:
            status = T.STATUS_CAME
        elif reg.attended is False:
            status = T.STATUS_ABSENT
        else:
            status = T.STATUS_UNMARKED
        if reg.is_waitlist:
            tmp = T.WAITLIST_YES
        else:
            tmp = T.WAITLIST_NO
        await message.answer(
            T.PARTICIPANT_CARD.format(
                name=reg.user.full_name,
                waitlist=tmp,
                username=reg.user.username,
                date=reg.registered_at.strftime('%d.%m.%Y'),
                status=status
            ),
            reply_markup=attendance_keyboard(reg.id, reg.attended)
        )


# ── ATTENDANCE CALLBACKS ─────────────────────────────

@router.callback_query(F.data.startswith("att_"))
async def mark_attendance(callback: CallbackQuery):
    if not await is_staff(callback.from_user.id):
        await callback.answer(T.STAFF_ACCESS_DENIED, show_alert=True)
        return

    # Format: att_true_1, att_false_1, att_none_1
    parts = callback.data.split("_")
    status = parts[1]   # true / false / none
    reg_id = int(parts[2])

    attended = None
    if status == "true":
        attended = True
    elif status == "false":
        attended = False

    async with async_session() as session:
        await db.mark_attendance(session, reg_id, attended)

    # Update the message with new buttons
    if attended is True:
        status_text = T.STATUS_CAME
    elif attended is False:
        status_text = T.STATUS_ABSENT
    else:
        status_text = T.STATUS_UNMARKED

    # Rebuild message text with updated status
    lines = callback.message.text.split("\n")
    new_text = "\n".join(lines[:3]) + "\n" + T.STATUS_LINE.format(status=status_text)

    await callback.message.edit_text(
        new_text,
        reply_markup=attendance_keyboard(reg_id, attended)
    )
    await callback.answer()
