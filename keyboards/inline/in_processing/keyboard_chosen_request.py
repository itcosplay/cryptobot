from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_chosen_requests = CallbackData('cb_chr', 'type_btn')


def create_kb_chosen_request(request):
    keyboard = InlineKeyboardMarkup()

    if not request[11] == 'Готово к выдаче':
        keyboard.add (
            InlineKeyboardButton (
                text='отложить на выдачу',
                callback_data=cb_chosen_requests.new(type_btn='ready_to_give')
            )
        )
    else:
        keyboard.add (
            InlineKeyboardButton (
                text = 'закрыть заявку',
                callback_data=cb_chosen_requests.new(type_btn='close')
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text = 'изменить заявку',
            callback_data=cb_chosen_requests.new(type_btn='change')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'отменить заявку',
            callback_data=cb_chosen_requests.new(type_btn='cancel')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'назад',
            callback_data=cb_chosen_requests.new(type_btn='back')
        )
    )

    return keyboard