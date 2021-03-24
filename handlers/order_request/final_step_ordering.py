from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot, permit
from states import Request
from utils import send_to_google
from utils import notify_about_balance
from keyboards import create_kb_plus_minus
from keyboards.default.admin_keyboard import main_menu
from keyboards import create_kb_choose_date

# from currency__how_much.py
@dp.callback_query_handler(state=Request.type_end)
async def set_type_of_end(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    request_data = await state.get_data()

    if call.data == 'add_currency':
        if request_data['operation_type'] == 'change':
            await state.update_data(type_end=call.data)
            await call.message.answer (
                text = 'Прием / Выдача',
                reply_markup=create_kb_plus_minus()
            )
            await Request.plus_minus.set()
            # to plus_or_minus_summ.py
        else:
            await state.update_data(type_end=call.data)
            result = await bot.send_message (
                chat_id = call.message.chat.id,
                text='введите сумму:'
            )
            await state.update_data(_del_message = result.message_id)

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
        await state.update_data(type_end=call.data)
        result = await call.message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        )

        try:
            request_id, permit_text = send_to_google(request_data)
            permit.write_new_permit(request_id, permit_text)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
            await call.message.answer (
                f'Ошибка! Проблемы с таблицами...\n==============================',
                reply_markup=main_menu
            )
            await state.finish()

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
        await call.message.answer (
            f'Заявка создана. Номер заявки: {request_id}\n===========',
            reply_markup=main_menu
        )
        await state.finish()
        await notify_about_balance()

    elif call.data == 'comment':
        await state.update_data(type_end=call.data)
        result = await call.message.answer('Напишите коментарий:')
        await state.update_data(_del_message = result.message_id)
        await Request.comment.set()

    elif call.data == 'change_date':
        await call.message.answer (
            text='Какую дату устанавливаем?',
            reply_markup=create_kb_choose_date()
        )
        await state.update_data(type_end=call.data)
        await Request.data_request.set()

    elif call.data == 'order_permit':
        await state.update_data(type_end=call.data)
        result = await call.message.answer('Напишите Ф.И.О. для пропуска:')
        await state.update_data(_del_message = result.message_id)
        await Request.permit.set()

    else:
        await call.message.answer (
            f'Создание заявки отменено\n========================',
            reply_markup=main_menu
        )
        await state.finish()
