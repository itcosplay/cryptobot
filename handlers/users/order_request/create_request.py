from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import super_admins
from filters import isAdmin_or_isChanger
import keyboards
from states import Request
from loader import dp, db
from keyboards import create_kp_operation_type


@dp.message_handler(isAdmin_or_isChanger(), text='создать заявку')
async def create_request(message:types.Message, state:FSMContext):
    ### for logs ### delete later
    print('to DATABASE request from -- handles/users/order_request/create_request.py --')
    ### for logs ### delete later

    if db.select_status_user(id=message.from_user.id) ==  \
    'admin' or message.from_user.id in super_admins:
        await state.update_data(applicant='changer')
    else:
        await state.update_data(applicant='changer')
    
    await message.answer (
        'Создаем заявку! Выберите тип операции:',
        reply_markup = create_kp_operation_type()
    )



    ### for logs ### delete later
    request_data = await state.get_data()
    print('=== state: ===')
    print(request_data)
    print('==============')
    ### for logs ### delete later

    await Request.operation_type.set()
    # to operation_type.py
    
