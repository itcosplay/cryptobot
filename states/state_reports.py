from aiogram.dispatcher.filters.state import StatesGroup, State


class Reportsstate(StatesGroup):
    enter_the_reports = State()
    recive_give_box_office = State()
    confirm_recive_box_office = State()
    confirm_give_box_office = State()
    cash_box_text = State()
    text_problem = State()
    message_to_delete = State()
    date_daily_report = State()
    finish_report = State()
    return_request_menu = State()
    finished_requests = State()
    chosen_request = State()
    change_fin_request = State()
    set_new_curr = State()
    set_change_curr = State()
    change_curr_amount = State()
    new_curr = State()
    new_curr_sign = State()
    add_curr_amount = State()

    