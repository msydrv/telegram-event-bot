# Ukrainian locale.
# Button texts are also used as handler filters (F.text == ...), so changing
# them breaks reply keyboards that users already have open in Telegram.

# ── Reply buttons ────────────────────────────────────
BTN_EVENTS = "🗓 Найближчі події"
BTN_MY_REGS = "🎟 Мої реєстрації"
BTN_ASK = "💬 Поставити запитання"
BTN_SUPPORT = "💬 Підтримка"
BTN_BY_EVENT = "🗓 По івентам"
BTN_BY_USER = "👥 По юзерам"
BTN_BACK = "🔙 Назад до меню"
BTN_MAIN_MENU = "🔙 Головне меню"
BTN_ALL_REGS = "📋 Всі реєстрації"
BTN_ADD_EVENT = "➕ Додати подію"
BTN_MANAGE_EVENT = "💥 Керувати подією"
BTN_STATS = "📊 Статистика"
BTN_MODERATORS = "👮 Модератори"
BTN_DELETE_EVENT = "🗑 Видалити подію"
BTN_CHANGE_CAPACITY = "📋 Змінити кількість місць"
BTN_CHANGE_TITLE = "➕ Змінити назву"
BTN_CHANGE_DESCRIPTION = "🔒 Змінити опис"
BTN_CLOSE_EVENT = "🔒 Завершити подію"
BTN_BROADCAST = "📊 Надіслати повідомлення участникам"

PLACEHOLDER_USER = "Обери опцію..."
PLACEHOLDER_ADMIN = "Оберіть опцію..."

# ── Inline buttons ───────────────────────────────────
CONFIRM_REG = "✅ Зареєструватися"
CANCEL_REG = "❌ Відмінити реєстрацію"
BTN_MARK_PRESENT = "✅ Відмітити присутнім"
BTN_MARK_ABSENT = "❌ Відмітити відсутнім"
BTN_CONFIRM = "✅Підтвердити"
BTN_CANCEL = "❌Відмінити"
BTN_YES = "✅ Так"
BTN_NO = "❌ Ні"
BTN_ANSWER = "💬 Відповісти"

# ── Onboarding ───────────────────────────────────────
WELCOM = (
    "👋 Для початку введи своє *ім'я та прізвище*\n\n"
    "Цей бот допоможе тобі:\n"
    "🎫 Реєструватися на події\n"
    "🔔 Отримувати нагадування"
)
NAME_INVALID = "❌ Для початку відправте *ПРІЗВИЩЕ ТА І'МЯ*:\n"
REGISTRATION = "✅ Реєстрацію підтверджено!"
COME_BACK = "👋 З поверненням!\n\n"

# ── Events and registration ──────────────────────────
NO_FUTURE_EVENTS = "😔 Наразі немає запланованих подій"
NEXT_EVENTS = "📅 Найближчі події\n"
CAPACITY_FREE = "👥 Вільних місць: {spots}"
CAPACITY_FULL_WAITLIST = (
    "🔴 Подія заповнена ({count}/{capacity}) \n"
    "Ви можете зареєструватись у лист очікування \n"
    " ⚠️⚠️⚠️ Список очікування не надає автоматичного права участі у івенті, "
    "вам просто прийде нагадування якщо місце з'явиться"
)
CAPACITY_FULL = "🔴 Подія заповнена ({count}/{capacity})"
CAPACITY_UNLIMITED = "👥 Зареєстровано: {count}"
ATTENDANCE_CONFIRMED = "✅ Реєстрацію підтвердженно"
# Must start with "⚠️": the "No" button cuts the event card at "\n\n⚠️"
EVENT_FULL_ASK_WAITLIST = "⚠️ Подія заповнена\nХочеш потрапити до листа очікування?"
REGISTERED = "✅ Ти зареєстрований! Нагадування прийде за три дні до івенту."
EVENT_LOCATION = "⚠️ Локація івенту: {address}"
ALREADY_REGISTERED = "⚠️ Ти вже зареєстрований!"
ALREADY_IN_LIST = "⚠️ Ти вже в списку!"
WAITLIST_JOINED = (
    "⏳ Тебе додано до листа очікування!\n\n"
    "Ми повідомимо тебе, якщо звільниться місце 🔔"
    "\n\n⚠️⚠️⚠️ Лист очікування не надає автоматичного права участі у івенті"
)
REG_CANCELLED = "❌ Реєстрацію скасовано!"
PROMOTED = (
    "🎉 Звільнилось місце!\n\nТебе автоматично переведено зі списку очікування на подію. "
    "Ти зареєстрований! ✅\n\n\n                        ⚠️ Локація івенту: {address}"
)
NOT_REGISTERED = "⚠️ Ти не був зареєстрований!"
NO_MY_EVENTS = (
    "🎫 Ти ще *не зареєструвався на жодну подію*\n\n"
    "Перегляни найближчі події та\n"
    "*зареєструйся вже зараз* 👇"
)
MY_REG_WAITLIST_NOTE = "\n\n ⚠️⚠️⚠️ ВИ У ЛИСТІ ОЧІКУВАННЯ, ЦЕ НЕ НАДАЄ ПРАВА ПРИЙМАТИ УЧАСТЬ У ІВЕНТІ"

