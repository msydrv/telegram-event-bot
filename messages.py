"""User-facing texts. The language is chosen with BOT_LANG (en | uk)."""
import os

from dotenv import load_dotenv

load_dotenv()

BOT_LANG = os.getenv("BOT_LANG", "en")

if BOT_LANG == "uk":
    from locales.uk import *  # noqa: F401,F403
elif BOT_LANG == "en":
    from locales.en import *  # noqa: F401,F403
else:
    raise ValueError(f"Unsupported BOT_LANG: {BOT_LANG}")
