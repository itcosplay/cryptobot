from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing
from keyboards import cb_chosen_requests


@dp.callback_query_handler(state=Processing.chosen_request_menu)
async def ready_to_give(call:CallbackQuery, state:FSMContext):
    await call.answer()

    data_btn = cb_chosen_requests.parse(call.data)
    
    if data_btn['type_btn'] == 'ready_to_give':
        pass

    await call.message.delete()
    await call.message.answer('Кнопка отложить на выдачу')
    await state.finish()


# @dp.callback_query_handler(cb_chosen_requests.filter(type_btn='change'))
# async def change(call:CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     await call.message.answer('Кнопка изменить')


# @dp.callback_query_handler(cb_chosen_requests.filter(type_btn='cancel'))
# async def cancel(call:CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     await call.message.answer('Кнопка отменить заявку')


# @dp.callback_query_handler(cb_chosen_requests.filter(type_btn='back'))
# async def back(call:CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     await call.message.answer('Кнопка отменить назад')