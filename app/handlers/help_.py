
from template import render_template

from aiogram import Dispatcher, types


#@dp.message_handler(commands=['help'], state=None)
async def cmd_help(message: types.Message):
    await message.answer(render_template("help.j2"), 
                         parse_mode="HTML")

def register_handlers_help(dp: Dispatcher):
    dp.register_message_handler(cmd_help, commands=["help"], state=None)
