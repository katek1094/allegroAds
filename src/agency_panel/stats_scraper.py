# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import ElementNotInteractableException
# from bs4 import BeautifulSoup
#
# from .agency_driver import AgencyScraper
#
# sponsored_labels = ['clicks', 'views', 'CTR', 'avg CPC', 'cost', 'return', 'interest', 'pcs sold ', 'sales value']
# graphic_labels = ['clicks', 'views', 'CTR', 'avg CPM', 'cost', 'return', 'range', 'interest', 'assisted sale',
#                   'pcs sold ', 'sales value']
#
# ads_types = ('sponsored', 'graphic')
#
# date_ranges = {
#     'yesterday': 'Wczoraj',
#     'today': 'Dzisiaj',
#     'last_week': 'Ostatnie 7 dni',
#     'last_month': 'Ostatnie 30 dni',
#     'last_billing_month': 'Poprzedni okres rozliczeniowy',
#     'current_billing_month': 'Bieżący okres rozliczeniowy',
# }
#
# detail_levels = ('campaigns', 'groups', 'offers', 'ads')
#
#
# class StatsScraper(AgencyScraper):
#     stats = []
#
#     def __init__(self, requirements):
#         """
#         requirements is an iterable of tuples consisting of 4 string values:
#         username, ads_type, date_range, detail_level
#         """
#         super().__init__()
#
#         for requirement in requirements:
#             self.open_client_and_stats(requirement[0])
#             self.set_ads_type(requirement[1])
#             self.set_date_range(requirement[2])
#             self.set_detail_level(requirement[3])
#             self.stats.append((requirement[0], self.scrape_stats(requirement[3])))
#             self.open_clients_list(requirement[0])
#
#     def open_client_and_stats(self, username):
#         self.click((By.XPATH, f"//*[text()='{username}']"))
#         self.click((By.LINK_TEXT, 'Statystyki'))
#
#     def open_clients_list(self, username):
#         self.click((By.LINK_TEXT, username))
#
#     def set_ads_type(self, ads_type):
#         if ads_type == 'graphic':
#             self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[1]/div[1]/div/div/a[2]'))
#
#     @staticmethod
#     def validate_requirements(self, requirements):
#         for requirement in requirements:
#             if not isinstance(requirement, tuple):
#                 raise TypeError(f'requirement "{requirement} has to be a tuple!')
#             for value in requirement:
#                 if not isinstance(value, str):
#                     raise TypeError(f'requirement value "{value}" has to be string!')
#             self.validate_arguments(*requirement[1:])
#
#     @staticmethod
#     def validate_arguments(ads_type, date_range, detail_level):
#         if ads_type not in ads_types:
#             raise ValueError(f'unknown ads type "{ads_type}"! please select one from the following: {ads_types}')
#         if date_range not in date_ranges.keys():
#             raise ValueError(
#                 f'unknown date range "{date_range}"! please select one from the following: {date_ranges.keys()}')
#         if detail_level not in detail_levels:
#             raise ValueError(
#                 f'unknown detail level "{detail_level}"! please select one from the following: {detail_levels}')
#         if ads_type == 'sponsored' and detail_level == 'ads':
#             raise ValueError('sponsored ads do not have "ads" detail level')
#         if ads_type == 'graphic' and detail_level == 'offers':
#             raise ValueError('graphic ads do not have "offers" detail level')
#
#     def set_date_range(self, date_range):
#         self.click((By.CSS_SELECTOR, 'div[title="Zmień zakres dat"]'))
#         self.click((By.XPATH, f"//*[text()='{date_ranges[date_range]}']"))
#         self.click((By.XPATH, "//*[text()='Aktualizuj']"))
#
#     def set_detail_level(self, detail_level):
#         if detail_level == 'groups':
#             self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[1]/div/div[2]/button'))
#         elif detail_level == 'offers' or detail_level == 'ads':
#             self.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[1]/div/div[3]/button'))
#
#     def scrape_stats(self, detail_level, number=1):
#         self.sleep(.1)  # without sleep time amount of scraped offers is smaller - probably due to loading
#         soup = BeautifulSoup(self.driver.page_source, 'html5lib')
#         names_table_body = soup.findAll("table")[0].find('tbody')
#
#         names = [link.text for link in names_table_body.findAll('a')[::3]]
#
#         ids = None
#         if detail_level == 'offers':
#             ids = [link['href'].split('/')[-1] for link in names_table_body.findAll('a')[::3]]
#
#         values_table_body = soup.findAll("table")[1].find('tbody')
#         trs = values_table_body.findAll('tr')
#         if number == 1:
#             trs = trs[1:]  # first row is summary stats
#
#         stats = []
#
#         if len(trs) != len(names):
#             raise ValueError('len of trs and names should be the same!')
#
#         for index in range(len(trs)):
#             tds = trs[index].findAll('td')
#             values = []
#             for td in tds:
#                 value = float(
#                     td.text.replace(" ", "").replace("%", "").replace("zł", "").replace(",", ".").replace('-', '0'))
#                 values.append(value)
#             values = tuple(values)
#             if detail_level == 'offers':
#                 stats.append((names[index], ids[index], values))
#             else:
#                 stats.append((names[index], values))
#
#         is_next_page = soup.find('span', text='następna')
#         if is_next_page:
#             try:
#                 self.click((By.CSS_SELECTOR, 'button[aria-label="następna strona"]'))
#                 stats.extend(self.scrape_stats(detail_level, number + 1))
#             except ElementNotInteractableException:  # button is always in html, but hidden and disabled
#                 pass
#         return stats
