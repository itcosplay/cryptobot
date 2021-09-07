from utils import set_minus_and_plus_currences
from utils.get_values_FGH_MNO import get_single_value
from utils.get_beauty_sum import get_beauty_sum
from data import all_emoji



def get_data_chosen_request(request):
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    operation_type_emoji = all_emoji[operation_type_request]
    request_status = all_emoji[request[11]]
        
    # красивые суммы из полей FGH
    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if rub != '': rub = rub + '\n'
    if usd != '': usd = usd + '\n'
    if eur != '': eur = eur + '\n'

    text = f'{operation_type_emoji} #N{id_request} от {date_request} {request_status},\n{operation_type_request}, суммы:\n{rub}{usd}{eur}'

    if request[12] != '0' or request[13] != '0' or request[14] != '0':
        ready_to_give_rub = ''
        recived_chunk_rub = ''
        ready_to_give_usd = ''
        recived_chunk_usd = ''
        ready_to_give_eur = ''
        recived_chunk_eur = ''
        reserve_to_ready = ''
        recived_chunk = ''

        if request[12] != '0':
            value = str(request[12])

            if value[0] == '-':
                ready_to_give_rub = value

            else:
                recived_chunk_rub = value

        if request[13] != '0':
            value = str(request[13])

            if value[0] == '-':
                ready_to_give_usd = value

            else:
                recived_chunk_usd = value

        if request[14] != '0':
            value = str(request[14])

            if value[0] == '-':
                ready_to_give_eur = value

            else:
                recived_chunk_eur = value
                print('recived_chunk_eur')
                print(recived_chunk_eur)


        if ready_to_give_rub != '' or ready_to_give_usd != '' or ready_to_give_eur != '':
            reserve_to_ready = f'Отложено к выдаче:\n'

            if ready_to_give_rub != '':
                ready_to_give_rub = get_single_value(ready_to_give_rub, 'rub')
                reserve_to_ready = reserve_to_ready + ready_to_give_rub + ' ' + set_minus_and_plus_currences.get_blue(request) + '\n'

            if ready_to_give_usd != '':
                ready_to_give_usd = get_single_value(ready_to_give_usd, 'usd')
                reserve_to_ready = reserve_to_ready + ready_to_give_usd + '\n'

            if ready_to_give_eur != '':
                ready_to_give_eur = get_single_value(ready_to_give_eur, 'eur')
                reserve_to_ready = reserve_to_ready + ready_to_give_eur + '\n'


        if recived_chunk_rub != '' or recived_chunk_usd != '' or recived_chunk_eur != '':
            recived_chunk = f'Принято частично:\n'

            if recived_chunk_rub != '':
                recived_chunk_rub = get_single_value(recived_chunk_rub, 'rub')
                recived_chunk = recived_chunk + recived_chunk_rub + ' ' + set_minus_and_plus_currences.get_blue(request) + '\n'

            if recived_chunk_usd != '':
                recived_chunk_usd = get_single_value(recived_chunk_usd, 'usd')
                recived_chunk = recived_chunk + recived_chunk_usd + '\n'

            if recived_chunk_eur != '':
                recived_chunk_eur = get_single_value(recived_chunk_eur, 'eur')
                recived_chunk = recived_chunk + recived_chunk_eur + '\n'

        
        text = text + reserve_to_ready + recived_chunk

    if request[10] != '0':
        persone = all_emoji['персона']
        text = text + f'{persone} @{request[10]}'

    if request[8] != '0':
        comment = all_emoji['коментарий']
        comment_text = request[8]

        text = text + '\n' + f'{comment}{comment_text}'

    return text


