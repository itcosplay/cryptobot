import datetime
import gspread
from operator import itemgetter



from oauth2client.service_account import ServiceAccountCredentials


class DataFromSheet:
    # def get_google_sheet(self):
    #     CREDENTIALS_FILE = 'creds.json'
    #     scope = [
    #         "https://spreadsheets.google.com/feeds",
    #         'https://www.googleapis.com/auth/spreadsheets',
    #         "https://www.googleapis.com/auth/drive.file",
    #         "https://www.googleapis.com/auth/drive"
    #     ]
    #     creds = ServiceAccountCredentials.from_json_keyfile_name (
    #         'creds.json',
    #         scope
    #     )
    #     client = gspread.authorize(creds)
    #     sheet = client.open("test_bot_sheet").sheet1  # test spreadsheet
    #     # sheet = client.open("test_bot_sheet").sheet1  # The real spreadsheet

    #     return sheet
        

    def get_google_sheet(self):
        CREDENTIALS_FILE = 'creds.json'
        scope = [
            "https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name (
            'sms.json',
            scope
        )
        client = gspread.authorize(creds)
        # sheet = client.open("test_bot_sheet").sheet1  # test spreadsheet
        # sheet = client.open("test_bot_sheet").sheet1  # The real spreadsheet
        sheet = client.open("VTL учёт").sheet1

        return sheet

    def get_google_sheet_card_balance(self):
        CREDENTIALS_FILE = 'creds.json'
        scope = [
            "https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name (
            'sms.json',
            scope
        )
        client = gspread.authorize(creds)
        # sheet = client.open("test_bot_sheet").sheet1  # test spreadsheet
        # sheet = client.open("test_bot_sheet").sheet1  # The real spreadsheet
        sheet = client.open("Учёт Оператора").sheet1

        return sheet

    def get_balance_AEG3(self):
        sheet = self.get_google_sheet()
        A3 = sheet.acell('A3').value
        E3 = sheet.acell('E3').value
        G3 = sheet.acell('G3').value
        return A3, E3, G3

    def get_balance_DFI3Q4(self):
        sheet = self.get_google_sheet()
        D3 = sheet.acell('D3').value
        F3 = sheet.acell('F3').value
        I3 = sheet.acell('I3').value
        Q4 = sheet.acell('Q4').value

        return D3, F3, I3, Q4

    def get_large_data(self):
        sheet = self.get_google_sheet()
        numb_of_last_row = len(sheet.col_values(1))
        data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}', 'A3', 'E3', 'G3', 'D3', 'F3', 'I3', 'Q4']) # 20 needs change to 30 or other
        A3 = data[1][0][0]
        E3 = data[2][0][0]
        G3 = data[3][0][0]
        D3 = data[4][0][0]
        F3 = data[5][0][0]
        I3 = data[6][0][0]
        Q4 = data[7][0][0]
        data = data[0]
        return data, A3, E3, G3, D3, F3, I3, Q4

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
            data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}'])[0] # 20 needs change to 30 or other

        except Exception as e:
            print(e)

            return 'exception'

        active_requests = []
        ready_requests = []

        for row in data:
            if row[11] == 'В обработке':
                # request = []
                # request.append(row[2]) # numb of request
                # request.append(row[5]) # rub
                # request.append(row[6]) # usd
                # request.append(row[7]) # eur

                active_requests.append(row)

            if row[11] == 'Готово к выдаче':
                # request = []
                # request.append(row[2]) # numb of request
                # request.append(row[5]) # rub
                # request.append(row[6]) # usd
                # request.append(row[7]) # eur
                
                ready_requests.append(row)

        return data, active_requests, ready_requests

    def replace_row(self, request):
        '''find row and replace'''
        if not request[5] == '0':
            request[5] = int(request[5])

        if not request[6] == '0':
            request[6] = int(request[6])

        if not request[7] == '0':
            request[7] = int(request[7])

        if not request[12] == '0':
            request[12] = int(request[12])

        if not request[13] == '0':
            request[13] = int(request[13])
            
        if not request[14] == '0':
            request[14] = int(request[14])

        if not request[16] == '0':
            request[16] = int(request[16])

        try:
            sheet = self.get_google_sheet()
            numb_of_last_row = len(sheet.col_values(1))
            data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}'])[0] # 20 needs change to 30 or other

        except Exception as e:
            print(e)

            return e
        
        index = numb_of_last_row - 30 - 1 # 20 needs change to 30 or other

        for row in data:
            index += 1
            
            if row[2] == request[2]:
                # ['14.04', '20', '1300', 'прием кэша', 'change', '0', 5000, 7000, '0', '0', 'itcosplay', 'В обработке', '0', '0', '0', '0', '0']
                # print(request)
                # print(index)
                sheet.update(f'A{index}:Q{index}', [request])
                # sheet.delete_rows(index)
                # sheet.insert_row(request, index)

                return
            
    def update_id_row(self, old_id, new_id):
        try:
            sheet = self.get_google_sheet()
            numb_of_last_row = len(sheet.col_values(1))
            data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}'])[0] # 20 needs change to 30 or other

        except Exception as e:
            print(e)

            return e
        
        index = numb_of_last_row - 30 - 1 # 20 needs change to 30 or other

        for row in data:
            index += 1
            
            if row[2] == old_id:
                new_id = int(new_id)
                sheet.update_cell(index, 3, new_id)

                return
    
    def get_request_by_id(self, request_id):
        try:
            sheet = self.get_google_sheet()
            numb_of_last_row = len(sheet.col_values(1))
            data = sheet.batch_get([f'A{numb_of_last_row - 20}:Q{numb_of_last_row}'])[0] # 20 needs change to 30 or other

        except Exception as e:
            print(e)

            return e
        
        index = numb_of_last_row - 30 - 1 # 20 needs change to 30 or other

        for row in data:
            index += 1
            
            if row[2] == request_id:

                return row

    def get_balances_with_request(self):
        # sheet = self.get_google_sheet()
        # numb_of_last_row = len(sheet.col_values(1))
        # data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}'])[0]
        # A3, E3, G3 = self.get_balance_AEG3()
        # D3, F3, I3, Q4 = self.get_balance_DFI3Q4()
        data, A3, E3, G3, D3, F3, I3, Q4 = self.get_large_data()

        A3 = int(A3)
        E3 = int(E3)
        G3 = int(G3)
        # datetime.datetime.today().strftime('%H%M')
        # current_date = datetime.datetime.today().strftime('%d.%m')
        current_date = datetime.datetime.today().strftime('%d.%m')
        current_date = datetime.datetime.strptime(current_date, '%d.%m')
        # current_year = datetime.datetime.today().strftime('%Y')
        # tomorrow_date =  (ddatetime.atetime.now() + ddatetime.timedelta(days=1)).strftime("%d.%m")
        # after_tomorrow_date = (ddatetime.datetime.now() + ddatetime.timedelta(days=2)).strftime("%d.%m")
        # d1 = datetime.strptime("01.02.2017", "%d.%m.%Y")
        # d2 = datetime.strptime("01.03.2017", "%d.%m.%Y")
        # print (d2 - d1).days
        future_requests = 0

        for row in data:
            request_date = row[0]
            request_date = datetime.datetime.strptime(request_date, '%d.%m')
            delta_days = (request_date - current_date).days
            
            if delta_days >= 1 or delta_days == -364:
                future_requests += 1
                A3 = A3 - int(row[5])
                E3 = E3 - int(row[6])
                G3 = G3 - int(row[7])
        
        print('we_are_here')

        return A3, E3, G3, future_requests, D3, F3, I3, Q4
    
    def get_card_balances(self):
        sheet = self.get_google_sheet_card_balance()
        data = sheet.batch_get(['B5:B8'])[0]

        C1A = data[0][0]
        C1A = C1A.replace(',', '.')

        C1T = data[1][0]
        C1T = C1T.replace(',', '.')

        C1D = data[2][0]
        C1D = C1D.replace(',', '.')

        S1V = data[3][0]
        S1V = S1V.replace(',', '.')

        total = float(C1A) + float(C1T) + float(C1D) + float(S1V)

        return C1A, C1T, C1D, S1V, total

    def sort_table_data(self):
        sheet = self.get_google_sheet()
        numb_of_last_row = len(sheet.col_values(1))
        data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}'])[0] # 20 needs change to 30 or other
        
        new_data = []

        for row in data:
            if row[11] == 'Исполнено' or row[11] == 'Отменена':
                new_data.append(row)

        for row in data:
            if row[11] == 'Готово к выдаче':
                new_data.append(row)

        data_sord_date = []

        for row in data:
            if row[11] == 'В обработке':
                data_sord_date.append(row)
        
        data_sord_date.sort(key=itemgetter(0))

        new_data = new_data + data_sord_date

        sheet.update(f'A{numb_of_last_row - 30}:Q{numb_of_last_row}', new_data) # 20 needs change to 30 or other

        return

    def send_to_google(self, state, creator_name):
        sheet = self.get_google_sheet() 
        numb_of_last_row = len(sheet.col_values(1))
        # print(numb_of_last_row)
        last_row = sheet.get(f'A{numb_of_last_row}:Q{numb_of_last_row}')[0]

        A__current_date = state['data_request']

        if last_row[0] == A__current_date:
            B__numb_of_request_for_today = int(last_row[1]) + 1
        else:
            B__numb_of_request_for_today = 1

        C__id_of_request = int(datetime.datetime.today().strftime('%H%M'))

        if numb_of_last_row - 40 <= 6:
            low_value_row = 6

        else:
            low_value_row = numb_of_last_row - 40
        
        last_20_ids = sheet.get(f'C{low_value_row}:C{numb_of_last_row}')
        last_20_ids = sum(last_20_ids, [])
        limit_while = 1

        while True:
            if str(C__id_of_request) in last_20_ids:
                C__id_of_request -= 1
                limit_while += 1
            
            else:

                break

            if limit_while == 50:

                return False

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

        F__sum = '0'
        G__sum = '0'
        H__sum = '0'
        
        if not state['comment'] == '':
            I__comment = state['comment']
        else:
            I__comment = '0'
        
        if state['operation_type'] == 'recive' or state['operation_type'] == 'cash_atm': # sign +
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
        # elif state['operation_type'] == 'cache_atm': # sing +
        #     pass

        J__remain = '0'
        K__executor = creator_name
        L__status = 'В обработке'
        M__fact_RUB = '0'
        N__fact_USD = '0'
        O__fact_EUR = '0'
        P__end_time = '0'
        Q__total_blue = '0'
        
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
        # print(inserRow)
        # sheet.insert_row(inserRow, numb_of_last_row + 1)
        numb_empty_row = numb_of_last_row + 1
        sheet.update(f'A{numb_empty_row}:Q{numb_empty_row}', [inserRow])

        self.sort_table_data()

        permit_text = state['permit']

        return C__id_of_request, permit_text, inserRow

    def get_last_30_id(self):
        '''
        Returns last 30 id like a list of string numbers
        '''
        sheet = self.get_google_sheet()
        numb_of_last_row = len(sheet.col_values(1))

        if numb_of_last_row - 30 <= 6:
            low_value_row = 6

        else:
            low_value_row = numb_of_last_row - 40

        last_30_id = sheet.get(f'C{low_value_row}:C{numb_of_last_row}')
        last_30_id = sum(last_30_id, [])

        return last_30_id
    
    def get_ready_to_give_requests(self):
        sheet = self.get_google_sheet()
        numb_of_last_row = len(sheet.col_values(1))
        data = sheet.batch_get([f'A{numb_of_last_row - 30}:Q{numb_of_last_row}'])[0] # 20 needs change to 30 or other

        ready_to_give_request = []

        for row in data:
            if row[11] == 'Готово к выдаче':
                ready_to_give_request.append(row)

        if len(ready_to_give_request) != 0:

            return ready_to_give_request
        
        else:

            return False

# def get_google_sheet():
#     CREDENTIALS_FILE = 'creds.json'
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         'https://www.googleapis.com/auth/spreadsheets',
#         "https://www.googleapis.com/auth/drive.file",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name (
#         'creds.json',
#         scope
#     )
#     client = gspread.authorize(creds)
#     sheet = client.open("test_bot_sheet").sheet1  # Open the spreadhseet

#     return sheet


# def get_google_sheet():
#     CREDENTIALS_FILE = 'sms.json'
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         'https://www.googleapis.com/auth/spreadsheets',
#         "https://www.googleapis.com/auth/drive.file",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name (
#         'sms.json',
#         scope
#     )
#     client = gspread.authorize(creds)
#     sheet = client.open("VTL учёт").sheet1  # Open the spreadhseet

#     return sheet



# test_sheet = DataFromSheet()