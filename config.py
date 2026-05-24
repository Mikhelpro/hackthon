from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "0").split(",") if x.strip()]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")
