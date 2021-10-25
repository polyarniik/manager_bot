from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    enter_manager_id = State()
    enter_manager_full_name = State()
