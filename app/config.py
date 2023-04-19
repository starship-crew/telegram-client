import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

PATH_TO_DB = os.path.join('..', 'db', 'starship.db')

DETAIL_CATEGORY = {
                    "Корпус": "🛰 Корпус", 
                    "Плазменный генератор": "🌀 Плазменный генератор", 
                    "Варп-двигатель": "🚂 Варп-двигатель", 
                    "Пустотные щиты": "🛡 Пустотные щиты", 
                    "Генератор поля Геллера": "🧲 Генератор поля Геллера", 
                    "Мостик": "🛳 Мостик", 
                    "Сенсоры": "🚦 Сенсоры", 
                    "Орудие": "🔫 Орудие", 
                  }
