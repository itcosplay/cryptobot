from emoji import emojize

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_chosen_requests = CallbackData('cb_chr', 'type_btn')


def create_kb_chosen_request(request):
    emo_snail = emojize(':snail:', use_aliases=True)
    keyboard = InlineKeyboardMarkup()

    if request[3] == 'выдача в офисе' or request[3] == 'доставка' or request[3] == 'кэшин' or request[3] == 'обмен':
        keyboard.add (
            InlineKeyboardButton (
                text = 'отложить на выдачу',
                callback_data=cb_chosen_requests.new(type_btn='to_ready_for_give')
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text = 'изменить заявку',
                callback_data=cb_chosen_requests.new(type_btn='change_request')
            )
        )
        keyboard.add (
            InlineKeyboardButton (
                text = 'отменить заявку',
                callback_data=cb_chosen_requests.new(type_btn='cancel_request')
            )
        )
    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data=cb_chosen_requests.new(type_btn='back_main_menu')
        )
    )

    return keyboard