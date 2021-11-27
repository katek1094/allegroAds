from offers_scraper.account_scraper import AccountScraper
from offers_scraper.excel_writer import ExcelWriter
from generate_accounts_list import generate_accounts_list


def scrape_account(username):
    account_scraper = AccountScraper(username)
    ExcelWriter(username, account_scraper.categories)


def scrape_all_accounts():
    accounts = generate_accounts_list()[17:]
    count = 0
    for account in accounts:
        scrape_account(account)
        count += 1
        print(f'finished {count}/{len(accounts)} accounts')


scrape_all_accounts()
