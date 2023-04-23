from template import render_template
from services import api, db
from handlers.details import get_numbers_keyboard

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cmd_ship(message: types.Message):
    API_TOKEN = db.get_api_token(message.from_id)
    response = api.get_ship(API_TOKEN)
    response["crew_name"] = api.get_crew(API_TOKEN)["name"]

    show_details = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(
        text="Установленные детали", callback_data="ship_details"
    )
    show_details.add(button)

    await message.answer(
        render_template("ship.j2", data=response), reply_markup=show_details
    )


async def seted_details(callback: types.CallbackQuery):
    API_TOKEN = db.get_api_token(callback.from_user.id)
    response = api.get_ship(API_TOKEN)

    if not response["detail_copies"]:
        await callback.answer("На корабле нет деталей")
        return

    numbers = get_numbers_keyboard(response['detail_copies'],
                                   "upgrade")
    await callback.message.answer(
        render_template("ship_details.j2", data=response), reply_markup=numbers
    )
    await callback.answer()


def register_handlers_ship(dp: Dispatcher):
    dp.register_message_handler(cmd_ship, text="🚀 Корабль", state="*")
    dp.register_callback_query_handler(seted_details, text="ship_details")
