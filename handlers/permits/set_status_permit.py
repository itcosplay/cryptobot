from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, permit
from states import Permitstate
from data import all_emoji
from utils import notify_someone
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_set_status_prmt



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
            f'===========\nПросмотр пропусков отменен\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    chosen_permit = data_state['chosen_permit']
    permit_id = chosen_permit[0]

    if data_btn['type_btn'] == 'permit_ordered':
        permit.update_permit_data(chosen_permit[0], 'заказан')
        permit_warning = 'пропуск заказан'
        permit_notify = f'#{permit_id} пропуск заказан'

        await notify_someone(permit_notify, 'admin', 'changer', 'executor')


    if data_btn['type_btn'] == 'in_office':
        permit.update_permit_data(chosen_permit[0], 'отработан')
        permit_warning = 'гость прибыл в офис'
        permit_notify = f'#{permit_id} в офисе'

        await notify_someone(permit_notify, 'admin', 'changer', 'executor')
    
    
    text = f'Все оповещены о том, что по заявке #{permit_id} {permit_warning}'
    
    await call.message.answer (
        text=text,
        reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
    )
    await state.finish()
    