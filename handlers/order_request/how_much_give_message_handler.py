from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_smart_choose_curr
from keyboards import main_menu


@dp.message_handler(state=Request.how_much_give)
async def set_how_much_give(message:types.Message, state:FSMContext):
    try:
        summ = int(message.text)
        await state.update_data(how_much_give=summ)
        data = await state.get_data()
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=data['_del_message']
        )
        request_data = await state.get_data()
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=create_kb_smart_choose_curr(request_data['currencies__give'])
            # reply_markup=create_kb_choose_currency()
        )    
        ### for logs ### delete later
        request_data = await state.get_data()
        print('=== state: ===')
        print(request_data)
        print('==============')
        ### for logs ### delete later

        await Request.currency__how_much__give.set()
        # currensy_for_how_much.py
    except Exception as e:
        print(e)
        print("EXEPTION HOW MACH GIVE")
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено\n====================================================',
            reply_markup=main_menu
        )
        await state.finish()
        await message.delete()