from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    in_processing = State()
    ready_to_give = State()
    current_requests = State()