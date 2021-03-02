from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_send_request
from keyboards import create_kb_send_request_for_change
from keyboards import create_kb_send_request_atm

# from final_step_ordering.py
@dp.message_handler(state=Request.permit)
async def permit(message:types.Message, state:FSMContext):
    text = message.text

    await state.update_data(permit=text)
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id - 1
    )
    request_data = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )      

    request_data = await state.get_data()

    if request_data['operation_type'] == 'recive' \
    or request_data['operation_type'] == 'takeout' \
    or request_data['operation_type'] == 'delivery' \
    or request_data['operation_type'] == 'cashin':
        keyboard = create_kb_send_request(request_data['currencies__how_much'])
    if request_data['operation_type'] == 'change':
        keyboard = create_kb_send_request_for_change(request_data['currencies__recive'], request_data['currencies__give'])
    if request_data['operation_type'] == 'cash_atm':
        data = await state.get_data()
        print(data)
        keyboard = create_kb_send_request_atm()
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + \
        'заявитель: ' + data['applicant'] + '\n' + \
        'тип операции: ' + data['operation_type'] + '\n' + \
        'комментарий: ' + data['comment'] + '\n' + \
        'пропуск на:' + data['permit'] + '\n'

        await message.answer(text, reply_markup=keyboard)
        await Request.type_end.set()
        # to final_step_ordering.py
        return
        

    ### for logs ### delete later
    request_data = await state.get_data()
    print('=== state: ===')
    print(request_data)
    print('==============')
    ### for logs ### delete later
    translate_keys_request = {
        'applicant': 'заявитель: ',
        'operation_type': 'тип операции: ',
        'sum_RUB__how_much':'СУММА(RUB): ',
        'sum_USD__how_much':'СУММА(USD): ',
        'sum_EUR__how_much':'СУММА(EUR): ',
        'sum_recive_RUB': 'СУММА ПРИЕМА(RUB): ',
        'sum_recive_USD': 'СУММА ПРИЕМА(USD): ',
        'sum_recive_EUR': 'СУММА ПРИЕМА(EUR): ',
        'sum_give_RUB': 'СУММА ВЫДАЧИ(RUB): ',
        'sum_give_USD': 'СУММА ВЫДАЧИ(USD): ',
        'sum_give_EUR': 'СУММА ВЫДАЧИ(EUR): ',
        'comment': 'комментарий: ',
        'permit': 'данные пропуска: '
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

    await message.answer (
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + result_data_to_show,
        reply_markup = keyboard
    )
    await Request.type_end.set()
    # to final_step_ordering.py

    