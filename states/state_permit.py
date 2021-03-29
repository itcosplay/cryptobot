from aiogram.dispatcher.filters.state import StatesGroup, State


class Permitstate(StatesGroup):
    all_permits = State()
    chosen_permit = State()
    status_permit = State()
    single_permit_data = State()
    message_to_delete = State()
