from aiohttp.client import request
import gspread
import datetime

from aiogram.dispatcher import FSMContext
# import pprint
from oauth2client.service_account import ServiceAccountCredentials

# Example of state
# state = {
#     'applicant': 'changer', 
#     'operation_type': 'cashin', # D --> 4
#     'type_of_card': 'sber',
#     'sum_RUB__how_much': '', 
#     'sum_USD__how_much': '500', 
#     'sum_EUR__how_much': '', 
#     'sum_recive_RUB': '', 
#     'sum_recive_USD': '', 
#     'sum_recive_EUR': '',
#     'sum_give_RUB': '',
#     'sum_give_USD': '', 
#     'sum_give_EUR': '', 
#     'currencies__how_much': ['rub'], 
#     'temp_sum_state': 500.0, 
#     'comment': 'тут какой-то коментарий', 
#     'permit': 'Аркадак Гурбангулы Махухуедов'
# }

# ['25.09', '7', '1549', 'Выдача в офисе', 'CHANGE', '50000', '', '', '', '', 'Andy', 'Исполнено', '-290500', '', '', '16:24']


class DataFromSheet:
    def get_google_sheet(self):
        CREDENTIALS_FILE = 'creds.json'
        scope = [
            "https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name (
            'creds.json',
            scope
        )
        client = gspread.authorize(creds)
        sheet = client.open("test_bot_sheet").sheet1  # Open the spreadhseet

        return sheet

    def get_balance_AEG3(self):
        sheet = self.get_google_sheet()
        A3 = sheet.acell('A3').value
        E3 = sheet.acell('E3').value
        G3 = sheet.acell('G3').value
        return A3, E3, G3

    def get_last_row(self):
        sheet = self.get_google_sheet()
        numb_of_last_row = len(sheet.col_values(1))
        last_row = sheet.get(f'A{numb_of_last_row}:Q{numb_of_last_row}')[0]

        return last_row

    def get_numbs_processing_and_ready_requests(self):
        '''return list of numb(str) of requests or empty list'''
        try:
            sheet = self.get_google_sheet()
            numb_of_last_row = len(sheet.col_values(1))
            data = sheet.batch_get([f'A{numb_of_last_row - 10}:Q{numb_of_last_row}'])[0] # 10 needs change to 30 or other

        except Exception as e:
            print(e)

            return 'exception'

        active_requests = []
        ready_requests = []

        for row in data:
            if row[11] == 'В обработке':
                request = []
                request.append(row[2]) # numb of request
                request.append(row[5]) # rub
                request.append(row[6]) # usd
                request.append(row[7]) # eur

                active_requests.append(request)

            if row[11] == 'Готово к выдаче':
                request = []
                request.append(row[2]) # numb of request
                request.append(row[5]) # rub
                request.append(row[6]) # usd
                request.append(row[7]) # eur
                
                ready_requests.append(request)

        return data, active_requests, ready_requests


