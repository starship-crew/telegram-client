from template import render_template
from services import api 
from services import db
from .help_ import cmd_help
from keyboard import kb
import config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types


class NewCerw(StatesGroup):
    crew_name = State()


#@dp.message_handler(commands=['start'], state=None)
async def cmd_start(message: types.Message):
    user_id = str(message.from_id)
    if db.get_api_token(user_id):
        await message.reply(render_template("not_new_user.j2"),
                            parse_mode="HTML",
                            reply_markup=kb)
        await cmd_help(message)
    else:
        await NewCerw.crew_name.set()
        await message.answer(render_template("start.j2"), 
                             parse_mode="HTML")


#@dp.message_handler(state=NewCerw.crew_name)
async def get_crew_name(message: types.Message, state: FSMContext):
    crew_name, user_id = message.text, message.from_id

    # verificatin
    response = api.create_crew(crew_name) 
    try :
        if response["message"]:
            return await message.reply(render_template("name_error.j2"), parse_mode="HTML")
    except Exception:
        pass
    
    # save api token
    API_TOKEN = response["token"]
    db.save_new_user(user_id, API_TOKEN)

    # save crew
    await state.finish()
    content = {
            "crew_name": crew_name, 
            }

    # send message
    await message.answer(render_template("sucsess_start.j2", content), 
                         parse_mode="HTML", 
                         reply_markup=kb)
    await cmd_help(message)

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state=None)
    dp.register_message_handler(get_crew_name, state=NewCerw.crew_name)
