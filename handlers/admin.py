from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import admin_menu, main_menu, MENU_BUTTONS, admin_menu_with_, admin_menu_control, stat_menu
from db.base import async_session
from db import requests as db
from config import ADMIN_IDS
from datetime import datetime
from db.models import Event, User
from asyncio import sleep
import messages as T




router = Router()


### ADMIN Filter

router.message.filter(F.from_user.id.in_(ADMIN_IDS))
router.callback_query.filter(F.from_user.id.in_(ADMIN_IDS))


class AddEventForm(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_capacity = State()
    waiting_for_address = State()
    waiting_for_date = State()


#_________Admin Menu_________

@router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer(T.ADMIN_MENU_OPENED, reply_markup=admin_menu)

@router.message(F.text == T.BTN_MAIN_MENU)
async def back_to_main(message: Message):
    await message.answer(T.MAIN_MENU_OPENED, reply_markup=main_menu)


@router.message(F.text == T.BTN_BACK)
async def back_to_adm_menu(message: Message, state : FSMContext):
    await state.clear()
    await message.answer(T.MAIN_MENU_OPENED, reply_markup=admin_menu)





#_________Statistics__________


@router.message(F.text == T.BTN_STATS)
async def statistics(message: Message):
    async with async_session() as session:
        stats = await db.get_global_statistics(session)

    text = T.GLOBAL_STATS.format(
        users=stats["t_users"],
        regs=stats["t_regs"],
        regs_month=stats["t_regs_month"],
        visited=stats["t_regs_vis"]
    )
    await message.answer(text, reply_markup=stat_menu)



@router.message(F.text == T.BTN_BY_EVENT)
async def event_stats(message: Message):
    async with async_session() as session:
        stats = await db.get_event_stat(session)
    text = T.EVENT_STATS_HEADER
    if not stats["events"]:
        text += T.EVENT_STATS_EMPTY
    else:
        for event in stats["events"]:
            status = T.EVENT_ACTIVE if event["is_active"] else T.EVENT_FINISHED
            capacity_text = str(event["capacity"]) if event["capacity"] else "∞"

            text += T.EVENT_STATS_ITEM.format(
                title=event['title'],
                status=status,
                attended=event['attended'],
                capacity=capacity_text,
                registered=event['registered']
            )
    if len(text) > 4096:
        for i in range(0, len(text), 4096):
            await message.answer(text[i:i+4096])
    else:
        await message.answer(text)


@router.message(F.text == T.BTN_BY_USER)
async def users_stat(message: Message):
    async with async_session() as session:
        stats = await db.get_users_stat(session)

    text = T.TOP_USERS_HEADER

    i = 1
    for tmp in stats:
        text += T.TOP_USERS_ITEM.format(i=i, name=tmp["full_name"], username=tmp["username"], count=tmp["attendance"])
        if i == 100:
            break
        i += 1

    await message.answer(text)


@router.message(Command("userstat"))
async def get_user_s(message: Message):
    us = message.text.split(" ")
    if len(us) != 2:
        await message.answer(T.USERSTAT_USAGE)
        return

    username = us[1].lstrip("@")

    async with async_session() as session:
        user_stat = await db.get_user_stat(session, username)
        if not user_stat:
            await message.answer(T.USER_NOT_FOUND.format(username=username))
            return

    text = T.USER_STAT_HEADER.format(
        name=user_stat["full_name"],
        username=user_stat["username"],
        created=user_stat["created_at"]
    )

    i = 1
    for r in user_stat["regs"]:

        text += f"{i}: {r[0]} : {r[1]}\n"
        i +=1

    await message.answer(text)



#_______________ADD_EVENT____________

@router.message(F.text == T.BTN_ADD_EVENT)
async def add_event_start(message: Message, state: FSMContext):
    await state.set_state(AddEventForm.waiting_for_title)
    await message.answer(T.ASK_TITLE, reply_markup=admin_menu_with_)

@router.message(AddEventForm.waiting_for_title)
async def add_event_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddEventForm.waiting_for_description)
    await message.answer(T.ASK_DESCRIPTION)

@router.message(AddEventForm.waiting_for_description)
async def add_event_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(AddEventForm.waiting_for_capacity)
    await message.answer(T.ASK_CAPACITY)

