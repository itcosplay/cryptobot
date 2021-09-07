import datetime

from aiogram import types 
from aiogram.dispatcher import FSMContext

from filters import isAdmin_or_isChanger
from states import Request
from loader import dp, bot
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
    await state.update_data(permit='данных нет...')
    await state.update_data(data_request=datetime.datetime.today().strftime('%d.%m'))

    result = await message.answer('Введите номер заявки')
    await Request.request_numb.set()
    await state.update_data(_del_message=result.message_id)

    return


@dp.message_handler(state=Request.request_numb)
async def set_request_id(message:types.Message, state:FSMContext):
    data_state = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['_del_message']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    await state.update_data(request_numb=message.text)

    await message.answer (
        text='Выберите тип операции',
        reply_markup=create_kp_operation_type()
    )

    await Request.operation_type.set()
    # to operation_type.py

    return


