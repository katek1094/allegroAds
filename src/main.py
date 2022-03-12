from offers_scraper import scrape_best_ids, scrape_account, scrape_ids_from_url

from UIVision import generate_json_script, generate_macros_by_priority
from utils import get_all_accounts_from_excel

from agency_panel import scrape_planner

# scrape_account('account_name')

# a = scrape_best_ids('account_name', 'accuracy', 40)

# scrape_ids_from_url('url', offers_amount)

# scrape_planner('phrase')

# generate_macros_by_priority()

# generate_json_script('last_month', get_all_accounts_from_excel(priority=1), True)

# generate_reports([acc.name for acc in get_all_accounts_from_excel()], True)

# r1 = Requirement('account_name', 'sponsored', 'last_month', 'campaigns')
# r2 = Requirement('art-account_name', 'sponsored', 'last_week', 'campaigns')
#
#
# # r3 = Requirement('account_name', 'sponsored', 'yesterday', 'offers')
# # r4 = Requirement('account_name', 'graphic', 'yesterday', 'groups')
# #
# #
# def scrape_stats(requirements):
#     driver = AgencyDriver()
#     for r in requirements:
#         scraper = find_scraper(driver, r)
#         print(scraper.scrape_stats())
#
# scrape_stats([r1, r2])

# run_budget_checker(get_accounts_from_excel(), BudgetCheckerModeChoices.current_billing_month)
