from data import all_emoji

def get_minus_FGH(request):
    '''
    Возвращает из полей 5,6,7 заявки (FGH)
    заявки только отрицательные суммы
    '''
    # sing minus: '−'
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
            rub = ''
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
            usd = ''
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
            eur = ''
    else: eur = ''

    return rub, usd, eur



  # убираем минусы и при обмене - добавляем плюсы
            # if request[3] == 'обмен':
                # if not request[5] == '-':
                #     rub = request[5]
                #     rub = str(rub)
                #     if rub[0] == '-': rub = rub + '₽  '
                #     else: rub = '+' + rub + '₽  '
                # else:
                #     rub = ''

                # if not request[6] == '-':
                #     usd = request[6]
                #     usd = str(usd)
                #     if usd[0] == '-': usd = usd + '$  '
                #     else: usd = '+' + usd + '$  '
                # else:
                #     usd = ''

                # if not request[7] == '-':
                #     eur = request[7]
                #     eur = str(eur)
                #     if eur[0] == '-': eur = eur + '€'
                #     else: eur = '+' + eur + '€'
            #     else:
            #         eur = ''

            # else:
            #     if not request[5] == '-':
            #         rub = request[5]
            #         rub = str(rub)
            #         if rub[0] == '-': rub = rub[1:] + '₽  '
            #         else: rub = rub + '₽  '
            #     else: rub = ''

            #     if not request[6] == '-':
            #         usd = request[6]
            #         usd = str(usd)
            #         if usd[0] == '-': usd = usd[1:] + '$  '
            #         else: usd = usd + '$  '
            #     else: usd = ''

            #     if not request[7] == '-':
            #         eur = request[7]
            #         eur = str(eur)
            #         if eur[0] == '-': eur = eur[1:] + '€'
            #         else: eur = eur + '€'
            #     else: eur = ''