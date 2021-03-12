from os import stat
from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    current_requests = State()
    chosen_request = State()
    chosen_request_menu = State()
    what_sum_ready = State()
    chosen_sum_to_ready = State()
    
    # currensy_for_change = State()
    # sum_for_change = State()
    # message_to_delete = State()
    