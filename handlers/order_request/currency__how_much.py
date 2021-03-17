from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Request
from keyboards import create_kb_send_request
from keyboards import main_menu
from utils import get_data_to_show


# from temp_sum_message_handler.py
@dp.callback_query_handler(state=Request.currencies__how_much)
async def set_currency__how_much (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()
    await call.message.delete()

    if call.data == 'exit':
        await call.message.answer (
            f'Создание заявки отменено. Испльзуйте меню\n=========================================',
            reply_markup=main_menu
        )
        await state.finish()

        return

    currency = call.data
    data_request = await state.get_data()
    # получаем список уже имеющихся валют либо пустой список
    currencies__how_much = data_request['currencies__how_much']

    if currency not in currencies__how_much:
        currencies__how_much.append(currency)
        await state.update_data(currencies__how_much=currencies__how_much)
    if currency == 'rub':
        await state.update_data(sum_RUB__how_much=data_request['temp_sum_state'])
    if currency == 'usd':
        await state.update_data(sum_USD__how_much=data_request['temp_sum_state'])
    if currency == 'eur':
        await state.update_data(sum_EUR__how_much=data_request['temp_sum_state'])

    request_data = await state.get_data()
    result_data_to_show, keyboard = get_data_to_show(request_data)

    await call.message.answer(text=result_data_to_show, reply_markup=keyboard)

    await Request.type_end.set()
    # to final_step_ordering.py

