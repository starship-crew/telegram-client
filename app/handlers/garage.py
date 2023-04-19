from template import render_template
from create_bot import dp
from services import api
import config

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
    details = 'TO-DO'
    
    await callback.message.answer(render_template("garage_info.j2"), 
                                  parse_mode="HTML")
    await callback.answer()


async def garage_put_off(callback: types.CallbackQuery):
    await callback.message.answer("put off")
    await callback.answer("Деталь снята")


async def garage_put_on(callback: types.CallbackQuery):
    await callback.message.answer("put on")
    await callback.answer("Деталь установлена")


def register_handlers_upgrade(dp: Dispatcher):
    dp.register_message_handler(cmd_garage, text="🔧 Гараж", state="*")
    dp.register_callback_query_handler(garage_info, text="garage_info")
    dp.register_callback_query_handler(garage_put_off, text="garage_put_off")
    dp.register_callback_query_handler(garage_put_on, text="garage_put_on")
