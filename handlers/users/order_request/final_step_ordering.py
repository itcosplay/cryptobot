from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_plus_minus
from utils import send_to_google
from keyboards.default.admin_keyboard import main_menu

# from currency__how_much.py
@dp.callback_query_handler(state=Request.type_end)
async def set_type_of_end(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    request_data = await state.get_data()

    if call.data == 'add_currency':
        if request_data['operation_type'] == 'change':
            print('to plus_or_minus_summ.py')
            await call.message.answer (
                text = 'Прием / Выдача',
                reply_markup=create_kb_plus_minus()
            )
            await Request.plus_minus.set()
            # to plus_or_minus_summ.py
        else:
            await state.update_data(type_end=call.data)
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

            


            ### for logs ### delete later
            request_data = await state.get_data()
            print('=== state: ===')
            print(request_data)
            print('==============')
            ### for logs ### delete later

    elif call.data == 'send_btn':
        request_id = send_to_google(request_data)

        await call.message.answer (
            f'Заявка создана. Номер заявки: {request_id}'
        )
        await state.finish()

    elif call.data == 'comment':
        result = await call.message.answer('Напишите коментарий:')
        await state.update_data(_del_message = result.message_id)
        await Request.comment.set()

    elif call.data == 'order_permit':
        result = await call.message.answer('Напишите Ф.И.О. для пропуска:')
        await state.update_data(_del_message = result.message_id)
        await Request.permit.set()

    else:
        await call.message.answer (
            f'Создание заявки отменено',
            reply_markup=main_menu
        )
        await state.finish()
