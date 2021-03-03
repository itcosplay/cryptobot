import gspread
import datetime
# import pprint
from oauth2client.service_account import ServiceAccountCredentials

# Example of state
state = {
    'applicant': 'changer', 
    'operation_type': 'recive', # D --> 4
    'type_of_card': '',
    'sum_RUB__how_much': 500.0, 
    'sum_USD__how_much': '', 
    'sum_EUR__how_much': '', 
    'sum_recive_RUB': '', 
    'sum_recive_USD': '', 
    'sum_recive_EUR': '',
    'sum_give_RUB': '',
    'sum_give_USD': '', 
    'sum_give_EUR': '', 
    'currencies__how_much': ['rub'], 
    'temp_sum_state': 500.0, 
    'comment': 'тут какой-то коментарий', 
    'permit': 'Аркадак Гурбангулы Махухуедов'
}

# ['25.09', '7', '1549', 'Выдача в офисе', 'CHANGE', '50000', '', '', '', '', 'Andy', 'Исполнено', '-290500', '', '', '16:24']


def send_to_google(): 
    sheet = get_google_sheet() 
    numb_of_last_row = len(sheet.col_values(1))
    print(numb_of_last_row)
    # last_row = sheet.get(f'A{numb_of_last_row}:Q{numb_of_last_row}')[0]

    # A__current_date = datetime.datetime.today().strftime('%d.%m')

    # if last_row[0] == A__current_date:
    #     B__numb_of_request_for_today = int(last_row[1]) + 1
    # else:
    #     B__numb_of_request_for_today = 1

    # C__id_of_request = datetime.datetime.today().strftime('%h.%M')
    # print(B__numb_of_request_for_today)




    # insertRow.append(A__current_date)
    # insertRow.append(B__numb_of_request_for_today)




    
    # number_of_empty_row = len(sheet.col_values(1)) + 1
    # sheet.insert_row(insertRow, number_of_empty_row)
    # data = sheet.get_all_records()

    # pprint(data)

    # data = sheet.col_values(1)
    # pprint(data)
    # print(len(data))





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


send_to_google()