from keyboards import create_kb_send_request
from keyboards import create_kb_send_request_for_change
from keyboards import create_kb_send_request_atm

def get_data_to_show(request_data):

    if request_data['operation_type'] == 'get_in'  \
    or request_data['operation_type'] == 'get_out' \
    or request_data['operation_type'] == 'cash_in_ATM':
        keyboard = create_kb_send_request(request_data['currencies__how_much'])

    elif request_data['operation_type'] == 'change':
        keyboard = create_kb_send_request_for_change(request_data['currencies__recive'], request_data['currencies__give'])

    elif request_data['operation_type'] == 'cash_out_ATM':
        keyboard = create_kb_send_request_atm()

    elif request_data['operation_type'] == 'documents':
        keyboard = create_kb_send_request_atm()

        result_data_to_show = 'Будет создана заявка "Документы"'
        
        return result_data_to_show, keyboard

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
        'permit': 'данные пропуска: ',
        'data_request': 'дата: '
    }

    translate_values_request = {
        'changer': 'change',
        'operator': 'оператор',

        'get_in': 'прием',
        'get_out': 'выдача',
        'change': 'обмен',
        'cash_in_ATM': 'кэшин', 
        'cash_out_ATM': 'снятие с карт',
        'documents': 'документы',

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

                elif key == 'data_request':
                    temp_1 = translate_keys_request[key]
                    temp_2 = request_data[key] + '\n'
                    result_data_to_show.append(temp_1 + temp_2)

                else:
                    temp_1 = translate_keys_request[key]
                    temp_2 = translate_values_request[request_data[key]] + '\n'
                    
                    result_data_to_show.append(temp_1 + temp_2)

    result_data_to_show = 'Будет создана заявка с данными:\n' + ''.join(result_data_to_show)

    return result_data_to_show, keyboard
