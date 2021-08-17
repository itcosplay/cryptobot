from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing

from keyboards import cb_current_requests
# from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_chosen_request
from utils import get_data_chosen_request

# <--- current_requests.py --->
# @dp.callback_query_handler(cb_current_requests.filter(type_btn='get_request'))
@dp.callback_query_handler(state=Processing.chosen_request)
async def show_chosen_request(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает нажатие на одну из заявок, выведенных списком
    '''
    await call.answer()
    await call.message.delete()

    data_btn = cb_current_requests.parse(call.data)

    if data_btn['type_btn'] == 'exit':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    current_requests = data_state['current_requests']

    for request in current_requests:

        if data_btn['id'] == request[1]:
            await state.update_data(chosen_request=request)

            break

    data_state = await state.get_data()
    request = data_state['chosen_request']
    text = get_data_chosen_request(request)
    
    await call.message.answer (
        text=text,
        reply_markup=create_kb_chosen_request(request)
        # > отложить на выдачу (для доставки, кэшина, обмена)
        # > принято частично (для приема кэша, снятия с карт, обмена)
        # > закрыть заявку
        # > сообщение
        # > изменить заявку
        # > добавить пропуск
        # > добавить комментарий
        # > распаковать
        # > отменить заявку
        # > назад
        # > главное меню
    )

    await Processing.enter_chosen_request_menu.set()

    return
    