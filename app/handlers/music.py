from create_bot import bot
from aiogram import types, Dispatcher


async def cmd_audio(message: types.Message):
    await bot.send_audio(
        message.from_user.id,
        open("audio.mp3", "rb"),
        performer="Performer",
        title="Космический саундтрек",
    )


def register_handlers_audio(dp: Dispatcher):
    dp.register_message_handler(cmd_audio, text="Космический саундтрек", state="*")
