from data import all_emoji


def set_minus_and_plus(request):
    '''
    Проверяет поля 5,6,7 заявки (FGH) и
    возвращает значения валют с плюсом или минусом
    с добавлением значка валюты.
    '''
    # sing minus: '−'
    if not request[5] == '0':
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

    if not request[6] == '0':
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

    if not request[7] == '0':
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
    else: eur = ''

    return rub, usd, eur


def set_minus_and_plus_MNO(request):
    '''
    Проверяет поля 12,13,14 заявки (MNO) и
    возвращает значения валют с плюсом или минусом
    с добавлением значка валюты.
    '''
    # sing minus: '−'
    if not request[12] == '0':
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
        rub = ''

    if not request[13] == '0':
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
        usd = ''

    if not request[14] == '0':
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
    else: eur = ''

    return rub, usd, eur


def get_blue(request):
    '''
    Проверяет поле 16 заявки (Q) и
    возвращает значения с плюсом или минусом
    '''
    if not request[16] == '0':
        blue = request[16]
        blue = str(blue)
        if blue[0] == '-':
            blue = blue[1:]
            blue = int(blue)
            blue = f'{blue:,}'
            blue = blue.replace(',', '.')
            blue = all_emoji['синих'] + '-' + blue
        else:
            blue = int(blue)
            blue = f'{blue:,}'
            blue = blue.replace(',', '.')
            blue = all_emoji['синих'] + '+' + blue
    else:
        blue = ''

    return blue