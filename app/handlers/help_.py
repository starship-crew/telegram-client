from telegram import Update
from telegram.ext import ContextTypes

from starship_bot.templates import render_template
from starship_bot.handlers.response import send_response


async def help(update: Update, context: ContextTypes):
    await send_response(update, context, response=render_template("help.j2"))
