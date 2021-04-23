import data
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Processing
from utils import get_minus_FGH
from utils import get_data_chosen_request
from keyboards import cb_what_sum_correct
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_what_sum_correct
from keyboards import create_kb_confirm_reserve
from keyboards import create_kb_what_blue


# from: enter_reserve_to_ready_menu.py
@dp.callback_query_handler(state=Processing.enter_correct_sum_to_ready_menu)
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

    data_btn = cb_what_sum_correct.parse(call.data)

    if data_btn['type_btn'] == 'change_curr':
        await state.update_data(reserve_to_ready__currency=data_btn['curr'])
        data_state = await state.get_data()
        request = data_state['chosen_request']
        rub, usd, eur = get_minus_FGH(request)

        if data_btn['curr'] == 'rub': initial_sum = rub
        if data_btn['curr'] == 'usd': initial_sum = usd
        if data_btn['curr'] == 'eur': initial_sum = eur

        result = await call.message.answer (
            f'Сумма по заявке: {initial_sum},\nсколько откладываем на выдачу?'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.reserve_to_ready__sum.set()

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.message_handler(state=Processing.reserve_to_ready__sum)
async def reserve_to_ready__sum_set(message:Message, state:FSMContext):
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
        reserve_to_ready__sum = int(message.text)
        
        if reserve_to_ready__sum <= 0:
            raise ValueError('fuck off')
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        print(e)

        return
    
    await state.update_data(reserve_to_ready__sum=reserve_to_ready__sum)

    data_state = await state.get_data()
    reserve_to_ready__currency = data_state['reserve_to_ready__currency']
    # rub usd eur
    print('RESERVE TO READY: ', reserve_to_ready__sum)
    if reserve_to_ready__currency == 'rub':
        chosen_request = data_state['chosen_request']
        chosen_request[12] = 0 - reserve_to_ready__sum
        await state.update_data(chosen_request=chosen_request)
        await message.answer (
            text='Сколько синих?',
            reply_markup=create_kb_what_blue()
            # > без синих
            # > ввести колличество синих
            # > вернуться к заявке
            # > назад - главное меню
        )
        
        await Processing.enter_to_blue_amount_menu.set()
        # to blue_amount_handlers.py

        return

    else:
        chosen_request = data_state['chosen_request']
        reserve_to_ready__sum = data_state['reserve_to_ready__sum']

        if reserve_to_ready__currency == 'usd':
            chosen_request[13] = 0 - reserve_to_ready__sum

        elif reserve_to_ready__currency == 'eur':
            chosen_request[14] = 0 - reserve_to_ready__sum

        await state.update_data(chosen_request=chosen_request)

        text = get_data_chosen_request(chosen_request)
        await message.answer (
            text=text,
            reply_markup=create_kb_confirm_reserve()
        )
        await Processing.enter_to_confirm_reserve_menu.set()

        return