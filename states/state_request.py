from aiogram.dispatcher.filters.state import StatesGroup, State


class Request(StatesGroup):
    # if 'создать заявку' нажал админ ('admin') заявителем будет чейндж
    # if 'создать заявку' нажал чейндж ('changer') заявителем будет чейндж
    request_id = State()
    applicant = State()
    operation_type = State()
    type_of_card = State() # альфа или сбер
    how_much = State() # сумма для прием/выдача/доставка/кэшин

    currencies__how_much = State()

    temp_sum_state = State() #
    sum_RUB__how_much = State()
    sum_USD__how_much = State()
    sum_EUR__how_much = State()

    sum_recive_RUB = State()
    sum_recive_USD = State()
    sum_recive_EUR = State()

    sum_give_RUB = State()
    sum_give_USD = State()
    sum_give_EUR = State()

    plus_minus = State() # Приход или Расход(+/-)

    how_much_recive = State() 
    how_much_give = State()

    currencies__recive = State()
    currencies__give = State()
    currency__how_much__recive = State()
    currency__how_much__give = State()

    comment = State()
    permit = State() # ФИО для пропуска
    type_end = State()
    data_request = State()

    _del_message = State()
