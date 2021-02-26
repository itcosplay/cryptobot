from aiogram.dispatcher.filters.state import StatesGroup, State

class Request(StatesGroup):
    executor = State() # чейндж или оператор
    type_of_operation = State()
    type_of_card = State() # альфа или сбер
    how_much = State() # сумма для прием/выдача/доставка/кэшин
    how_much_curr = State()
    how_much_recive = State() # сколько принимаем при обмене
    how_much_recive_curr = State()
    how_much_give = State() # сколько выдаем при обмене
    how_much_give_curr = State()
    comment = State()
    permit = State() # ФИО для пропуска
    type_of_end = State()
    summ_plus_minus = State() # Приход или Расход(+/-)