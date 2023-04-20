from template import render_template
from services import api, db

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button_details = InlineKeyboardButton(text="Установленные детали", callback_data="ship_details")

details = InlineKeyboardMarkup(row_width=1).add(button_details)


async def cmd_ship(message: types.Message):
    API_TOKEN = db.get_api_token(message.from_id)
    response = api.get_ship(API_TOKEN)
    response["crew_name"] = api.get_crew(API_TOKEN)["crew_name"]

    await message.answer(render_template("ship.j2", data=response), 
                         parse_mode="HTML",
                         reply_markup=details)


async def ship_details(callback: types.CallbackQuery):
    response = api.get_ship(
                db.get_api_token(callback.message.from_id)
            )

    numbers = InlineKeyboardMarkup(row_width=5)
    for i, detail in enumerate(response["details"]):
        button = InlineKeyboardButton(text=str(i + 1), callback_data=f"detail_num_{detail['id']}_{detail['kind']['name']}")
        numbers.insert(button)

    await callback.message.answer(render_template("ship_details.j2", data=response),
                                  parse_mode="HTML", 
                                  reply_markup=numbers)
    await callback.answer()


def register_handlers_ship(dp: Dispatcher):
    dp.register_message_handler(cmd_ship, text="🚀 Корабль", state="*")
    dp.register_callback_query_handler(ship_details, text="ship_details")
