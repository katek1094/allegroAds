from .account_scraper import AccountScraper
from .excel_writer import ExcelWriter
from .ids_scrapers import BestOffersScraper, UrlIdsScraper


def scrape_account(username: str):
    scraper = AccountScraper(username)
    ExcelWriter(username, scraper.categories)


def scrape_all_accounts(accounts_names: iter):
    for count, account in enumerate(accounts_names):
        scrape_account(account)
        print(f'finished {count + 1}/{len(accounts_names)} accounts')


def scrape_best_ids(username: str, mode: str, target_amount: int):
    return BestOffersScraper(username, mode, target_amount).ids


def scrape_ids_from_url(url: str, target_amount: int):
    return UrlIdsScraper(url, target_amount).ids

