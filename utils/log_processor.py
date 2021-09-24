import copy
import datetime
import json

from data import all_emoji

from .get_values_FGH_MNO import get_values_FGH_sort


def get_request_as_string(request):
    str_request = copy.copy(request)
    str_request[9] = '0'

    str_request = json.dumps(str_request, ensure_ascii=False)
    str_request = str_request.replace('"', r'\"')

    return str_request


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

    return text


def get_request_as_array(request:str):
    request = request.replace('\\\"', r'"')
    request = json.loads(request)

    return request