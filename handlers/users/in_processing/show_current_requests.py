from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, sheet
from filters import isExecutor_and_higher
from states import Processing

from keyboards import create_kb_current_requests


@dp.message_handler(isExecutor_and_higher(), text='в работе')
async def show_current_requests(message:Message, state:FSMContext):
    '''
    Обрабатывает команду "в работе" и отображает список текущих
    заявок в виде кнопок с номером и суммами. Если текущих заявок
    нет, то отвечает - "Все заявки исполненны."
    '''
    try:
        current_requests,\
        in_processing_requests,\
        ready_to_give_requests = \
        sheet.get_numbs_processing_and_ready_requests()      

    except Exception as e:
        print(e)
        await message.answer('Не удалось получить данные с гугл таблицы :(')

        return

    await state.update_data(current_requests=current_requests)
    
    if len(in_processing_requests) == 0 and len(ready_to_give_requests) == 0:
        await message.delete()
        await message.answer('Все заявки исполненны.')
        await state.finish()
        
    else:
        await message.delete()
        await message.answer (
            'Текущие заявки:',
            reply_markup=create_kb_current_requests (
                in_processing_requests,
                ready_to_give_requests
            )
        )
        # await Processing.chosen_request.set()
        # to show_chosen_requests.py
        