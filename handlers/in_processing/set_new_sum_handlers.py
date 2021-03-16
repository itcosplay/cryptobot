from ssl import ALERT_DESCRIPTION_CERTIFICATE_UNOBTAINABLE
from keyboards.inline import request_kb
import data
from aiogram.types import Message, CallbackQuery, message
from aiogram.dispatcher import FSMContext

from loader import dp, bot, sheet
from states import Processing
from keyboards import cb_choose_currency
from keyboards import create_kb_chosen_request




@dp.callback_query_handler(state=Processing.sum_currency_to_change)
async def set_currency_to_change(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_choose_currency.parse(call.data)
    await state.update_data(sum_currency_to_change=data_btn['curr'])
    # {'@': 'cbkbws', 'curr': 'USD', 'type_btn': 'change_curr'}

    data_state = await state.get_data()
    request = data_state['chosen_request']

    if data_state['sum_currency_to_change'] == 'RUB':
        old_sum = request[5] + ' RUB'
    if data_state['sum_currency_to_change'] == 'USD':
        old_sum = request[6] + ' USD'
    if data_state['sum_currency_to_change'] == 'EUR':
        old_sum = request[7] + ' EUR'

    if data_state['chosen_request_menu'] == 'change_request':
        old_comment = request[8]
        new_comment = old_comment + '; прежняя сумма: ' + old_sum + ';'
        request[8] = new_comment
        await state.update_data(chosen_request=request)


    result = await call.message.answer (
        f'СТАРАЯ СУММА:  {old_sum}. ВВЕДИТЕ НОВУЮ СУММУ:\n'
    )
    await state.update_data(message_to_delete=result.message_id)
    await Processing.sum_amount_to_change.set()



@dp.message_handler(state=Processing.sum_amount_to_change)
async def set_sum_for_change(message:Message, state:FSMContext):
    try:
        new_sum = int(message.text)
        
    except Exception as e:
        await message.answer('Редактирование отменено. Формат суммы не правильный.')
        await state.finish()
        print(e)
    
    await state.update_data(sum_amount_to_change=new_sum)

    data_state = await state.get_data()
    request = data_state['chosen_request']

    currency = data_state['sum_currency_to_change']

    if currency == 'RUB':
        old_sum = request[5]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''
            
        request[5] = plus_or_minus + str(new_sum)

    if currency == 'USD':
        old_sum = request[6]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''

        request[6] = plus_or_minus + str(new_sum)

    if currency == 'EUR':
        old_sum = request[7]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''

        request[7] = plus_or_minus + str(new_sum)

    await state.update_data(chosen_request=request)

    data_state = await state.get_data()
    request = data_state['chosen_request']

    
    
    data_state = await state.get_data()
    request = data_state['chosen_request']

    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]

    if not request[5] == '-': sum_RUB = request[5] + ' RUB\n'
    else: sum_RUB = ''

    if not request[6] == '-': sum_USD = request[6] + ' USD\n'
    else: sum_USD = ''

    if not request[7] == '-': sum_EUR = request[7] + ' EUR'
    else: sum_EUR = ''


    if data_state['chosen_request_menu'] == 'change_request':
        request[11] = 'В обработке'
        sheet.replace_row(request)
        await state.update_data(chosen_request=request)


    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )    

    # data_state = await state.get_data()
    # request = data_state['chosen_request']

    await message.answer (
        'заявка {} от {}\nоперация: {}\nсуммы:\n{}{}{}'.format (
            id_request, 
            date_request, 
            operation_type_request,
            sum_RUB,
            sum_USD,
            sum_EUR
        ),
        reply_markup=create_kb_chosen_request(request)
    )
    
    
    await Processing.chosen_request_menu.set()
