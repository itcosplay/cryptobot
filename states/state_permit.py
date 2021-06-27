from aiogram.dispatcher.filters.state import StatesGroup, State


class Permitstate(StatesGroup):
    all_permits = State()
    chosen_permit = State()
    status_permit = State()
    message_to_delete = State()

    single_permit_full_name = State()
    single_permit_id = State()
    single_permit_numb = State()
    single_permit_text = State()
    single_permit_date = State()
    single_permit_confirm = State()

    confirm_delete_permit = State()
    permit_numb = State()

    permit_is_exist = State()
    
