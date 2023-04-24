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
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


class Fight(StatesGroup):
    ready = State()
    action = State()


async def cmd_fight(message: types.Message, state: FSMContext):
    button_yes = KeyboardButton("✅ Да")
    button_no = KeyboardButton("❌ Нет")

    kb_ready = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_ready.row(button_yes, button_no)

    await message.answer("Готов к бою?", reply_markup=kb_ready)
    await state.set_state(Fight.ready.state)


attack_btn = KeyboardButton("⚔ Атака")
dodge_btn = KeyboardButton("Уворот")
update_btn = KeyboardButton("Состояние боя")
quit_btn = KeyboardButton("Выход")


action_kb = ReplyKeyboardMarkup(resize_keyboard=True)

action_kb.row(attack_btn)
action_kb.row(dodge_btn)
action_kb.row(update_btn)

action2_kb = ReplyKeyboardMarkup(resize_keyboard=True)
action2_kb.row(update_btn)

action3_kb = ReplyKeyboardMarkup(resize_keyboard=True)
action3_kb.row(attack_btn)
action3_kb.row(dodge_btn)
action3_kb.row(update_btn)
action3_kb.row(quit_btn)

search_kb = ReplyKeyboardMarkup(resize_keyboard=True)
check_search_btn = KeyboardButton("Проверить состояние поиска")
search_kb.row(check_search_btn)


def combat_text(combat):
    return render_template("combat.j2", combat)


async def ready(message: types.Message, state: FSMContext):
    if message.text in ["✅ Да", "Проверить состояние поиска"]:
        await bot.send_message(
            message.chat.id,
            "🔍 Поиск соперника ...",
            reply_markup=search_kb,
        )
        API_TOKEN = db.get_api_token(message.from_id)

        if api.get_combat(API_TOKEN).get("action", None) is None:
            await state.set_state(Fight.action.state)
        return

    await message.answer("Дуэль отменена", reply_markup=kb)
    await state.finish()


async def action(message: types.Message, state: FSMContext):
    API_TOKEN = db.get_api_token(message.from_id)
    combat = api.get_combat(API_TOKEN)

    if combat["won"] is not None:
        await bot.send_message(
            chat_id=message.chat.id,
            text=combat_text(combat),
            reply_markup=action3_kb,
        )
        return

    if message.text == "⚔ Атака":
        print(api.post_combat_action(API_TOKEN, "Attack"))
    elif message.text == "Уворот":
        print(api.post_combat_action(API_TOKEN, "Dodge"))

    if len(combat["actions"]) == 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text=combat_text(combat),
            reply_markup=action2_kb,
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=combat_text(combat),
            reply_markup=action_kb,
        )


def register_handlers_fight(dp: Dispatcher):
    dp.register_message_handler(cmd_fight, text="🔫 Дуэль", state="*")
    dp.register_message_handler(ready, state=Fight.ready)
    dp.register_message_handler(action, state=Fight.action)
