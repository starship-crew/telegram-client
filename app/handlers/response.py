from typing import cast

import telegram
from telegram import Chat, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


def _get_chatid(update: Update):
    return cast(Chat, update.effective_chat).id


async def send_respnse(update: Update, 
                       context: ContextTypes.DEFAULT_TYPE, 
                       response: str,
                       keyboard: InlineKeyboardMarkup) -> None:

    args = {
            "chat_id": _get_chatid(update),
            "disable_web_page_preview": True,
            "text": response,
            "parse_mode": telegram.constants.ParseMode.HTML,
    }

    if keyboard: 
        args["raply_markup"] = keyboard

    await context.bot.send_message(**args)
