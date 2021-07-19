from traceback import print_exc
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_coustom_main_menu
from utils import get_data_to_show


# from create_request.py
@dp.callback_query_handler(state=Request.operation_type)
async def set_operation_type (
    call:types.CallbackQuery,
    state:FSMContext
):  
    await call.answer()
    await call.message.delete()

    print(call.data)

    if call.data == 'get_in'  \
    or call.data == 'get_out' \
    or call.data == 'cash_in_ATM':
        await state.update_data(operation_type=call.data)

        currencies__how_much = []
        await state.update_data (
            currencies__how_much = currencies__how_much
        )

        result = await bot.send_message (
            chat_id = call.message.chat.id,
            text='введите сумму:'
        )
        await state.update_data(_del_message = result.message_id)

        await Request.temp_sum_state.set()
        # to temp_sum_message_handler.py  

    elif call.data == 'change':
        await state.update_data(operation_type=call.data)
        await state.update_data(currencies__recive=[])
        await state.update_data(currencies__give=[])
        await state.update_data(plus_minus='no')
        result = await call.message.answer(f'Сколько принимаем?')
        await state.update_data(_del_message = result.message_id)
        await Request.how_much_recive.set()
        # to how_much_recive.py

    elif call.data == 'cash_out_ATM':
        await state.update_data(operation_type='cash_atm')
        # request_data = await state.get_data()

        # text, keyboard = get_data_to_show(request_data)

        # await call.message.answer(text, reply_markup=keyboard)
        currencies__how_much = []
        await state.update_data (
            currencies__how_much = currencies__how_much
        )

        result = await bot.send_message (
            chat_id = call.message.chat.id,
            text='введите сумму:'
        )
        await state.update_data(_del_message = result.message_id)

        await Request.temp_sum_state.set()
        # to temp_sum_message_handler.py

        # await Request.type_end.set()
        # to final_step_ordering.py

    elif call.data == 'documents':
        await state.update_data(operation_type=call.data)

        request_data = await state.get_data()
        result_data_to_show, keyboard = get_data_to_show(request_data)

        await call.message.answer(text=result_data_to_show, reply_markup=keyboard)

        await Request.type_end.set()

        return

    else:
        await call.answer()
        await call.message.answer (
            f'Создание заявки отменено. Испльзуйте меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
