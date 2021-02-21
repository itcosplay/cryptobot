from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db
from data.config import super_admins

class IsAdmin(BoundFilter):
    async def check(self, message:types.Message):
        print('filter: IsAdmin')
        admins = db.select_id_users(status='admin')
        list_admins_id = []

        for item in admins:
            list_admins_id.append(item[0])

        return message.from_user.id in list_admins_id or message.from_user.id in super_admins