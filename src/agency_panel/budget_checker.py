import datetime

from .agency_driver import AgencyDriver
from .stats_scraper import find_scraper, Requirement


class BudgetCheckerModeChoices:
    last_billing_month = 'last_billing_month'
    # last_week = 'last_week'
    current_billing_month = 'current_billing_month'
    last_month = 'last_month'


# class BudgetChecker:
#     billing_month_start_day = 26
#     month_days = 30
#
#     def __init__(self):
#         pass


def run_budget_checker(accounts, mode):
    driver = AgencyDriver()
    for account in accounts:
        r = Requirement(account.name, 'sponsored', mode, 'campaigns')
        scraper = find_scraper(driver, r)
        data = scraper.scrape_stats()
        costs = data['summary_stats']['cost']

        if account.is_graphic:
            r = Requirement(account.name, 'graphic', mode, 'campaigns')
            scraper = find_scraper(driver, r)
            data = scraper.scrape_stats()
            costs += data['summary_stats']['cost']

        if mode == BudgetCheckerModeChoices.last_month or mode == BudgetCheckerModeChoices.last_billing_month:
            is_overspend = account.monthly_budget < costs

        elif mode == BudgetCheckerModeChoices.current_billing_month:
            today = datetime.date.today()
            if 31 >= today.day >= 26:
                is_overspend = (((today.day - 25) / 30) * account.monthly_budget) < costs
            else:
                is_overspend = (((today.day + 4) / 30) * account.monthly_budget) < costs

        else:
            raise ValueError('budget checker choice not implemented')

        print(account.name, account.monthly_budget, costs)
        if is_overspend:
            print('OVERSPEND')
        print('')
