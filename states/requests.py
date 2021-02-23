from aiogram.dispatcher.filters.state import StatesGroup, State

class Request(StatesGroup):
    executor = State() # чейндж или оператор
    type_of_operation = State()
    type_of_card = State()
    how_much = State() # сумма для прием/выдача/доставка/кэшин-альфа/кэшин-сбер
    how_much_recive = State() # сколько принимаем при обмене