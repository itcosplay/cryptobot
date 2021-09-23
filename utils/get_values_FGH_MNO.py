from traceback import print_tb
from data import all_emoji

def get_plus_FGH(request):
    '''
    Возвращает из полей 5,6,7 заявки (FGH)
    только положительны суммы
    с плюсами эмоджи и знаками валют
    '''
    if request[5] != '0':
        rub = request[5]
        rub = str(rub)
        if rub[0] != '-':
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['плюс'] + rub + '₽'
        else:
            rub = ''
    else:
        rub = ''

    if request[6] != '0':
        usd = request[6]
        usd = str(usd)
        if usd[0] != '-':
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['плюс'] + usd + '$'
        else:
            usd = ''
    else:
        usd = ''

    if request[7] != '0':
        eur = request[7]
        eur = str(eur)
        if eur[0] != '-':
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['плюс'] + eur + '€'
        else:
            eur = ''
    else:
        eur = ''

    return rub, usd, eur


def get_values_FGH(request):
    '''
    Возвращает из полей 5,6,7 (FGH) заявки
    значения сумм в "красивом" виде, если это
    поле не равно "0".
    '''
    if request[5] != '0':
        rub = request[5]
        rub = str(rub)
        print('we into rub')
        if rub[0] == '-':
            rub = rub[1:]
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['минус'] + rub + '₽'
        else:
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['плюс'] + rub + '₽'
    else:
        rub = ''

    if request[6] != '0':
        usd = request[6]
        usd = str(usd)

        if usd[0] == '-':
            usd = usd[1:]
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['минус'] + usd + '$'
        else:
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['плюс'] + usd + '$'
    else:

        usd = ''

    if request[7] != '0':
        eur = request[7]
        eur = str(eur)

        if eur[0] == '-':
            eur = eur[1:]
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['минус'] + eur + '€'
        else:
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['плюс'] + eur + '€'
    else:
        eur = ''

    return rub, usd, eur


def get_values_FGH_sort(request):
    '''
    Возвращает из полей 5,6,7 (FGH) заявки
    значения сумм в "красивом" виде, если это
    поле не равно "0".
    '''
    result = []

    if request[5] != '0':
        rub = request[5]
        rub = str(rub)

        if rub[0] == '-':
            rub = rub[1:]
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['минус'] + rub + '₽' + '\n'

        else:
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['плюс'] + rub + '₽' + '\n'

        result.append(rub)
    else:
        rub = ''

    if request[6] != '0':
        usd = request[6]
        usd = str(usd)

        if usd[0] == '-':
            usd = usd[1:]
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['минус'] + usd + '$' + '\n'

        else:
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['плюс'] + usd + '$' + '\n'

        result.append(usd)
    else:

        usd = ''

    if request[7] != '0':
        eur = request[7]
        eur = str(eur)

        if eur[0] == '-':
            eur = eur[1:]
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['минус'] + eur + '€' + '\n'

        else:
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['плюс'] + eur + '€' + '\n'

        result.append(eur)
    else:
        eur = ''

    result.sort()

    return result


def get_minus_MNO(request):
    '''
    Возвращает из полей 12,13,14 заявки (MNO)
    заявки только отрицательные суммы
    '''
    # sing minus: '−'
    if request[12] != '0':
        rub = request[12]
        rub = str(rub)
        if rub[0] == '-':
            rub = rub[1:]
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['минус'] + rub + ' ₽'
        else:
            rub = ''
    else:
        rub = ''

    if request[13] != '0':
        usd = request[13]
        usd = str(usd)
        if usd[0] == '-': 
            usd = usd[1:]
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['минус'] + usd + ' $'
        else:
            usd = ''
    else:
        usd = ''

    if request[14] != '0':
        eur = request[14]
        eur = str(eur)
        if eur[0] == '-':
            eur = eur[1:]
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['минус'] + eur + ' €'
        else:
            eur = ''
    else: eur = ''

    return rub, usd, eur


def get_single_value(value:str, currency:str):
    '''
    ('-234', 'usd')
    Возвращает из красивое значение
    со знаком минус или плюс и валютой
    '''
    if value[0] == '-':
        value = value[1:]
        value = int(value)
        value = f'{value:,}'
        value = value.replace(',', '.')
        value = all_emoji['минус'] + value
    else:
        value = int(value)
        value = f'{value:,}'
        value = value.replace(',', '.')
        value = all_emoji['плюс'] + value

    if currency == 'rub': value = value + '₽'
    if currency == 'usd': value = value + '$'
    if currency == 'eur': value = value + '€'

    return value


