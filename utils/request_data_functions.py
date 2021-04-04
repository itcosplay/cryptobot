from utils import set_minus_and_plus_currences
from data import all_emoji

def get_data_chosen_request(request):
    print('Функция get_data_chosen_request')
    print(request)
    
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    operation_type_emoji = all_emoji[operation_type_request]
    request_status = all_emoji[request[11]]

    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if rub != '': rub = rub + '\n'
    if usd != '': usd = usd + '\n'

    text = f'Заявка {operation_type_emoji} #N{id_request} от {date_request} {request_status},\n{operation_type_request}, суммы:\n{rub}{usd}{eur}'

    if request[12] != '0' or request[13] != '0' or request[14] != '0':
        ready_to_give_rub = ''
        ready_to_give_usd = ''
        ready_to_give_eur = ''
        recived_chunk_rub = ''
        recived_chunk_usd = ''
        recived_chunk_eur = ''

        if request[12] != '0':
            value = str(request[12])

            if value[0] == '-':
                ready_to_give_rub = value + '₽'

            else:
                recived_chunk_rub = value + '₽'

        if request[13] != '0':
                value = str(request[13])

                if value[0] == '-':
                    ready_to_give_usd = value + '$'

                else:
                    recived_chunk_usd = value + '$'

        if request[14] != '0':
                value = str(request[14])

                if value[0] == '-':
                    ready_to_give_eur = value + '€'

                else:
                    recived_chunk_eur = value + '€'

        if ready_to_give_rub != '' or ready_to_give_usd != '' or ready_to_give_eur != '':
            rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus_MNO(request)

            if ready_to_give_rub != '' and rub[0] == all_emoji['минус']:
                ready_to_give_rub = rub + '\n'
            else:
                ready_to_give_rub = ''

            if ready_to_give_usd != '' and usd[0] == all_emoji['минус']:
                ready_to_give_usd = usd + '\n'
            else:
                ready_to_give_usd = ''

            if ready_to_give_eur != '' and eur[0] == all_emoji['минус']:
                ready_to_give_eur = eur + '\n'
            else:
                ready_to_give_eur = ''

            if recived_chunk_rub != '' and rub[0] == all_emoji['плюс']:
                recived_chunk_rub = rub + '\n'
            else:
                recived_chunk_rub = ''

            if recived_chunk_usd != '' and usd[0] == all_emoji['плюс']:
                recived_chunk_usd = usd + '\n'
            else:
                recived_chunk_usd = ''

            if recived_chunk_eur != '' and eur[0] == all_emoji['плюс']:
                recived_chunk_eur = eur + '\n'
            else:
                recived_chunk_eur = ''

            if recived_chunk_rub == '' and recived_chunk_usd == '' and recived_chunk_eur == '':
                recived_chunk = ''
            else:
                recived_chunk = f'Принято частично:\n{recived_chunk_rub}{recived_chunk_usd}{recived_chunk_eur}'

            if ready_to_give_rub == '' and ready_to_give_usd == '' and ready_to_give_eur == '':
                reserve_to_ready = ''
            else:
                reserve_to_ready = f'Отложенно к выдаче:\n{ready_to_give_rub}{ready_to_give_usd}{ready_to_give_eur}'

        text = text + reserve_to_ready + recived_chunk

    if request[10] != '0':
        persone = all_emoji['персона']
        text = text + f'{persone} {request[10]}'

    return text