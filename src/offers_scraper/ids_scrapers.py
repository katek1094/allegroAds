from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class IdsScraper:
    allegro_url = 'https://allegro.pl'
    target_amount = 0
    ids = []

    def __init__(self, target_amount):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.target_amount = target_amount

    def get_offers_ids(self):
        finished = False
        while not finished:
            ids, next_page_button = self.get_ids_from_page(self.target_amount - len(self.ids))
            self.ids += ids
            finished = len(self.ids) == self.target_amount or not next_page_button

    def get_ids_from_page(self, limit):
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        items_div = soup.find('div', {'data-box-name': 'items container'})
        offers = items_div.findAll('article', {'data-role': 'offer'})[:limit]
        ids = []
        for offer in offers:
            ids.append(int(offer.find('a')['href'].split('-')[-1].split('?')[0]))
        next_page_button = soup.find('a', {'data-role': 'next-page'})
        if next_page_button:
            time.sleep(0.3)
            self.driver.get(next_page_button['href'])
        return ids, next_page_button


class BestOffersScraper(IdsScraper):
    modes = ('accuracy', 'popularity')

    def __init__(self, username, mode, target_amount):
        super().__init__(target_amount)
        if mode not in self.modes:
            print('ERROR: unkown mode!')
            return
        elif mode == self.modes[0]:
            self.driver.get(self.allegro_url + '/uzytkownik/' + username)
        elif mode == self.modes[1]:
            self.driver.get(self.allegro_url + '/uzytkownik/' + username + '?order=qd')

        self.get_offers_ids()
        if self.target_amount > len(self.ids):
            print('target amount was bigger than amount of offers to scrape!')
        print('scraping finished')
        print(self.ids)
        self.driver.close()


class UrlIdsScraper(IdsScraper):
    def __init__(self, url, target_amount):
        super().__init__(target_amount)
        self.driver.get(url)
        self.get_offers_ids()
        if self.target_amount > len(self.ids):
            print('target amount was bigger than amount of offers to scrape!')
        print('scraping finished')
        print(self.ids)
        self.driver.close()