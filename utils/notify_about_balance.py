async def notify_about_balance():
    from loader import dp, db, sheet
    from data.config import super_admins
    from data.config import group_chat
    from data import all_emoji

    balance_rub, balance_usd, balance_eur = sheet.get_balance_AEG3()
    warning = 'Для исполнеия всех заявок не хватает: '
    if int(balance_rub) < 0:
        balance_rub = abs(int(balance_rub))
        balance_rub = f'{balance_rub:,}'
        balance_rub = balance_rub.replace(',', '.')
        balance_rub = balance_rub + '₽'
        warning = warning + balance_rub + ' '
    if int(balance_usd) < 0:
        balance_usd = abs(int(balance_usd))
        balance_usd = f'{balance_usd:,}'
        balance_usd = balance_usd.replace(',', '.')
        balance_usd = balance_usd + '$'
        warning = warning + balance_usd + ' '
    if int(balance_eur) < 0:
        balance_eur = abs(int(balance_eur))
        balance_eur = f'{balance_eur:,}'
        balance_eur = balance_eur.replace(',', '.')
        balance_eur = balance_eur + '€'
        warning = warning + balance_eur

    if warning == 'Для исполнеия всех заявок не хватает: ':

        return

    else:
        warning = all_emoji['квз'] + warning + all_emoji['квз']
        await dp.bot.send_message(group_chat, warning)

        admins = db.select_id_users(status='admin')
        change = db.select_id_users(status='changer')

        if not len(super_admins) == 0:
            for user in super_admins:
                await dp.bot.send_message(user, warning)

        if not len(admins) == 0:
            list_admins_id = []

            for item in admins:
                list_admins_id.append(item[0])

            for user in list_admins_id:
                await dp.bot.send_message(user, warning)

        if not len(change) == 0:
            list_changers_id = []

            for item in change:
                list_changers_id.append(item[0])

            for user in list_changers_id:
                await dp.bot.send_message(user, warning)
    
