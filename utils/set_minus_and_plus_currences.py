
def set_minus_and_plus(request):
    
    if not request[5] == '-':
        rub = request[5]
        rub = str(rub)
        if rub[0] == '-': rub = rub + '₽  '
        else: rub = '+' + rub + '₽  '
    else:
        rub = ''

    if not request[6] == '-':
        usd = request[6]
        usd = str(usd)
        if usd[0] == '-': usd = usd + '$  '
        else: usd = '+' + usd + '$  '
    else:
        usd = ''

    if not request[7] == '-':
        eur = request[7]
        eur = str(eur)
        if eur[0] == '-': eur = eur + '€'
        else: eur = '+' + eur + '€'
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