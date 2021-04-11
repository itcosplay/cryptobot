from keyboards.default.admin_keyboard import create_kb_coustom_main_menu
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards import cb_change_request
from keyboards import create_kb_change_date
from keyboards import create_kb_new_request_type
from keyboards import create_kb_which_sum_close
from keyboards import create_kb_another_currecy_add
from loader import dp
from states import Processing


@dp.callback_query_handler(state=Processing.change_request_menu)
async def change_request_menu_handler(call:CallbackQuery, state:FSMContext):
    '''
    keyboards/inline/in_processin/change_request_keyboards.create_kb_change_request
    > иная дата             another_data
    > новый номер           new_id
    > переопределить тип    change_type
    > изменить сумму        update_sum
    > другая валюта         more_currency
    > добавить коментарий   add_commetn
    > назад - главное меню  back__main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(change_request_menu='+')

    data_btn = cb_change_request.parse(call.data)

    if data_btn['type_btn'] == 'another_data':
        await call.message.answer (
            text='Выберите дату',
            reply_markup=create_kb_change_date()
        )
        await Processing.select_date.set()

    elif data_btn['type_btn'] == 'new_id':
        result = await call.message.answer (
            text='Введите новый четырех значный номер заявки'
        )
        
        await state.update_data(message_to_delete=result.message_id)
        await Processing.new_request_id.set()

        return

    elif data_btn['type_btn'] == 'change_type':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        await call.message.answer (
            text='Выберите новый тип заявки',
            reply_markup=create_kb_new_request_type(chosen_request[3])
        )
        await Processing.new_request_type.set()

        return

    elif data_btn['type_btn'] == 'update_sum':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        await call.message.answer (
            text='Какая сумма будет изменена?',
            reply_markup=create_kb_which_sum_close(chosen_request)
        )
        await Processing.which_sum_change.set()

        return

    elif data_btn['type_btn'] == 'more_currency':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        if chosen_request[5] == '0' or chosen_request[6] == '0' or chosen_request[7] == '0':
            await call.message.answer (
                text='Выберите валюту, которую необходимо добавить?',
                reply_markup=create_kb_another_currecy_add(chosen_request)
            )
            await Processing.another_currency_add_menu.set()        
        else:
            await call.message.answer (
                text='Невозможно добавить другую валюту... Выход в главное меню',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )
            await state.finish()

        return