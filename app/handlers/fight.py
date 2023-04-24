from asyncio import sleep
from template import render_template
from create_bot import bot
from services import api, db
from keyboard import kb

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


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
        await state.set_state(Fight.searched)
        return

    await message.answer("Дуэль отменена", reply_markup=kb)
    await state.finish()


async def search(message: types.Message, state: FSMContext):
    API_TOKEN = db.get_api_token(message.from_id)

    await message.answer(
        "🔍 Начинаю поиск соперника ...", reply_markup=types.ReplyKeyboardRemove()
    )

    while not api.get_combat(API_TOKEN).get("action", None):
        await sleep(0.5)

    await state.set_state(Fight.move)


def action_reply_markup(combat):
    kb = ReplyKeyboardMarkup()

    attack_btn = KeyboardButton("⚔ Атака")
    dodge_btn = KeyboardButton("Уворот")

    if len(combat["actions"]) != 0:
        kb.row(attack_btn)
        kb.row(dodge_btn)

    return kb


def combat_text(combat):
    return render_template("combat.j2", combat)


async def action(message: types.Message, state: FSMContext):
    API_TOKEN = db.get_api_token(message.from_id)
    combat = api.get_combat(API_TOKEN)

    msg = await bot.send_message(
        message.chat.id, combat_text(combat), reply_markup=action_reply_markup(combat)
    )

    while (combat := api.get_combat(API_TOKEN))["won"] is None:
        await msg.edit_text(combat_text(combat))
        await msg.edit_reply_markup(action_reply_markup(combat))

    await state.finish()


def register_handlers_fight(dp: Dispatcher):
    dp.register_message_handler(cmd_fight, text="🔫 Дуэль", state="*")
    dp.register_message_handler(ready, state=Fight.ready)
    dp.register_message_handler(search, state=Fight.searched)
    dp.register_message_handler(action, state=Fight.move)
