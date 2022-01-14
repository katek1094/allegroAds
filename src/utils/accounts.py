import openpyxl


class AdsAccount:
    def __init__(self, name: str, is_graphic: bool, monthly_budget: int, revenue_target: int):
        self.name = name
        self.is_graphic = is_graphic
        self.monthly_budget = monthly_budget
        self.revenue_target = revenue_target


def get_all_accounts_from_excel():
    path = '/home/kajetan/Documents/pryzmat/accounts.xlsx'
    wb = openpyxl.load_workbook(path)
    ws = wb.active

    accounts_list = []

    row = 3
    col = 1

    while True:
        name = ws.cell(row=row, column=col).value
        monthly_budget = ws.cell(row=row, column=col + 1).value
        revenue_target = ws.cell(row=row, column=col + 2).value
        is_graphic = ws.cell(row=row, column=col + 3).value == 'tak'
        if name:
            accounts_list.append(AdsAccount(name, monthly_budget, revenue_target, is_graphic))
            row += 1
        else:
            break
    return accounts_list