def send_to_google(state): 
    sheet = get_google_sheet() 
    numb_of_last_row = len(sheet.col_values(1))
    # print(numb_of_last_row)
    last_row = sheet.get(f'A{numb_of_last_row}:Q{numb_of_last_row}')[0]

    A__current_date = datetime.datetime.today().strftime('%d.%m')

    if last_row[0] == A__current_date:
        B__numb_of_request_for_today = int(last_row[1]) + 1
    else:
        B__numb_of_request_for_today = 1

    C__id_of_request = int(datetime.datetime.today().strftime('%H%M'))
    
    if C__id_of_request == int(last_row[2]):
        C__id_of_request += 1

    C__id_of_request = str(C__id_of_request)
    C__id_of_request = C__id_of_request.zfill(4)

    translate_values_request = {
        'changer': 'change',
        'operator': 'оператор',
        'recive': 'прием кэша',
        'takeout': 'выдача в офисе',
        'delivery': 'доставка',
        'cashin': 'кэшин',
        'change': 'обмен',
        'cash_atm': 'снятие с карт',
        'alfa': 'альфа-банк',
        'sber': 'сбер',
        'rub': 'рубли',
        'usd': 'доллары',
        'eur': 'евро',
        'sum_plus': '',
        'sum_minus': '',
        'ok': ''
    }

    D__type_of_operation = translate_values_request[state['operation_type']]
    E__applicant = translate_values_request[state['applicant']]

    F__sum = '-'
    G__sum = '-'
    H__sum = '-'
    
    if not state['comment'] == '':
        I__comment = state['comment']
    else:
        I__comment = '-'
    
    if state['operation_type'] == 'recive': # sign +
        if state['sum_RUB__how_much'] != '':
            F__sum = int(state['sum_RUB__how_much'])
        if state['sum_USD__how_much'] != '':
            G__sum = int(state['sum_USD__how_much'])
        if state['sum_EUR__how_much'] != '':
            H__sum = int(state['sum_EUR__how_much'])

    elif state['operation_type'] == 'takeout' or state['operation_type'] == 'delivery': # sing -
        if state['sum_RUB__how_much'] != '':
            F__sum = 0 - int(state['sum_RUB__how_much'])
        if state['sum_USD__how_much'] != '':
            G__sum = 0 - int(state['sum_USD__how_much'])
        if state['sum_EUR__how_much'] != '':
            H__sum = 0 - int(state['sum_EUR__how_much'])

    elif state['operation_type'] == 'cashin': # sing -
        if state['type_of_card'] == 'alfa':
            I__comment = I__comment + '\n' + 'альфа-банк'
        if state['type_of_card'] == 'sber':
            I__comment = I__comment + '\n' + 'сбер'
        if state['sum_RUB__how_much'] != '':
            F__sum = 0 - int(state['sum_RUB__how_much'])
        if state['sum_USD__how_much'] != '':
            G__sum = 0 - int(state['sum_USD__how_much'])
        if state['sum_EUR__how_much'] != '':
            H__sum = 0 - int(state['sum_EUR__how_much'])

    elif state['operation_type'] == 'change': # sing +/-
        if state['sum_recive_RUB'] != '':
            F__sum = int(state['sum_recive_RUB'])
        if state['sum_recive_USD'] != '':
            G__sum = int(state['sum_recive_USD'])
        if state['sum_recive_EUR'] != '':
            H__sum = int(state['sum_recive_EUR'])
        # --- change --- #
        if state['sum_give_RUB'] != '':
            F__sum = 0 - int(state['sum_give_RUB'])
        if state['sum_give_USD'] != '':
            G__sum = 0 - int(state['sum_give_USD'])
        if state['sum_give_EUR'] != '':
            H__sum = 0 - int(state['sum_give_EUR'])    
    elif state['operation_type'] == 'cache_atm': # sing +
        pass

    J__remain = '-'
    K__executor = '-'
    L__status = 'В обработке'
    M__fact_RUB = '-'
    N__fact_USD = '-'
    O__fact_EUR = '-'
    P__end_time = '-'
    Q__total_blue = '-'
    
    inserRow = []
    inserRow.append(A__current_date)
    inserRow.append(B__numb_of_request_for_today)
    inserRow.append(C__id_of_request)
    inserRow.append(D__type_of_operation)
    inserRow.append(E__applicant)
    inserRow.append(F__sum)
    inserRow.append(G__sum)
    inserRow.append(H__sum)
    inserRow.append(I__comment)
    inserRow.append(J__remain)
    inserRow.append(K__executor)
    inserRow.append(L__status)
    inserRow.append(M__fact_RUB)
    inserRow.append(N__fact_USD)
    inserRow.append(O__fact_EUR)
    inserRow.append(P__end_time)
    inserRow.append(Q__total_blue)

    # number_of_empty_row = len(sheet.col_values(1)) + 1
    sheet.insert_row(inserRow, numb_of_last_row + 1)

    permit_data = state['permit']

    return C__id_of_request, permit_data


def get_google_sheet():
    CREDENTIALS_FILE = 'creds.json'
    scope = [
        "https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name (
        'creds.json',
        scope
    )
    client = gspread.authorize(creds)
    sheet = client.open("test_bot_sheet").sheet1  # Open the spreadhseet

    return sheet

