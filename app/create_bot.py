import config
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

bot = Bot(token=config.TELEGRAM_BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
