from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.base import async_session
from db import requests as db
from config import ADMIN_IDS
from keyboards.reply import main_menu
import messages as T

router = Router()


# ── FSM ──────────────────────────────────────────────

class SupportForm(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()


# ── USER ASKS QUESTION ───────────────────────────────

@router.message(F.text == T.BTN_ASK)
async def support_start(message: Message, state: FSMContext):
    await state.set_state(SupportForm.waiting_for_question)
    await message.answer(T.SUPPORT_ASK, parse_mode="MarkdownV2")


@router.message(SupportForm.waiting_for_question)
async def process_question(message: Message, state: FSMContext, bot: Bot):
    question = message.text
    x = [T.BTN_EVENTS, T.BTN_MY_REGS, T.BTN_ASK]
    if question in x:
        await state.clear()
        await message.answer(T.SUPPORT_MISCLICK)
        return
    # Save ticket to DB
    async with async_session() as session:
        ticket = await db.create_ticket(session, message.from_user.id, question)
        mod_ids = await db.get_moderator_ids(session)

    await state.clear()
    await message.answer(T.SUPPORT_RECEIVED, parse_mode="MarkdownV2")

    # Build reply button for moderators
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=T.BTN_ANSWER,
                callback_data=f"answer_{ticket.id}"
            )
        ]]
    )

    # Forward question to admin and all moderators
    staff_ids = set(mod_ids + ADMIN_IDS)
    for staff_id in staff_ids:
        try:
            await bot.send_message(
                chat_id=staff_id,
                text=T.NEW_TICKET.format(
                    name=message.from_user.full_name,
                    username=message.from_user.username,
                    ticket_id=ticket.id,
                    question=question
                ),
                reply_markup=reply_keyboard
            )
        except Exception as e:
            print(f"Could not notify staff {staff_id}: {e}")


# ── MODERATOR ANSWERS ────────────────────────────────

@router.callback_query(F.data.startswith("answer_"))
async def start_answer(callback: CallbackQuery, state: FSMContext):
    # Check if user is admin or moderator
    ticket_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        is_mod = await db.is_moderator(session, callback.from_user.id)
        answered = await db.is_answered(session, ticket_id)

    is_admin = callback.from_user.id in ADMIN_IDS
    if answered:
        await callback.answer(T.TICKET_ALREADY_ANSWERED)
        return
    if not is_mod and not is_admin:
        await callback.answer(T.ACCESS_DENIED, show_alert=True)
        return

    await state.update_data(ticket_id=ticket_id)
    await state.set_state(SupportForm.waiting_for_answer)

    await callback.message.edit_text(
        callback.message.text + "\n\n" + T.WRITE_ANSWER
    )
    await callback.answer()


@router.message(SupportForm.waiting_for_answer)
async def process_answer(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    ticket_id = data["ticket_id"]
    answer = message.text

    async with async_session() as session:
        ticket = await db.get_ticket_by_id(session, ticket_id)
        if not ticket:
            await message.answer(T.TICKET_NOT_FOUND)
            await state.clear()
            return

        await db.answer_ticket(session, ticket_id, answer)
        user_id = ticket.user_id

    await state.clear()

    # Send answer back to user
    try:
        if answer == T.BTN_MAIN_MENU :
            return
        await bot.send_message(
            chat_id=user_id,
            text=T.ANSWER_TO_USER.format(question=ticket.question, answer=answer)
        )
        await message.answer(T.ANSWER_SENT, reply_markup=main_menu)
    except Exception as e:
        await message.answer(T.ANSWER_FAILED.format(error=e))
