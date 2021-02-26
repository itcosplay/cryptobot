from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request


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
        await state.update_data(executor=call.data)
        await call.message.delete()

        keyboard = create_kp_operation_type()

        await call.message.answer (
            f'Выберите тип операци:', reply_markup = keyboard
        )
        await Request.type_of_operation.set()