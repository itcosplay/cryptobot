from aiohttp.client import request
import gspread
import datetime

from aiogram.dispatcher import FSMContext

from oauth2client.service_account import ServiceAccountCredentials


class SmsInfoSheet:
    def get_google_sheet(self):
        CREDENTIALS_FILE = 'sms.json'
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
        sheet = client.open("Данные с смс").sheet1  # test spreadsheet
        # sheet = client.open("test_bot_sheet").sheet1  # The real spreadsheet

        return sheet

    def check_sms(self, sms_numb):
        sheet = self.get_google_sheet()

        value = sheet.acell(f'A{sms_numb}').value
        if value == str(sms_numb):
            note = sheet.acell(f'M{sms_numb}').value

            return note
        else:

            return False

    def push_data(self, state):
        sheet = self.get_google_sheet()
        sms_numb = state['sms_numb']
        data_to_update = []

        who_waste = state['who_waste']
        data_to_update.append(who_waste)

        if not state['for_what_waste'] == '-':
            for_what_waste = state['for_what_waste']
        else:
            for_what_waste = ''

        data_to_update.append(for_what_waste)

        if not state['note_waste'] == '-':
            note_waste = state['note_waste']
            
        else:
            note_waste = ''

        data_to_update.append(note_waste)
        
        sheet.update(f'K{sms_numb}:M{sms_numb}', [data_to_update])

        operation_type = sheet.acell(f'H{sms_numb}').value
        card = sheet.acell(f'C{sms_numb}').value

        return operation_type, card, sms_numb, who_waste, for_what_waste, note_waste




# test = SmsInfoSheet()

# state = {'message_to_delete': 8334, 'sms_numb': '1995', 'for_what_waste': 'Посуда', 'note_waste': 'Ебаная заметка', 'who_waste': 'Личные Кэт'}
# print(test.push_data(state))
# print()