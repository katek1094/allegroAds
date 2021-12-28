from .account_scraper import AccountScraper
from .excel_writer import ExcelWriter


def scrape_account(username: str):
    scraper = AccountScraper(username)
    ExcelWriter(username, scraper.categories)


def scrape_all_accounts(accounts_names: iter):
    for count, account in enumerate(accounts_names):
        scrape_account(account)
        print(f'finished {count + 1}/{len(accounts_names)} accounts')
