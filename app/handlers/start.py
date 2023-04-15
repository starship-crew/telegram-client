from template import render_template
from services.all import create_crew
from .help_ import cmd_help
from keyboard import kb

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types


class NewCerw(StatesGroup):
    crew_name = State()


#@dp.message_handler(commands=['start'], state=None)
async def cmd_start(message: types.Message):
    await NewCerw.crew_name.set()
    await message.answer(render_template("start.j2"), 
                         parse_mode="HTML")


#@dp.message_handler(state=NewCerw.crew_name)
async def get_crew_name(message: types.Message, state: FSMContext):
    crew_name, user_id = message.text, message.from_id
    #check_newness_user(user_id)
    
    if not create_crew(crew_name):
        return await message.reply(render_template("name_error.j2"), parse_mode="HTML")
    
    await state.finish()
    print(message.from_user.id)
    content = {
            "crew_name": crew_name, 
            }
    await message.answer(render_template("sucsess_start.j2", content), 
                         parse_mode="HTML", 
                         reply_markup=kb)
    await cmd_help(message)

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state=None)
    dp.register_message_handler(get_crew_name, state=NewCerw.crew_name)
