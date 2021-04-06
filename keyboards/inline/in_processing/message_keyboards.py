from emoji import emojize
from data import all_emoji

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_message_keyboard = CallbackData('cb_mk', 'type_btn')
def create_kb_message_keyboard():
    emo_snail = all_emoji['back__main_menu']
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'принял без пересчета',
            callback_data = cb_message_keyboard.new(type_btn='recived_without')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'до сих пор не было',
            callback_data = cb_message_keyboard.new(type_btn='nobody')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вышел из офиса',
            callback_data = cb_message_keyboard.new(type_btn='go_out_office')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'в доставке',
            callback_data = cb_message_keyboard.new(type_btn='in_delivery')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'ожидаю подтверждения',
            callback_data = cb_message_keyboard.new(type_btn='wait_confirm')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'связался',
            callback_data = cb_message_keyboard.new(type_btn='contacted')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'свой текст сообщения',
            callback_data = cb_message_keyboard.new(type_btn='other_text')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = cb_message_keyboard.new(type_btn='back__main_menu')
        )
    )

    return keyboard