from aiogram.utils.callback_data import CallbackData

from data import callback_data_attrs as ca

SUBJECT_CALLBACK = CallbackData(ca.BOT, ca.SUBJECT)
SALE_TYPE_CALLBACK = CallbackData(ca.BOT, ca.SUBJECT, ca.SALE_TYPE)
TARIFF_CALLBACK = CallbackData(ca.BOT, ca.SUBJECT, ca.SALE_TYPE, ca.TARIFF)
MONTH_CALLBACK = CallbackData(ca.BOT, ca.SUBJECT, ca.SALE_TYPE, ca.TARIFF, ca.MONTH)

MANAGER_INFO_CALLBACK = CallbackData(ca.MANAGER, ca.MANAGER_ID)
DELETE_MANAGER = CallbackData(ca.DELETE_MANAGER, ca.MANAGER_ID)
