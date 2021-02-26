from os import waitpid
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp, bot
from states import Request


@dp.callback_query_handler(state=Request.type_of_end)
async def set_type_of_end(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'add_summ':
        from keyboards.inline.request_kb import create_kb_plus_minus

        await state.update_data(type_of_end=call.data)

        keyboard = create_kb_plus_minus()

        await call.message.answer (
            f'Приход / Расход ?',
            reply_markup=keyboard
        )
        await Request.summ_plus_minus.set()
    elif call.data == 'send_btn':
        pass
    elif call.data == 'comment':
        pass
    elif call.data == 'order_permit':
        pass
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