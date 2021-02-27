from aiogram.dispatcher.filters.state import StatesGroup, State

class Request(StatesGroup):
    # if 'создать заявку' нажал админ ('admin') заявителем будет чейндж
    # if 'создать заявку' нажал чейндж ('changer') заявителем будет чейндж
    applicant = State()
    operation_type = State()
    type_of_card = State() # альфа или сбер
    how_much = State() # сумма для прием/выдача/доставка/кэшин
    currencies__how_much = State()

    temp_sum_state = State() #
    sum_RUB__how_much = State()
    sum_USD__how_much = State()
    sum_EUR__how_much = State()

    sum_plus_minus = State() # Приход или Расход(+/-)
    addition = State()
    substraction = State()


    how_much_recive = State() # сколько принимаем при обмене
    how_much_recive_curr = State()
    how_much_give = State() # сколько выдаем при обмене

    

    how_much_give_curr = State()
    comment = State()
    permit = State() # ФИО для пропуска
    type_end = State()
    
    adding_sum = State()
    adding_sum_currency = State()

