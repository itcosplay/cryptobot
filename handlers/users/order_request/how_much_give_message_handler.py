from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_smart_choose_curr

@dp.message_handler(state=Request.how_much_give)
async def set_how_much_give(message:types.Message, state:FSMContext):
    try:
        summ = float(message.text)
        await state.update_data(how_much_give=summ)
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
        request_data = await state.get_data()
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=create_kb_smart_choose_curr(request_data['currencies__give'])
        )    
        ### for logs ### delete later
        request_data = await state.get_data()
        print('=== state: ===')
        print(request_data)
        print('==============')
        ### for logs ### delete later

        await Request.currency__how_much__give.set()
        # currensy_for_how_much.py
    except Exception:
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено.'
        )
        await state.finish()
        await message.delete()