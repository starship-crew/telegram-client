from config import PATH_TO_DB
from data.db_session import global_init
from create_bot import dp
from handlers import (
    start,
    help_,
    ship,
    store,
    fight,
    garage,
    wallet,
)

import logging
from aiogram import executor


logging.basicConfig(level=logging.INFO)


def main():
    global_init(PATH_TO_DB)

    start.register_handlers_start(dp)
    help_.register_handlers_help(dp)
    fight.register_handlers_fight(dp)
    garage.register_handlers_garage(dp)
    ship.register_handlers_ship(dp)
    wallet.register_handlers_wallet(dp)
    store.register_handlers_store(dp)


if __name__ == "__main__":
    main()
    executor.start_polling(dp, skip_updates=True)
