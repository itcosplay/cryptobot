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
            f'===========\nОтмена, выход в главное меню\n===========',
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

    if reserve_to_ready__currency == 'rub':
        pass
        # тут откладывается колличество синих купюр

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

    



    # data_state = await state.get_data()
    # request = data_state['chosen_request']

    # currency = data_state['reserve_to_ready__currency']

    # await state.update_data(chosen_request=request)

    # data_state = await state.get_data()
    # request = data_state['chosen_request']

    # id_request = request[2]
    # date_request = request[0]
    # operation_type_request = emo_in_chosen_request[request[3]]


    # await state.update_data(chosen_request=request)


    # await message.answer (
    #     text=f'#{id_request} {operation_type_request} от {date_request}\nОтложить к выдаче c суммами?\n{rub}{usd}{eur}',
    #     reply_markup=create_kb_corrected_sum()
    # )
    
    # await Processing.confirm_correct_to_ready.set()
    # to chosen_request_menu.py


# @dp.callback_query_handler(state=Processing.confirm_correct_to_ready)
# async def confirm_correct_to_ready(call:CallbackQuery, state:FSMContext):
#     await call.answer()
#     await call.message.delete()

#     data_btn = cb_corrected_sum.parse(call.data)

#     if data_btn['type_btn'] == 'confirm':
#         data_state = await state.get_data()
#         request = data_state['chosen_request']

#         ###########################
#         if request[5] != '-':
#             await call.message.answer (
#                 text='Сколько синих?',
#                 reply_markup=create_kb_what_blue()
#             )
            
#             await Processing.blue_amount.set()
#             # to blue_amount_handlers.py
#             return
#         ###########################

#         request[11] = 'Готово к выдаче'
#         request[16] = '0' # тут синих быть не должно

        # try:
        #     result = await call.message.answer_sticker (
        #     'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        #     )
        #     sheet.replace_row(request)

        # except Exception as e:
        #     print(e)
        #     await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
        #     await call.message.answer_sticker (
        #         'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
        #     )
        #     await call.message.answer (
        #         text='Не удалось соединиться с гугл таблицей',
        #         reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        #     )

        #     return

#         await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

#         data_state = await state.get_data()
#         request = data_state['chosen_request']

#         id_request = request[2]

#         await call.message.answer (
#             text=f'Заявка #{id_request} отложена к выдаче.',
#             reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
#         )

#         await state.finish()

#         return

#     if data_btn['type_btn'] == 'correct_else':
#         data_state = await state.get_data()
#         request = data_state['chosen_request']

#         await call.message.answer (
#             'Какую сумму меняем?',
#             reply_markup=create_kb_what_sum_correct(request)
#         )
#         await Processing.correct_curr_sum_ready.set()
#         # to def set_currency_to_correct
#         return

#     else: # back_main_menu
#         await call.message.answer (
#             text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
#             reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
#         )
#         await state.finish()

#         return
