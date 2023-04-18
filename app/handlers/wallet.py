from template import render_template
from services import api
import config

from aiogram import types, Dispatcher



async def cmd_wallet(message: types.Message):
    response = api.get_crew(config.API_TOKEN)
    await message.answer(render_template("wallet.j2", data=response), 
                         parse_mode="HTML")


def register_handlers_wallet(dp: Dispatcher):
    dp.register_message_handler(cmd_wallet, text="💰 Кошелёк", state="*")
