from config.config import MONTHS, TARIFFS, SUBJECTS, SALE_TYPES
from data.database import Month, Tariff, Subject, SaleType


async def fill_db():
    for column, name in MONTHS.items():
        if await Month.query.where(Month.name == name).gino.first() is None:
            await Month.create(name == name, column == column)

    for tariff in TARIFFS:
        if await Tariff.query.where(Tariff.name == tariff).gino.first() is None:
            await Tariff.create(name=tariff)

    for subject in SUBJECTS:
        if await Subject.query.where(Subject.name == subject).gino.first() is None:
            await Subject.create(name=subject)

    for sale_type in SALE_TYPES:
        if await SaleType.query.where(SaleType.name == sale_type).gino.first() is None:
            await SaleType.create(name=sale_type)
