from template import render_template
from services import api, db
from create_bot import dp
from handlers.details import get_numbers_keyboard

from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


garage_detail_list_cb = CallbackData("garage_detail_list", "category_string_id")


async def cmd_garage(message: types.Message):
    API_TOKEN = db.get_api_token(message.from_id)
    response = api.get_garage(API_TOKEN)

    empty = True
    for _, value in response["detail_copies"].items():
        if value:
            empty = False
            break
    if empty:
        await message.answer("Тут пусто..")
        return

    detail_categories = InlineKeyboardMarkup(row_width=1)
    for i in response["detail_types"]:
        if response["detail_copies"][i["id"]]:
            button = InlineKeyboardButton(
                i["name"], callback_data=garage_detail_list_cb.new(i["id"])
            )
            detail_categories.insert(button)

    await message.answer(
        "Какого типа деталь тебя интересует?", reply_markup=detail_categories
    )


@dp.callback_query_handler(garage_detail_list_cb.filter())
async def garage_list_details(callback: types.CallbackQuery, callback_data: dict):
    if callback_data["@"] == "garage_detail_list":
        API_TOKEN = db.get_api_token(callback.from_user.id)
        category_string_id = callback_data["category_string_id"]
        response = api.get_garage(API_TOKEN)

        for i in response["detail_types"]:
            if i["id"] == category_string_id:
                category_name = i["name"]

        data = {
            "category_name": category_name,
            "detail_copies": response["detail_copies"][category_string_id],
        }
        numbers = get_numbers_keyboard(
            response["detail_copies"][category_string_id], "upgrade"
        )
        await callback.message.answer(
            render_template("garage.j2", data=data), reply_markup=numbers
        )
        await callback.answer()


def register_handlers_garage(dp: Dispatcher):
    dp.register_message_handler(cmd_garage, text="🔧 Гараж", state="*")
