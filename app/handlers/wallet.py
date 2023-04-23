from template import render_template
from services import api, db

from aiogram import types, Dispatcher



async def cmd_wallet(message: types.Message):
    API_TOKEN = db.get_api_token(message.from_id)
    response = api.get_crew(API_TOKEN)
    await message.answer(render_template("wallet.j2", data=response), 
                         parse_mode="HTML")


def register_handlers_wallet(dp: Dispatcher):
    dp.register_message_handler(cmd_wallet, text="💰 Кошелёк", state="*")
