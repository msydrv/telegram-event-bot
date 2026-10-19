from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import messages as T

def event_keyboard(event_id: int, is_registered: bool):
    """callback for basic event registration"""
    if is_registered:
        button = InlineKeyboardButton(
            text= T.CANCEL_REG,
            callback_data = f"unregister_{event_id}"
        )
    else:
        button = InlineKeyboardButton(
            text= T.CONFIRM_REG,
            callback_data = f"register_{event_id}"
        )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])

def attendance_keyboard(registration_id: int, attended: bool | None):
    """Staff tracks event attendance"""
    if attended is True:
        buttons = [
            InlineKeyboardButton(text=T.STATUS_CAME, callback_data=f"att_none_{registration_id}"),
            InlineKeyboardButton(text=T.BTN_MARK_ABSENT, callback_data=f"att_false_{registration_id}")
        ]
    elif attended is False:
        buttons = [
            InlineKeyboardButton(text=T.BTN_MARK_PRESENT, callback_data=f"att_true_{registration_id}"),
            InlineKeyboardButton(text=T.STATUS_ABSENT, callback_data=f"att_none_{registration_id}")
        ]
    else:

        buttons = [
            InlineKeyboardButton(text=T.STATUS_CAME, callback_data=f"att_true_{registration_id}"),
            InlineKeyboardButton(text=T.STATUS_ABSENT, callback_data=f"att_false_{registration_id}")
        ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def notification_keyboard(event_id: int):
    """Notification after moving from waitlist"""
    buttons = [
        InlineKeyboardButton(text=T.BTN_CONFIRM, callback_data=f"nottrue"),
        InlineKeyboardButton(text=T.BTN_CANCEL, callback_data=f"unregister_{event_id}")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def waitlist_keyboard(event_id: int):
    """Asks if user ready to enter waitlist"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=T.BTN_YES,
                callback_data=f"waitlist_yes_{event_id}"
            ),
            InlineKeyboardButton(
                text=T.BTN_NO,
                callback_data=f"waitlist_no_{event_id}"
            )
        ]]
    )
