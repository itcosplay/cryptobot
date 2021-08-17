from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Processing
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_plus_or_minus_sum
from keyboards import create_kb_change_request
from utils import get_data_chosen_request


@dp.callback_query_handler(state=Processing.which_sum_change__currency)
async def set_currency_to_correct(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает клавиатуру create_kb_choose_currency()
    - рубли      rub
    - доллары    usd
    - евро       eur
    '''
    await call.answer()
    await call.message.delete()

    currency = call.data

    await state.update_data(which_sum_change__currency=currency)
    await call.message.answer (
        'Принимаем или выдаем?',
        reply_markup=create_kb_plus_or_minus_sum()
    )
    await Processing.which_sum_change__ask.set()

    return


@dp.callback_query_handler(state=Processing.which_sum_change__ask)
async def sum_amount(call:CallbackQuery, state:FSMContext):
    '''
    Here we have currency and sign of sum (- or +).
    After we need to ask about amount of sum.
    '''
    await call.answer()
    await call.message.delete()

    sum_sign = call.data

    await state.update_data(which_sum_change__sign=sum_sign)

    result = await call.message.answer('Введите сумму')

    await state.update_data(message_to_delete=result.message_id)
    await Processing.which_sum_change__amount.set()

    return


@dp.message_handler(state=Processing.which_sum_change__amount)
async def close__sum_set(message:Message, state:FSMContext):
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
        which_sum_change__amount = int(message.text)
        
        if which_sum_change__amount < 0:
            raise ValueError('fuck off')
        which_sum_change__amount = str(which_sum_change__amount)
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        await state.finish()

        return
    
    await state.update_data(which_sum_change__amount=which_sum_change__amount)

    data_state = await state.get_data()

    which_sum_change__sign = data_state['which_sum_change__sign']
    currency = data_state['which_sum_change__currency']

    if which_sum_change__sign == 'minus':
        sum = '-' + which_sum_change__amount
    else:
        sum = which_sum_change__amount

    changed_request = data_state['changed_request']

    if currency == 'rub':
        changed_request[5] = sum

    if currency == 'usd':
        changed_request[6] = sum

    if currency == 'eur':
        changed_request[7] = sum
            
    is_changed = True

    await state.update_data(is_changed=is_changed)
    await state.update_data(changed_request=changed_request)
    
    all_changes_data = data_state['all_changes_data']

    if 'sum' not in all_changes_data:
        all_changes_data.append('sum')
        await state.update_data(all_changes_data=all_changes_data)

    text = get_data_chosen_request(changed_request) + \
    '\n\n Выберите изменение:'

    await message.answer (
        text,
        reply_markup=create_kb_change_request(changed_request, is_changed)
    )

    await Processing.change_request_menu.set()

    return