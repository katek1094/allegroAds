import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/home/kajetan/Documents/pryzmat/reports'}
options.add_experimental_option('prefs', prefs)


class SeleniumDriver:
    driver = None

    TIMEOUT = 6
    SLEEP_TIME_MIN = 1
    SLEEP_TIME_MAX = 3
    sleep_mode = False

    def __init__(self, url):
        self.start(url)

    def start(self, url):
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.driver.get(url)
        self.driver.maximize_window()

    def sleep(self, duration=None):
        if self.sleep_mode or duration:
            time.sleep(random.randrange(self.SLEEP_TIME_MIN, self.SLEEP_TIME_MAX))

    def wait(self, element):
        WebDriverWait(self.driver, self.TIMEOUT).until(element)

    def click(self, selector):
        self.sleep()
        self.wait(ec.presence_of_element_located(selector))
        self.driver.find_element(*selector).click()

    @property
    def page_source(self):
        return self.driver.page_source
