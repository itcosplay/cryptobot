async def notify_about_cancel_request(request, username, user_id):
    from emoji import emojize
    
    from loader import bot, db
    from data.config import super_admins


    emo_issuing_office = emojize(':office:', use_aliases=True)    
    emo_cash_recive = emojize(':chart_with_upwards_trend:', use_aliases=True)
    emo_delivery = emojize(':steam_locomotive:', use_aliases=True)
    emo_exchange = emojize(':recycle:', use_aliases=True)
    emo_cash_in = emojize(':atm:', use_aliases=True)
    emo_cash_atm = emojize(':credit_card:', use_aliases=True)

    emo_request = {
        'выдача в офисе': emo_issuing_office,
        'прием кэша': emo_cash_recive,
        'доставка': emo_delivery,
        'обмен': emo_exchange,
        'кэшин': emo_cash_in,
        'снятие с карт': emo_cash_atm,
    }

    type_operation = emo_request[request[3]]
    number_request = request[2]
    date_request = request[0]

    warning = f'Заявка {type_operation} #{number_request} от {date_request} была отменена. Отменил - {username}'

    admins = db.select_id_users(status='admin')
    change = db.select_id_users(status='changer')

    if not len(super_admins) == 0:
        for user in super_admins:
            if user == user_id:
                pass
            else:
                await bot.send_message(user, warning)

    if not len(admins) == 0:
        list_admins_id = []

        for item in admins:
            list_admins_id.append(item[0])

        for user in list_admins_id:
            if user == user_id:
                pass
            else:
                await bot.send_message(user, warning)

    if not len(change) == 0:
        list_changers_id = []

        for item in change:
            list_changers_id.append(item[0])

        for user in list_changers_id:
            if user == user_id:
                await bot.send_message(user, warning)

    return