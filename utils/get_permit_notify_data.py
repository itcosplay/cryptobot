from utils import set_minus_and_plus_currences
# from utils.get_values_FGH_MNO import get_single_value
from data import all_emoji


def permit_notify_data(request, ready_or_office):
    print('')
    print('')
    print('##### #####')
    print('utils/get_permit_notify_data/permit_notify_data')
    print(request)
    print('##### #####')

    # id_request = request[2]
    # date_request = request[0]
    operation_type_request = request[3]
    # operation_type_emoji = all_emoji[operation_type_request]
    # request_status = all_emoji[request[11]]
    request_numb = request[2]
    comments = request[8]

    if comments == '0':
        comments = ''
    else:
        comments = f'📝{comments}'

    request_type = request[3]

    if ready_or_office == 'ready':
        permit_status = all_emoji['заказан']
        permit_notify = f'{permit_status} #N{request_numb} пропуск заказан {permit_status}'
    else:
        permit_status = '⚠️'
        permit_notify = f'{permit_status} #N{request_numb} В ОФИСЕ {permit_status}'

    if operation_type_request == 'документы':
        text = f'{permit_notify}\nдокументы\n{comments}'
    
        return text

    else:
        # красивые суммы из полей FGH
        rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
        
        if rub != '': rub = rub + '\n'
        if usd != '': usd = usd + '\n'
        if eur != '': eur = eur + '\n'

        text = f'{permit_notify}\n{request_type}, суммы:\n{rub}{usd}{eur}{comments}'

        return text