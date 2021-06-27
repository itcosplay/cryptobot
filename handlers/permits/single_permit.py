import data
from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_single_permit
from loader import dp, bot, permit
from states import Permitstate
from utils import notify_about_permit_to_order


# from main_menu 'создать пропуск'
@dp.message_handler(text='создать пропуск')
async def enter_to_single_permit(message:Message, state:FSMContext):
    '''
    Asks coustom permint numb
    '''
    await message.delete()
    await state.finish()
    # permit_is_exist means that all permit data is ready,
    # (permit_is_exist='+')
    # so, we can edit current permit.
    # Here permit is not ready
    await state.update_data(permit_is_exist='-')

    result = await message.answer(text='Введите номер пропуска')

    await state.update_data(message_to_delete=result.message_id)
    await Permitstate.single_permit_numb.set()


@dp.message_handler(state=Permitstate.single_permit_numb)
async def set_single_permit_data(message:Message, state:FSMContext):
    '''
    Reads in state coustom permint numb and asks full name
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

    await state.update_data(single_permit_numb=message.text)

    data_state = await state.get_data()
    
    if data_state['permit_is_exist'] == '+':
        single_permit_numb = data_state['single_permit_numb']
        single_permit_full_name = data_state['single_permit_full_name']

        text = \
            'Подтверждаете новый пропуск?\n' + \
            f'номер: {single_permit_numb}\n' + \
            f'ФИО: {single_permit_full_name}'

        await message.answer (
            text=text,
            reply_markup=create_kb_confirm_single_permit()
        )

        await Permitstate.single_permit_confirm.set()

    else:
        result = await message.answer(text='Введите ФИО')

        await state.update_data(message_to_delete=result.message_id)
        await Permitstate.single_permit_full_name.set()


@dp.message_handler(state=Permitstate.single_permit_full_name)
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

    await state.update_data(single_permit_full_name=message.text)

    permit_id = datetime.today().strftime('%d%H%M%S')
    permit_date = datetime.today().strftime('%d.%m')

    await state.update_data(single_permit_id=permit_id)
    await state.update_data(single_permit_date=permit_date)

    data_state = await state.get_data()
    single_permit_numb = data_state['single_permit_numb']
    single_permit_full_name = data_state['single_permit_full_name']

    await state.update_data(permit_is_exist='+')

    text = \
        'Подтверждаете новый пропуск?\n' + \
        f'номер: {single_permit_numb}\n' + \
        f'ФИО: {single_permit_full_name}'

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
        permit_numb = data_state['single_permit_numb']
        permit_full_name = data_state['single_permit_full_name']
        permit_date = data_state['single_permit_date']
        username = call.message.chat.username

        permit.write_new_permit(permit_id, permit_numb, permit_date, permit_text=permit_full_name)
        await notify_about_permit_to_order(permit_numb, username)

        await call.message.answer (
            text=f'Новый пропуск #N{permit_numb} добавлен, секретарь оповещен!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return

    elif call.data == 'edit_numb':
        result = await call.message.answer(text='Введите номер пропуска')

        await state.update_data(message_to_delete=result.message_id)
        await Permitstate.single_permit_numb.set()

        return

    elif call.data == 'edit_full_name':
        result = await call.message.answer(text='Введите ФИО')

        await state.update_data(message_to_delete=result.message_id)
        await Permitstate.single_permit_full_name.set()

        return

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход в главное меню. Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return