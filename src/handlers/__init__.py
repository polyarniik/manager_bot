from aiogram import Dispatcher

from handlers import admin, manager


def setup(dp: Dispatcher):
    admin.setup(dp)
    manager.setup(dp)
