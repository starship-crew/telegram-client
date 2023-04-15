from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_store = KeyboardButton("🛒 Магазин")
button_upgrade = KeyboardButton("/Гараж🔧")
button_fight = KeyboardButton("/Дуэль🔫")


kb = ReplyKeyboardMarkup()
kb.row(button_store, 
       button_upgrade, 
       button_fight, 
    )
