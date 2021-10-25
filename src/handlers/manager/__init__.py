from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

import handlers.manager.main as mh
from filters.StaffFilters import IsStaff
from keyboards.inline import callback_datas as cd
from states.ManagerState import ManagerState


def setup(dp: Dispatcher):
    print("setup manager")
    dp.register_message_handler(
        mh.start,
        CommandStart(),
        IsStaff(),
        state="*",
    )
    dp.register_message_handler(
        mh.start,
        IsStaff(),
        commands=["start_sale", "cancel_sale"],
        state="*",
    )
    dp.register_callback_query_handler(
        mh.get_subject_handler,
        IsStaff(),
        cd.SUBJECT_CALLBACK.filter(),
    )
    dp.register_callback_query_handler(
        mh.get_sale_type_handler,
        IsStaff(),
        cd.SALE_TYPE_CALLBACK.filter(),
    )
    dp.register_message_handler(
        mh.check_email_existing,
        state=ManagerState.enter_existing_email,
    )
    dp.register_callback_query_handler(
        mh.is_founded_user_correct,
        IsStaff(),
        lambda c: str(c.data).startswith("student_"),
    )
    dp.register_callback_query_handler(
        mh.get_tariff_handler,
        IsStaff(),
        cd.TARIFF_CALLBACK.filter(),
    )
    dp.register_callback_query_handler(
        mh.get_month_handler,
        IsStaff(),
        cd.MONTH_CALLBACK.filter(),
    )
    dp.register_message_handler(
        mh.get_vk_name_handler,
        IsStaff(),
        state=ManagerState.enter_vk_name,
    )
    dp.register_message_handler(
        mh.get_vk_url_handler,
        IsStaff(),
        state=ManagerState.enter_vk_url,
    )
    dp.register_message_handler(
        mh.get_email_handler,
        IsStaff(),
        state=ManagerState.enter_email,
    )
    dp.register_callback_query_handler(
        mh.confirm_subscribe,
        IsStaff(),
        lambda c: str(c.data).startswith("confirm"),
    )
