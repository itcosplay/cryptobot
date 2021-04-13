from datetime import datetime
from keyboards.inline.in_processing.blue_keyboard import create_kb_confirm_blue
from os import stat

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from utils import notify_about_permit_to_order
from loader import dp, bot, permit
from states import Permitstate
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_single_permit


# from 'создать пропуск' main_menu
@dp.message_handler(text='создать пропуск')
async def enter_to_single_permit(message:Message, state:FSMContext):
    '''
    Запрашивает данные для отдельного пропуска
    '''
    await message.delete()
    await state.finish()
    result = await message.answer(text='Введите Ф.И.О. для пропуска')
    await state.update_data(message_to_delete=result.message_id)
    await Permitstate.single_permit_data.set()


@dp.message_handler(state=Permitstate.single_permit_data)
async def set_single_permit(message:Message, state:FSMContext):
    '''
    Создаем новый пропуск
    '''
    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    await state.update_data(single_permit_data='+')

    all_permit_id_list = permit.get_all_permit_id()

    permit_id = 9999
    limit_while = 1

    while True:
        if str(permit_id) in all_permit_id_list:
            permit_id -= 1
            limit_while += 1

        else:

            break

        if limit_while == 50:

            return False

    permit_id = str(permit_id)
    permit_id = permit_id.zfill(4)

    permit_text = message.text
    permit_date = datetime.today().strftime('%d.%m')

    await state.update_data(single_permit_id=permit_id)
    await state.update_data(single_permit_text=permit_text)
    await state.update_data(single_permit_date=permit_date)

    text = f'Подтверждаете новый пропуск с данными:\n{permit_text}'

    await message.answer (
        text=text,
        reply_markup=create_kb_confirm_single_permit()
    )

    await Permitstate.single_permit_confirm.set()


@dp.callback_query_handler(state=Permitstate.single_permit_confirm)
async def confirm_single_permit(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'confirm':
        data_state = await state.get_data()

        permit_id = data_state['single_permit_id']
        permit_text = data_state['single_permit_text']
        permit_date = data_state['single_permit_date']

        permit.write_new_permit(permit_id, permit_date, permit_text=permit_text)
        await notify_about_permit_to_order()

        await call.message.answer (
            text=f'Новый пропуск #N{permit_id} добавлен, секретарь оповещен!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход в главное меню. Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return