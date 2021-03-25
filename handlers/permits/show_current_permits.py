from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp, bot, permit
from states import Permitstate
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_all_permits

# from 'пропуска' main_menu
@dp.message_handler(text='пропуска')
async def show_current_requests(message:Message, state:FSMContext):
    '''
    Обрабатывает команду "пропуска" и отображает список текущих
    пропусков. Если текущих пропусков
    нет, то отвечает - "На сегодня и последующие даты пропусков нет."
    '''
    await message.delete()

    try:
        result = await message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA',
            reply_markup=ReplyKeyboardRemove()
        )

        permits = permit.get_all_permits()

    except Exception as e:
        print(e)
        await message.answer_sticker (
            'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
        )
        await message.answer (
            text='Не удалось получить данные таблицы пропусков...',
            reply_markup=create_cb_coustom_main_menu(message.from_user.id)
        )

        return

    await state.update_data(all_permits=permits)

    if len(permits) == 0:
        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
        await message.answer (
            text='На сегодня и последующие даты пропусков нет.',
            reply_markup=create_kb_coustom_main_menu(message.from_user.id)
        )
        await state.finish()

    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
        await message.answer (
            text='Пропуска:',
            reply_markup=create_kb_all_permits(permits)
        )
        
        await Permitstate.chosen_permit.set()
        # to ...
