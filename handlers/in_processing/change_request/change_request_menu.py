from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards import cb_change_request
from keyboards import create_kb_change_date
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

        return

    if data_btn['type_btn'] == 'new_id':
        result = await call.message.answer (
            text='Введите новый четырех значный номер заявки'
        )
        
        await state.update_data(message_to_delete=result.message_id)
        await Processing.new_request_id.set()

        return