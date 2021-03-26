import time

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, smsinfo
from states import SMSstate
from data import all_emoji

from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_who_waste
from keyboards import cb_who_waste
from keyboards import create_kb_yes_no_note
from keyboards import cb_yes_no_note


# from 'информация о смс' main_menu
@dp.message_handler(text='информация о смс')
async def enter_the_smsinfo(message:Message, state:FSMContext):
    '''
    В ответ запрашивает номер смс
    '''
    await message.delete()
    result = await message.answer(text='Введите порядковый номер смс')
    await state.update_data(message_to_delete=result.message_id)
    await SMSstate.sms_numb.set()


@dp.message_handler(state=SMSstate.sms_numb)
async def question_who_waste(message:Message, state:FSMContext):
    sms_numb = message.text
    await state.update_data(sms_numb=sms_numb)

    data_state = await state.get_data()
    await bot.delete_message (
        chat_id = message.chat.id,
        message_id = data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    try:
        result = await message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA',
            reply_markup=ReplyKeyboardRemove()
        )
        is_checked = smsinfo.check_sms(sms_numb)

    except Exception as e:
        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
        print(e)
        await message.answer_sticker (
            'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
        )
        await message.answer (
            text='Не удалось получить данные google таблицы',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    if not is_checked == True:
        await message.answer (
            text='Нет такой смс',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        
        return

    await message.answer (
        text='Кто тратит?',
        reply_markup=create_kb_who_waste()
    )
    await state.update_data(for_what_waste='-')
    await state.update_data(note_waste='-')
    await SMSstate.who_waste.set()

   

@dp.callback_query_handler(state=SMSstate.who_waste)
async def set_who_waste(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_who_waste.parse(call.data)

    if data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            f'===========\nВыход в главное меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    await state.update_data(who_waste=data_btn['type_btn'])
    
    data_state = await state.get_data()
    who_waste = data_state['who_waste']

    if who_waste == 'Личные Вит' or \
        who_waste == 'Личные Кэт' or \
        who_waste == 'Ошибка':

        await call.message.answer (
            text='Добавить примечание?',
            reply_markup=create_kb_yes_no_note()
        )
        await SMSstate.yes_no_note.set()
    

@dp.callback_query_handler(state=SMSstate.yes_no_note)
async def set_yes_no_note(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_yes_no_note.parse(call.data)
    
    if data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            f'===========\nВыход в главное меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    elif data_btn['type_btn'] == 'yes':
        pass

    elif data_btn['type_btn'] == 'no':
        data_state = await state.get_data()
        print(data_state)



#     data_state = await state.get_data()
#     chosen_permit = data_state['chosen_permit']

#     permit_id = chosen_permit[0]
#     permit_status = all_emoji[chosen_permit[3]]
#     permit_date = chosen_permit[2]
#     permit_text = chosen_permit[1]
#     text = f'Пропуск\n#{permit_id} {permit_status} {permit_date}\n{permit_text}'
    
#     await call.message.answer (
#         text=text,
#         reply_markup=create_kb_set_status_permit()
#         # > пропуск заказан
#         # > в офисе
#         # > назад главное меню
#     )
#     await Permitstate.status_permit.set()
    