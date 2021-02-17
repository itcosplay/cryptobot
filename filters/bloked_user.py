from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db

class BlokedUser(BoundFilter):
    async def check(self, message:types.Message):
        bloked_users = db.select_id_users(status='block')
        list_bloked_id = []

        for item in bloked_users:
            list_bloked_id.append(item[0])
        
        return message.from_user.id in list_bloked_id
