import gspread
from openpyxl import Workbook


def get_data_from_gsheets():
    if __name__ == '__main__':
        filename = 'service_credentials.json'
    else:
        filename = 'google_sheets/service_credentials.json'
    service_account = gspread.service_account(filename=filename)
    spreadsheet = service_account.open('AdsKajetan')
    worksheet = spreadsheet.worksheet('accounts')

    headers = worksheet.get('A1:G1')[0]
    accounts_data = worksheet.get('A3:G52')

    return headers, accounts_data


def update_local_excel_file(data):
    path = '/home/kajetan/Documents/pryzmat/accounts.xlsx'
    wb = Workbook()
    ws = wb.active

    headers, accounts_data = data
    ws.append(headers)
    ws.append([])
    for account_data in accounts_data:
        ws.append(account_data)

    wb.save(path)


def update_accounts_list():
    update_local_excel_file(get_data_from_gsheets())
