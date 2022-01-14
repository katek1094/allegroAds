import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from .constants import date_ranges, ads_types, detail_levels
from .selenium_driver import SeleniumDriver

load_dotenv()

AGENCY_EMAIL = os.getenv('AGENCY_EMAIL')
AGENCY_PASSWORD = os.getenv('AGENCY_PASSWORD')


class AgencyDriver(SeleniumDriver):
    current_account = None

    def __init__(self):
        super().__init__('https://ads.allegro.pl/panel/agency/clients')

        self.click((By.CSS_SELECTOR, 'button[data-role="accept-consent"]'))
        self.fill_and_submit_login_form()
        self.click((By.CSS_SELECTOR, 'button[aria-label="Zamknij"]'))
        self.click((By.LINK_TEXT, 'Przełącz na klienta'))

    def fill_and_submit_login_form(self):
        self.sleep()
        email = AGENCY_EMAIL
        password = AGENCY_PASSWORD
        self.wait(ec.presence_of_element_located((By.ID, 'login')))
        self.driver.find_element(By.ID, 'login').send_keys(email)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    def open_client_and_stats(self, username):
        self.open_clients_list(username)
        if self.current_account != username:
            self.click((By.XPATH, f"//*[text()='{username}']"))
            self.open_stats()
            self.current_account = username

    def open_client(self, username):
        self.open_clients_list(username)
        if self.current_account != username:
            self.click((By.XPATH, f"//*[text()='{username}']"))
            self.current_account = username

    def open_stats(self):
        self.click((By.LINK_TEXT, 'Statystyki'))

    def open_my_files(self):
        self.click((By.XPATH, '//*[@id="main"]/div[2]/div/header/div/div/div[2]/div/div/div/div/div[1]/nav/div/a'))

    def open_clients_list(self, username):
        if not self.current_account:
            return
        elif self.current_account == username:
            return
        else:
            self.click((By.LINK_TEXT, self.current_account))

    def set_ads_type(self, ads_type):
        if ads_type not in ads_types:
            raise ValueError('wrong ads type!')
        if ads_type == 'sponsored':
            self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[1]/div[1]/div/div/a[1]'))
        elif ads_type == 'graphic':
            self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[1]/div[1]/div/div/a[2]'))

    def set_date_range(self, date_range):
        if date_range not in date_ranges.keys():
            raise ValueError('wrong date range')
        self.click((By.CSS_SELECTOR, 'div[title="Zmień zakres dat"]'))
        self.click((By.XPATH, f"//*[text()='{date_ranges[date_range]}']"))
        self.click((By.XPATH, "//*[text()='Aktualizuj']"))

    def set_detail_level(self, detail_level):
        if detail_level not in detail_levels:
            raise ValueError('wrong detail level')
        if detail_level == 'groups':
            self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[1]/div/div[2]/button'))
        elif detail_level == 'offers' or detail_level == 'ads':
            self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[1]/div/div[3]/button'))
