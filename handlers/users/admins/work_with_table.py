from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp, bot
from states import Request


@dp.message_handler(text='создать заявку')
async def enter_to_request(message:types.Message):
    from keyboards.inline.request_kb import create_kb_request_from

    keyboard = create_kb_request_from()
    
    await message.answer (
        'Создаем заявку! Через кого создаем заявку?',
        reply_markup = keyboard
    )
    await Request.executor.set()


@dp.callback_query_handler(state=Request.executor)
async def set_request_from(call:types.CallbackQuery, state:FSMContext):
    from keyboards.inline.request_kb import create_kp_operation_type

    if call.data == 'exit':
        await call.answer()
        await call.message.answer(f'Создание заявки отменено')
        await call.message.delete()
        await state.finish()
    else:
        await call.answer()
        await state.update_data(executor=call.data)
        await call.message.delete()

        keyboard = create_kp_operation_type()

        await call.message.answer (
            f'Выберите тип операци:', reply_markup = keyboard
        )
        await Request.type_of_operation.set()


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
        await call.answer()
        await state.update_data(type_of_operation=call.data)
        await call.message.delete()
        await call.message.answer(f'Тут должны быть данные с таблицы')
    else:
        await call.answer()
        await call.message.answer(f'Создание заявки отменено')
        await state.finish()
        await call.message.delete()


@dp.callback_query_handler(state=Request.type_of_card)
async def set_type_of_card(call:types.CallbackQuery, state:FSMContext):
    await call.answer()

    card = call.data

    await state.update_data(type_of_card=card)
    await call.message.delete()
    await call.message.answer(f'укажите сумму:')
    await Request.how_much.set()


@dp.message_handler(state=Request.how_much)
async def set_how_much(message:types.Message, state:FSMContext):
    from keyboards.inline.request_kb import create_kb_choose_currency

    try:
        summ = float(message.text)
        await state.update_data(how_much=summ)
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )

        keyboard = create_kb_choose_currency()
        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=keyboard
        )    
        await Request.how_much_curr.set()
    except Exception:
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено.'
        )
        await state.finish()
        await message.delete()


@dp.message_handler(state=Request.how_much_recive)
async def set_how_much_recive(message:types.Message, state:FSMContext):
    from keyboards.inline.request_kb import create_kb_choose_currency

    try:
        summ = float(message.text)
        await state.update_data(how_much_recive=summ)
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )

        keyboard = create_kb_choose_currency()
        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=keyboard
        )    
        await Request.how_much_recive_curr.set()
    except Exception:
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено.'
        )
        await state.finish()
        await message.delete()


@dp.message_handler(state=Request.how_much_give)
async def set_how_much_give(message:types.Message, state:FSMContext):
    from keyboards.inline.request_kb import create_kb_choose_currency

    try:
        summ = float(message.text)
        await state.update_data(how_much_give=summ)
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )

        keyboard = create_kb_choose_currency()
        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=keyboard
        )    
        await Request.how_much_give_curr.set()
    except Exception:
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено.'
        )
        await state.finish()
        await message.delete()


@dp.callback_query_handler(state=Request.how_much_curr)
async def set_how_much_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    from keyboards.inline.request_kb import create_kb_send_request

    await call.answer()

    currency = call.data

    await state.update_data(how_much_curr=currency)

    data = await state.get_data()
    # print(data) # example:
    # {
    # 'executor': 'changer',
    # 'type_of_operation': 'cache_in',
    # 'type_of_card': 'alfa',
    # 'how_much': 100.0,
    # 'how_much_curr': 'usd'
    # }

    translate_keys_request = {
        'executor': 'исполнитель - ',
        'type_of_operation': 'тип операции - ',
        'type_of_card': 'карта - ',
        'how_much': 'сумма - ',
        'how_much_recive': 'cумма - ',
        'how_much_give': 'сумма - ',
        'how_much_curr': 'валюта - ',
        'how_much_recive_curr': 'валюта - ',
        'how_much_give_curr': 'валюта - ',
        'comment': 'комментарий - '
    } 
    translate_values_request = {
        'changer': 'чейнджер',
        'operator': 'оператор',
        'recive': 'прием',
        'takeout': 'выдача',
        'delivery': 'доставка',
        'cache_in': 'кэшин',
        'change': 'обмен',
        'cache_atm': 'снятие с карт',
        'alfa': 'альфа-банк',
        'sber': 'сбер',
        'rub': 'рубли',
        'usd': 'доллары',
        'eur': 'евро'
    }
    result_data_to_show = []

    for key in data.keys():
        if key in translate_keys_request:
            if (type(data[key]) == int or type(data[key]) == float):
                result_data_to_show.append (
                    translate_keys_request[key] + str(data[key]) + '\n'
                )
            else:
                temp_1 = translate_keys_request[key]
                temp_2 = translate_values_request[data[key]] + '\n'
                
                result_data_to_show.append(temp_1 + temp_2)

    result_data_to_show = ''.join(result_data_to_show)
    keyboard = create_kb_send_request()
    
    await call.message.delete()
    await call.message.answer (
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + result_data_to_show,
        reply_markup = keyboard
    )
    await Request.comment.set()


