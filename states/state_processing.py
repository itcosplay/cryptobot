from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    current_requests = State()
    chosen_request = State()
    reserve_to_ready__currency = State()
    reserve_to_ready__sum = State()
    close__currency = State()
    close__sum = State()
    blue_amount = State()
    blue_amount_chunk = State()
    blue_amount_close = State()
    chunk_recive__currency = State()
    chunk_recive__sum = State()
    other_message = State()

    enter_chosen_request_menu = State()
    enter_reserve_to_ready_menu = State()
    enter_correct_sum_to_ready_menu = State()
    enter_to_confirm_reserve_menu = State()
    enter_to_blue_amount_menu = State()
    enter_to_confirm_blue_menu = State()
    message_to_delete = State()

    enter_correct_sum_chunk_menu = State()
    enter_to_confirm_chunk_menu = State()
    enter_blue_amount_chunk_menu = State()
    enter_to_confirm_blue_menu_chunk = State()

    message_processing = State()
    
    close_request_menu = State()
    which_sum_correct_menu = State()