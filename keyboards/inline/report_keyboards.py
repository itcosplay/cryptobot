from datetime import datetime
from datetime import timedelta

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji
from utils import set_minus_and_plus_currences


def create_kb_reports_menu():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='касса',
            callback_data='box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='суточный отчет',
            callback_data='daily_report'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='исполненые сделки',
            callback_data='finished_requests'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


def create_kb_box_office():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='принять кассу',
            callback_data='recive_box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='сдать кассу',
            callback_data='give_box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


def create_kb_confirm_box_office():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='Подтвердить!',
            callback_data='confirm_box_office'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='сообщить о проблеме',
            callback_data='raise_problem'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


def create_kb_what_date_report():
    today = datetime.today().strftime('%d.%m')
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m")
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text=f'сегодня ({today})',
            callback_data=today
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'вчера ({yesterday})',
            callback_data=yesterday
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


def create_kb_daily_report():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()

    keyboard.add (
        InlineKeyboardButton (
            text='подтвердить',
            callback_data='confirm'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='сообщить о проблеме',
            callback_data='raise_problem'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


cb_finished_requests = CallbackData('cb_fr', 'id', 'type_btn')
def create_kb_finished_requests(finished_requests):
    keyboard = InlineKeyboardMarkup()
    current_date = datetime.today().strftime('%d.%m')

    if len(finished_requests) != 0:
        for request in finished_requests:

            if not current_date == request[0]:
                date_request = '(' + request[0] + ') '
            else:
                date_request = ''

            type_operation = all_emoji[request[3]]
            number_request = request[2]
            request_id = request[1]
            status_operation = all_emoji[request[11]]

            # добавляем плюсы только для отображения
            rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)

            if (rub != '' and usd != '') or (rub != '' and eur != ''):
                rub = rub + ', '
            if usd != '' and eur != '':
                usd = usd + ', '
            
            keyboard.add (
                InlineKeyboardButton (
                    text = '{}{} N{} {} {}{}{}'.format(date_request, type_operation, number_request, status_operation, rub, usd, eur),
                    callback_data = cb_finished_requests.new (
                        id=request_id,
                        type_btn='get_request'
                    )
                )
            )
            
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_finished_requests.new (
                id='-',
                type_btn='exit'
            )
        )
    )

    return keyboard


def create_kb_change_fin_request():
    back__main_menu = all_emoji['back__main_menu']
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add (
        InlineKeyboardButton (
            text='посмотреть историю',
            callback_data='show_history'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='добавить валюту с возвратом в работу',
            callback_data='add_another_curr'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text='изменить сумму с возвратом в работу',
            callback_data='change_sum'
        )
    )
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data='back__main_menu'
        )
    )

    return keyboard


cb_anoter_currency_add_fin = CallbackData('cbacn', 'curr', 'type_btn')
def create_kb_another_currecy_add_fin(request):
    from utils import get_values_FGH
    
    keyboard = InlineKeyboardMarkup()
    rub, usd, eur = get_values_FGH(request)

    if rub == '':
        keyboard.add (
            InlineKeyboardButton (
                text='RUB',
                callback_data = cb_anoter_currency_add_fin.new (
                    curr='rub',
                    type_btn='add_curr'
                )
            )
        )

    if usd == '':
        keyboard.add (
            InlineKeyboardButton (
                text='USD',
                callback_data = cb_anoter_currency_add_fin.new (
                    curr='usd',
                    type_btn='add_curr'
                )
            )
        )

    if eur == '':
        keyboard.add (
            InlineKeyboardButton (
                text='EUR',
                callback_data = cb_anoter_currency_add_fin.new (
                    curr='eur',
                    type_btn='add_curr'
                )
            )
        )

    emo_snail = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_anoter_currency_add_fin.new (
                curr='-',
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard


cb_change_finished_req = CallbackData('cbacn', 'curr', 'type_btn')
def create_kb_change_sum_finished_req(request):
    from utils import get_values_FGH
    
    keyboard = InlineKeyboardMarkup()
    rub, usd, eur = get_values_FGH(request)

    if rub != '':
        keyboard.add (
            InlineKeyboardButton (
                text=rub,
                callback_data = cb_change_finished_req.new (
                    curr='rub',
                    type_btn='change_sum'
                )
            )
        )

    if usd != '':
        keyboard.add (
            InlineKeyboardButton (
                text=usd,
                callback_data = cb_change_finished_req.new (
                    curr='usd',
                    type_btn='change_sum'
                )
            )
        )

    if eur != '':
        keyboard.add (
            InlineKeyboardButton (
                text=eur,
                callback_data = cb_change_finished_req.new (
                    curr='eur',
                    type_btn='change_sum'
                )
            )
        )

    emo_snail = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {emo_snail} главное меню',
            callback_data=cb_change_finished_req.new (
                curr='-',
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard
