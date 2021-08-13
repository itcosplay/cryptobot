import traceback

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from data import sticker
from loader import dp, sheet, bot
from filters import isExecutor_and_higher
from states import Processing

from keyboards import create_kb_current_requests
from keyboards import create_kb_coustom_main_menu
# from keyboards import main_menu

# from 'в работе' main_menu
@dp.message_handler(isExecutor_and_higher(), text='в работе')
async def show_current_requests(message:Message, state:FSMContext):
    '''
    Обрабатывает команду (button) "в работе" и отображает список текущих
    заявок в виде кнопок с номером и суммами. Если текущих заявок
    нет, то отвечает - "Все заявки исполненны."
    '''
    await message.delete()

    result = await message.answer_sticker (
        sticker['go_to_table'],
        reply_markup=ReplyKeyboardRemove()
    )

    try:
        current_requests,\
        in_processing_requests,\
        ready_to_give_requests =\
        sheet.get_numbs_processing_and_ready_requests()

    except Exception as e:
        traceback.print_exc()

        await message.answer_sticker (
            sticker['not_connection']
        )

        await message.answer (
            text='Не удалось получить данные с гугл таблицы',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        await state.finish()

        return

    await bot.delete_message (
        chat_id=message.chat.id, message_id=result.message_id
    )

    await state.update_data(current_requests=current_requests)

    if len(in_processing_requests) == 0 and len(ready_to_give_requests) == 0:

        await message.answer (
            text='Все заявки исполненны.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        await state.finish()
        
    else:

        await message.answer (
            'Текущие заявки:',

            reply_markup=create_kb_current_requests (
                in_processing_requests,
                ready_to_give_requests
            )

        )
        
        await Processing.chosen_request.set()
        