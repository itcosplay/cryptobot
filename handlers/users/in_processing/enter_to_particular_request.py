from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from filters import isExecutor_and_higher
from loader import dp

from keyboards.inline.callback_data import get_info_request_data
from keyboards import create_kb_for_particular_request

@dp.callback_query_handler(isExecutor_and_higher(), get_info_request_data.filter(type_btn='GETINFOREQUEST'))
async def enter_to_particular_req(call:CallbackQuery, state:FSMContext):
    

    list_current_requests = await state.get_data()
    list_current_requests = list_current_requests['current_requests']

    btn_data = get_info_request_data.parse(call.data)
    # {'@': 'gird', 'id': '1328', 'type_btn': 'GETINFOREQUEST'}

    for request in list_current_requests:
        if btn_data['id'] == request[2]:
            await state.update_data(choosed_request=request)
            id_request = request[2]
            date_request = request[0]
            operation_type_request = request[3]
            if not request[5] == '-': sum_RUB = request[5] + 'RUB; '
            else: sum_RUB = ''

            if not request[6] == '-': sum_USD = request[6] + 'USD; '
            else: sum_USD =''

            if not request[7] == '-': sum_EUR = request[7] + 'EUR'
            else: sum_EUR = ''

            break

    await call.message.answer (
        'заявка № {}\nдата создания: {}\nоперация: {}\nсуммы:\n{}{}{}'.format (
            id_request, 
            date_request, 
            operation_type_request,
            sum_RUB,
            sum_USD,
            sum_EUR
        ),
        reply_markup=create_kb_for_particular_request()
    )
    await call.message.delete()