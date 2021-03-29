import time

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, permit
from states import Permitstate
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_all_permits
from keyboards import cb_all_permits
from keyboards import create_kb_set_status_permit

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
        time.sleep(1)

    except Exception as e:
        print(e)
        await message.answer_sticker (
            'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
        )
        await message.answer (
            text='Не удалось получить данные таблицы пропусков...',
            reply_markup=create_kb_coustom_main_menu(message.from_user.id)
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


# @dp.callback_query_handler(cb_current_requests.filter(type_btn='get_request'))
@dp.callback_query_handler(state=Permitstate.chosen_permit)
async def show_chosen_request(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает нажатие на один из пропусков, выведенных списком
    '''
    await call.answer()
    await call.message.delete()

    data_btn = cb_all_permits.parse(call.data)

    if data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            f'===========\nПросмотр пропусков отменен\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    all_permits = data_state['all_permits']

    for permit in all_permits:
        if data_btn['id'] == permit[0]:
            await state.update_data(chosen_permit=permit)
            break

    data_state = await state.get_data()
    chosen_permit = data_state['chosen_permit']

    permit_id = chosen_permit[0]
    permit_status = all_emoji[chosen_permit[3]]
    permit_date = chosen_permit[2]
    permit_text = chosen_permit[1]
    text = f'Пропуск\n#N{permit_id} {permit_status} {permit_date}\n{permit_text}'
    
    await call.message.answer (
        text=text,
        reply_markup=create_kb_set_status_permit()
        # > пропуск заказан
        # > в офисе
        # > назад главное меню
    )
    await Permitstate.status_permit.set()
    