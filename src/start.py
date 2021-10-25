import aiogram
from aiogram import types

import handlers
from config.config import (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_SERVER,
    DATABASE_NAME,
    COORDINATOR_ID,
    COORDINATOR_NAME,
)
from config.loader import dp
from data.database import db, Coordinator
from utils.fill_db import fill_db


async def on_startup(*args, **kwargs):
    await db.set_bind(
        f"postgresql://"
        f"{DATABASE_USER}:"
        f"{DATABASE_PASSWORD}@"
        f"{DATABASE_SERVER}:5432/"
        f"{DATABASE_NAME}"
    )
    try:
        await Coordinator.create(telegram_id=COORDINATOR_ID, full_name=COORDINATOR_NAME)
    except:
        await Coordinator.update.values(full_name=COORDINATOR_NAME).gino.status()
    await db.gino.create_all()
    await fill_db()

    handlers.setup(dp)
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Перезапуск"),
        types.BotCommand("start_sale", "Зарегистрировать продажу"),
        types.BotCommand("cancel_sale", "Тест"),
    ])
    print("Bot started")


async def on_shutdown(*args, **kwargs):
    await db.pop_bind().close()


if __name__ == "__main__":

    def start():
        aiogram.executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )

    start()
