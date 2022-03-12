import openpyxl


class AdsAccount:
    def __init__(self, name: str, monthly_budget: int, revenue_target: int, priority: int, is_graphic: bool, ):
        self.name = name
        self.monthly_budget = monthly_budget
        self.revenue_target = revenue_target
        self.priority = priority
        self.is_graphic = is_graphic

    def __repr__(self):
        return self.name


def get_all_accounts_from_excel(*, priority: int = False):
    path = '/home/kajetan/Documents/pryzmat/accounts.xlsx'
    wb = openpyxl.load_workbook(path)
    ws = wb.active

    accounts_list = []

    row = 3
    col = 1

    while True:
        account_name = ws.cell(row=row, column=col).value
        account_monthly_budget = ws.cell(row=row, column=col + 1).value
        account_revenue_target = ws.cell(row=row, column=col + 2).value
        account_priority = ws.cell(row=row, column=col + 4).value
        account_is_graphic = ws.cell(row=row, column=col + 5).value == 'tak'
        if account_name:
            accounts_list.append(
                AdsAccount(account_name, account_monthly_budget, account_revenue_target, account_priority,
                           account_is_graphic))
            row += 1
        else:
            break

    if priority:
        return [account for account in accounts_list if account.priority == priority]
    else:
        return accounts_list
