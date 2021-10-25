from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import callback_data_attrs as ca
from data.database import Manager
from keyboards.inline import callback_datas as cd


async def show_admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Список менеджеров",
            callback_data=ca.MANAGER_LIST,
        ),
        InlineKeyboardButton(
            text="Добавить менеджера",
            callback_data=ca.ADD_MANAGER,
        ),
    )
    return keyboard


async def show_manager_list() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    managers = await Manager.query.gino.all()
    page = 0
    for manager in managers[page * 8 : (page + 1) * 8]:
        keyboard.add(
            InlineKeyboardButton(
                text=manager.full_name,
                callback_data=cd.MANAGER_INFO_CALLBACK.new(
                    **{
                        ca.MANAGER_ID: manager.telegram_id,
                    }
                ),
            ),
        )
    keyboard.add(
        InlineKeyboardButton(
            text="В меню",
            callback_data="admin",
        ),
    )

    return keyboard


async def show_manager_info(manager_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=cd.DELETE_MANAGER.new(
                **{
                    ca.MANAGER_ID: manager_id,
                }
            ),
        ),
        InlineKeyboardButton(text="Назад", callback_data=ca.MANAGER_LIST),
    )
    return keyboard
