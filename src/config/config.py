import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_SERVER = os.environ.get("DATABASE_SERVER")
GOOGLE_SPREADSHEET_ID = os.environ.get("GOOGLE_SPREADSHEET_ID")

COORDINATOR_ID = os.environ.get("COORDINATOR_ID")
COORDINATOR_NAME = os.environ.get("COORDINATOR_NAME")

# Номер столбца месяца и его название
MONTHS = {
    8: "Сентябрь",
    9: "Октябрь",
    10: "Ноябрь",
    11: "Декабрь",
    12: "Январь",
    13: "Февраль",
    14: "Март",
    15: "Апрель",
    16: "Май",
}

TARIFFS = ["VIP", "Стандарт"]

# Название должно совпадать с названием листа
SUBJECTS = ["Математика", "Информатика", "Обществознание"]

# Названия не менять!
SALE_TYPES = ["Новая продажа", "Продление"]
