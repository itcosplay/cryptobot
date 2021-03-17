from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request
from keyboards import create_kb_send_request_for_change
from keyboards import main_menu
from utils import get_data_to_show



@dp.callback_query_handler(state=Request.currency__how_much__recive)
async def set_how_much_recive_curr (
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
    currencies__recive = data_request['currencies__recive']
    if currency not in currencies__recive:
        currencies__recive.append(currency)
        await state.update_data(currencies__recive=currencies__recive)

    if currency == 'rub':
        await state.update_data(sum_recive_RUB=data_request['how_much_recive'])

    if currency == 'usd':
        await state.update_data(sum_recive_USD=data_request['how_much_recive'])

    if currency == 'eur':
        await state.update_data(sum_recive_EUR=data_request['how_much_recive'])

    request_data = await state.get_data()

    if request_data['plus_minus'] == 'yes':
        result_data_to_show, keyboard = get_data_to_show(request_data)

        await call.message.answer(text=result_data_to_show, reply_markup=keyboard)
        await Request.type_end.set()
        # to final_step_ordering.py

    else:
        result = await call.message.answer(f'Сколько выдаем?')
        await state.update_data(_del_message = result.message_id)
        await Request.how_much_give.set()
        # to how_much_give_message_handler.py

    

    
