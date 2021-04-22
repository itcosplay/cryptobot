from aiogram.dispatcher.filters.state import StatesGroup, State


class Reportsstate(StatesGroup):
    enter_the_reports = State()
    recive_give_box_office = State()
    confirm_recive_box_office = State()
    confirm_give_box_office = State()