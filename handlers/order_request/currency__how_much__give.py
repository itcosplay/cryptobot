from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request
from keyboards import create_kb_send_request_for_change
# from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu
from utils import get_data_to_show

@dp.callback_query_handler(state=Request.currency__how_much__give)
async def set_how_much_give_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()
    await call.message.delete()

    if call.data == 'exit':
        await call.message.answer (
            f'Создание заявки отменено. Испльзуйте меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return

    currency = call.data
    request_data = await state.get_data()
    # получаем список уже имеющихся валют либо пустой список
    currencies__give = request_data['currencies__give']

    if currency not in currencies__give:
        currencies__give.append(currency)
        await state.update_data(currencies__give=currencies__give)

    if currency == 'rub':
        await state.update_data(sum_give_RUB=request_data['how_much_give'])
    if currency == 'usd':
        await state.update_data(sum_give_USD=request_data['how_much_give'])
    if currency == 'eur':
        await state.update_data(sum_give_EUR=request_data['how_much_give'])

    request_data = await state.get_data()
    result_data_to_show, keyboard = get_data_to_show(request_data)
    
    await call.message.answer(text=result_data_to_show, reply_markup=keyboard)
    await Request.type_end.set()
    # to final_step_ordering.py

