import copy
import datetime
import json



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
    Returns updated log for current action.
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

    # update_type = update_type.split(':')

    # if update_type[0] == 'MESSAGE':
    #     log_data['additional_data'] = {
    #         'text_message': update_type[1]
    #     }

    if update_type == 'MESSAGE':
        log_data['additional_data'] = {
            'text_message': update_data
        }


    full_log_data = request[9]
    full_log_data = json.loads(full_log_data)
    full_log_data.append(log_data)
    full_log_data = json.dumps(full_log_data,  ensure_ascii=False)

    return full_log_data