from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing


@dp.message_handler(state=Processing.sum_for_change)
async def set_sum_for_change(message:Message, state:FSMContext):
    try:
        new_sum = int(message.text)
        await state.update_data(sum_for_change=new_sum)
        
        await message.answer('Введена сумма: ', new_sum)

    except Exception as e:
        await message.answer('Формат суммы не правильный. Выход.')
        print(e)