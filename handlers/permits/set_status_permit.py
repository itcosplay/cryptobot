from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, permit
from states import Permitstate
from data import all_emoji
from utils import notify_someone
from utils import notify_in_group_chat
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_set_status_prmt
from keyboards import create_kb_confirm_single_permit


@dp.callback_query_handler(state=Permitstate.status_permit)
async def set_status_permit(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает нажатие на один из пропусков, выведенных списком
    '''
    await call.answer()
    await call.message.delete()

    data_btn = cb_set_status_prmt.parse(call.data)

    if data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            f'Выход из меню "ПРОПУСКА". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    chosen_permit = data_state['chosen_permit']
    permit_id = chosen_permit[0]
    request_numb = chosen_permit[1]
    print('request_Numb^ ', request_numb)

    if data_btn['type_btn'] == 'permit_ordered':
        permit.update_permit_data(permit_id, 'заказан')
        permit_warning = 'пропуск заказан'
        permit_ready = all_emoji['заказан']
        permit_notify = f'{permit_ready} #N{request_numb} пропуск заказан {permit_ready}'

        await notify_someone(permit_notify, 'admin', 'changer', 'executor')
        await notify_in_group_chat(permit_notify)

    if data_btn['type_btn'] == 'in_office':
        permit.update_permit_data(permit_id, 'отработан')
        permit_warning = 'гость прибыл в офис'
        permit_notify = f'⚠️ #N{request_numb} В ОФИСЕ ⚠️'

        await notify_someone(permit_notify, 'admin', 'changer', 'executor')
        await notify_in_group_chat(permit_notify)

    if data_btn['type_btn'] == 'delete_permit':
        await call.message.answer (
            f'Удаляем пропуск №{request_numb}?',
            reply_markup=create_kb_confirm_single_permit()
        )
        await state.update_data(status_permit=permit_id)
        await state.update_data(permit_numb=request_numb)
        await Permitstate.confirm_delete_permit.set()

        return
        
    
    text = f'Все оповещены о том, что по заявке #N{request_numb} {permit_warning}'
    
    await call.message.answer (
        text=text,
        reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
    )
    await state.finish()

    return


@dp.callback_query_handler(state=Permitstate.confirm_delete_permit)
async def delete_permit(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'confirm':
        data_state = await state.get_data()
        permit_id = data_state['status_permit']
        permit_numb = data_state['permit_numb']
        username = call.message.chat.username

        permit.delete_permit(permit_id)

        permit_warning = 'пропуск удален'
        permit_notify = f'#N{permit_numb} пропуск удален @{username}'

        await notify_someone(permit_notify, 'admin', 'changer', 'executor')
        await notify_in_group_chat(permit_notify)

        text = f'Все оповещены о том, что по заявке #N{permit_numb} {permit_warning}'

        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return


    elif call.data == 'back__main_menu':
        await call.message.answer (
            f'Выход из меню "ПРОПУСКА". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return