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
            usd = all_emoji['минус'] + eur + '€'
        else:
            eur = int(eur)
            eur = f'{eur:,}'
            eur = eur.replace(',', '.')
            eur = all_emoji['плюс'] + eur + '€'
    else:
        eur = ''

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