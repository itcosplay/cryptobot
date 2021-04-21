from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import all_emoji


cb_all_permits = CallbackData('cb_all_permits', 'id', 'type_btn')
def create_kb_all_permits(permits):
    current_date = datetime.today().strftime('%d.%m')

    keyboard = InlineKeyboardMarkup()

    for permit in permits:

        if current_date != permit[3]:
            permit_date = permit[3]
        else:
            permit_date = ''
        
        if permit[4] == 'нужно заказать':
            permit_status = all_emoji['квз']

        elif permit[4] == 'заказан':
            permit_status = all_emoji['заказан']

        elif permit[4] == 'отработан':
            permit_status = all_emoji['отработан']

        else:
            permit_status = 'БЛЯ'

        permit_id = permit[1]
        permit_text = permit[2]
       
        keyboard.add (
            InlineKeyboardButton (
                text=f'{permit_date}{permit_status} #N{permit_id} {permit_text}',
                callback_data = cb_all_permits.new (
                    id=permit_id,
                    type_btn='get_permit'
                )
            )
        )
            
    back__main_menu = all_emoji['back__main_menu']
    keyboard.add (
        InlineKeyboardButton (
            text=f'назад {back__main_menu} главное меню',
            callback_data=cb_all_permits.new (
                id='-',
                type_btn='back__main_menu'
            )
        )
    )

    return keyboard



              