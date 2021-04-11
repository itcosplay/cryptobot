from datetime import datetime
from datetime import timedelta
import keyboards

from data import all_emoji

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


cb_change_request = CallbackData('cb_mk', 'type_btn')
def create_kb_change_request(request):
    emo_snail = all_emoji['back__main_menu']
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = 'иная дата',
            callback_data = cb_change_request.new(type_btn='another_data')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'новый номер',
            callback_data = cb_change_request.new(type_btn='new_id')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'переопределить тип',
            callback_data = cb_change_request.new(type_btn='change_type')
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'изменить сумму',
            callback_data = cb_change_request.new(type_btn='update_sum')
        )
    )

    if request[5] == '0' or request[6] == '0' or request[7] == '0':
        keyboard.add (
            InlineKeyboardButton (
                text = 'другая валюта',
                callback_data = cb_change_request.new(type_btn='more_currency')
            )
        )

    keyboard.add (
        InlineKeyboardButton (
            text = 'добавить коментарий',
            callback_data = cb_change_request.new(type_btn='add_commetn')
        )
    )

    keyboard.add (
        InlineKeyboardButton (
            text = f'назад {emo_snail} главное меню',
            callback_data = cb_change_request.new(type_btn='back__main_menu')
        )
    )

    return keyboard


def create_kb_change_date():
    emo_snail = all_emoji['back__main_menu']
    # current_date = datetime.today().strftime('%d.%m')
    tomorrow_date =  (datetime.now() + timedelta(days=1)).strftime("%d.%m")
    after_tomorrow_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m")

    keyboard = InlineKeyboardMarkup()
    keyboard.add (
        InlineKeyboardButton (
            text = f'на завтра ({tomorrow_date})',
            callback_data = 'set_tomorrow_date'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'на послезавтара ({after_tomorrow_date})',
            callback_data = 'set_after_tomorrow_date'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'ввести дату в ручную',
            callback_data = 'enter_coustom_date'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = 'back_to_request'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'отменить {emo_snail} главное меню',
            callback_data = 'back__main_menu'
        )
    )

    return keyboard


def create_kb_new_request_type(request_type):
    emo_snail = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()

    all_request_types = {
        'выдача в офисе': 'issuing_office',
        'прием кэша': 'cash_recive',
        'доставка': 'delivery',
        'обмен': 'exchange',
        'кэшин': 'cash_in',
        'снятие с карт': 'cash_out'
    }

    for key in all_request_types.keys():
        if key != request_type:
            keyboard.add (
                InlineKeyboardButton (
                    text = key,
                    callback_data = all_request_types[key]
                )
            )

    keyboard.add (
        InlineKeyboardButton (
            text = 'вернуться к заявке',
            callback_data = 'back_to_request'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text = f'отменить {emo_snail} главное меню',
            callback_data = 'back__main_menu'
        )
    )

    return keyboard


cb_anoter_currency_add = CallbackData('cbacn', 'curr', 'type_btn')
def create_kb_another_currecy_add(request):
    from utils import get_values_FGH
    
    keyboard = InlineKeyboardMarkup()
    rub, usd, eur = get_values_FGH(request)

    if rub == '':
        keyboard.add (
            InlineKeyboardButton (
                text='RUB',
                callback_data = cb_anoter_currency_add.new (
                    curr='rub',
                    type_btn='add_curr'
                )
            )
        )

    if usd == '':
        keyboard.add (
            InlineKeyboardButton (
                text='USD',
                callback_data = cb_anoter_currency_add.new (
                    curr='usd',
                    type_btn='add_curr'
                )
            )
        )

    if eur == '':
        keyboard.add (
            InlineKeyboardButton (
                text='EUR',
                callback_data = cb_anoter_currency_add.new (
                    curr='eur',
                    type_btn='add_curr'
                )
            )
        )

    emo_snail = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_anoter_currency_add.new (
                curr='-',
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard


def create_kb_choose_give_recive_change():
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text='принимаем',
            callback_data='recive_money'
            
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='выдаем',
            callback_data='give_money'
            
        )
    )

    emo_snail = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data='back__main_menu'
            
        )
    )

    return keyboard
