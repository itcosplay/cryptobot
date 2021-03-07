from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db
from data.config import super_admins

class isExecutor_and_higher(BoundFilter):
    async def check(self, message:types.Message):
        print('filter: isExecutor_and_higher')
        admins = db.select_id_users(status='admin')
        list_admins_id = []

        for item in admins:
            list_admins_id.append(item[0])

        print('filter: isExecutor_and_higher')
        changers = db.select_id_users(status='changer')
        list_changers_id = []

        for item in changers:
            list_changers_id.append(item[0])
        
        print('filter: isExecutor_and_higher')
        executors = db.select_id_users(status='executor')
        list_executors_id = []

        for item in executors:
            list_executors_id.append(item[0])
        
        return\
            message.from_user.id in super_admins or\
            message.from_user.id in list_admins_id or\
            message.from_user.id in list_changers_id or\
            message.from_user.id in list_executors_id