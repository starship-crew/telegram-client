from create_bot import  dp
from handlers import start

import logging
from aiogram import executor


logging.basicConfig(level=logging.INFO)


def main():
    start.register_handlers_start(dp)


if __name__ == '__main__':
    main()
    executor.start_polling(dp, skip_updates=True)
