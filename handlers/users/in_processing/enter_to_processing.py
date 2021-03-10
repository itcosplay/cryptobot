from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import isExecutor_and_higher
from loader import dp, sheet
from keyboards import create_kb_current_requests
from states import Processing

@dp.message_handler(isExecutor_and_higher(), text='в работе')
async def inter_to_processing(message:types.Message, state:FSMContext):
    await message.delete()

    current_requests, in_processing, ready_to_give = sheet.get_numbs_processing_and_ready_requests()

    await state.update_data(current_requests=current_requests)
    
    if len(in_processing) == 0 and len(ready_to_give) == 0:
        await message.answer('Все заявки исполненны.')
        
    else:

        if len(in_processing) == 0:
            await message.answer('Заявки со статусом "В обработке" отсутствуют')

        else:

            await message.answer (
                'Заявки в обработке:',
                reply_markup=create_kb_current_requests(in_processing))

        if len(ready_to_give) == 0:
            await message.answer('Заявки со статусом "Готово к выдаче" отсутствуют')

        else:

            await message.answer (
                'Готовые к выдаче:',
                reply_markup=create_kb_current_requests(ready_to_give)
            )