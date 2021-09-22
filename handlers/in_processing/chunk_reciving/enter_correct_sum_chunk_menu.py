from keyboards.inline.in_processing.blue_keyboard import create_kb_confirm_blue
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Processing
from utils import get_plus_FGH
from utils import get_data_chosen_request
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_sum_correct_chunk
from keyboards import create_kb_confirm_reserve
from keyboards import create_kb_what_blue


@dp.callback_query_handler(state=Processing.enter_correct_sum_chunk_menu)
async def set_currency_to_correct(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает клавиатуру create_kb_what_sum_correct(request)
    из keyboards_sum_ready.py
    - sum rub
    - sum usd
    - sum eur
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_correct_sum_to_ready_menu='+')

    data_btn = cb_sum_correct_chunk.parse(call.data)

    if data_btn['type_btn'] == 'change_curr':
        await state.update_data(chunk_recive__currency=data_btn['curr'])
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        rub, usd, eur = get_plus_FGH(chosen_request)

        if data_btn['curr'] == 'rub': initial_sum = rub
        if data_btn['curr'] == 'usd': initial_sum = usd
        if data_btn['curr'] == 'eur': initial_sum = eur

        result = await call.message.answer (
            f'По заявке нужно принять сумму {initial_sum},\nсколько принято по факту?'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.chunk_recive__sum.set()

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.message_handler(state=Processing.chunk_recive__sum)
async def recive_chunk__sum_set(message:Message, state:FSMContext):
    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    try:
        chunk_recive__sum = int(message.text)
        
        if chunk_recive__sum <= 0:
            raise ValueError('fuck off')
        
    except Exception as e:
        await message.answer (
            text='Изменение отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        print(e)

        return
    
    await state.update_data(chunk_recive__sum=chunk_recive__sum)

    data_state = await state.get_data()
    chunk_recive__currency = data_state['chunk_recive__currency']
    # rub usd eur

    if chunk_recive__currency == 'rub':
        chosen_request = data_state['chosen_request']
        chosen_request[12] = chunk_recive__sum
        await state.update_data(chosen_request=chosen_request)
        await message.answer (
            text='Сколько синих?',
            reply_markup=create_kb_what_blue()
            # > без синих
            # > ввести колличество синих
            # > вернуться к заявке
            # > назад - главное меню
        )
        
        await Processing.enter_blue_amount_chunk_menu.set()
        # to blue_amount_handlers.py

        return

    else:
        chosen_request = data_state['chosen_request']
        chunk_recive__sum = data_state['chunk_recive__sum']

        if chunk_recive__currency == 'usd':
            chosen_request[13] = chunk_recive__sum

        elif chunk_recive__currency == 'eur':
            chosen_request[14] = chunk_recive__sum

        await state.update_data(chosen_request=chosen_request)

        text = get_data_chosen_request(chosen_request)

        await message.answer (
            text=text,
            reply_markup=create_kb_confirm_blue()
        )
        await Processing.enter_to_confirm_chunk_menu.set()

        return
