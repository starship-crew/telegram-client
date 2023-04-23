from template import render_template
from services import api, db
from create_bot import dp

from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


store_detail_list_cb = CallbackData("store_detail_list", "category_string_id")
buy_detail_cb = CallbackData("buy_detial", "detail_type_id")
detail_personal_buy_page_cb = CallbackData("personal_buy_page", "detail_type_id")


def get_personal_buy_keboard(detail_type_id: str):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            text="Купить 💵",
            callback_data=buy_detail_cb.new(detail_type_id=detail_type_id),
        ),
    )


async def cmd_store(message: types.Message):
    response = api.get_store()

    detail_categories = InlineKeyboardMarkup(row_width=1)
    for i in response['detail_types']:
        if response['details'][i['string_id']]:
            button = InlineKeyboardButton(i['name'], callback_data=store_detail_list_cb.new(i['string_id']))
            detail_categories.insert(button)

    await message.answer("Кокого типа деталь тебя интересует?", 
                         reply_markup=detail_categories)


@dp.callback_query_handler(store_detail_list_cb.filter())
async def store_detail_list(callback: types.CallbackQuery, callback_data: dict):
    from handlers.details import get_numbers_keyboard


    if callback_data["@"] == "store_detail_list":
        category_string_id = callback_data["category_string_id"]
        response = api.get_store()

        for i in response["detail_types"]:
            if i['string_id'] == category_string_id:
                category_name = i['name']

        data = {
                "category_name": category_name, 
                "detail_copies": response['details'][category_string_id], 
                }

        numbers = get_numbers_keyboard(response['details'][category_string_id], 
                                       'buy')
        await callback.message.answer(
            render_template("garage.j2", data=data), reply_markup=numbers
        )
        await callback.answer()


@dp.callback_query_handler(detail_personal_buy_page_cb.filter())
async def detail_personal_buy_page(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['@'] == "personal_buy_page":
        detail_type_id = callback_data["detail_type_id"]
        API_TOKEN = db.get_api_token(callback.from_user.id)

        detail = api.get_detail_type(API_TOKEN, "string_id")[detail_type_id]
        print(detail)

        buttons = get_personal_buy_keboard(detail_type_id=detail_type_id)
        await callback.message.answer(
            render_template("detail_personal_page.j2", data={"detail": detail}),
            reply_markup=buttons,
        )
        await callback.answer()


@dp.callback_query_handler(buy_detail_cb.filter())
async def buy_detail(callback: types.CallbackQuery, callback_data: dict):
    print(callback_data)
    detail_type_id = int(callback_data["detail_type_id"])
    API_TOKEN = db.get_api_token(callback.from_user.id)

    cost = int(api.get_detail_type(API_TOKEN, detail_type_id)["upgrade_cost"])
    currency = api.get_crew(API_TOKEN)["currency"]

    if cost > currency:
        await callback.answer(f"Недостаточно средств")
        return

    api.buy_detail(API_TOKEN, detail_type_id)

    detail = api.get_detail_copy(API_TOKEN, detail_id)

    buttons = get_personal_buy_keboard()

    await callback.message.edit_text(
        render_template("detail_personal_page.j2", data={"detail": detail}),
        reply_markup=buttons,
    )
    await callback.answer(f"-{cost} Qk")


def register_handlers_store(dp: Dispatcher):
    dp.register_message_handler(cmd_store, text="🛒 Магазин", state="*")
