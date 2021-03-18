async def notify_about_balance():
    from loader import dp, bot, db, sheet
    from data.config import super_admins

    balance_rub, balance_usd, balance_eur = sheet.get_balance_AEG3()
    warnig = 'Для исполнеия всех заявок не хватает: '
    if int(balance_rub) < 0:
        warnig = warnig + str(abs(int(balance_rub))) + 'RUB' + ' '
    if int(balance_usd) < 0:
        warnig = warnig + str(abs(int(balance_usd))) + 'USD' + ' '
    if int(balance_eur) < 0:
        warnig = warnig + str(abs(int(balance_eur))) + 'EUR'

    if warnig == 'Для исполнеия всех заявок не хватает: ':

        return

    else:
        print('notify_about_balance:')
        admins = db.select_id_users(status='admin')
        change = db.select_id_users(status='changer')

        if not len(super_admins) == 0:
            for user in super_admins:
                await dp.bot.send_message(user, warnig)

        if not len(admins) == 0:
            list_admins_id = []

            for item in admins:
                list_admins_id.append(item[0])

            for user in list_admins_id:
                await dp.bot.send_message(user, warnig)

        if not len(change) == 0:
            list_changers_id = []

            for item in change:
                list_changers_id.append(item[0])

            for user in list_changers_id:
                await dp.bot.send_message(user, warnig)
    
