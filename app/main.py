from create_bot import  dp
from handlers import (
        start, 
        help_, 
        ship, 
        shop, 
        fight, 
        garage, 
        wallet, 
    )

import logging
from aiogram import executor


logging.basicConfig(level=logging.INFO)


from template import render_template
from aiogram import types


def main():
    start.register_handlers_start(dp)
    help_.register_handlers_help(dp)
    shop.register_handlers_shop(dp)
    fight.register_handlers_fight(dp)
    garage.register_handlers_upgrade(dp)
    ship.register_handlers_ship(dp)
    wallet.register_handlers_wallet(dp)


if __name__ == '__main__':
    main()
    executor.start_polling(dp, skip_updates=True)
