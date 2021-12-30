from offers_scraper import scrape_account, scrape_all_accounts, scrape_best_ids, scrape_ids_from_url
from src.utils import generate_accounts_list
from UIVision import generate_json_script
from agency_panel import scrape_stats, Requirement

# generate_json_script('last_week', generate_accounts_list())

# generate_json_script('campaigns', generate_accounts_list())

# scrape_all_accounts(generate_accounts_list())

# scrape_account('wwwkoomputerypl')

# scrape_best_ids()

# scrape_ids_from_url()


r = Requirement('veltini', 'sponsored', 'last_week', 'campaigns')

stats = scrape_stats(r)
print(stats)
