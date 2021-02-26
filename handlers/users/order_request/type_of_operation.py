from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp, bot
from states import Request


@dp.callback_query_handler(state=Request.type_of_operation)
async def set_type_of_operation (
    call:types.CallbackQuery, state:FSMContext
):
    chat_id = call.message.chat.id

    if call.data == 'recive' or call.data == 'takeout' \
    or call.data == 'delivery':
        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        await bot.send_message(chat_id=chat_id, text='укажите сумму:')
        await Request.how_much.set()

    elif call.data == 'cache_in':
        from keyboards.inline.request_kb import create_kb_choose_card

        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()

        keyboard = create_kb_choose_card()

        await call.message.answer (
            f'Выберете с какой карты:',
            reply_markup=keyboard
        )
        await Request.type_of_card.set()

    elif call.data == 'change':
        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        await call.message.answer(f'Сколько принимаем?')
        await Request.how_much_recive.set()

    elif call.data == 'cache_atm':
        from keyboards.inline.request_kb import create_kb_send_request

        await state.update_data(type_of_operation=call.data)

        data = await state.get_data()
        print(data)

        await call.answer()
        await state.update_data(type_of_operation=call.data)
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
