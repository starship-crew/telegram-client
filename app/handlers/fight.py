from template import render_template

from aiogram import types, Dispatcher



async def cmd_fight(message: types.Message):
    await message.answer(render_template("fight.j2"), 
                         parse_mode="HTML")


def register_handlers_fight(dp: Dispatcher):
    dp.register_message_handler(cmd_fight, commands=["Дуэль🔫"], state=None)
