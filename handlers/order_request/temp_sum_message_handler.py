from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp.client import request
from dotenv import main

from loader import dp, bot
from states import Request
from keyboards import create_kb_smart_choose_curr
# from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu

# from operation_type.py
@dp.message_handler(state=Request.temp_sum_state)
async def set_how_much(message:types.Message, state:FSMContext):
    try:
        summ = int(message.text)
        await state.update_data(temp_sum_state=summ)

        request_data = await state.get_data()
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=request_data['_del_message']
        )
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )

        await message.answer (
            f'Выберете валюту:',
            reply_markup=create_kb_smart_choose_curr(request_data['currencies__how_much'])
        )
    
    
        operation_type = request_data['operation_type']
        print('WE ARE HERE 0000000')

        if \
        operation_type == 'get_in' or \
        operation_type == 'get_out' or \
        operation_type == 'cash_in_ATM' or operation_type == 'cash_out_ATM':
            print('WE ARE HERE')
            await Request.currencies__how_much.set()
            # to currency__how_much.py

    # if operation_type == 'change':
    #     request_data = await state.get_data()
    #     if len(request_data['currencies__recive']) != 0:


    #     await Request.currency__how_much__recive.set()
    #     # to currency__how_much__recive.py

    #     await Request.currency__how_much__recive.set()
    #     # to currency__how_much__recive.py
    
        ### for logs ### delete later
        request_data = await state.get_data()
        print('=== state: ===')
        print(request_data)
        print('==============')
        ### for logs ### delete later

    except Exception as e:
        print(e)
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено\n===========',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        await message.delete()