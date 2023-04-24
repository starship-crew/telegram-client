from asyncio import sleep
from aiogram.utils.callback_data import CallbackData

from aiogram.utils.exceptions import MessageNotModified
from template import render_template
from create_bot import bot, dp
from services import api, db
from keyboard import kb

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class Fight(StatesGroup):
    ready = State()


attack_cb = CallbackData("attack_action")
dodge_cb = CallbackData("dodge_action")


async def cmd_fight(message: types.Message, state: FSMContext):
    button_yes = KeyboardButton("✅ Да")
    button_no = KeyboardButton("❌ Нет")

    kb_ready = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_ready.row(button_yes, button_no)

    await message.answer("Готов к бою?", reply_markup=kb_ready)
    await state.set_state(Fight.ready.state)


def action_reply_markup(combat):
    kb = InlineKeyboardMarkup(resize_keyboard=True)

    attack_btn = InlineKeyboardButton("⚔ Атака", callback_data=attack_cb.new())
    dodge_btn = InlineKeyboardButton("Уворот", callback_data=dodge_cb.new())

    if len(combat["actions"]) != 0:
        kb.row(attack_btn)
        kb.row(dodge_btn)

    return kb


def combat_text(combat):
    return render_template("combat.j2", combat)


async def ready(message: types.Message, state: FSMContext):
    if message.text != "✅ Да":
        await message.answer("Дуэль отменена", reply_markup=kb)
        await state.finish()

    await bot.send_message(
        message.chat.id,
        "🔍 Начинаю поиск соперника ...",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    API_TOKEN = db.get_api_token(message.from_id)

    while (combat := api.get_combat(API_TOKEN)).get("action", None):
        await sleep(0.5)

    msg = await bot.send_message(
        message.chat.id, combat_text(combat), reply_markup=action_reply_markup(combat)
    )

    while (combat := api.get_combat(API_TOKEN))["won"] is None:
        try:
            await msg.edit_text(
                combat_text(combat), reply_markup=action_reply_markup(combat)
            )
        except MessageNotModified:
            pass
        await sleep(0.5)

    await state.finish()


def register_handlers_fight(dp: Dispatcher):
    dp.register_message_handler(cmd_fight, text="🔫 Дуэль", state="*")
    dp.register_message_handler(ready, state=Fight.ready)


@dp.callback_query_handler(attack_cb.filter())
async def attack_action(callback: CallbackQuery, callback_data):
    print("attack_action")
    API_TOKEN = db.get_api_token(callback.from_user.id)
    api.post_combat_action(API_TOKEN, "Attack")
    await callback.answer()


@dp.callback_query_handler(dodge_cb.filter())
async def dodge_action(callback: CallbackQuery, callback_data):
    print("dodge_action")
    API_TOKEN = db.get_api_token(callback.from_user.id)
    api.post_combat_action(API_TOKEN, "Dodge")
    await callback.answer()