@router.message(AddEventForm.waiting_for_capacity)
async def add_capacity(message: Message, state: FSMContext):
    try:
        await state.update_data(capacity = int(message.text))
        await state.set_state(AddEventForm.waiting_for_address)

        await message.answer(T.ASK_ADDRESS)
    except:
        await message.answer(T.INVALID_FORMAT)

@router.message(AddEventForm.waiting_for_address)
async def add_adress(message: Message, state: FSMContext):
    try:
        await state.update_data(adress = message.text)
        await state.set_state(AddEventForm.waiting_for_date)
        await message.answer(T.ASK_DATE)
    except:
        await message.answer(T.INVALID_FORMAT_ADDRESS)

@router.message(AddEventForm.waiting_for_date)
async def add_event_date(message: Message, state: FSMContext):

    try:
        date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")

    except ValueError:
        await message.answer(T.INVALID_DATE)
        return


    data = await state.get_data()
    await state.clear()

    async with async_session() as session:
        from db.models import Event
        event = Event(
            title=data["title"],
            description=data["description"],
            capacity = data["capacity"],
            date=date,
            is_active=True,
            adress = data["adress"]
        )
        session.add(event)
        await session.commit()

    await message.answer(
        T.EVENT_CREATED.format(
            title=data['title'],
            description=data['description'],
            capacity=data['capacity'],
            date=date.strftime('%d.%m.%Y %H:%M')
        ),
        reply_markup=admin_menu
    )



# ── MODERATORS MANAGEMENT ────────────────────────────

@router.message(F.text == T.BTN_MODERATORS)
async def moderators_list(message: Message):
    async with async_session() as session:
        mods = await db.get_all_moderators(session)

    if not mods:
        await message.answer(T.NO_MODERATORS)
        return

    text = T.MODERATORS_HEADER
    for mod in mods:
        text += f"• {mod.user.full_name} (@{mod.user.username}) — ID: {mod.user_id}\n"

    text += T.MODERATORS_FOOTER
    await message.answer(text)


