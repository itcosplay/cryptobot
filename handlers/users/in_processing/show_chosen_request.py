from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing

from keyboards import cb_current_requests
from keyboards import main_menu
from keyboards import create_kb_chosen_request


@dp.callback_query_handler(state=Processing.chosen_request)
async def show_chosen_request(call:CallbackQuery, state:FSMContext):
    await call.answer()

    data_btn = cb_current_requests.parse(call.data)
    # {'id': , 'type_btn': }

    if data_btn['type_btn'] == 'exit':
        await call.message.delete()
        await call.message.answer (
            f'Просмотр заявок отменен',
            reply_markup=main_menu
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    current_requests = data_state['current_requests']

    for request in current_requests:
        if data_btn['id'] == request[2]:
            await state.update_data(chosen_request=request)

            id_request = request[2]
            date_request = request[0]
            operation_type_request = request[3]
            if not request[5] == '-': sum_RUB = request[5] + ' RUB\n'
            else: sum_RUB = ''

            if not request[6] == '-': sum_USD = request[6] + ' USD\n'
            else: sum_USD =''

            if not request[7] == '-': sum_EUR = request[7] + ' EUR'
            else: sum_EUR = ''

            break
    
    await call.message.delete()
    await call.message.answer (
        'заявка {} от {}\nоперация: {}\nсуммы:\n{}{}{}'.format (
            id_request, 
            date_request, 
            operation_type_request,
            sum_RUB,
            sum_USD,
            sum_EUR
        ),
        reply_markup=create_kb_chosen_request()
    )
    await Processing.chosen_request_menu.set()
    