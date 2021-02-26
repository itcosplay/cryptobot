from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request


@dp.callback_query_handler(state=Request.how_much_give_curr)
async def set_how_much_give_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    from keyboards.inline.request_kb import create_kb_send_request

    await call.answer()

    currency = call.data

    await state.update_data(how_much_give_curr=currency)

    data = await state.get_data()
    # print(data) # example:
    # {
    # 'executor': 'changer',
    # 'type_of_operation': 'cache_in',
    # 'type_of_card': 'alfa',
    # 'how_much': 100.0,
    # 'how_much_curr': 'usd'
    # }

    translate_keys_request = {
        'executor': 'исполнитель - ',
        'type_of_operation': 'тип операции - ',
        'type_of_card': 'карта - ',
        'how_much': 'сумма - ',
        'how_much_recive': 'cумма приема - ',
        'how_much_give': 'сумма выдачи - ',
        'how_much_curr': 'валюта - ',
        'how_much_recive_curr': 'валюта приема - ',
        'how_much_give_curr': 'валюта выдачи - ',
        'comment': 'комментарий - '
    } 
    translate_values_request = {
        'changer': 'чейнджер',
        'operator': 'оператор',
        'recive': 'прием',
        'takeout': 'выдача',
        'delivery': 'доставка',
        'cache_in': 'кэшин',
        'change': 'обмен',
        'cache_atm': 'снятие с карт',
        'alfa': 'альфа-банк',
        'sber': 'сбер',
        'rub': 'рубли',
        'usd': 'доллары',
        'eur': 'евро'
    }
    result_data_to_show = []

    for key in data.keys():
        if key in translate_keys_request:
            if (type(data[key]) == int or type(data[key]) == float):
                result_data_to_show.append (
                    translate_keys_request[key] + str(data[key]) + '\n'
                )
            else:
                temp_1 = translate_keys_request[key]
                temp_2 = translate_values_request[data[key]] + '\n'
                
                result_data_to_show.append(temp_1 + temp_2)

    result_data_to_show = ''.join(result_data_to_show)
    keyboard = create_kb_send_request()
    
    await call.message.delete()
    await call.message.answer (
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + result_data_to_show,
        reply_markup = keyboard
    )
    await Request.type_of_end.set()

