from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup

from .agency_driver import AgencyDriver
from .stats import SponsoredOfferStats

sponsored_labels = ['clicks', 'views', 'CTR', 'avg CPC', 'cost', 'return', 'interest', 'pcs sold ', 'sales value']
graphic_labels = ['clicks', 'views', 'CTR', 'avg CPM', 'cost', 'return', 'range', 'interest', 'assisted sale',
                  'pcs sold ', 'sales value']

ads_types = ('sponsored', 'graphic')

date_ranges = {
    'yesterday': 'Wczoraj',
    'today': 'Dzisiaj',
    'last_week': 'Ostatnie 7 dni',
    'last_month': 'Ostatnie 30 dni',
    'last_billing_month': 'Poprzedni okres rozliczeniowy',
    'current_billing_month': 'Bieżący okres rozliczeniowy',
}

detail_levels = ('campaigns', 'groups', 'offers', 'ads')


class Requirement:
    username = None
    ads_type = None
    date_range = None
    detail_level = None

    def __init__(self, username: str, ads_type: str, date_range: str, detail_level: str):
        self.username = username
        self.ads_type = ads_type
        self.date_range = date_range
        self.detail_level = detail_level

        self.validate_arguments()

    def validate_arguments(self):
        if self.ads_type not in ads_types:
            raise ValueError(f'unknown ads type "{self.ads_type}"! please select one from the following: {ads_types}')
        if self.date_range not in date_ranges.keys():
            raise ValueError(
                f'unknown date range "{self.date_range}"! please select one from the following: {date_ranges.keys()}')
        if self.detail_level not in detail_levels:
            raise ValueError(
                f'unknown detail level "{self.detail_level}"! please select one from the following: {detail_levels}')
        if self.ads_type == 'sponsored' and self.detail_level == 'ads':
            raise ValueError('sponsored ads do not have "ads" detail level')
        if self.ads_type == 'graphic' and self.detail_level == 'offers':
            raise ValueError('graphic ads do not have "offers" detail level')


class GenericStatsScraper(ABC):
    def __init__(self, driver: AgencyDriver, requirement: Requirement):
        super().__init__()

        self.driver = driver
        self.requirement = requirement

    def scrape_stats(self):
        self.open_client_and_stats()
        self.set_ads_type()
        self.set_date_range()
        self.set_detail_level()

        self.scrape_data_from_page()
        self.open_clients_list()

        return self.formatted_data()

    def open_client_and_stats(self):
        self.driver.click((By.XPATH, f"//*[text()='{self.requirement.username}']"))
        self.driver.click((By.LINK_TEXT, 'Statystyki'))

    def open_clients_list(self):
        self.driver.click((By.LINK_TEXT, self.requirement.username))

    @abstractmethod
    def set_ads_type(self):
        pass

    def set_date_range(self):
        self.driver.click((By.CSS_SELECTOR, 'div[title="Zmień zakres dat"]'))
        self.driver.click((By.XPATH, f"//*[text()='{date_ranges[self.requirement.date_range]}']"))
        self.driver.click((By.XPATH, "//*[text()='Aktualizuj']"))

    def set_detail_level(self):
        detail_level = self.requirement.detail_level
        if detail_level == 'groups':
            self.driver.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[1]/div/div[2]/button'))
        elif detail_level == 'offers' or detail_level == 'ads':
            self.driver.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[1]/div/div[3]/button'))

    def scrape_data_from_page(self, index=1):
        self.driver.sleep(.1)  # without sleep time amount of scraped offers is smaller - probably due to loading
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')

        self.scrape_names_table(soup)
        self.scrape_values_table(soup, index == 1)

        is_next_page = soup.find('span', text='następna')
        if is_next_page:
            try:
                self.driver.click((By.CSS_SELECTOR, 'button[aria-label="następna strona"]'))
                self.scrape_data_from_page(index + 1)
            except ElementNotInteractableException:  # button is always in html, but hidden and disabled
                pass

    @abstractmethod
    def scrape_names_table(self, soup):
        pass

    @abstractmethod
    def scrape_values_table(self, soup, is_first_page):
        pass

    @abstractmethod
    def formatted_data(self):
        pass


class SponsoredScraperMixin:
    driver: AgencyDriver
    stats_values = []

    def set_ads_type(self):
        pass


class GraphicScraperMixin:
    driver: AgencyDriver

    def set_ads_type(self):
        self.driver.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[1]/div[1]/div/div/a[2]'))


class SponsoredOffersScraper(SponsoredScraperMixin, GenericStatsScraper):
    offers_names = []
    groups_names = []
    campaigns_names = []
    offers_ids = []

    def scrape_names_table(self, soup):
        names_table_body = soup.findAll("table")[0].find('tbody')
        self.offers_names.extend([link.text for link in names_table_body.findAll('a')[::3]])
        self.groups_names.extend([link['title'] for link in names_table_body.findAll('a')[2::3]])
        self.campaigns_names.extend([link['title'] for link in names_table_body.findAll('a')[1::3]])
        self.offers_ids.extend([link['href'].split('/')[-1] for link in names_table_body.findAll('a')[::3]])

    def scrape_values_table(self, soup, is_first_page):
        values_table_body = soup.findAll("table")[1].find('tbody')
        trs = values_table_body.findAll('tr')
        if is_first_page:
            trs = trs[1:]  # first row is summary stats

        for index in range(len(trs)):
            tds = trs[index].findAll('td')
            values = []
            for td in tds:
                value = float(
                    td.text.replace(" ", "").replace("%", "").replace("zł", "").replace(",", ".").replace('-', '0'))
                values.append(value)
            self.stats_values.append(tuple(values))

    def formatted_data(self):
        self.check_data()
        stats = []
        for idx in range(len(self.offers_names)):
            args = (self.offers_names[idx],
                    self.offers_ids[idx],
                    self.campaigns_names[idx],
                    self.groups_names[idx],
                    self.stats_values[idx])
            stats.append(SponsoredOfferStats(*args))
        return stats

    def check_data(self):
        lists = [
            self.offers_names,
            self.groups_names,
            self.campaigns_names,
            self.offers_ids,
            self.stats_values
        ]
        return len({len(i) for i in lists}) == 1


class SponsoredGroupsScraper(SponsoredScraperMixin):
    pass


class SponsoredCampaignsScraper(SponsoredScraperMixin):
    pass


class GraphicAdsScraper(GraphicScraperMixin):
    pass


class GraphicGroupsScraper(GraphicScraperMixin):
    pass


class GraphicCampaignsScraper(GraphicScraperMixin):
    pass


def scrape_stats(requirement: Requirement):
    driver = AgencyDriver()
    scraper = SponsoredOffersScraper(driver, requirement)
    return scraper.scrape_stats()
