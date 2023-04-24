from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_wallet = KeyboardButton("💰 Кошелёк")
button_ship = KeyboardButton("🚀 Корабль")
button_store = KeyboardButton("🛒 Магазин")
button_upgrade = KeyboardButton("🔧 Гараж")
button_fight = KeyboardButton("🔫 Дуэль")
button_audio = KeyboardButton("🎸 Космический саундтрек")


kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(
    button_wallet,
    button_ship,
)
kb.row(
    button_store,
    button_upgrade,
    button_fight,
)
kb.row(button_audio)
