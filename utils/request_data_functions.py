from utils import set_minus_and_plus_currences
from data import all_emoji

def get_data_chosen_request(request):
    print(request)
    

    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    operation_type_emoji = all_emoji[operation_type_request]

    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if rub != '': rub = rub + '\n'
    if usd != '': usd = usd + '\n'

    text = f'Заявка {operation_type_emoji} #N{id_request} от {date_request},\n{operation_type_request}, суммы:\n{rub}{usd}{eur}'

    if request[12] != '0' or request[13] != '0' or request[14] != '0':
        ready_to_give_rub = ''
        ready_to_give_usd = ''
        ready_to_give_eur = ''
        recived_chunk_rub = ''
        recived_chunk_usd = ''
        recived_chunk_eur = ''

        if request[12] != 0:
            value = str(request[12])

            if value[0] == '-':
                ready_to_give_rub = value + '₽'

            else:
                recived_chunk_rub = value + '₽'

        if request[13] != 0:
                value = str(request[13])

                if value[0] == '-':
                    ready_to_give_usd = value + '$'

                else:
                    recived_chunk_usd = value + '$'

        if request[14] != 0:
                value = str(request[14])

                if value[0] == '-':
                    ready_to_give_eur = value + '€'

                else:
                    recived_chunk_eur = value + '€'

        if ready_to_give_rub != '' or ready_to_give_usd != '' or ready_to_give_eur != '':

            if ready_to_give_rub != '': ready_to_give_rub + '\n'
            if ready_to_give_usd != '': ready_to_give_usd + '\n'

            reserve_to_ready = f'Отложенно к выдаче:\n{ready_to_give_rub} {ready_to_give_usd} {ready_to_give_eur}'


        text = text + add_text

    return text