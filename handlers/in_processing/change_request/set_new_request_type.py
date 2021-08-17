from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards import create_kb_change_request
from keyboards import create_kb_coustom_main_menu
from loader import dp
from states import Processing
from utils import get_data_chosen_request


@dp.callback_query_handler(state=Processing.new_request_type)
async def set_date_from_buttons(call:CallbackQuery, state:FSMContext):
    '''
    > выдача                 issuing_office
    > прием                  cash_recive
    > доставка               delivery
    > обмен                  exchange
    > кэшин                  cash_in
    > снятие с карт          cash_out
    > документы              documents
    > назад                  back
    > главное меню           main_menu
    '''
    await call.answer()
    await call.message.delete()

    if call.data == 'issuing_office':
        new_request_type = 'выдача'
    
    elif call.data == 'cash_recive':
        new_request_type = 'прием'

    elif call.data == 'delivery':
        new_request_type = 'доставка'

    elif call.data == 'exchange':
        new_request_type = 'обмен'

    elif call.data == 'cash_in':
        new_request_type = 'кэшин'
    
    elif call.data == 'cash_out':
        new_request_type = 'снятие с карт'

    elif call.data == 'documents':
        new_request_type = 'документы'

    elif call.data == 'back':
        data_state = await state.get_data()

        changed_request = data_state['changed_request']
        is_changed = data_state['is_changed']

        text = get_data_chosen_request(changed_request) + \
        '\n\n Выберите изменение:'
        
        await call.message.answer (
            text,
            reply_markup=create_kb_change_request(changed_request, is_changed)
        )

        await Processing.change_request_menu.set()

        return

    elif call.data == 'main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return
    
    data_state = await state.get_data()

    is_changed = True
    changed_request = data_state['changed_request']
    
    changed_request[3] = new_request_type
    # changed_request[5] = '0'
    # changed_request[6] = '0'
    # changed_request[7] = '0'
    # changed_request[11] = 'В обработке'
    # changed_request[12] = '0'
    # changed_request[13] = '0'
    # changed_request[14] = '0'
    # changed_request[16] = '0'

    await state.update_data(is_changed=is_changed)
    await state.update_data(changed_request=changed_request)

    all_changes_data = data_state['all_changes_data']

    if 'request_type' not in all_changes_data:
        all_changes_data.append('request_type')
        await state.update_data(all_changes_data=all_changes_data)

    text = get_data_chosen_request(changed_request) + \
    '\n\n Выберите изменение:'

    await call.message.answer (
        text,
        reply_markup=create_kb_change_request(changed_request, is_changed)
    )

    await Processing.change_request_menu.set()

    return
