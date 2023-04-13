from template import render_template

from aiogram import types, Dispatcher



async def cmd_shop(message: types.Message):
    await message.answer(render_template("shop.j2"), 
                         parse_mode="HTML")


def register_handlers_shop(dp: Dispatcher):
    dp.register_message_handler(cmd_shop, commands=["Магазин🛒"], state=None)
