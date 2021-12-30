from .agency_driver import AgencyDriver
from .stats_scraper import find_scraper, Requirement


def run_budget_checker(accounts):
    driver = AgencyDriver()
    for account in accounts:
        r = Requirement(account.name, 'sponsored', 'last_billing_month', 'campaigns')
        scraper = find_scraper(driver, r)
        data = scraper.scrape_stats()
        costs = data['summary_stats']['cost']

        if account.is_graphic:
            r = Requirement(account.name, 'graphic', 'last_billing_month', 'campaigns')
            scraper = find_scraper(driver, r)
            data = scraper.scrape_stats()
            costs += data['summary_stats']['cost']

        is_overspend = account.monthly_budget < costs

        print(account.name, account.monthly_budget, costs)
        if is_overspend:
            print('OVERSPEND')
        print('')
