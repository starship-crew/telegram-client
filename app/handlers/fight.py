from template import render_template
from create_bot import storage, dp, bot
from services import api, db
from keyboard import kb

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Fight(StatesGroup):
    ready = State()
    searched = State()
    move = State()
    final = State()

    head = State()


async def cmd_fight(message: types.Message, state: FSMContext):
    button_yes = KeyboardButton("✅ Да")
    button_no = KeyboardButton("❌ Нет")

    kb_ready = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_ready.row(button_yes, button_no)

    await message.answer("Готов к бою?", reply_markup=kb_ready)
    await state.set_state(Fight.ready)


async def ready(message: types.Message, state: FSMContext):
    if message.text == "✅ Да":
        await message.answer(
            "🔍 Начинаю поиск соперника ...", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(Fight.searched)
        return

    await message.answer("Дуэль отменена", reply_markup=kb)


async def search(message: types.Message, state: FSMContext):
    API_TOKEN = db.get_api_token(message.from_id)

    combat = api.get_combat(API_TOKEN)
    print(combat)

    await bot.send_message(message.chat.id, "Ваш соперник:")
    await bot.send_message(message.chat.id, render_template("opponent.j2", combat))


async def move(message: types.Message, state: FSMContext):
    API_TOKEN = db.get_api_token(message.from_id)

    button_attack = KeyboardButton("⚔ Атака")
    button_no = KeyboardButton("❌ Нет")

    kb_move = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_move.row()


# async def final(message: teypes.0


def register_handlers_fight(dp: Dispatcher):
    dp.register_message_handler(cmd_fight, text="🔫 Дуэль", state="*")
    dp.register_message_handler(ready, state=Fight.ready)
    dp.register_message_handler(search, state=Fight.searched)
    dp.register_message_handler(move, state=Fight.move)
