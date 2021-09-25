import copy
import datetime
import json

from aiohttp.client import request

from data import all_emoji

from .get_values_FGH_MNO import get_values_FGH_sort
from .request_data_functions import get_beauty_sum


def get_request_as_string(request):
    str_request = copy.copy(request)
    str_request[9] = '0'

    str_request = json.dumps(str_request, ensure_ascii=False)
    str_request = str_request.replace('"', r'\"')

    return str_request


def replace_shit_in_string(some_string:str, shit:str):
    if shit == '\"':
        some_string = some_string.replace('\\"', r'"')

    return some_string


def get_request_as_array(request:str):
    request = request.replace('\\\"', r'"')
    request = json.loads(request)

    return request


def updating_log (
    update_type:str,
    user:str,
    request:str,
    update_data:str=''
):
    '''
    Returns updated log for current action
    like a string.
    '''
    log_time = datetime.datetime.today().strftime("%H:%M %d/%m/%y")
    updated_request = get_request_as_string(request)

    log_data = {
        'ACTION_NAME': update_type,
        'action_date': log_time,
        'user_name': user,
        'entire_request': updated_request,
        'additional_data': 'empty'
    }

    if update_type == 'MESSAGE':
        log_data['additional_data'] = {
            'text_message': update_data
        }

    if update_type == 'PERMIT':
        log_data['additional_data'] = {
            'permit_status': update_data
        }

    if update_type == 'COMMENT':
        log_data['additional_data'] = {
            'comment_text': update_data
        }

    full_log_data = request[9]
    
    if full_log_data == '0' or full_log_data == 0:
        full_log_data = '[]'

    full_log_data = json.loads(full_log_data)
    full_log_data.append(log_data)
    full_log_data = json.dumps(full_log_data,  ensure_ascii=False)

    return full_log_data


def get_text_after_change_request_for_log(old_request, changed_request):
    # ['01.09', '16152t5', '8888', 'прием', 'change', '500', '0', '-500', 'комментарий', '0', 'proprosh', 'В обработке', '0', '0', '0', '0', '0']
    # ['02.09', '16152t5', '8888', 'прием', 'change',  500 , '0',  -500 , 'комментарий', '0', 'proprosh', 'В обработке', '0', '0', '0', '0', '0']
    text = ''

    if old_request[0] != changed_request[0]:
        text = text + '\n🗓️ новая дата 🗓️\n'
        text = text + old_request[0] + ' 👉 ' + changed_request[0]
    
    if old_request[2] != changed_request[2]:
        text = text + '\n#️⃣ новый номер #️⃣\n'
        text = text + '#N' + old_request[2] + ' 👉 ' + '#N' + changed_request[2]

    if old_request[3] != changed_request[3]:
        text = text + '\n🚻 новый тип 🚻\n'
        text = text + old_request[3] + ' 👉 ' + changed_request[3]

    if str(old_request[5]) != str(changed_request[5]) \
    or str(old_request[6]) != str(changed_request[6]) \
    or str(old_request[7]) != str(changed_request[7]):
        text = text + '\n⚠️ изменение в суммах ⚠️'
       
        if str(old_request[5]) != str(changed_request[5]):
            old_rub = str(old_request[5])
            new_rub = str(changed_request[5])

            old_rub = get_beauty_sum(old_rub)
            new_rub = get_beauty_sum(new_rub)

            text = text + '\n'
            text = text + old_rub + '₽' + ' 👉 ' + new_rub + '₽'

        if str(old_request[6]) != str(changed_request[6]):
            old_usd = str(old_request[6])
            new_usd = str(changed_request[6])

            old_usd = get_beauty_sum(old_usd)
            new_usd = get_beauty_sum(new_usd)

            text = text + '\n'
            text = text + old_usd + '$' + ' 👉 ' + new_usd + '$'

        if str(old_request[7]) != str(changed_request[7]):
            old_eur = str(old_request[7])
            new_eur = str(changed_request[7])

            old_eur = get_beauty_sum(old_eur)
            new_eur = get_beauty_sum(new_eur)

            text = text + '\n'
            text = text + old_eur + '€' + ' 👉 ' + new_eur + '€'

    text += '\n'

    return text


def beauty_text_log_builder(data_log):
    text = ''
    count = 0
    data_log = json.loads(data_log)

    for event in data_log:
        count += 1
        date = event['action_date']
        user = event['user_name']
        request = get_request_as_array(event['entire_request'])
        
        if event['ACTION_NAME'] == 'CREATE_REQUEST':
            request_numb = request[2]
            request_type = request[3]
            currencies = get_values_FGH_sort(request)

            for currency in currencies:
                if currency == '0': currency = ''

            text += f'⚙️ Создание заявки N{request_numb}\n'
            text += f'🕑 {date}\n'
            text += f'{all_emoji[request_type]} {request_type}, суммы:\n'
            text += f'{currencies[0]}{currencies[1]}{currencies[2]}'
            text += f'🧑‍🔧 @{user}'
        
        if event['ACTION_NAME'] == 'COMMENT':
            comment = event['additional_data']['comment_text']

            text += '\n\n\n'
            text += '📝 Добавлен коментарий\n'
            text += f'🕑 {date}\n'
            text += f'✏️ {comment}\n'
            text += f'👤 @{user}'

        if event['ACTION_NAME'] == 'PERMIT':
            permit_status = event['additional_data']['permit_status']

            text += '\n\n\n'
            text += f'🎫 {permit_status}\n'
            text += f'🕑 {date}\n'
            text += f'👤 @{user}'

        if event['ACTION_NAME'] == 'MESSAGE':
            text_message = event['additional_data']['text_message']

            text += '\n\n\n'
            text += '✉️ Оставлено сообщение\n'
            text += f'🕑 {date}\n'
            text += f'📃 {text_message}\n'
            text += f'👤 @{user}'

        if event['ACTION_NAME'] == 'CHANGE':
            prev_request_condition = data_log[count - 2]['entire_request']
            prev_request_condition = replace_shit_in_string (
                prev_request_condition,
                '\"'
            )
            prev_request_condition = json.loads(prev_request_condition)

            curr_request_condition = event['entire_request']
            curr_request_condition = replace_shit_in_string (
                curr_request_condition,
                '\"'
            )
            curr_request_condition = json.loads(curr_request_condition)

            text += '\n\n\n'
            text += '↔️ Изменение в заявке\n'
            text += f'🕑 {date}'
            text += get_text_after_change_request_for_log (
                prev_request_condition,
                curr_request_condition
            )
            text += f'👤 @{user}'
            
    return text