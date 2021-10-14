from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Processing
from utils import get_values_FGH
from utils import get_text_before_close_request
from keyboards import cb_which_sum_close
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_close_request


# from: close_request_menu.pu
@dp.callback_query_handler(state=Processing.which_sum_correct_menu)
async def set_currency_to_correct(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает клавиатуру create_kb_which_sum_close(request)
    - sum rub
    - sum usd
    - sum eur
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(which_sum_correct_menu='+')

    data_btn = cb_which_sum_close.parse(call.data)

    if data_btn['type_btn'] == 'change_curr':
        await state.update_data(close__currency=data_btn['curr'])
        # data_state = await state.get_data()

        result = await call.message.answer (
            text='C какой суммой хотите закрыть?'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.close__sum.set()

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.message_handler(state=Processing.close__sum)
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
        close__sum = int(message.text)
        
        if close__sum <= 0:
            raise ValueError('fuck off')
        close__sum = str(close__sum)
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        print(e)

        return
    
    await state.update_data(close__sum=close__sum)
    # close__sum close__currency

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    correct_currency = data_state['close__currency']
    correct_sum = data_state['close__sum']

    if correct_currency == 'rub':
        if chosen_request[5][0] == '-':
            chosen_request[12] = str(0 - int(correct_sum))
        else: chosen_request[12] = correct_sum

    if correct_currency == 'usd':
        if chosen_request[6][0] == '-':
            chosen_request[13] = str(0 - int(correct_sum))
        else: chosen_request[13] = correct_sum

    if correct_currency == 'eur':
        if chosen_request[7][0] == '-':
            chosen_request[14] = str(0 - int(correct_sum))
        else: chosen_request[14] = correct_sum

    await state.update_data(chosen_request=chosen_request)

    text = get_text_before_close_request(chosen_request)

    await message.answer (
        text=text,
        reply_markup=create_kb_confirm_close_request(chosen_request)
        # > подтверждаю!
        # > закрыть с другой суммой
        # > скорректировать синие
        # > вернуться к заявке
        # > назад - главное меню
    )
    await Processing.close_request_menu.set()

    return