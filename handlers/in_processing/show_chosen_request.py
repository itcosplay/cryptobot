from os import stat
import re
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing

from keyboards import cb_current_requests
from keyboards import main_menu
from keyboards import create_kb_chosen_request

from keyboards import cb_current_requests

# from show_current_requests

# @dp.callback_query_handler(cb_current_requests.filter(type_btn='get_request'))
@dp.callback_query_handler(state=Processing.chosen_request)
async def show_chosen_request(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает нажатие на одну из заявок, выведенных списком
    '''
    await call.answer()

    data_btn = cb_current_requests.parse(call.data)
    # {'id': , 'type_btn': }

    if data_btn['type_btn'] == 'exit':
        await call.message.delete()
        await call.message.answer (
            f'===========\nПросмотр заявок отменен\n===========',
            reply_markup=main_menu
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    current_requests = data_state['current_requests']

    for request in current_requests:
        if data_btn['id'] == request[2]:
            await state.update_data(chosen_request=request)
            break

    data_state = await state.get_data()
    request = data_state['chosen_request']


    
    
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    
    # убираем минусы и при обмене - добавляем плюсы
    if request[3] == 'обмен':
        if not request[5] == '-':
            rub = request[5]
            rub = str(rub)
            if rub[0] == '-': rub = rub + '₽  '
            else: rub = '+' + rub + '₽  '
        else:
            rub = ''

        if not request[6] == '-':
            usd = request[6]
            usd = str(usd)
            if usd[0] == '-': usd = usd + '$  '
            else: usd = '+' + usd + '$  '
        else:
            usd = ''

        if not request[7] == '-':
            eur = request[7]
            eur = str(eur)
            if eur[0] == '-': eur = eur + '€'
            else: eur = '+' + eur + '€'
        else:
            eur = ''

    else:
        if not request[5] == '-':
            rub = request[5]
            rub = str(rub)
            if rub[0] == '-': rub = rub[1:] + '₽  '
            else: rub = rub + '₽  '
        else: rub = ''

        if not request[6] == '-':
            usd = request[6]
            usd = str(usd)
            if usd[0] == '-': usd = usd[1:] + '$  '
            else: usd = usd + '$  '
        else: usd = ''

        if not request[7] == '-':
            eur = request[7]
            eur = str(eur)
            if eur[0] == '-': eur = eur[1:] + '€'
            else: eur = eur + '€'
        else: eur = ''

    await call.message.delete()
    await call.message.answer (
        'Заявка #{} от {}\n{}\n{}{}{}'.format (
            id_request, 
            date_request, 
            operation_type_request,
            rub,
            usd,
            eur
        ),
        reply_markup=create_kb_chosen_request(request)
    )
    await Processing.chosen_request_menu.set()
    # to chosen_request_menu
    