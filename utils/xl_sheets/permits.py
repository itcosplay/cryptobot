from datetime import datetime

from openpyxl import load_workbook

class DataPermits:
    def get_permit_data(self, request_numb):
        wb = load_workbook('permits.xlsx')
        sheet = wb['Лист1']

        request_numb = int(request_numb)
        last_row = 50 # max row in permit table

        for i in range(1, last_row):
            cell_obj = sheet.cell(row=i, column=1)
            if cell_obj.value == request_numb:

                return sheet.cell(row=i, column=2).value

        return False


    def update_permit_data(self, request_numb, new_permit_text):
        wb = load_workbook('permits.xlsx')
        sheet = wb['Лист1']
        # request_numb = int(request_numb)
        last_row = 50 # max row in permit table

        for i in range(1, last_row):
            cell_obj = sheet.cell(row=i, column=1)
            if cell_obj.value == request_numb:
                sheet.cell(row=i, column=2).value = new_permit_text
                wb.save('permits.xlsx')

                return True

        return False


    def write_new_permit(self, permit_id, permit_date, permit_text=''):
        permit_id = str(permit_id)

        if permit_text == '':
            permit_status = 'empty'
        else:
            permit_status = 'waiting'
        

        wb = load_workbook('permits.xlsx')
        sheet = wb['Лист1']

        last_row = 50

        for i in range(1, last_row):
            cell_obj = sheet.cell(row=i, column=1)
            if cell_obj.value == None:
                sheet.cell(row=i, column=1).value = permit_id
                sheet.cell(row=i, column=2).value = permit_text
                sheet.cell(row=i, column=3).value = permit_date
                sheet.cell(row=i, column=4).value = permit_status
                wb.save('permits.xlsx')

                return True

        return False


    def delete_permit(self, request_numb):
        wb = load_workbook('permits.xlsx')
        sheet = wb['Лист1']
        last_row = 50 # max row in permit table

        for i in range(1, last_row):
            cell_obj = sheet.cell(row=i, column=1)
            
            if cell_obj.value == request_numb:
                sheet.cell(row=i, column=1).value = ''
                sheet.cell(row=i, column=2).value = ''
                wb.save('permits.xlsx')

                return True

        return False


test = DataPermits()

test.write_new_permit(1234, '24.03')
# test.write_new_permit(permit_id=1234, permit_text='Аркадаг', permit_date='24.03')
