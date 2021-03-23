from utils import set_minus_and_plus_currences

def get_data_chosen_request(request):
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]

    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if not rub == '': rub = rub + '\n'

    if not usd == '': usd = usd + '\n'

    if not eur == '': eur = eur + '\n'

    text = f'заявка #{id_request} от {date_request}\n{operation_type_request}\n{rub}{usd}{eur}'

    return text