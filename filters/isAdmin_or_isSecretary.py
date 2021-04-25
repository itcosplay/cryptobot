from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db
from data.config import super_admins

class isAdmin_or_isSecretary(BoundFilter):
    async def check(self, message:types.Message):
        print('filter: isAdmin_or_isChanger')
        admins = db.select_id_users(status='admin')
        list_admins_id = []

        for item in admins:
            list_admins_id.append(item[0])

        print('filter: isAdmin_or_isSecretary')
        changers = db.select_id_users(status='secretary')
        list_changers_id = []

        for item in changers:
            list_changers_id.append(item[0])
        

        return \
        message.from_user.id in list_admins_id or  \
        message.from_user.id in super_admins or  \
        message.from_user.id in list_changers_id