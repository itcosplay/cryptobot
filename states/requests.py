from aiogram.dispatcher.filters.state import StatesGroup, State

class Request(StatesGroup):
    executor = State()
    type_of_operation = State()
    type_of_card = State()