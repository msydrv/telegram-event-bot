from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing")
if not ADMIN_IDS:
    raise ValueError("ADMIN_ID is missing")