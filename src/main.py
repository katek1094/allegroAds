from offers_scraper import scrape_account
from agency_panel import scrape_planner


# scrape_planner('makrama')

# generate_json_script('last_month', generate_accounts_list())

# generate_json_script('campaigns', generate_accounts_list())

# scrape_all_accounts(generate_accounts_list())

scrape_account('NEUTREA')

# scrape_best_ids()

# scrape_ids_from_url()


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
