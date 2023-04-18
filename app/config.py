import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

PATH_TO_DB = os.path.join('..', 'db', 'starship.db')

API_TOKEN = ""

CREW_NAME = ""