# ── Reminders ────────────────────────────────────────
REMINDER_3_DAYS = (
    "🔔 Нагадування!\n\n"
    "Через 3 дні відбудеться подія:\n\n"
    "🎯 {title}\n"
    "📆 {date}\n\n"
    "Ти зареєстрований на цю подію ✅\n\n"
    "Підтверди участь:"
)
REMINDER_1_DAY = (
    "⏰ Нагадування!\n\n"
    "Вже завтра відбудеться подія:\n\n"
    "🎯 {title}\n"
    "📆 {date}\n\n"
    "Підтверди участь:"
)

# ── Support ──────────────────────────────────────────
SUPPORT_ASK = "✍️ *Напиши своє запитання* і я передам його модераторам:"
SUPPORT_MISCLICK = "✍️ Cхоже ти клікнув не туди, натисни на бажану кнопку ще раз"
SUPPORT_RECEIVED = (
    "✅ *Твоє запитання отримано*\n"
    "Модератор відповість тобі найближчим часом\\."
)
NEW_TICKET = (
    "📩 Нове запитання\n\n"
    "👤 {name} (@{username})\n"
    "🆔 Ticket #{ticket_id}\n\n"
    "❓ {question}"
)
TICKET_ALREADY_ANSWERED = "На нього вже відповіли"
ACCESS_DENIED = "❌ Доступу немає\\."
WRITE_ANSWER = "✍️ Пишіть відповідь:"
TICKET_NOT_FOUND = "❌ Тікет не знайдено\\."
ANSWER_TO_USER = (
    "📬 Відповідь на твоє запитання:\n\n"
    "❓ {question}\n\n"
    "💬 {answer}"
)
ANSWER_SENT = "✅ Відповідь надіслано"
ANSWER_FAILED = "❌ Не змогли відпрвити користувачу пов: {error}"

# ── Staff ────────────────────────────────────────────
MOD_MENU_OPENED = "👮 Відкрито меню модераторів"
MAIN_MENU_OPENED = "🔙 Головне меню"
NO_EVENTS = "📅 Івентів не знайдено."
CHOOSE_EVENT_ID = "📅 Обери івент відправивши айді, якщо потрібно більше інформації:\n\n"
INVALID_EVENT_ID = "❌ Відправте правильне івент айді."
EVENT_NOT_FOUND = "❌ Івент не знайдено {event_id}"
NO_REGISTRATIONS = "📋Наразі немає реєстрацій на '{title}'."
REGISTRATIONS_HEADER = (
    "📋 Реєстрації на: {title}\n"
    "📆 {date}\n"
    "👥 Загалом: {count}"
)
STATUS_CAME = "✅ Прийшов"
STATUS_ABSENT = "❌ Не прийшов"
STATUS_UNMARKED = "⏳ Не відмічено"
WAITLIST_YES = "Waitlist ✅"
WAITLIST_NO = "Waitlist ❌"
STATUS_LINE = "Status: {status}"
PARTICIPANT_CARD = (
    "👤 {name}: {waitlist}\n"
    "📱 @{username}\n"
    "📆 Зареєстровано: {date}\n"
    "Status: {status}"
)
STAFF_ACCESS_DENIED = "❌ Access denied."

