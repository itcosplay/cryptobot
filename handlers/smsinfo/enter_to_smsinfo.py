import time

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from filters import isAdmin_or_isSecretary
from loader import dp, bot, smsinfo, db
from states import SMSstate
from data import all_emoji
from data import sticker
from data import sms_chat
from utils import notify_someone

from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_who_waste
from keyboards import cb_who_waste
from keyboards import create_kb_yes_no_note
from keyboards import cb_yes_no_note
from keyboards import create_kb_for_what_waste


# from 'информация о смс' main_menu
@dp.message_handler(isAdmin_or_isSecretary(),text='информация о смс')
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

    try:
        sms_numb = int(message.text)
        if sms_numb <= 0:
            raise ValueError('fuck off')
    except Exception as e:
        print(e)
        await message.answer_sticker (
            sticker['false_data']
        )
        await message.answer (
            text='Неправильный формат номера смс. Возврат в главное меню.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()

        return

    sms_numb = str(sms_numb)

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
            sticker['go_to_table'],
            reply_markup=ReplyKeyboardRemove()
        )
        is_checked = smsinfo.check_sms(sms_numb)

    except Exception as e:
        print(e)
        await message.answer_sticker (
            sticker['not_connection']
        )
        await message.answer (
            text='Не удалось получить данные google таблицы',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    if is_checked == False:
        await message.answer (
            text='Нет такой смс',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        
        return
    
    if is_checked == None: is_checked = '-'

    await message.answer (
        text='Кто тратит?',
        reply_markup=create_kb_who_waste()
    )
    await state.update_data(for_what_waste='-')
    await state.update_data(note_waste=is_checked)
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

    else:
        await call.message.answer (
            text='На что потрачено?',
            reply_markup=create_kb_for_what_waste(who_waste)
        )
        await SMSstate.for_what_waste.set()
        # ---> set_for_what_waste.py <---
    

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
        result = await call.message.answer (
            text='Введите примечание'
        )
        await SMSstate.note_waste.set()
        await state.update_data(message_to_delete=result.message_id)

    # to-table --->>>>
    elif data_btn['type_btn'] == 'no':
        data_state = await state.get_data()
        user = call.message.chat.first_name
        ######
        ######
        ######
        try:
            result = await call.message.answer_sticker (
                'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA',
                reply_markup=ReplyKeyboardRemove()
            )
            data_sms_info = smsinfo.push_data(data_state, user)

        except Exception as e:
            print(e)
            await call.message.answer_sticker (
                'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        operation_type = data_sms_info[0]
        card = data_sms_info[1]
        sms_numb = data_sms_info[2]

        who_waste = data_sms_info[3]
        who_waste = f'Кто потратил: {who_waste}'

        for_what_waste = data_sms_info[4]
        
        if not for_what_waste == '':
            for_what_waste = f'\nНа что потрачено: {for_what_waste}'

        note_waste = data_sms_info[5]

        if not note_waste == '':
            note_waste = f'\nПримечание: {note_waste}'

        user = f'Пользователь: {user}'

        if operation_type == 'Перевод':
            text_emodji = all_emoji['Перевод']
            text_emodji = f'{text_emodji}{text_emodji}{text_emodji}'

        elif operation_type == 'Пополнение':
            text_emodji = all_emoji['Пополнение']
            text_emodji = f'{text_emodji}{text_emodji}{text_emodji}'

        elif operation_type == 'Покупка':
            text_emodji = all_emoji['Покупка']
            text_emodji = f'{text_emodji}{text_emodji}{text_emodji}'

        elif operation_type == 'Снятие':
            text_emodji = all_emoji['Снятие']
            text_emodji = f'{text_emodji}{text_emodji}{text_emodji}'

        else:
            operation_type = 'Другие'
            text_emodji = all_emoji['Другие']
            text_emodji = f'{text_emodji}{text_emodji}{text_emodji}'

        text = f'{text_emodji} #{operation_type} #{card} #N{sms_numb}\n{user}\n{who_waste}{for_what_waste}{note_waste}'
        ######
        ######
        ######
        await call.message.answer (
            text='Информация обновлена!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        ######
        ######
        ######
        notification_list = ['admin', 'changer', 'secretary']

        await notify_someone(text, *notification_list)
        await bot.send_message(sms_chat, text)
        ######
        ######
        ######
        await state.finish()

        


