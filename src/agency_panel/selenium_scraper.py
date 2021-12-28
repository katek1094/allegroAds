import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class SeleniumScraper:
    driver = None

    TIMEOUT = 6
    SLEEP_TIME_MIN = 1
    SLEEP_TIME_MAX = 3
    sleep_mode = False

    def __init__(self, url):
        self.start_driver(url)

    def start_driver(self, url):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.maximize_window()

    def sleep(self):
        if self.sleep_mode:
            time.sleep(random.randrange(self.SLEEP_TIME_MIN, self.SLEEP_TIME_MAX))

    def wait(self, element):
        WebDriverWait(self.driver, self.TIMEOUT).until(element)

    def click(self, selector):
        self.sleep()
        self.wait(ec.presence_of_element_located(selector))
        self.driver.find_element(*selector).click()