@router.message(Command("addmod"))
async def add_mod(message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer(T.ADDMOD_USAGE)
        return

    username = parts[1].lstrip("@")  # remove @ if user included it

    async with async_session() as session:
        user = await db.get_user_by_username(session, username)
        if not user:
            await message.answer(T.USER_NOT_FOUND.format(username=username))
            return
        added = await db.add_moderator(session, user.id)

    if added:
        await message.answer(T.MOD_ADDED.format(username=username))
    else:
        await message.answer(T.MOD_ALREADY.format(username=username))


@router.message(Command("removemod"))
async def remove_mod(message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer(T.REMOVEMOD_USAGE)
        return

    username = parts[1].lstrip("@")  # remove @ if user included it

    async with async_session() as session:
        user = await db.get_user_by_username(session, username)
        if not user:
            await message.answer(T.REMOVEMOD_USER_NOT_FOUND.format(username=username))
            return
        removed = await db.remove_moderator(session, user.id)

    if removed:
        await message.answer(T.MOD_REMOVED.format(username=username))
    else:
        await message.answer(T.MOD_NOT_FOUND.format(username=username))




#________control event_______


class ControlEvent(StatesGroup):
    waiting_for_event_id = State()
    waiting_for_option = State()
    waiting_for_capacity = State()
    waiting_for_new_name = State()
    waiting_for_new_description = State()
    waiting_for_message_to_users = State()


@router.message(F.text == T.BTN_MANAGE_EVENT)
async def control_event(message: Message, state: FSMContext):

    async with async_session() as session:
        events = await db.get_all_events(session)

    active_events = [e for e in events if e.is_active]

    if not active_events:
        await message.answer(T.NO_ACTIVE_EVENTS)
        return
    text = T.CHOOSE_EVENT_TO_MANAGE
    for event in active_events:
        text += f"ID:<b>{event.id}</b> — {event.title} ({event.date.strftime('%d.%m.%Y')})\n"

    await state.set_state(ControlEvent.waiting_for_event_id)
    await message.answer(text, parse_mode= "HTML", reply_markup=admin_menu_with_)


@router.message(ControlEvent.waiting_for_event_id)
async def deactivate_event_confirm(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(T.INVALID_ID)
        return
    event_id = int(message.text)
    await state.update_data(event_id = event_id)
    await state.set_state(ControlEvent.waiting_for_option)
    await message.answer(T.CHOOSE_OPTION, reply_markup= admin_menu_control)


@router.message(ControlEvent.waiting_for_option)
async def deactivate_event_confirm(message: Message, state: FSMContext):
    if message.text == T.BTN_CHANGE_CAPACITY:
        await state.set_state(ControlEvent.waiting_for_capacity)
        await message.answer(T.ASK_NEW_CAPACITY)
        return
    elif message.text == T.BTN_CHANGE_TITLE:
        await message.answer(T.ASK_NEW_TITLE)
        await state.set_state(ControlEvent.waiting_for_new_name)
        return
    elif message.text == T.BTN_CHANGE_DESCRIPTION:
        await message.answer(T.ASK_NEW_DESCRIPTION)
        await state.set_state(ControlEvent.waiting_for_new_description)
        return
    elif message.text == T.BTN_BROADCAST:
        await message.answer(T.ASK_BROADCAST)
        await state.set_state(ControlEvent.waiting_for_message_to_users)
        return
    elif message.text == T.BTN_DELETE_EVENT:

        data = await state.get_data()
        event_id = data.get('event_id')
        async with async_session() as session:
            deleted = await db.delete_event(session, event_id)
        if deleted:
            await message.answer(T.EVENT_DELETED.format(event_id=event_id), parse_mode= "HTML", reply_markup=admin_menu)
        else:
            await message.answer(T.EVENT_NOT_FOUND_HTML.format(event_id=event_id), parse_mode= "HTML")
        await state.clear()


    elif message.text == T.BTN_CLOSE_EVENT:
        data = await state.get_data()
        event_id = data.get('event_id')
        async with async_session() as session:
            deactivated = await db.deactivate_event(session, event_id)
        if deactivated:
            await message.answer(
                T.EVENT_CLOSED.format(event_id=event_id),
                reply_markup=admin_menu
            )
        else:
            await message.answer(T.EVENT_TO_CLOSE_NOT_FOUND.format(event_id=event_id))
        await state.clear()


    else:
        await message.answer(T.UNKNOWN_OPTION)





@router.message(ControlEvent.waiting_for_capacity)
async def change_capacity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(T.INVALID_NUMBER)
        return
    await state.update_data(capacity = int(message.text))
    data = await state.get_data()
    async with async_session() as session:
        change = await db.change_capacity(session, data['event_id'], data['capacity'])
    await state.set_state(ControlEvent.waiting_for_option)

    if change:
        await message.answer(T.CAPACITY_CHANGED.format(value=message.text), reply_markup=admin_menu_control)
    else:
        await message.answer(T.EVENT_NOT_FOUND_SHORT)
    await state.clear()




@router.message(ControlEvent.waiting_for_new_name)
async def change_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    async with async_session() as session:
        change = await db.change_name(session, data['event_id'], data['name'])
    await state.set_state(ControlEvent.waiting_for_option)
    if change:
        await message.answer(T.TITLE_CHANGED.format(value=message.text), reply_markup=admin_menu_control)
    else:
        await message.answer(T.EVENT_NOT_FOUND_SHORT)
    await state.clear()

@router.message(ControlEvent.waiting_for_new_description)
async def change_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    data = await state.get_data()
    async with async_session() as session:
        change = await db.change_description(session, data['event_id'], data['description'])
    await state.set_state(ControlEvent.waiting_for_option)
    if change:
        await message.answer(T.DESCRIPTION_CHANGED.format(value=message.text), reply_markup=admin_menu_control)
    else:
        await message.answer(T.EVENT_NOT_FOUND_SHORT)
    await state.clear()


@router.message(ControlEvent.waiting_for_message_to_users)
async def send_notifications(message: Message, state: FSMContext):
    data = await state.get_data()
    async with async_session() as session:
        users = await db.get_event_registrations(session, data['event_id'])
    await state.set_state(ControlEvent.waiting_for_option)
    for reg in users:
        if reg.is_waitlist:
            continue
        else:
            await sleep(0.05)
            await message.bot.send_message(chat_id=reg.user_id, text=message.text)
    await message.answer(T.BROADCAST_SENT)
    await state.clear()
