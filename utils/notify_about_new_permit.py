async def notify_about_balance():
    from loader import dp, db
    from data import emoji

    kvz = emoji.all_emoji['квз']

    warning = f'УВЕДОМЛЕНИЕ\n{kvz}{kvz}{kvz}Новая заявка на пропуск{kvz}{kvz}{kvz}'

    secretary = db.select_id_users(status='admin')

    if not len(secretary) == 0:
        list_secretary_id = []

        for item in secretary:
            list_secretary_id.append(item[0])

        for user in list_secretary_id:
            await dp.bot.send_message(user, warning)
            print('УВЕДОМЛЕНИЕ ОТПРАВЛЕННО')

    else:
        print('СЕКРЕТАРЕЙ НЕТ В БАЗЕ')

    return