@dp.callback_query_handler(state=Request.how_much_recive_curr)
async def set_how_much_recive_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()

    currency = call.data

    await state.update_data(how_much_recive_curr=currency)
    await call.message.delete()
    await call.message.answer(f'Сколько выдаем?')
    await Request.how_much_give.set()


@dp.callback_query_handler(state=Request.how_much_give_curr)
async def set_how_much_give_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    from keyboards.inline.request_kb import create_kb_send_request

    await call.answer()

    currency = call.data

    await state.update_data(how_much_give_curr=currency)

    data = await state.get_data()
    # print(data) # example:
    # {
    # 'executor': 'changer',
    # 'type_of_operation': 'cache_in',
    # 'type_of_card': 'alfa',
    # 'how_much': 100.0,
    # 'how_much_curr': 'usd'
    # }

    translate_keys_request = {
        'executor': 'исполнитель - ',
        'type_of_operation': 'тип операции - ',
        'type_of_card': 'карта - ',
        'how_much': 'сумма - ',
        'how_much_recive': 'cумма приема - ',
        'how_much_give': 'сумма выдачи - ',
        'how_much_curr': 'валюта - ',
        'how_much_recive_curr': 'валюта приема - ',
        'how_much_give_curr': 'валюта выдачи - ',
        'comment': 'комментарий - '
    } 
    translate_values_request = {
        'changer': 'чейнджер',
        'operator': 'оператор',
        'recive': 'прием',
        'takeout': 'выдача',
        'delivery': 'доставка',
        'cache_in': 'кэшин',
        'change': 'обмен',
        'cache_atm': 'снятие с карт',
        'alfa': 'альфа-банк',
        'sber': 'сбер',
        'rub': 'рубли',
        'usd': 'доллары',
        'eur': 'евро'
    }
    result_data_to_show = []

    for key in data.keys():
        if key in translate_keys_request:
            if (type(data[key]) == int or type(data[key]) == float):
                result_data_to_show.append (
                    translate_keys_request[key] + str(data[key]) + '\n'
                )
            else:
                temp_1 = translate_keys_request[key]
                temp_2 = translate_values_request[data[key]] + '\n'
                
                result_data_to_show.append(temp_1 + temp_2)

    result_data_to_show = ''.join(result_data_to_show)
    keyboard = create_kb_send_request()
    
    await call.message.delete()
    await call.message.answer (
        text = 'БУДЕТ ОТПРАВЛЕННА ЗАЯВКА ' + \
        'СО СЛЕДУЮЩИМИ ДАННЫМИ:\n' + result_data_to_show,
        reply_markup = keyboard
    )
    await Request.comment.set()


@dp.callback_query_handler(state=Request.comment)
async def set_comm_or_else(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await state.finish()
    pass
    # await call.answer()
    # comm = ''
    # await state.update_data(comment=comm)



# @dp.message_handler(state=Request.type_of_operation)
# async def set_type_of_operation(message:types.Message, state:FSMContext):
#     data = await state.get_data()
#     executor = data.get('executor')
#     type_of_operation = message.text

#     if type_of_operation == 'кэшин':
#         await state.update_data(type_of_operation = type_of_operation)
#         await message.answer (
#             '''
#             Введите с какой карты:
#             - "Альфа-банк"
#             - "Сбер"
#             '''
#         )
#         await Request.type_of_card.set()
#     else:
#         await message.answer('Ваша заявка сформированна!')
#         await message.answer (
#             f'Заявка содержит следующие данные: {executor} {type_of_operation}'
#         )
#         await state.finish()


# @dp.message_handler(state=Request.type_of_card)
# async def set_type_of_card(message:types.Message, state:FSMContext):
#     data = await state.get_data()
#     executor = data.get('executor')
#     type_of_operation = data.get('type_of_operation')
#     type_of_card = message.text

#     await message.answer('Ваша заявка сформированна!')
#     await message.answer (
#         f'Заявка содержит следующие данные: {executor} {type_of_operation} {type_of_card}'
#     )
#     await state.finish()