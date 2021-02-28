from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_plus_minus

# from currency__how_much.py
@dp.callback_query_handler(state=Request.type_end)
async def set_type_of_end(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    request_data = await state.get_data()

    if call.data == 'add_currency':
        if request_data['operation_type'] == 'change':
            print('to plus_or_minus_summ.py')
            await call.message.answer (
                text = 'Прием / Выдача',
                reply_markup=create_kb_plus_minus()
            )
            await Request.plus_minus.set()
            # to plus_or_minus_summ.py
        else:
            await state.update_data(type_end=call.data)
            await bot.send_message (
                chat_id = call.message.chat.id,
                text='введите сумму:'
            )

            ### for logs ### delete later
            request_data = await state.get_data()
            print('=== state: ===')
            print(request_data)
            print('==============')
            ### for logs ### delete later

            await Request.temp_sum_state.set()
            # to temp_sum_message_handler.py

            


            ### for logs ### delete later
            request_data = await state.get_data()
            print('=== state: ===')
            print(request_data)
            print('==============')
            ### for logs ### delete later

    elif call.data == 'send_btn':
        await call.message.answer('Заявка отправленна!')
        await state.finish()
    elif call.data == 'comment':
        await call.message.answer('Напишите коментарий:')
        await Request.comment.set()
    elif call.data == 'order_permit':
        await call.message.answer('Напишите Ф.И.О. для пропуска:')
        await Request.permit.set()
    else:
        await call.message.answer(f'Создание заявки отменено')
        await state.finish()
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