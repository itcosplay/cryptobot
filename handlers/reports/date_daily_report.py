import traceback

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import sticker
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_daily_report
from loader import dp, sheet, bot
from states import Reportsstate
from utils import get_value_for_reports
from utils import get_values_FGH


@dp.callback_query_handler(state=Reportsstate.date_daily_report)
async def show_daily_report(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_the_reports='+')

    result = await call.message.answer_sticker (
        sticker['go_to_table']
    )

    try:
        data = sheet.get_daily_report(call.data)

    except Exception as e:
        print(e)
        traceback.print_exception()

        await call.message.answer_sticker (
            sticker['not_connection']
        )
        await call.message.answer (
            text='Не удалось получить данные с гугл таблицы',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return


    await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

    date = data['date']
    deal_amount = data['deal_amount']

    deal_amount_text = f'За {date} сделок проведено: {deal_amount}\n'

    up_rub = data['up_rub']
    up_rub = get_value_for_reports(str(up_rub), 'rub')
    up_usd = data['up_usd']
    up_usd = get_value_for_reports(str(up_usd), 'usd')
    up_eur = data['up_eur']
    up_eur = get_value_for_reports(str(up_eur), 'eur')

    up_text = f'Из них пополнений: {up_rub}, {up_usd}, {up_eur}\n'

    down_rub = data['down_rub']
    down_rub = get_value_for_reports(str(down_rub), 'rub')
    down_usd = data['down_usd']
    down_usd = get_value_for_reports(str(down_usd), 'usd')
    down_eur = data['down_eur']
    down_eur = get_value_for_reports(str(down_eur), 'eur')

    down_text = f'Из них выдач на: {down_rub}, {down_usd}, {down_eur}\n\n'

    last_rub = data['last_rub']
    last_rub = get_value_for_reports(last_rub, 'rub')
    last_usd = data['last_usd']
    last_usd = get_value_for_reports(last_usd, 'usd')
    last_eur = data['last_eur']
    last_eur = get_value_for_reports(last_eur, 'eur')

    remain = f'Остаток VTL Change на конец дня: {last_rub}, {last_usd}, {last_eur}\n\n'

    requests_processing = data['requests_processing']
    requests_ready_to_give = data['requests_ready_to_give']

    if len(requests_processing) != 0:
        current_req = 'Текущие заявки:\n'

        for request in requests_processing:
            rub, usd, eur = get_values_FGH(request)
            if usd != '' or eur != '': rub = rub + ', '
            if eur != '': usd = usd + ', '
            if rub == ', ': rub = ''
            if usd == ', ': usd = ''
    
            request_date = request[0]
            request_numb = request[2]
            request_type = all_emoji[request[3]]
            current_req = current_req + f'{request_date} {request_type} {request_numb}\n     {rub}{usd}{eur}\n'
    else:
        current_req = ''

    if len(requests_ready_to_give) != 0:
            ready_req = 'Отложены к выдаче:\n'

            for request in requests_ready_to_give:
                rub, usd, eur = get_values_FGH(request)
                if usd != '' or eur != '': rub = rub + ', '
                if eur != '': usd = usd + ', '
                if rub == ', ': rub = ''
                if usd == ', ': usd = ''
        
                request_date = request[0]
                request_numb = request[2]
                request_type = all_emoji[request[3]]
                ready_req = ready_req + f'{request_date} {request_type} {request_numb}\n     {rub}{usd}{eur}\n'
    
    else:
        ready_req = ''

    if len(requests_processing) == 0 and len(requests_ready_to_give) == 0:
        requests = 'Все заявки исполненны\n'
    else:
        requests = '\n'

    replenishment = data['replenishment']
    replenishment = get_value_for_reports(replenishment, 'rub')

    repl_text = f'Пополнений на карты за {date}: {replenishment}\n\n'

    text = deal_amount_text + up_text + down_text + remain + repl_text  + current_req + requests + ready_req

    await state.update_data(daily_report_text=text)

    await call.message.answer (
        text = text,
        reply_markup=create_kb_daily_report()
    )

    await Reportsstate.finish_report.set()

    return


@dp.callback_query_handler(state=Reportsstate.finish_report)
async def finish_report(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(finish_report='+')

    if call.data == 'confirm':
        data_state = await state.get_data()
        text = data_state['daily_report_text']

        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return


    if call.data == 'raise_problem':
        result = await call.message.answer('Подробно изложите выявленные расхождения')
        await state.update_data(message_to_delete=result.message_id)

        await Reportsstate.text_problem.set()

        return


    if call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "Отчетность". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return