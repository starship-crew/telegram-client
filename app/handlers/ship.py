from template import render_template
from services import api
import config

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button_details = InlineKeyboardButton(text="Установленные детали", callback_data="ship_details")

details = InlineKeyboardMarkup(row_width=1).add(button_details)


async def cmd_ship(message: types.Message):
    response = api.get_ship(config.API_TOKEN)
    response["crew_name"] = config.CREW_NAME

    await message.answer(render_template("ship.j2", data=response), 
                         parse_mode="HTML",
                         reply_markup=details)

async def ship_details(callback: types.CallbackQuery):
    response = api.get_ship(config.API_TOKEN)

    await callback.message.answer(render_template("ship_details.j2", data=response),
                                  parse_mode="HTML")
    await callback.answer()


def register_handlers_ship(dp: Dispatcher):
    dp.register_message_handler(cmd_ship, text="🚀 Корабль", state="*")
    dp.register_callback_query_handler(ship_details, text="ship_details")
