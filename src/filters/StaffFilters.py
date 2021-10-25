from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from data.database import Manager, Coordinator


class IsStaff(BoundFilter):
    key = "is_staff"

    async def check(self, message: Message) -> bool:
        return await IsManager().check(message) or await IsCoordinator().check(message)


class IsManager(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = await Manager.query.where(
            Manager.telegram_id == message.from_user.id
        ).gino.first()
        return True if user else False


class IsCoordinator(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = await Coordinator.query.where(
            Coordinator.telegram_id == message.from_user.id,
        ).gino.first()

        return True if user else False
