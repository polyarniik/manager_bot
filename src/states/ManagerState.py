from aiogram.dispatcher.filters.state import StatesGroup, State


class ManagerState(StatesGroup):
    enter_existing_email = State()
    enter_email = State()
    enter_vk_name = State()
    enter_vk_url = State()
