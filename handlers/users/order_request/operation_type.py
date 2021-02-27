from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request

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
        from keyboards.inline.request_kb import create_kb_choose_card

        await call.answer()
        await state.update_data(operation_type=call.data)
        await call.message.delete()

        keyboard = create_kb_choose_card()

        await call.message.answer (
            f'Выберете с какой карты:',
            reply_markup=keyboard
        )
        await Request.type_of_card.set()

    elif call.data == 'change':
        await call.answer()
        await state.update_data(operation_type=call.data)
        await call.message.delete()
        await call.message.answer(f'Сколько принимаем?')
        await Request.how_much_recive.set()

    elif call.data == 'cache_atm':
        from keyboards.inline.request_kb import create_kb_send_request

        await state.update_data(operation_type=call.data)

        data = await state.get_data()
        print(data)

        await call.answer()
        await state.update_data(operation_type=call.data)
        await call.message.delete()

        keyboard = create_kb_send_request()
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + \
        'исполнитель - ' + data['executor'] + '\n' + \
        'тип операции - ' + data['type_of_operation']

        await call.message.answer(text, reply_markup=keyboard)
    else:
        await call.answer()
        await call.message.answer(f'Создание заявки отменено')
        await state.finish()
        await call.message.delete()
