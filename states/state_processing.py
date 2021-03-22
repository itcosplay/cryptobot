from os import stat
from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    current_requests = State()
    chosen_request = State()
    chosen_request_menu = State()
    confirm_cancel_request = State()
    what_sum_ready = State()
    chosen_sum_to_ready = State()
    sum_currency_to_change = State()
    sum_currency_to_change = State()
    sum_amount_to_change = State()
    message_to_delete = State()
    blue_amount = State()
    enter_blue_amount = State()
    confirm_blue_amount = State()
    correct_curr_sum_ready = State()
    correct_amount_sum_ready = State()
    confirm_correct_to_ready = State()
    
    