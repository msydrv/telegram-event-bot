# English locale.
# Keys must match locales/uk.py. Texts sent with parse_mode="MarkdownV2"
# (WELCOM, NAME_INVALID, NO_MY_EVENTS, SUPPORT_ASK, SUPPORT_RECEIVED) must
# escape the MarkdownV2 special characters: _ * [ ] ( ) ~ ` > # + - = | { } . !

# ── Reply buttons ────────────────────────────────────
BTN_EVENTS = "🗓 Upcoming events"
BTN_MY_REGS = "🎟 My registrations"
BTN_ASK = "💬 Ask a question"
BTN_SUPPORT = "💬 Support"
BTN_BY_EVENT = "🗓 By event"
BTN_BY_USER = "👥 By user"
BTN_BACK = "🔙 Back to menu"
BTN_MAIN_MENU = "🔙 Main menu"
BTN_ALL_REGS = "📋 All registrations"
BTN_ADD_EVENT = "➕ Add event"
BTN_MANAGE_EVENT = "💥 Manage event"
BTN_STATS = "📊 Statistics"
BTN_MODERATORS = "👮 Moderators"
BTN_DELETE_EVENT = "🗑 Delete event"
BTN_CHANGE_CAPACITY = "📋 Change capacity"
BTN_CHANGE_TITLE = "✏️ Change title"
BTN_CHANGE_DESCRIPTION = "📝 Change description"
BTN_CLOSE_EVENT = "🔒 Close event"
BTN_BROADCAST = "📣 Message participants"

PLACEHOLDER_USER = "Choose an option..."
PLACEHOLDER_ADMIN = "Choose an option..."

# ── Inline buttons ───────────────────────────────────
CONFIRM_REG = "✅ Register"
CANCEL_REG = "❌ Cancel registration"
BTN_MARK_PRESENT = "✅ Mark as present"
BTN_MARK_ABSENT = "❌ Mark as absent"
BTN_CONFIRM = "✅ Confirm"
BTN_CANCEL = "❌ Cancel"
BTN_YES = "✅ Yes"
BTN_NO = "❌ No"
BTN_ANSWER = "💬 Reply"

# ── Onboarding ───────────────────────────────────────
WELCOM = (
    "👋 To get started, send your *first and last name*\n\n"
    "This bot will help you:\n"
    "🎫 Register for events\n"
    "🔔 Get reminders"
)
NAME_INVALID = "❌ To get started, send your *FIRST AND LAST NAME*:\n"
REGISTRATION = "✅ You're all set!"
COME_BACK = "👋 Welcome back!\n\n"

# ── Events and registration ──────────────────────────
NO_FUTURE_EVENTS = "😔 No upcoming events right now"
NEXT_EVENTS = "📅 Upcoming events\n"
CAPACITY_FREE = "👥 Seats left: {spots}"
CAPACITY_FULL_WAITLIST = (
    "🔴 The event is full ({count}/{capacity}) \n"
    "You can join the waitlist \n"
    " ⚠️ The waitlist doesn't guarantee a seat: "
    "you'll get a notification if one opens up"
)
CAPACITY_FULL = "🔴 The event is full ({count}/{capacity})"
CAPACITY_UNLIMITED = "👥 Registered: {count}"
ATTENDANCE_CONFIRMED = "✅ Attendance confirmed"
# Must start with "⚠️": the "No" button cuts the event card at "\n\n⚠️"
EVENT_FULL_ASK_WAITLIST = "⚠️ The event is full\nDo you want to join the waitlist?"
REGISTERED = "✅ You're registered! You'll get a reminder three days before the event."
EVENT_LOCATION = "⚠️ Event location: {address}"
ALREADY_REGISTERED = "⚠️ You're already registered!"
ALREADY_IN_LIST = "⚠️ You're already on the list!"
WAITLIST_JOINED = (
    "⏳ You've been added to the waitlist!\n\n"
    "We'll let you know if a seat opens up 🔔"
    "\n\n⚠️ The waitlist doesn't guarantee a seat at the event"
)
REG_CANCELLED = "❌ Registration cancelled!"
PROMOTED = (
    "🎉 A seat opened up!\n\nYou've been moved from the waitlist to the event. "
    "You're registered! ✅\n\n⚠️ Event location: {address}"
)
NOT_REGISTERED = "⚠️ You weren't registered!"
NO_MY_EVENTS = (
    "🎫 You haven't *registered for any events* yet\n\n"
    "Check out the upcoming events and\n"
    "*sign up now* 👇"
)
MY_REG_WAITLIST_NOTE = "\n\n ⚠️ YOU ARE ON THE WAITLIST, THIS DOESN'T GUARANTEE A SEAT AT THE EVENT"

