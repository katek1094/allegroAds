import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from dotenv import load_dotenv

from .selenium_driver import SeleniumDriver

load_dotenv()

AGENCY_EMAIL = os.getenv('AGENCY_EMAIL')
AGENCY_PASSWORD = os.getenv('AGENCY_PASSWORD')


class AgencyDriver(SeleniumDriver):

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
