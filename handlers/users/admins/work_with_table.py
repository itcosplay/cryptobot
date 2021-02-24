import keyboards
from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import chat, message
from aiogram.types.callback_query import CallbackQuery

from loader import dp, bot
from states import Request



@dp.message_handler(text='создать заявку')
async def enter_to_request(message:types.Message):
    from keyboards.inline.request_kb import create_kb_request_from

    keyboard = create_kb_request_from()
    
    await message.answer (
        'Создаем заявку! Через кого создаем заявку?',
        reply_markup = keyboard
    )

    await Request.executor.set()


@dp.callback_query_handler(state=Request.executor)
async def set_request_from(call:types.CallbackQuery, state:FSMContext):
    from keyboards.inline.request_kb import create_kp_operation_type
    if call.data == 'exit':
        await call.answer()
        await call.message.answer(f'Создание заявки отменено')
        await call.message.delete()
        
        await state.finish()

    else:
        await call.answer()
        # pressed button - call.data
        await state.update_data(executor=call.data)
        await call.message.delete()

        keyboard = create_kp_operation_type()
        await call.message.answer(f'Выберите тип операци:', reply_markup=keyboard)
        await Request.type_of_operation.set()


@dp.callback_query_handler(state=Request.type_of_operation)
async def set_type_of_operation(call:types.CallbackQuery, state:FSMContext):
    chat_id = call.message.chat.id
    if call.data == 'recive' or call.data == 'takeout' or call.data == 'delivery':
        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        
        # await call.message.answer(f'укажите сумму:')
        await bot.send_message(chat_id=chat_id, text='укажите сумму:')
        await Request.how_much.set()

    elif call.data == 'cache_in':
        from keyboards.inline.request_kb import create_kb_choose_card

        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        keyboard = create_kb_choose_card()
        await call.message.answer(f'Выберете с какой карты:', reply_markup=keyboard)
        await Request.type_of_card.set()

    elif call.data == 'change':
        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        await call.message.answer(f'Выберете с какой карты:') # message handler
        await Request.how_much_recive.set()

    elif call.data == 'cache_atm':
        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        await call.message.answer(f'Тут должны быть данные с таблицы')
        # await Request.how_much_recive.set()

    else:
        await call.answer()
        await call.message.answer(f'Создание заявки отменено')
        await state.finish()
        await call.message.delete()


@dp.callback_query_handler(state=Request.type_of_card)
async def set_type_of_card(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    card = call.data
    await state.update_data(type_of_card=card)

    await call.message.delete()
    await call.message.answer(f'укажите сумму:')
    await Request.how_much.set()


@dp.message_handler(state=Request.how_much)
async def set_how_much(message:types.Message, state:FSMContext):
    from keyboards.inline.request_kb import create_kb_choose_currency
    try:
        summ = float(message.text)
        await state.update_data(how_much=summ)
        # print(message)
        # await message.delete()
        # chat_id = message.chat.id
        # message_id = message.message_id
        # message_id_new = message.message_id - 2
        # print('==========')
        # print('CHAT_ID: ', chat_id)
        # print('MESSAGE_ID : ', message_id)
        # print('MESSAGE_ID_NEW :', message_id_new)
        # print('==========')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        keyboard = create_kb_choose_currency()
        
        
        await message.answer(f'Выберете валюту:', reply_markup=keyboard)
        await Request.how_much_curr.set()

    except Exception:
        await message.answer(f'Формат суммы неправильный. Создание заявки отменено.')
        await state.finish()
        await message.delete()


@dp.callback_query_handler(state=Request.how_much_curr)
async def set_how_much_curr(call:types.CallbackQuery, state:FSMContext):
    from keyboards.inline.request_kb import create_kb_send_request

    await call.answer()
    currency = call.data
    await state.update_data(how_much_curr=currency)

    data = await state.get_data()
    
    print(data)

    keyboard = create_kb_send_request()
    await call.message.delete()
    await call.message.answer(f'заявка сформированна со след параметрами {data}:', reply_markup=keyboard)
    await Request.comment.set()


@dp.callback_query_handler(state=Request.comment)
async def set_comm_or_else(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await state.finish()
    pass
    # await call.answer()
    # comm = ''
    # await state.update_data(comment=comm)



# @dp.message_handler(state=Request.type_of_operation)
# async def set_type_of_operation(message:types.Message, state:FSMContext):
#     data = await state.get_data()
#     executor = data.get('executor')
#     type_of_operation = message.text

#     if type_of_operation == 'кэшин':
#         await state.update_data(type_of_operation = type_of_operation)
#         await message.answer (
#             '''
#             Введите с какой карты:
#             - "Альфа-банк"
#             - "Сбер"
#             '''
#         )
#         await Request.type_of_card.set()
#     else:
#         await message.answer('Ваша заявка сформированна!')
#         await message.answer (
#             f'Заявка содержит следующие данные: {executor} {type_of_operation}'
#         )
#         await state.finish()


# @dp.message_handler(state=Request.type_of_card)
# async def set_type_of_card(message:types.Message, state:FSMContext):
#     data = await state.get_data()
#     executor = data.get('executor')
#     type_of_operation = data.get('type_of_operation')
#     type_of_card = message.text

#     await message.answer('Ваша заявка сформированна!')
#     await message.answer (
#         f'Заявка содержит следующие данные: {executor} {type_of_operation} {type_of_card}'
#     )
#     await state.finish()