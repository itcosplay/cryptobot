async def notify_about_permit_to_order(permit_numb, username):
    from loader import dp, db
    from data import emoji
    from utils import notify_someone

    kvz = emoji.all_emoji['квз']

    warning = f'УВЕДОМЛЕНИЕ\n{kvz}Новая заявка на пропуск{kvz}\nпропуск #N{permit_numb} заказал @{username}'

    await notify_someone(warning, 'admin')

    secretary = db.select_id_users(status='secretary')

    if not len(secretary) == 0:
        list_secretary_id = []

        for item in secretary:
            list_secretary_id.append(item[0])

        for user in list_secretary_id:
            await dp.bot.send_message(user, warning)

        return

    else:
        print('СЕКРЕТАРЕЙ НЕТ В БАЗЕ')

    return
