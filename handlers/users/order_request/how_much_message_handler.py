from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp, bot
from states import Request


@dp.message_handler(state=Request.how_much)
async def set_how_much(message:types.Message, state:FSMContext):
    from keyboards.inline.request_kb import create_kb_choose_currency

    try:
        summ = float(message.text)
        await state.update_data(how_much=summ)
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )

        keyboard = create_kb_choose_currency()
        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=keyboard
        )    
        await Request.how_much_curr.set()
    except Exception:
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено.'
        )
        await state.finish()
        await message.delete()