from template import render_template
from services.all import create_crew

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
    crew_name = message.text
    if not create_crew(crew_name):
        await message.reply(render_template("name_error.j2"))
        tmp = message.text
        while crew_name == tmp:
            tmp = message.text
        await get_crew_name(message, state)

    await state.finish()
    await message.answer(render_template("sucsess_start.j2"))


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state=None)
    dp.register_message_handler(get_crew_name, state=NewCerw.crew_name)
