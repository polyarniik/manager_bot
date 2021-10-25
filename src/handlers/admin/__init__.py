from aiogram import Dispatcher

from filters import IsCoordinator
from handlers.admin import main as mh
from keyboards.inline import callback_datas as cd
from states.AdminState import AdminState


def setup(dp: Dispatcher):
    dp.register_message_handler(
        mh.get_admin_panel,
        IsCoordinator(),
        commands=[
            "admin",
        ],
        state="*",
    )
    dp.register_callback_query_handler(
        mh.get_managers_list,
        IsCoordinator(),
        lambda c: c.data == "manager_list",
    )
    dp.register_callback_query_handler(
        mh.add_manager_handler,
        IsCoordinator(),
        lambda c: c.data == "add_manager",
    )

    dp.register_message_handler(
        mh.get_manager_id,
        IsCoordinator(),
        state=AdminState.enter_manager_id,
    )
    dp.register_message_handler(
        mh.get_manager_full_name,
        IsCoordinator(),
        state=AdminState.enter_manager_full_name,
    )
    dp.register_callback_query_handler(
        mh.show_manager,
        IsCoordinator(),
        cd.MANAGER_INFO_CALLBACK.filter(),
    )
    dp.register_callback_query_handler(
        mh.delete_manager,
        IsCoordinator(),
        cd.DELETE_MANAGER.filter(),
    )
    dp.register_callback_query_handler(
        mh.get_admin_panel_callback,
        IsCoordinator(),
        lambda c: c.data == "admin",
    )
