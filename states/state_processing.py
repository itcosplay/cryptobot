from aiogram.dispatcher.filters.state import StatesGroup, State


class Processing(StatesGroup):
    is_changed = State() # mark of change request
    all_changes_data = State()
    changed_request = State()

    current_requests = State()
    in_processing_requests = State()
    ready_to_give_requests = State()
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
    change_request_menu = State()
    which_sum_correct_menu = State()

    select_date = State()
    typing_coustom_date = State()
    new_request_id = State()
    new_request_type = State()

    which_sum_change = State()
    which_sum_change__currency = State()
    which_sum_change__amount = State()

    another_currency_add_menu = State()
    another_currency__give_recive = State()
    another_currecy__currency = State()
    another_currecy__amount = State()
    
    add_another_comment = State()

    add_permit = State()

    confirm_cancel_request = State()