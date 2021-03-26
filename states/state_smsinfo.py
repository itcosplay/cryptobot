from aiogram.dispatcher.filters.state import StatesGroup, State


class SMSstate(StatesGroup):
    sms_numb = State()
    message_to_delete = State()
    who_waste = State()
    for_what_waste = State()
    yes_no_note = State()
    note_waste = State()
    
