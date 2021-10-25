from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import callback_data_attrs as ca
from data.database import Subject, Tariff, Month, SaleType
from keyboards.inline import callback_datas as cd


async def show_subjects() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    subjects = await Subject.query.gino.all()
    for subject in subjects:
        keyboard.add(
            InlineKeyboardButton(
                text=subject.name,
                callback_data=cd.SUBJECT_CALLBACK.new(**{ca.SUBJECT: subject.id}),
            )
        )

    return keyboard


async def show_sale_types(callback_data: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    sale_types = await SaleType.query.gino.all()
    for sale_type in sale_types:
        keyboard.add(
            InlineKeyboardButton(
                text=sale_type.name,
                callback_data=cd.SALE_TYPE_CALLBACK.new(
                    **{
                        ca.SUBJECT: callback_data[ca.SUBJECT],
                        ca.SALE_TYPE: sale_type.id,
                    },
                ),
            )
        )

    return keyboard


async def show_tariffs(callback_data: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    tariffs = await Tariff.query.gino.all()
    for tariff in tariffs:
        keyboard.add(
            InlineKeyboardButton(
                text=tariff.name,
                callback_data=cd.TARIFF_CALLBACK.new(
                    **{
                        ca.SUBJECT: callback_data[ca.SUBJECT],
                        ca.SALE_TYPE: callback_data[ca.SALE_TYPE],
                        ca.TARIFF: tariff.id,
                    },
                ),
            ),
        )

    return keyboard


async def show_months(callback_data: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    months = await Month.query.gino.all()
    for month in months:
        keyboard.insert(
            InlineKeyboardButton(
                text=month.name,
                callback_data=cd.MONTH_CALLBACK.new(
                    **{
                        ca.SUBJECT: callback_data[ca.SUBJECT],
                        ca.SALE_TYPE: callback_data[ca.SALE_TYPE],
                        ca.TARIFF: callback_data[ca.TARIFF],
                        ca.MONTH: month.id,
                    },
                ),
            ),
        )
    keyboard.add(
        InlineKeyboardButton(
            text="Весь год",
            callback_data=cd.MONTH_CALLBACK.new(
                **{
                    ca.SUBJECT: callback_data[ca.SUBJECT],
                    ca.SALE_TYPE: callback_data[ca.SALE_TYPE],
                    ca.TARIFF: callback_data[ca.TARIFF],
                    ca.MONTH: "all_year",
                },
            ),
        ),
    )
    return keyboard


async def show_student_is_correct():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Да",
            callback_data="student_correct",
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Нет",
            callback_data="student_incorrect",
        )
    )
    return keyboard


async def show_confirm() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Да",
            callback_data="confirm:yes",
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Нет",
            callback_data="confirm:no",
        ),
    )

    return keyboard
