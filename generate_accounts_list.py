import openpyxl


def generate_accounts_list():
    path = '/home/kajetan/Documents/pryzmat/accounts.xlsx'
    wb = openpyxl.load_workbook(path)
    ws = wb.active

    accounts_list = []

    row = 3
    col = 1
    while True:
        value = ws.cell(row=row, column=col).value
        if value:
            accounts_list.append(value)
            row += 1
        else:
            break
    return accounts_list
