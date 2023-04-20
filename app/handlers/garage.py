from template import render_template
from create_bot import dp
from services import api, db
import config

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text


async def cmd_garage(message: types.Message):
    response = api.get_garage(
                db.get_api_token(message.from_id)
            )["details"]

    details_category = InlineKeyboardMarkup(row_width=2)
    for key, _ in response.items():
        category_button = InlineKeyboardButton(text=config.DETAIL_CATEGORY[key], callback_data=f"category_{key}")
        details_category.add(category_button)
    await message.answer("Детали какого вида тебя интересуют?", 
                                  parse_mode="HTML", 
                                  reply_markup=details_category)


@dp.callback_query_handler(Text(startswith="category_"))
async def detail_by_category(callback: types.CallbackQuery):
    select_category = callback.data.split('_')[1]
    API_TOKEN = db.get_api_token(callback.message.from_id)
    response = {
            "category_name": select_category, 
            "details": api.get_garage(API_TOKEN)["details"][select_category], 
            "detail_with_emoji": config.DETAIL_CATEGORY,
            }

    numbers = InlineKeyboardMarkup(row_width=5)
    for i, detail in enumerate(response["details"]):
        button = InlineKeyboardButton(text=str(i + 1), callback_data=f"detail_num_{detail['id']}_{select_category}")
        numbers.insert(button)
    await callback.message.answer(render_template("garage.j2", data=response), 
                                  parse_mode="HTML", 
                                  reply_markup=numbers)
    await callback.answer()


@dp.callback_query_handler(Text(startswith="detail_num_"))
async def detail_personal_page(callback: types.CallbackQuery):
    select_detail = int(callback.data.split('_')[2])
    select_category = callback.data.split('_')[3]

    buttons = InlineKeyboardMarkup(row_width=5)
    button_upgrade = InlineKeyboardButton(text="LVL 🔼", callback_data=f"upgrade_{select_detail}_{select_category}")
    button_set = InlineKeyboardButton(text="Установить", callback_data="put_on_{select_detail}")
    buttons.row(button_upgrade, button_set)

    API_TOKEN = db.get_api_token(callback.message.from_id)
    try:
        response = api.get_garage(API_TOKEN)["details"][select_category]
    except Exception:
        response = api.get_ship(API_TOKEN)["details"]
    for i in response:
        if i["id"] == select_detail:
            response = i
            break

    await callback.message.answer(render_template("detail_personal_page.j2", data={"detail": response}), 
                                  parse_mode="HTML", 
                                  reply_markup=buttons)
    await callback.answer()


@dp.callback_query_handler(Text(startswith="upgrade_"))
async def detail_upgrade(callback: types.CallbackQuery):
    select_detail = int(callback.data.split('_')[1])
    select_category = callback.data.split('_')[2]

    buttons = InlineKeyboardMarkup(row_width=5)
    button_upgrade = InlineKeyboardButton(text="LVL 🔼", callback_data=f"upgrade_{select_detail}_{select_category}")
    button_set = InlineKeyboardButton(text="Установить", callback_data="put_on_{select_detail}")
    buttons.row(button_upgrade, button_set)

    API_TOKEN = db.get_api_token(callback.message.from_id)
    api.upgrade_detail(API_TOKEN, select_detail)

    try:
        response = api.get_garage(API_TOKEN)["details"][select_category]
    except Exception:
        response = api.get_ship(API_TOKEN)["details"]
    for i in response:
        if i["id"] == select_detail:
            name = i["name"]
            upgrade_cost = i["upgrade_cost"]
            break

    await callback.answer(f"Деталь {name} была улучшена за {upgrade_cost} Qk", show_alert=True)
    await callback.message.edit_text(text="si", #render_template("detail_personal_page.j2", data={"detail": response}), 
                                     parse_mode="HTML", 
                                     reply_markup=buttons)


async def garage_put_off(callback: types.CallbackQuery):
    await callback.message.answer("put off")
    
    """
    if деталь была обязательной:
        await callback.answer("Деталь снята", show_alert=True)
    else: 
        await callback.answer("Деталь снята")
    """


async def garage_put_on(callback: types.CallbackQuery):
    await callback.message.answer("put on")
    await callback.answer("Деталь установлена")


def register_handlers_upgrade(dp: Dispatcher):
    dp.register_message_handler(cmd_garage, text="🔧 Гараж", state="*")

    dp.register_callback_query_handler(garage_put_off, text="garage_put_off")
