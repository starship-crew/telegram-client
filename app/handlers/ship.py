from template import render_template
from services import api
import config

from aiogram import types, Dispatcher


async def cmd_ship(message: types.Message):
    response = api.get_ship(config.API_TOKEN)
    response["crew_name"] = config.CREW_NAME

    await message.answer(render_template("ship.j2", data=response), 
                         parse_mode="HTML")


def register_handlers_ship(dp: Dispatcher):
    dp.register_message_handler(cmd_ship, text="🚀 Корабль", state="*")
