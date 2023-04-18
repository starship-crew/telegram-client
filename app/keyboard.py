from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_ship = KeyboardButton("🚀 Корабль")
button_store = KeyboardButton("🛒 Магазин")
button_upgrade = KeyboardButton("🔧 Гараж")
button_fight = KeyboardButton("🔫 Дуэль")


kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(
        button_ship,
        button_store, 
        button_upgrade, 
        button_fight, 
    )
