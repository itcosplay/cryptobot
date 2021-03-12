from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing
from keyboards import cb_chosen_requests
from keyboards import create_kb_what_sum


@dp.callback_query_handler(state=Processing.chosen_request_menu)
async def chosen_request_menu(call:CallbackQuery, state:FSMContext):
    await call.answer()

    data_btn = cb_chosen_requests.parse(call.data)
    
    if data_btn['type_btn'] == 'ready_to_give':
        await state.update_data(chosen_request_menu='chosen_request_menu')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.delete()
        await call.message.answer (
            'С какой суммой отложить на выдачу?',
            reply_markup=create_kb_what_sum(request)
        )
        await Processing.chosen_sum_to_ready.set()
        # to currency_and_sum_to_ready.py

        return

    if data_btn['type_btn'] == 'change':
        await call.message.delete()
        await call.message.answer('Кнопка изменить заявку')

        return

    if data_btn['type_btn'] == 'cancel':
        await call.message.delete()
        await call.message.answer('Кнопка отменить заявку')

        return

    if data_btn['type_btn'] == 'back':
        await call.message.delete()
        await call.message.answer('Кнопка назад')

        return