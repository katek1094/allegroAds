from offers_scraper import scrape_best_ids, scrape_account, scrape_ids_from_url

from UIVision import generate_json_script
from utils import get_all_accounts_from_excel

from agency_panel import scrape_planner

# generate_reports([acc.name for acc in get_all_accounts_from_excel()])


# a = False
# for account in scrape_accounts():
#     if account == 'Ecomi-screen':
#         a = True
#     if a:
#         scrape_account(account)+

# scrape_account('Mario_Store')

# a = scrape_best_ids('TopkKable', 'accuracy', 40)
# scrape_ids_from_url('https://allegro.pl/uzytkownik/handlowiec-rs-pl/spawarki-polautomaty-spawalnicze-306093?marka=Magnum', 10)

scrape_planner('szkło hartowane')
# format()

# generate_json_script('download_reports', get_all_accounts_from_excel())

# generate_json_script('last_month', get_all_accounts_from_excel())

# scrape_all_accounts(generate_accounts_list())

# scrape_account('Auto-od-A-do-Z')

# scrape_best_ids('TopkKable', 'accuracy', 20)

# r1 = Requirement('_BRUBECK_', 'sponsored', 'last_month', 'campaigns')
# r2 = Requirement('art-fotografia', 'sponsored', 'last_week', 'campaigns')
#
#
# # r3 = Requirement('Kaysershop', 'sponsored', 'yesterday', 'offers')
# # r4 = Requirement('Kaysershop', 'graphic', 'yesterday', 'groups')
# #
# #
# def scrape_stats(requirements):
#     driver = AgencyDriver()
#     for r in requirements:
#         scraper = find_scraper(driver, r)
#         print(scraper.scrape_stats())
#
#
# scrape_stats([r1, r2])

# run_budget_checker(get_accounts_from_excel(), BudgetCheckerModeChoices.current_billing_month)
