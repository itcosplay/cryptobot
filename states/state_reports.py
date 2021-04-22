from aiogram.dispatcher.filters.state import StatesGroup, State


class Reportsstate(StatesGroup):
    enter_the_reports = State()