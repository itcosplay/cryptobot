from handlers.users.order_request.permit import permit
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_choose_card
from keyboards import create_kb_send_request_atm
from keyboards.default.admin_keyboard import main_menu

# from create_request.py
@dp.callback_query_handler(state=Request.operation_type)
async def set_operation_type (
    call:types.CallbackQuery,
    state:FSMContext
):  
    await call.answer()
    await call.message.delete()

    if call.data == 'recive' or call.data == 'takeout' \
    or call.data == 'delivery':
        await state.update_data(operation_type=call.data)

        currencies__how_much = []

        await state.update_data (
            currencies__how_much = currencies__how_much
        )
        await bot.send_message (
            chat_id = call.message.chat.id,
            text='введите сумму:'
        )

        ### for logs ### delete later
        request_data = await state.get_data()
        print('=== state: ===')
        print(request_data)
        print('==============')
        ### for logs ### delete later

        await Request.temp_sum_state.set()
        # to temp_sum_message_handler.py

    elif call.data == 'cashin':
        await state.update_data(operation_type=call.data)

        currencies__how_much = []

        await state.update_data (
            currencies__how_much = currencies__how_much
        )

        ### for logs ### delete later
        request_data = await state.get_data()
        print('=== state: ===')
        print(request_data)
        print('==============')
        ### for logs ### delete later

        await call.message.answer (
            f'Выберете карточку:',
            reply_markup=create_kb_choose_card()
        )
        await Request.type_of_card.set()
        # to type_of_card_if_cash_in.py

    elif call.data == 'change':
        await state.update_data(operation_type=call.data)
        await state.update_data(currencies__recive=[])
        await state.update_data(currencies__give=[])
        await state.update_data(plus_minus='no')
        await call.message.answer(f'Сколько принимаем?')
        await Request.how_much_recive.set()
        # to how_much_recive.py

    elif call.data == 'cash_atm':
        await state.update_data(operation_type=call.data)

        data = await state.get_data()
        print(data)

        await state.update_data(operation_type=call.data)
        await state.update_data(comment='')
        await state.update_data(permit='')

        keyboard = create_kb_send_request_atm()

        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + \
        'заявитель - ' + data['applicant'] + '\n' + \
        'тип операции - ' + data['operation_type']

        await call.message.answer(text, reply_markup=keyboard)
        await Request.type_end.set()
        # to final_step_ordering.py

    else:
        await call.answer()
        await call.message.answer(f'Создание заявки отменено. Испльзуйте меню.', reply_markup=main_menu)
        await state.finish()