# ── Reminders ────────────────────────────────────────
REMINDER_3_DAYS = (
    "🔔 Reminder!\n\n"
    "This event is in 3 days:\n\n"
    "🎯 {title}\n"
    "📆 {date}\n\n"
    "You're registered for it ✅\n\n"
    "Please confirm you're coming:"
)
REMINDER_1_DAY = (
    "⏰ Reminder!\n\n"
    "This event is tomorrow:\n\n"
    "🎯 {title}\n"
    "📆 {date}\n\n"
    "Please confirm you're coming:"
)

# ── Support ──────────────────────────────────────────
SUPPORT_ASK = "✍️ *Type your question* and I'll forward it to the moderators:"
SUPPORT_MISCLICK = "✍️ Looks like you tapped a menu button. Tap the button you need again"
SUPPORT_RECEIVED = (
    "✅ *Your question has been received*\n"
    "A moderator will reply as soon as possible\\."
)
NEW_TICKET = (
    "📩 New question\n\n"
    "👤 {name} (@{username})\n"
    "🆔 Ticket #{ticket_id}\n\n"
    "❓ {question}"
)
TICKET_ALREADY_ANSWERED = "This question has already been answered"
ACCESS_DENIED = "❌ Access denied."
WRITE_ANSWER = "✍️ Type your answer:"
TICKET_NOT_FOUND = "❌ Ticket not found."
ANSWER_TO_USER = (
    "📬 Answer to your question:\n\n"
    "❓ {question}\n\n"
    "💬 {answer}"
)
ANSWER_SENT = "✅ Answer sent"
ANSWER_FAILED = "❌ Couldn't send the answer to the user: {error}"

# ── Staff ────────────────────────────────────────────
MOD_MENU_OPENED = "👮 Moderator menu opened"
MAIN_MENU_OPENED = "🔙 Main menu"
NO_EVENTS = "📅 No events found."
CHOOSE_EVENT_ID = "📅 Send an event ID to see its registrations:\n\n"
INVALID_EVENT_ID = "❌ Please send a valid event ID."
EVENT_NOT_FOUND = "❌ Event not found {event_id}"
NO_REGISTRATIONS = "📋 No registrations for '{title}' yet."
REGISTRATIONS_HEADER = (
    "📋 Registrations for: {title}\n"
    "📆 {date}\n"
    "👥 Total: {count}"
)
STATUS_CAME = "✅ Came"
STATUS_ABSENT = "❌ Didn't come"
STATUS_UNMARKED = "⏳ Not marked"
WAITLIST_YES = "Waitlist ✅"
WAITLIST_NO = "Waitlist ❌"
STATUS_LINE = "Status: {status}"
PARTICIPANT_CARD = (
    "👤 {name}: {waitlist}\n"
    "📱 @{username}\n"
    "📆 Registered: {date}\n"
    "Status: {status}"
)
STAFF_ACCESS_DENIED = "❌ Access denied."

