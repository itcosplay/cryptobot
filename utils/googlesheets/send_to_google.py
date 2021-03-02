import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


def send_to_google():
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

    # data = sheet.get_all_records()

    # pprint(data)

    data = sheet.col_values(1)
    pprint(data)
    print(len(data))
