from data import all_emoji

def get_plus_FGH(request):
    '''
    Возвращает из полей 5,6,7 заявки (FGH)
    заявки только положительны суммы
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