# ── Admin ────────────────────────────────────────────
ADMIN_MENU_OPENED = "➕ Admin menu opened"
GLOBAL_STATS = (
    "📊 Overall statistics\n\n"
    "👥 Total users: {users}\n\n"
    "📋 Total registrations: {regs}\n"
    "📝 Registrations in the last month: {regs_month}\n"
    "🎯 Event visits: {visited}"
)
EVENT_STATS_HEADER = (
    "📅 Event history:\n\n \\eventStat \\{@eventID\\}\n"
    "🔴 For details about a specific event \n\n"
)
EVENT_STATS_EMPTY = "No events."
EVENT_ACTIVE = "🟢 Active"
EVENT_FINISHED = "🔴 Finished"
EVENT_STATS_ITEM = (
    "🎯 {title}: {status}\n"
    "👥 Attendance: {attended}/{capacity}\n"
    "📋 Registered: {registered}\n\n"
)
TOP_USERS_HEADER = "Most active users: \n\n\n"
TOP_USERS_ITEM = "{i}: {name}, @{username} -- {count}\n"
USERSTAT_USAGE = "Wrong command usage"
USER_NOT_FOUND = "❌ User @{username} not found.\n"
USER_STAT_HEADER = "Statistics for {name}, {username}: \n Joined: {created}\n\n"

ASK_TITLE = "Enter the event title:"
ASK_DESCRIPTION = "Enter the event description:"
ASK_CAPACITY = "Enter the maximum number of participants"
ASK_ADDRESS = "Enter the address participants will receive after registering"
ASK_DATE = (
    "Enter the event date and time:\n"
    "Format: DD.MM.YYYY HH:MM\n"
    "Example: 25.04.2026 18:00"
)
INVALID_FORMAT = "❌ Invalid format!"
INVALID_FORMAT_ADDRESS = "invalid format"
INVALID_DATE = (
    "❌ Invalid format! Try again:\n"
    "Example: 25.04.2026 18:00"
)
EVENT_CREATED = (
    "✅ Event added!\n\n"
    "🎯 {title}\n"
    "📝 {description}\n"
    "👥 {capacity}\n"
    "📆 {date}"
)

NO_MODERATORS = (
    "There are no moderators yet.\n\n"
    "Add one with:\n/addmod username"
)
MODERATORS_HEADER = "👮 Moderators:\n\n"
MODERATORS_FOOTER = "\nTo add: /addmod USER_ID\nTo remove: /removemod USER_ID"
ADDMOD_USAGE = "Usage: /addmod @username"
MOD_ADDED = "✅ @{username} is now a moderator!"
MOD_ALREADY = "⚠️ @{username} is already a moderator."
REMOVEMOD_USAGE = "Usage: /removemod @username"
REMOVEMOD_USER_NOT_FOUND = "❌ User @{username} not found."
MOD_REMOVED = "✅ @{username} is no longer a moderator."
MOD_NOT_FOUND = "❌ @{username} wasn't a moderator."

NO_ACTIVE_EVENTS = "No active events."
CHOOSE_EVENT_TO_MANAGE = "Which event do you want to manage? *Send its ID*:\n\n"
INVALID_ID = "❌ Send a valid ID."
CHOOSE_OPTION = "💥 Choose an option"
ASK_NEW_CAPACITY = "👥 Send the new number of participants"
ASK_NEW_TITLE = "👥 Send the new title"
ASK_NEW_DESCRIPTION = "👥 Send the new description"
ASK_BROADCAST = "👥 Send the message text (text only for now)"
EVENT_DELETED = "✅ Event <b>{event_id}</b> deleted!"
EVENT_NOT_FOUND_HTML = "❌ Event <b>{event_id}</b> not found."
EVENT_CLOSED = (
    "🔒 Event {event_id} closed!\n"
    "It no longer appears in the event list."
)
EVENT_TO_CLOSE_NOT_FOUND = "❌ Event {event_id} not found."
UNKNOWN_OPTION = "❌ Unknown option"
INVALID_NUMBER = "❌ Invalid format! Enter a number."
CAPACITY_CHANGED = "✅ Capacity changed to {value}"
EVENT_NOT_FOUND_SHORT = "❌ Event not found"
TITLE_CHANGED = "✅ Title changed to {value}"
DESCRIPTION_CHANGED = "✅ Description changed to {value}"
BROADCAST_SENT = "Sent"