def get_data_finished_request(request):
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    operation_type_emoji = all_emoji[operation_type_request]
    request_status = all_emoji[request[11]]

    # красивые суммы из полей FGH
    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if rub != '': rub = rub + '\n'
    if usd != '': usd = usd + '\n'
    if eur != '': eur = eur + '\n'

    text = f'{operation_type_emoji} #N{id_request} от {date_request} {request_status},\n{operation_type_request}, суммы:\n{rub}{usd}{eur}'

    if request[10] != '0':
        persone = all_emoji['персона']
        text = text + f'{persone} @{request[10]}'

    if request[8] != '0':
        comment = all_emoji['коментарий']
        comment_text = request[8]

        text = text + '\n' + f'{comment}{comment_text}'

    return text


def get_data_request_short(request):
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    operation_type_emoji = all_emoji[operation_type_request]
    request_status = all_emoji[request[11]]

    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if rub != '': rub = rub + '\n'
    if usd != '': usd = usd + '\n'
    if eur != '': eur = eur + '\n'

    text = f'Заявка {operation_type_emoji} #N{id_request} от {date_request} {request_status},\n{operation_type_request}, суммы:\n{rub}{usd}{eur}'

    return text


def get_data_request_unpack(request):
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    operation_type_emoji = all_emoji[operation_type_request]
    request_status = all_emoji[request[11]]

    rub, usd, eur = set_minus_and_plus_currences.set_minus_and_plus(request)
    
    if rub != '': rub = rub + '\n'
    if usd != '': usd = usd + '\n'
    if eur != '': eur = eur + '\n'

    text = f'Заявка {operation_type_emoji} #N{id_request} от {date_request} {request_status},\n{operation_type_request}, суммы:\n{rub}{usd}{eur}'

    return text


def get_text_before_close_request(request):
    '''
    Возвращает текст сообщения перед
    закрытием заявки
    '''
    # from utils import get_values_FGH
    from utils import get_values_MNO_or_FGH_ifMNO_is_empty

    request_id = request[2]
    request_date = request[0] 
    request_type_emoji = all_emoji[request[3]]

    # rub, usd, eur = get_values_FGH(request)
    rub, usd, eur = get_values_MNO_or_FGH_ifMNO_is_empty(request)
    blue = set_minus_and_plus_currences.get_blue(request)

    if rub != '': rub = rub + blue + '\n'
    if usd != '': usd = usd + '\n'
    if eur != '': eur = eur + '\n'
    
    text = f'Заявка {request_type_emoji} #N{request_id} от {request_date} будет закрыта с суммами:\n{rub}{usd}{eur}Подтверждаете?'

    return text


def get_text_after_close_request(request, initial_rub, initial_usd, initial_eur):
    '''
    Возвращает текст сообщения оповещния 
    и информации по закрытой заявке
    '''
    from utils import get_single_value
    from utils import get_blue

    request_type_emoji = all_emoji[request[3]]
    request_id = request[2]
    persone = all_emoji['персона']

    text = f'✅ ✅ ✅\n{request_type_emoji} #N{request_id}\n'

    if initial_rub == request[5] and initial_usd == request[6] and initial_eur == request[7]:
        if initial_rub != '0':
            initial_rub = get_single_value(initial_rub, 'rub')
            blue = get_blue(request)
            text = text + f'{initial_rub}{blue}\n'
        if initial_usd != '0':
            initial_usd = get_single_value(initial_usd, 'usd')
            text = text + f'{initial_usd}\n'
        if initial_eur != '0':
            initial_eur = get_single_value(initial_eur, 'eur')
            text = text + f'{initial_eur}\n'

        text = text + f'{persone} @{request[10]}'

        return text

    if initial_rub != request[5]:
        initial_rub = get_single_value(initial_rub, 'rub')
        final_rub = get_single_value(request[5], 'rub')
        blue = get_blue(request)
        text = text + f'{initial_rub}👉{final_rub}{blue}\n'
    elif initial_rub == request[5] and initial_rub != '0':
        initial_rub = get_single_value(initial_rub, 'rub')
        blue = get_blue(request)
        text = text + f'{initial_rub}{blue}\n'


    if initial_usd != request[6]:
        initial_usd = get_single_value(initial_usd, 'usd')
        final_usd = get_single_value(request[6], 'usd')
        text = text + f'{initial_usd}👉{final_usd}\n'
    elif initial_usd == request[6] and initial_usd != '0':
        initial_usd = get_single_value(initial_usd, 'usd')
        text = text + f'{initial_usd}\n'

    if initial_eur != request[7]:
        initial_eur = get_single_value(initial_eur, 'eur')
        final_eur = get_single_value(request[7], 'eur')
        text = text + f'{initial_eur}👉{final_eur}\n'
    elif initial_eur == request[7] and initial_eur != '0':
        initial_eur = get_single_value(initial_eur, 'eur')
        text = text + f'{initial_eur}\n'

    text = text + f'{persone} @{request[10]}\n'

    return text


