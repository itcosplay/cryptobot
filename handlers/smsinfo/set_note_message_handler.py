import time

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, smsinfo
from states import SMSstate
from data import all_emoji


@dp.message_handler(state=SMSstate.note_waste)
async def set_note_waste(message:Message, state:FSMContext):
    data_state = await state.get_data()
    old_note = data_state['note_waste']
    if old_note == None:
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


    ######
    data_sms_info = smsinfo.push_data(data_state)
    print(data_sms_info)
    
    ######
    await state.finish()


    # try:
    #     result = await message.answer_sticker (
    #         'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA',
    #         reply_markup=ReplyKeyboardRemove()
    #     )
    #     is_checked = smsinfo.check_sms(sms_numb)

    # except Exception as e:
    #     await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
    #     print(e)
    #     await message.answer_sticker (
    #         'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
    #     )
    #     await message.answer (
    #         text='Не удалось получить данные google таблицы',
    #         reply_markup=create_kb_coustom_main_menu(message.chat.id)
    #     )

    #     return

    # await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    # if is_checked == False:
    #     await message.answer (
    #         text='Нет такой смс',
    #         reply_markup=create_kb_coustom_main_menu(message.chat.id)
    #     )
    #     await state.finish()
        
    #     return

    # await message.answer (
    #     text='Кто тратит?',
    #     reply_markup=create_kb_who_waste()
    # )
    # await state.update_data(for_what_waste='-')
    # await state.update_data(note_waste=is_checked)
    # await SMSstate.who_waste.set()

