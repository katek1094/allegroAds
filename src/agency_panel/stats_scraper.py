from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup

from .agency_driver import AgencyDriver
from .stats import SponsoredOfferStats, SponsoredGroupStats, SponsoredCampaignStats, \
    GraphicAdStats, GraphicGroupStats, GraphicCampaignStats

allowed_ads_types = ('sponsored', 'graphic')

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
        if self.ads_type not in allowed_ads_types:
            raise ValueError(
                f'unknown ads type "{self.ads_type}"! please select one from the following: {allowed_ads_types}')
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

        self.stats_values = []
        self.summary_stats_values = None

        self.driver = driver
        self.requirement = requirement

    def scrape_stats(self):
        self.driver.open_client_and_stats(self.requirement.username)
        self.set_ads_type()
        self.set_date_range()
        self.set_detail_level()

        self.scrape_data_from_page()

        return self.formatted_data()

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

    def scrape_data_from_page(self):
        self.driver.sleep(.15)  # without sleep time amount of scraped offers is smaller - probably due to loading
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        names_table_body = soup.findAll("table")[0].find('tbody')

        self.scrape_names_table(names_table_body)
        self.scrape_values_table(soup)

        is_next_page = soup.find('span', text='następna')
        if is_next_page:
            try:
                self.driver.click((By.CSS_SELECTOR, 'button[aria-label="następna strona"]'))
                self.scrape_data_from_page()
            except ElementNotInteractableException:  # button is always in html, but hidden and disabled
                pass

    def scrape_values_table(self, soup):
        values_table_body = soup.findAll("table")[1].find('tbody')
        trs = values_table_body.findAll('tr')

        for index in range(len(trs)):
            tds = trs[index].findAll('td')
            if self.requirement.detail_level == 'groups':
                tds = tds[:len(tds) - 1]
            values = []
            for td in tds:
                value = float(
                    td.text.replace(" ", "").replace("%", "").replace("zł", "").replace(",", ".").replace('-', '0'))
                values.append(value)
            if index == 0:
                self.summary_stats_values = tuple(values)
            else:
                self.stats_values.append(tuple(values))

    @abstractmethod
    def scrape_names_table(self, names_table_body):
        pass

    def formatted_data(self):
        data_len = self.check_data_len()
        data = {
            'account': self.requirement.username,
            'ads_type': self.requirement.ads_type,
            'date_range': self.requirement.date_range,
            'detail_level': self.requirement.detail_level,
            'summary_stats': self.generate_summary_stats(),
            'stats': []
        }
        for idx in range(data_len):
            args = tuple(data_list[idx] for data_list in self.data_lists)
            data['stats'].append(self.stats_class(*args))
        return data

    def generate_summary_stats(self):
        assert len(self.stats_class.labels) == len(self.summary_stats_values)
        zip_iterator = zip(self.stats_class.labels, self.summary_stats_values)
        return dict(zip_iterator)

    @property
    @abstractmethod
    def stats_class(self):
        pass

    def check_data_len(self):
        if not len({len(i) for i in self.data_lists}) == 1:
            raise ValueError('data lists are not equal length!')
        return len(self.stats_values)

    @property
    @abstractmethod
    def data_lists(self):
        pass


class SponsoredScraperMixin:
    driver: AgencyDriver

    def set_ads_type(self):
        self.driver.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[1]/div[1]/div/div/a[1]'))


class GraphicScraperMixin:
    driver: AgencyDriver

    def set_ads_type(self):
        self.driver.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[1]/div[1]/div/div/a[2]'))


class SponsoredOffersScraper(SponsoredScraperMixin, GenericStatsScraper):
    stats_class = SponsoredOfferStats

    def __init__(self, *args):
        super().__init__(*args)
        self.offers_names = []
        self.groups_names = []
        self.campaigns_names = []
        self.offers_ids = []

    def scrape_names_table(self, names_table_body):
        self.offers_names.extend([link.text for link in names_table_body.findAll('a')[::3]])
        self.groups_names.extend([link['title'] for link in names_table_body.findAll('a')[2::3]])
        self.campaigns_names.extend([link['title'] for link in names_table_body.findAll('a')[1::3]])
        self.offers_ids.extend([link['href'].split('/')[-1] for link in names_table_body.findAll('a')[::3]])

    @property
    def data_lists(self):
        return [
            self.offers_names,
            self.groups_names,
            self.campaigns_names,
            self.offers_ids,
            self.stats_values
        ]


class SponsoredGroupsScraper(SponsoredScraperMixin, GenericStatsScraper):
    stats_class = SponsoredGroupStats

    def __init__(self, *args):
        super().__init__(*args)
        self.groups_names = []
        self.campaigns_names = []

    def scrape_names_table(self, names_table_body):
        self.groups_names.extend([link.text for link in names_table_body.findAll('a')[::2]])
        self.campaigns_names.extend([link['title'] for link in names_table_body.findAll('a')[1::2]])

    @property
    def data_lists(self):
        return [
            self.groups_names,
            self.campaigns_names,
            self.stats_values
        ]


class SponsoredCampaignsScraper(SponsoredScraperMixin, GenericStatsScraper):
    stats_class = SponsoredCampaignStats

    def __init__(self, *args):
        super().__init__(*args)
        self.campaigns_names = []

    def scrape_names_table(self, names_table_body):
        self.campaigns_names.extend([link['title'] for link in names_table_body.findAll('a')])

    @property
    def data_lists(self):
        return [
            self.campaigns_names,
            self.stats_values
        ]


class GraphicAdsScraper(GraphicScraperMixin, GenericStatsScraper):
    stats_class = GraphicAdStats

    def __init__(self, *args):
        super().__init__(*args)
        self.ads_names = []

    def scrape_names_table(self, names_table_body):
        self.ads_names.extend([span['title'] for span in names_table_body.findAll('span')])

    @property
    def data_lists(self):
        return [
            self.ads_names,
            self.stats_values
        ]


class GraphicGroupsScraper(GraphicScraperMixin, GenericStatsScraper):
    stats_class = GraphicGroupStats

    def __init__(self, *args):
        super().__init__(*args)
        self.groups_names = []

    def scrape_names_table(self, names_table_body):
        self.groups_names.extend([link['title'] for link in names_table_body.findAll('a')])

    @property
    def data_lists(self):
        return [
            self.groups_names,
            self.stats_values
        ]


class GraphicCampaignsScraper(GraphicScraperMixin, GenericStatsScraper):
    stats_class = GraphicCampaignStats

    def __init__(self, *args):
        super().__init__(*args)
        self.campaigns_names = []

    def scrape_names_table(self, names_table_body):
        self.campaigns_names.extend([link['title'] for link in names_table_body.findAll('a')])

    @property
    def data_lists(self):
        return [
            self.campaigns_names,
            self.stats_values
        ]


def find_scraper(driver: AgencyDriver, requirement: Requirement):
    scrapers = [
        SponsoredOffersScraper,
        SponsoredGroupsScraper,
        SponsoredCampaignsScraper,
        GraphicAdsScraper,
        GraphicGroupsScraper,
        GraphicCampaignsScraper
    ]
    for s in scrapers:
        if s.stats_class.detail_level == requirement.detail_level and s.stats_class.ads_type == requirement.ads_type:
            return s(driver, requirement)
