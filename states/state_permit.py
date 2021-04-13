from aiogram.dispatcher.filters.state import StatesGroup, State


class Permitstate(StatesGroup):
    all_permits = State()
    chosen_permit = State()
    status_permit = State()
    message_to_delete = State()

    single_permit_data = State()
    single_permit_id = State()
    single_permit_text = State()
    single_permit_date = State()
    single_permit_confirm = State()
    
