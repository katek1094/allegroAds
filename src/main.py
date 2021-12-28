from offers_scraper import scrape_account, scrape_all_accounts, scrape_best_ids, scrape_ids_from_url
from src.utils import generate_accounts_list
from UIVision import generate_json_script
from agency_panel import StatsScraper

# generate_json_script('last_week', generate_accounts_list())

# generate_json_script('campaigns', generate_accounts_list())

# scrape_all_accounts(generate_accounts_list())

# scrape_account('wwwkoomputerypl')

# scrape_best_ids()

# scrape_ids_from_url()

scraper = StatsScraper([('art-fotografia', 'sponsored', 'last_week', 'offers'),
                        ('Kaysershop', 'sponsored', 'last_week', 'offers')])
print(scraper.stats)