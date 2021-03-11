from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    current_requests = State()
    choosed_request = State()