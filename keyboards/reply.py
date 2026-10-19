from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import messages as T

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=T.BTN_EVENTS)],
        [KeyboardButton(text=T.BTN_MY_REGS)],
        [KeyboardButton(text=T.BTN_ASK)]
    ],
    resize_keyboard=True,
    input_field_placeholder=T.PLACEHOLDER_USER
)

stat_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=T.BTN_BY_EVENT), KeyboardButton(text=T.BTN_BY_USER)],
        [KeyboardButton(text=T.BTN_BACK)]
    ],
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=T.BTN_ALL_REGS)],
        [KeyboardButton(text=T.BTN_ADD_EVENT)],
        [KeyboardButton(text=T.BTN_MANAGE_EVENT)],
        [KeyboardButton(text=T.BTN_STATS), KeyboardButton(text=T.BTN_MODERATORS)],
        [KeyboardButton(text=T.BTN_MAIN_MENU)]
    ],
    resize_keyboard=True,
    input_field_placeholder=T.PLACEHOLDER_ADMIN
)

admin_menu_with_ = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=T.BTN_ALL_REGS)],
        [KeyboardButton(text=T.BTN_ADD_EVENT), KeyboardButton(text=T.BTN_DELETE_EVENT)],
        [KeyboardButton(text=T.BTN_MANAGE_EVENT)],
        [KeyboardButton(text=T.BTN_STATS), KeyboardButton(text=T.BTN_MODERATORS)],
        [KeyboardButton(text=T.BTN_BACK)]
    ],
    resize_keyboard=True,
    input_field_placeholder=T.PLACEHOLDER_ADMIN
)


staff_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=T.BTN_ALL_REGS)],
        [KeyboardButton(text=T.BTN_BACK)]
    ],
    input_field_placeholder=T.PLACEHOLDER_ADMIN,
    resize_keyboard=True
)


admin_menu_control = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=T.BTN_CHANGE_CAPACITY)],
        [KeyboardButton(text=T.BTN_CHANGE_TITLE), KeyboardButton(text=T.BTN_DELETE_EVENT)],
        [KeyboardButton(text=T.BTN_CHANGE_DESCRIPTION), KeyboardButton(text=T.BTN_CLOSE_EVENT)],
        [KeyboardButton(text=T.BTN_BROADCAST)],
        [KeyboardButton(text=T.BTN_BACK)]
    ],
    resize_keyboard=True,
    input_field_placeholder=T.PLACEHOLDER_ADMIN
)

MENU_BUTTONS = [
    T.BTN_MAIN_MENU,
    T.BTN_EVENTS,
    T.BTN_MY_REGS,
    T.BTN_SUPPORT,
    T.BTN_ALL_REGS,
    T.BTN_ADD_EVENT,
    T.BTN_DELETE_EVENT,
    T.BTN_CLOSE_EVENT,
    T.BTN_STATS,
    T.BTN_MODERATORS,
    T.BTN_BACK,
    T.BTN_BY_EVENT,
    T.BTN_BY_USER
]
