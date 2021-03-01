from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Request
from keyboards import create_kb_send_request


# from temp_sum_message_handler.py
@dp.callback_query_handler(state=Request.currencies__how_much)
async def set_currency__how_much (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()
    await call.message.delete()

    currency = call.data
    data_request = await state.get_data()
    # получаем список уже имеющихся валют либо пустой список
    currencies__how_much = data_request['currencies__how_much']

    if currency not in currencies__how_much:
        currencies__how_much.append(currency)
        await state.update_data(currencies__how_much=currencies__how_much)
    if currency == 'rub':
        await state.update_data(sum_RUB__how_much=data_request['temp_sum_state'])
    if currency == 'usd':
        await state.update_data(sum_USD__how_much=data_request['temp_sum_state'])
    if currency == 'eur':
        await state.update_data(sum_EUR__how_much=data_request['temp_sum_state'])

    ### for logs ### delete later
    request_data = await state.get_data()
    print('=== state: ===')
    print(request_data)
    print('==============')
    ### for logs ### delete later

    request_data = await state.get_data()

    translate_keys_request = {
        'applicant': 'заявитель: ',
        'operation_type': 'тип операции: ',
        'card_type': 'карта: ',
        'sum_RUB__how_much' : 'СУММА(RUB): ',
        'sum_USD__how_much' : 'СУММА(USD): ',
        'sum_EUR__how_much' : 'СУММА(EUR): ',
        'type_of_card': 'карточка: ',
        'how_much_recive': 'cумма - ',
        'how_much_give': 'сумма - ',
        'how_much_curr': 'валюта - ',
        'how_much_recive_curr': 'валюта - ',
        'how_much_give_curr': 'валюта - ',
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
        if request_data[key] == '':
            pass
        else:

            if key in translate_keys_request:
                if \
                (type(request_data[key]) == int or \
                type(request_data[key]) == float):
                    result_data_to_show.append (
                        translate_keys_request[key] + \
                        str(request_data[key]) + '\n'
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
                    temp_2 = translate_values_request[request_data[key]] \
                    + '\n'

                    result_data_to_show.append(temp_1 + temp_2)

    result_data_to_show = ''.join(result_data_to_show)
    text = \
    'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
    'СО СЛЕДУЮЩИМИ ДАННЫМИ\n' + \
    result_data_to_show

    await call.message.answer (
        text = text,
        reply_markup = create_kb_send_request(request_data['currencies__how_much'])
    )
    await Request.type_end.set()
    # to final_step_ordering.py

