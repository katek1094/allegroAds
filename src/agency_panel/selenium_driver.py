import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/home/kajetan/Documents/pryzmat/reports'}
options.add_experimental_option('prefs', prefs)


class SeleniumDriver:
    driver = None

    TIMEOUT = 10
    SLEEP_TIME_MIN = 2
    SLEEP_TIME_MAX = 4
    sleep_mode = False

    def __init__(self, url):
        self.start(url)

    def start(self, url):
        # noinspection DuplicatedCode
        opt = Options()
        # opt.headless = True
        opt.add_argument("--window-size=1920,1080")
        # opt.add_argument("--headless")
        # opt.add_argument("--disable-gpu")
        # a = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        # b = " (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        # c = a + b
        # opt.add_argument(c)
        # noinspection PyArgumentList
        self.driver = webdriver.Chrome(options=opt, service=Service(ChromeDriverManager().install()))

        self.driver.get(url)

    def sleep(self, duration=None):
        if self.sleep_mode or duration:
            time.sleep(random.randrange(self.SLEEP_TIME_MIN, self.SLEEP_TIME_MAX))

    def wait(self, element, timeout=None):
        if not timeout:
            timeout = self.TIMEOUT
        WebDriverWait(self.driver, timeout).until(element)

    def click(self, selector):
        self.sleep()
        self.wait(ec.presence_of_element_located(selector))
        self.driver.find_element(*selector).click()

    @property
    def page_source(self):
        return self.driver.page_source
