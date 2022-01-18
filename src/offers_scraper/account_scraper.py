import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .data_types import Offer, Category


class AccountScraper:
    MIN_SLEEP_TIME = 1
    MAX_SLEEP_TIME = 3
    ALLEGRO_URL = 'https://allegro.pl'

    categories: [Category]

    def __init__(self, username: str):
        self.ids = set()
        self.max_level = 0
        # noinspection PyArgumentList
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.minimize_window()

        print(f'scraping started on account {username}')

        self.categories = [Category(name="Wszystkie oferty", url=self.ALLEGRO_URL + '/uzytkownik/' + username,
                                    offers_amount=self.scrape_offers_amount(username), subcategories=[], offers=[],
                                    level=0)]

        _, _ = self.scrape_subcategories_tree(self.categories, 0)

        self.driver.close()
        print(f'scraping finished on account {username}')

    def update_ids(self, id_number: int):
        len_before = len(self.ids)
        self.ids.add(id_number)
        len_after = len(self.ids)
        first = '' if len_after == 1 else '\r'
        end = '\n' if len_after == self.categories[0].offers_amount else ''
        if len_after != len_before:
            print(first, f"scraped {len_after}/{self.categories[0].offers_amount} offers", sep='', end=end)

    def start_driver(self):
        # noinspection PyArgumentList
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.minimize_window()

    def sleep_time(self):
        time.sleep(random.randrange(self.MIN_SLEEP_TIME, self.MAX_SLEEP_TIME))  # to avoid allegro captcha ban

    def scrape_offers_amount(self, username) -> int:
        self.driver.get(self.ALLEGRO_URL + '/uzytkownik/' + username)
        attempts = 0
        while attempts < 3:
            try:
                soup = BeautifulSoup(self.driver.page_source, 'html5lib')
                user_info = soup.find('div', {'data-box-name': 'user info'})
                amount = int(user_info.find('span', {'data-role': 'counter-value'}).text.replace(' ', ''))
                return amount
            except AttributeError:
                print('DRIVER CLOSED')
                attempts += 1
                self.driver.close()
                self.start_driver()
                continue

    def scrape_subcategories_tree(self, categories: [Category], level):
        if level > self.max_level:
            self.max_level = level
        offers = []
        for category in categories:
            attempts = 0
            while attempts < 3:
                try:
                    self.driver.get(category.url)
                    self.sleep_time()
                    category.subcategories, category.offers = self.scrape_subcategories(self.driver.page_source,
                                                                                        level + 1)
                    if len(category.subcategories):
                        category.subcategories, category.offers = self.scrape_subcategories_tree(category.subcategories,
                                                                                                 level + 1)
                except AttributeError:
                    print('DRIVER CLOSED')
                    attempts += 1
                    self.driver.close()
                    self.start_driver()
                    continue
                break
            offers += category.offers
        return categories, offers

    def scrape_subcategories(self, page_source: str, level: int):
        """
        scrapes categories and offers (if there is not more nested categories) from a given page
        """
        soup = BeautifulSoup(page_source, 'html5lib')
        tags = soup.find('div', {'data-box-name': 'Categories'}).find('div', {'data-role': 'Categories'}).ul.contents
        subcategories = []
        offers = []
        for tag in tags:
            if not tag.div.a:  # if category do not have subcategories, scrape offers and break the loop
                offers = self.scrape_subcategory_offers(page_source)
                break
            else:  # scrape subcategories
                name = tag.div.a.text.strip()
                href = self.ALLEGRO_URL + tag.div.a['href']
                amount = int(tag.div.span.text)
                subcategories.append(
                    Category(name=name, url=href, offers_amount=amount, subcategories=[], offers=[], level=level))
        return subcategories, offers

    def scrape_subcategory_offers(self, page_source):
        offers = []
        source = page_source
        while source:
            page_offers, next_page_button = self.scrape_offers_from_page(source)
            offers += page_offers
            if next_page_button:
                self.driver.get(next_page_button['href'])
                self.sleep_time()
                source = self.driver.page_source
            else:
                source = False
        return offers

    def scrape_offers_from_page(self, page_source):
        soup = BeautifulSoup(page_source, 'html5lib')
        items_div = soup.find('div', {'data-box-name': 'items container'})
        offers_tags = items_div.findAll('article', {'data-role': 'offer'})
        offers = []
        for tag in offers_tags:
            price_tail = tag.find('span', class_='_qnmdr')
            tail = float(price_tail.text[:2])
            front = float(price_tail.previous_sibling[:-1].replace(" ", ''))
            price = front + tail / 100
            title = tag.findAll('a')[1].text
            link = tag.find('a')['href']
            try:
                id_number = int(tag.find('a')['href'].split('-')[-1].split('?')[0])
                self.update_ids(id_number)
                offers.append(Offer(id_number=id_number, price=price, title=title, link=link))
            except ValueError:
                print('passed offer - allegro lokalnie')
        next_page_button = soup.find('a', {'data-role': 'next-page'})
        return offers, next_page_button
