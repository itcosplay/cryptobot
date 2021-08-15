from data import all_emoji

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_chosen_requests = CallbackData('cb_chr', 'type_btn')


def create_kb_chosen_request(request):
    keyboard = InlineKeyboardMarkup()

    if request[3] == 'выдача' or request[3] == 'кэшин' or request[3] == 'обмен':
        keyboard.add (
            InlineKeyboardButton (
                text = 'отложить на выдачу',
                callback_data=cb_chosen_requests.new(type_btn='to_ready_for_give')
            )
        )
    
    if request[3] == 'обмен' or request[3] == 'прием' or request[3] == 'снятие с карт':
        keyboard.add (
            InlineKeyboardButton (
                text = 'принято частично',
                callback_data=cb_chosen_requests.new(type_btn='recived_chunck')
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text = 'закрыть заявку',
            callback_data=cb_chosen_requests.new(type_btn='close_request')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'сообщение',
            callback_data=cb_chosen_requests.new(type_btn='message_to')
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
            text = 'добавить данные пропуска',
            callback_data=cb_chosen_requests.new(type_btn='add_permit')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'добавить коментарий',
            callback_data=cb_chosen_requests.new(type_btn='add_comment')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'распаковать',
            callback_data=cb_chosen_requests.new(type_btn='unpack')
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
            text = f'назад',
            callback_data=cb_chosen_requests.new(type_btn='back')
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text = f'главное меню',
            callback_data=cb_chosen_requests.new(type_btn='main_menu')
        )
    )

    return keyboard