from os import stat
from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    current_requests = State()
    chosen_request = State()
    reserve_to_ready__currency = State()
    reserve_to_ready__sum = State()

    enter_chosen_request_menu = State()
    enter_reserve_to_ready_menu = State()
    enter_correct_sum_to_ready_menu = State()
    message_to_delete = State()
    