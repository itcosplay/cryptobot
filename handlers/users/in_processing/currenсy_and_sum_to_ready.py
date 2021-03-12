from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing
from loader import sheet
from keyboards import cb_what_sum


@dp.callback_query_handler(state=Processing.chosen_sum_to_ready)
async def choose_currency(call:CallbackQuery, state:FSMContext):
    # await call.answer()

    data_btn = cb_what_sum.parse(call.data)

    if data_btn['type_btn'] == 'with_current':
        await state.update_data(chosen_sum_to_ready='with_current')
        data_state = await state.get_data()
        request = data_state['chosen_request']

        request[12] = request[5]
        request[13] = request[6]
        request[14] = request[7]
        request[11] = 'Готово к выдаче'

        sheet.replace_row(request)
        await call.answer()
        await call.message.delete()
        await call.message.answer (
            f'Для заявки {request[2]} установлен статус "Готово к выдаче"'
        )
        await state.finish()

        