from template import render_template

from aiogram import types, Dispatcher



async def cmd_upgrade(message: types.Message):
    await message.answer(render_template("upgrade.j2"), 
                         parse_mode="HTML")


def register_handlers_upgrade(dp: Dispatcher):
    dp.register_message_handler(cmd_upgrade, commands=["Гараж🔧"], state=None)
