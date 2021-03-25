from aiogram.dispatcher.filters.state import StatesGroup, State


class Permitstate(StatesGroup):
    all_permits = State()
    chosen_permit = State()
