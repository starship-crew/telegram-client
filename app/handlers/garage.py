from template import render_template
from create_bot import dp
from services import api, db
import config

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text


button_info = InlineKeyboardButton(text="Свободные детали", callback_data="garage_info")
button_put_off = InlineKeyboardButton(text="Снять деталь", callback_data="garage_put_off")
button_put_on = InlineKeyboardButton(text="Установить деталь", callback_data="garage_put_on")
start_upgrade = InlineKeyboardMarkup(row_width=1).add(button_info)
start_upgrade.row(button_put_off, button_put_on)



async def cmd_garage(message: types.Message):
    await message.answer(render_template("garage.j2"), 
                         parse_mode="HTML", 
                         reply_markup=start_upgrade)


async def garage_info(callback: types.CallbackQuery):
    response = api.get_garage(
                db.get_api_token(str(callback.message.from_id))
            )["details"]

    details_category = InlineKeyboardMarkup(row_width=2)
    for key, _ in response.items():
        category_button = InlineKeyboardButton(text=config.DETAIL_CATEGORY[key], callback_data=f"category_{key}")
        details_category.add(category_button)
    
    await callback.message.answer("Детали какого вида тебя интересуют?", 
                                  parse_mode="HTML", 
                                  reply_markup=details_category)
    await callback.answer()


@dp.callback_query_handler(Text(startswith="category_"))
async def garage_info_category(callback: types.CallbackQuery):
    select_category = callback.data.split('_')[1]
    API_TOKEN = db.get_api_token(callback.message.from_id)
    response = {
            "category_name": select_category, 
            "details": api.get_garage(API_TOKEN)["details"][select_category], 
            "detail_with_emoji": config.DETAIL_CATEGORY,
            }

    await callback.message.answer(render_template("garage_info.j2", data=response), 
                                  parse_mode="HTML")
    await callback.answer()


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

    dp.register_callback_query_handler(garage_info, text="garage_info")
    #dp.register_callback_query_handler(garage_info_category, 
    #                                   filters=Text(startswith="category_"))

    dp.register_callback_query_handler(garage_put_off, text="garage_put_off")
    dp.register_callback_query_handler(garage_put_on, text="garage_put_on")
