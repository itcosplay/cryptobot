from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import isExecutor_and_higher
from loader import dp, sheet
from keyboards import create_kb_current_requests
from states import Processing

@dp.message_handler(isExecutor_and_higher(), text='в работе')
async def inter_to_processing(message:types.Message, state:FSMContext):
    current_requests, processing_req, ready_req = sheet.get_numbs_processing_and_ready_requests()

    await state.update_data(current_requests=current_requests)
    
    if len(processing_req) == 0 and len(ready_req) == 0:
        await message.answer('Все заявки исполненны.')
        await message.delete()
    else:
        await message.answer (
            'Актуальные заявки:',
            reply_markup=create_kb_current_requests(processing_req, ready_req)
        )
        await message.delete()