# ── Admin ────────────────────────────────────────────
ADMIN_MENU_OPENED = "➕ Адмінське меню відкрито"
GLOBAL_STATS = (
    "📊 Загальна статистика\n\n"
    "👥 Всього користувачів: {users}\n\n"
    "📋 Всього реєстрацій: {regs}\n"
    "📝 Реєстрацій за останній місяць: {regs_month}\n"
    "🎯 Відвідувань івентів: {visited}"
)
EVENT_STATS_HEADER = (
    "📅 Історія подій:\n\n \\eventStat \\{@eventID\\}\n"
    "🔴 Для докладної інформації про конкретний івент \n\n"
)
EVENT_STATS_EMPTY = "Немає подій\\."
EVENT_ACTIVE = "🟢 Активна"
EVENT_FINISHED = "🔴 Завершена"
EVENT_STATS_ITEM = (
    "🎯 {title}: {status}\n"
    "👥 Відвідування: {attended}/{capacity}\n"
    "📋 Зареєстровано: {registered}\n\n"
)
TOP_USERS_HEADER = "Рейтинг самих активних юзерів: \n\n\n"
TOP_USERS_ITEM = "{i}: {name}, @{username} -- {count}\n"
USERSTAT_USAGE = "Невірне використання команди"
USER_NOT_FOUND = "❌ Користувач @{username} не знайдений.\n"
USER_STAT_HEADER = "Статистика користувача {name}, {username}: \n Зареєстрований: {created}\n\n"

ASK_TITLE = "Уведіть назву івенту:"
ASK_DESCRIPTION = "Уведіть опис івенту:"
ASK_CAPACITY = "Уведіть максимальну кількість участників"
ASK_ADDRESS = "Уведіть адрессу яка прийде участникам після реєстрації"
ASK_DATE = (
    "Увести час та дату івенту:\n"
    "Формат: DD.MM.YYYY HH:MM\n"
    "Приклад: 25.04.2026 18:00"
)
INVALID_FORMAT = "❌ Невірний формат!"
INVALID_FORMAT_ADDRESS = "невірний формат"
INVALID_DATE = (
    "❌ Невірний формат! Спробуйте ще раз:\n"
    "Приклад: 25.04.2026 18:00"
)
EVENT_CREATED = (
    "✅ Івент додано!\n\n"
    "🎯 {title}\n"
    "📝 {description}\n"
    "👥 {capacity}\n"
    "📆 {date}"
)

NO_MODERATORS = (
    "Наразі немає модераторів.\n\n"
    "Їх можна додати командою:\n/addmod username"
)
MODERATORS_HEADER = "👮 Список Модераторів:\n\n"
MODERATORS_FOOTER = "\nЩоб додати: /addmod USER_ID\nЩоб прибрати: /removemod USER_ID"
ADDMOD_USAGE = "Використання: /addmod @username"
MOD_ADDED = "✅ @{username} тепер модератор!"
MOD_ALREADY = "⚠️ @{username} вже є модератором."
REMOVEMOD_USAGE = "Usage: /removemod @username"
REMOVEMOD_USER_NOT_FOUND = "❌ User @{username} not found."
MOD_REMOVED = "✅ @{username} тепер не модератор."
MOD_NOT_FOUND = "❌ @{username} і не був модератором."

NO_ACTIVE_EVENTS = "Немає активних подій."
CHOOSE_EVENT_TO_MANAGE = "Якою подією керувати? *Надішли ID*:\n\n"
INVALID_ID = "❌ Надішли валідний ID."
CHOOSE_OPTION = "💥 Обери опцію"
ASK_NEW_CAPACITY = "👥 Надішліть нову кількість участників"
ASK_NEW_TITLE = "👥 Надішліть нову назву"
ASK_NEW_DESCRIPTION = "👥 Надішліть новий опис"
ASK_BROADCAST = "👥 Надішліть текст повідомлення(поки що тільки текст)"
EVENT_DELETED = "✅ Івент <b>{event_id}</b> видалено!"
EVENT_NOT_FOUND_HTML = "❌ Івент <b>{event_id}</b> не знайдено."
EVENT_CLOSED = (
    "🔒 Подію {event_id} завершено!\n"
    "Вона більше не відображається у списку подій."
)
EVENT_TO_CLOSE_NOT_FOUND = "❌ Подію {event_id} не знайдено."
UNKNOWN_OPTION = "❌ Неіснуюча опція"
INVALID_NUMBER = "❌ Невірний формат! Введіть число."
CAPACITY_CHANGED = "✅ Кількість учасників змінено на {value}"
EVENT_NOT_FOUND_SHORT = "❌ Івент не знайдено"
TITLE_CHANGED = "✅ Ім'я змінено на {value}"
DESCRIPTION_CHANGED = "✅Опис змінено на {value}"
BROADCAST_SENT = "Відправлено"