def get_text_message_to(request):
    request_id = request[2]
    request_type_emoji = all_emoji[request[3]]

    rub = ''
    usd = ''
    eur = ''

    if request[5] != '0':
        rub = request[5]
        rub = int(rub)
        rub = f'{rub:,}'
        rub = rub.replace(',', '.')
        rub = str(rub)

        if rub[0] == '-': rub = all_emoji['минус'] + rub + '₽' + '\n'
        else: rub = all_emoji['плюс'] + rub + '₽' + '\n'

    if request[6] != '0':
        usd = request[6]
        usd = int(usd)
        usd = f'{usd:,}'
        usd = usd.replace(',', '.')
        usd = str(usd)

        if usd[0] == '-': usd = all_emoji['минус'] + usd + '$' + '\n'
        else: usd = all_emoji['плюс'] + usd + '$' + '\n'

    if request[7] != '0':
        eur = request[7]
        eur = int(eur)
        eur = f'{eur:,}'
        eur = eur.replace(',', '.')
        eur = str(eur)

        if eur[0] == '-': eur = all_emoji['минус'] + eur + '€' + '\n'
        else: eur = all_emoji['плюс'] + eur + '€' + '\n'

    text = f'Какое сообщение по заявке {request_type_emoji} #N{request_id} c суммами:\n{rub}{usd}{eur}хотите отправить?'

    return text


def get_text_after_change_request(old_request, changed_request):
    # ['01.09', '16152t5', '8888', 'прием', 'change', '500', '0', '-500', 'комментарий', '0', 'proprosh', 'В обработке', '0', '0', '0', '0', '0']
    # ['02.09', '16152t5', '8888', 'прием', 'change',  500 , '0',  -500 , 'комментарий', '0', 'proprosh', 'В обработке', '0', '0', '0', '0', '0']
    text = f'❗ Изменение в заявке #N{old_request[2]} ❗'

    if old_request[0] != changed_request[0]:
        text = text + '\n\n🗓️ новая дата 🗓️\n'
        text = text + old_request[0] + ' 👉 ' + changed_request[0]
    
    if old_request[2] != changed_request[2]:
        text = text + '\n\n#️⃣ новый номер #️⃣\n'
        text = text + '#N' + old_request[2] + ' 👉 ' + '#N' + changed_request[2]

    if old_request[3] != changed_request[3]:
        text = text + '\n\n🚻 новый тип 🚻\n'
        text = text + old_request[3] + ' 👉 ' + changed_request[3]

    if str(old_request[5]) != str(changed_request[5]) \
    or str(old_request[6]) != str(changed_request[6]) \
    or str(old_request[7]) != str(changed_request[7]):
        text = text + '\n\n⚠️ изменение в суммах ⚠️'
       
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

    text = text + '\n\n' + '👤' + '@' + changed_request[10]

    return text

# old_req = ['01.09', '16152t5', '8888', 'прием', 'change', '60000', '0', '-500', 'комментарий', '0', 'proprosh', 'В обработке', '0', '0', '0', '0', '0']
# new_req = ['02.09', '16152t5', '8888', 'прием', 'change',  50000 , '0',  -600 , 'комментарий', '0', 'proprosh', 'В обработке', '0', '0', '0', '0', '0']

# text = get_text_after_change_request(old_req, new_req)

# print(text)