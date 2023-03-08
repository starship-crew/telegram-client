import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from starship_bot import config
from starship_bot import handlers


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
)


COMMAND_HANDLERS = {
    "help": handlers.help_,
}


if not config.TELEGRAM_BOT_TOKEN:
    raise ValueError(
            '''TELEGRAM_BOT_TOKEN was not found'''
            )


def main():
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    for command_name, command_hendler in COMMAND_HANDLERS.items():
        app.add_handler(CommandHandler(command_name, command_hendler))

    app.run_polling()


if __name__ == "__main__":
    main()
