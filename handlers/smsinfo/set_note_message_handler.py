import time

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot, smsinfo
from states import SMSstate
from data import all_emoji
from utils import notify_someone
from keyboards import create_kb_coustom_main_menu


@dp.message_handler(state=SMSstate.note_waste)
async def set_note_waste(message:Message, state:FSMContext):
    data_state = await state.get_data()
    old_note = data_state['note_waste']

    if old_note == '-':
        old_note = ''

    else:
        old_note = old_note + ' || '
    new_note = old_note + message.text

    await state.update_data(note_waste=new_note)

    data_state = await state.get_data()
    await bot.delete_message (
        chat_id = message.chat.id,
        message_id = data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    data_state = await state.get_data()
    user = message.chat.first_name
    ######
    ######
    ######
    try:
        result = await message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA',
            reply_markup=ReplyKeyboardRemove()
        )
        data_sms_info = smsinfo.push_data(data_state, user)

    except Exception as e:
        print(e)
        await message.answer_sticker (
            'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
        )
        await message.answer (
            text='Не удалось соединиться с гугл таблицей',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        
        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

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
    await message.answer (
        text='Информация обновлена!',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )
    ######
    ######
    ######
    notification_list = ['admin', 'changer', 'secretary']

    await notify_someone(text, *notification_list)
    ######
    ######
    ######
    await state.finish()

