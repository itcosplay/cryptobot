import datetime

from aiogram import types 
from aiogram.dispatcher import FSMContext

from filters import isAdmin_or_isChanger
from states import Request
from loader import dp
from keyboards import create_kp_operation_type

# from 'создать заявку' main_menu
@dp.message_handler(isAdmin_or_isChanger(), text='создать заявку')
async def create_request(message:types.Message, state:FSMContext):
    await message.delete()
    await message.answer (
        '===========\nСоздание новой заявки',
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.update_data(applicant='changer') 
    await state.update_data(operation_type='')
    await state.update_data(type_of_card='')

    await state.update_data(sum_RUB__how_much='')
    await state.update_data(sum_USD__how_much='')
    await state.update_data(sum_EUR__how_much='')

    await state.update_data(sum_recive_RUB='')
    await state.update_data(sum_recive_USD='')
    await state.update_data(sum_recive_EUR='')
    await state.update_data(sum_give_RUB='')
    await state.update_data(sum_give_USD='')
    await state.update_data(sum_give_EUR='')

    await state.update_data(comment='')
    await state.update_data(permit='')
    await state.update_data(data_request=datetime.datetime.today().strftime('%d.%m'))

    result = await message.answer (
        text='Выберите тип операции',
        reply_markup=create_kp_operation_type()
    )

    await Request.operation_type.set()
    # to operation_type.py
