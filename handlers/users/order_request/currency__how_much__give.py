from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request
from keyboards import create_kb_send_request_for_change

@dp.callback_query_handler(state=Request.currency__how_much__give)
async def set_how_much_give_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()
    await call.message.delete()

    currency = call.data
    request_data = await state.get_data()
    # получаем список уже имеющихся валют либо пустой список
    currencies__give = request_data['currencies__give']

    if currency not in currencies__give:
        currencies__give.append(currency)
        await state.update_data(currencies__give=currencies__give)

    if currency == 'rub':
        await state.update_data(sum_give_RUB=request_data['how_much_give'])
    if currency == 'usd':
        await state.update_data(sum_give_USD=request_data['how_much_give'])
    if currency == 'eur':
        await state.update_data(sum_give_EUR=request_data['how_much_give'])

    ### for logs ### delete later
    request_data = await state.get_data()
    print('=== state: ===')
    print(request_data)
    print('==============')
    ### for logs ### delete later

    translate_keys_request = {
        'applicant': 'заявитель: ',
        'operation_type': 'тип операции: ',
        'sum_recive_RUB': 'СУММА ВЫДАЧИ(RUB): ',
        'sum_recive_USD': 'СУММА ВЫДАЧИ(USD): ',
        'sum_recive_EUR': 'СУММА ВЫДАЧИ(EUR): ',
        'sum_give_RUB': 'СУММА ПРИЕМА(RUB): ',
        'sum_give_USD': 'СУММА ПРИЕМА(USD): ',
        'sum_give_EUR': 'СУММА ПРИЕМА(EUR): ',
        'comment': 'комментарий: ',
        'permit': 'пропуск на '
    } 
    translate_values_request = {
        'changer': 'чейнджер',
        'operator': 'оператор',
        'recive': 'прием',
        'takeout': 'выдача',
        'delivery': 'доставка',
        'cashin': 'кэшин',
        'change': 'обмен',
        'cache_atm': 'снятие с карт',
        'alfa': 'альфа-банк',
        'sber': 'сбер',
        'rub': 'рубли',
        'usd': 'доллары',
        'eur': 'евро',
        'sum_plus': '',
        'sum_minus': '',
        'ok': ''
    }
    result_data_to_show = []
    for key in request_data.keys():
        if key in translate_keys_request:
            if (type(request_data[key]) == int or type(request_data[key]) == float):
                result_data_to_show.append (
                    translate_keys_request[key] + str(request_data[key]) + '\n'
                )
            elif key == 'comment':
                temp_1 = translate_keys_request[key]
                temp_2 = request_data[key] + '\n'

                result_data_to_show.append(temp_1 + temp_2)
            elif key == 'permit':
                temp_1 = translate_keys_request[key]
                temp_2 = request_data[key] + '\n'

                result_data_to_show.append(temp_1 + temp_2)
            else:
                temp_1 = translate_keys_request[key]
                temp_2 = translate_values_request[request_data[key]] + '\n'
                
                result_data_to_show.append(temp_1 + temp_2)

    result_data_to_show = ''.join(result_data_to_show)

    keyboard = create_kb_send_request_for_change(request_data['currencies__recive'], request_data['currencies__give'])
    
    await call.message.answer (
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + result_data_to_show,
        reply_markup = keyboard
    )
    await Request.type_end.set()
    # to final_step_ordering.py

