async def notify_someone(text, *args):
    '''
    *args - statuses of users. For ex.:
    notify_someone(text, admin, changer, operator, secretary)
    '''
    from loader import dp, db
    from data.config import super_admins

    groups = args

    for user in super_admins:
        await dp.bot.send_message(user, text)

    for item in groups:
        group = db.select_id_users(status=item)

        if not len(group) == 0:
            list_group_id =[]

            for some_item in group:
                list_group_id.append(some_item[0])

            for user in list_group_id:
                if user not in super_admins:
                    await dp.bot.send_message(user, text)

    return