def get_value_for_reports(value:str, currency:str):
    if value[0] == '-':
        value = value[1:]
        value = int(value)
        value = f'{value:,}'
        value = value.replace(',', '.')
    else:
        value = int(value)
        value = f'{value:,}'
        value = value.replace(',', '.')

    if currency == 'rub': value = value + '₽'
    if currency == 'usd': value = value + '$'
    if currency == 'eur': value = value + '€'

    return value


def get_single_value_float(value:float, currency:str):
    value = f'{value:,}'
    value = value.replace('.', '-')
    value = value.replace(',', '.')
    value = value.replace('-', ',')

    if currency == 'rub': value = value + ' ₽'
    if currency == 'usd': value = value + ' $'
    if currency == 'eur': value = value + ' €'

    return value


def get_single_value_int(value:int, currency:str):
    value = f'{value:,}'
    value = value.replace(',', '.')

    if currency == 'rub': value = value + ' ₽'
    if currency == 'usd': value = value + ' $'
    if currency == 'eur': value = value + ' €'

    return value


def get_single_value_without_cur(value:int):
    value = f'{value:,}'
    value = value.replace(',', '.')

    return value


def get_values_MNO_or_FGH_ifMNO_is_empty(request):
    '''
    Возвращает из полей 12, 13, 14 (MNO) заявки
    значения сумм в "красивом" виде. Если MNO пустые,
    то возвращаются значения из 5, 6, 7 (FGH), если поля
    FGH сами не являются пустыми.
    '''
    if request[12] != '0':
        rub = request[12]
        rub = str(rub)
       
        if rub[0] == '-':
            rub = rub[1:]
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['минус'] + rub + '₽'
        else:
            rub = int(rub)
            rub = f'{rub:,}'
            rub = rub.replace(',', '.')
            rub = all_emoji['плюс'] + rub + '₽'
    else:      
        if request[5] != '0':
            rub = request[5]
            rub = str(rub)

            if rub[0] == '-':
                rub = rub[1:]
                rub = int(rub)
                rub = f'{rub:,}'
                rub = rub.replace(',', '.')
                rub = all_emoji['минус'] + rub + '₽'
            else:
                rub = int(rub)
                rub = f'{rub:,}'
                rub = rub.replace(',', '.')
                rub = all_emoji['плюс'] + rub + '₽'

        else:
            rub = ''


    if request[13] != '0':
        usd = request[13]
        usd = str(usd)
       
        if usd[0] == '-':
            usd = usd[1:]
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['минус'] + usd + '$'
        else:
            usd = int(usd)
            usd = f'{usd:,}'
            usd = usd.replace(',', '.')
            usd = all_emoji['плюс'] + usd + '$'
    else:      
        if request[6] != '0':
            usd = request[6]
            usd = str(usd)

            if usd[0] == '-':
                usd = usd[1:]
                usd = int(usd)
                usd = f'{usd:,}'
                usd = usd.replace(',', '.')
                usd = all_emoji['минус'] + usd + '$'
            else:
                usd = int(usd)
                usd = f'{usd:,}'
                usd = usd.replace(',', '.')
                usd = all_emoji['плюс'] + usd + '$'

        else:
            usd = ''

    
    if request[14] != '0':
        eur = request[14]
        eur = str(eur)
       
        if eur[0] == '-':
            eur = eur[1:]
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['минус'] + eur + '€'
        else:
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['плюс'] + eur + '€'
    else:      
        if request[7] != '0':
            eur = request[7]
            eur = str(eur)

            if eur[0] == '-':
                eur = eur[1:]
                eur = int(eur)
                eur = f'{eur:,}'
                eur = eur.replace(',', '.')
                eur = all_emoji['минус'] + eur + '€'
            else:
                eur = int(eur)
                eur = f'{eur:,}'
                eur = eur.replace(',', '.')
                eur = all_emoji['плюс'] + eur + '€'

        else:
            eur = ''


    return rub, usd, eur

# values = '12214214,00'
# cur = 'rub'
# get_value_for_reports(values, cur)
