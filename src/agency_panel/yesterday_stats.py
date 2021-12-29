# import datetime
#
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
# from openpyxl import Workbook
#
# from .agency_driver import AgencyScraper
#
#
# class YesterdayStatsScraper(AgencyScraper):
#     accounts_data = {}
#     clients_list = []
#     sponsored_labels = ['clicks', 'views', 'CTR', 'avg CPC', 'cost', 'return', 'interest', 'pcs sold ', 'sales value']
#     graphic_labels = ['clicks', 'views', 'CTR', 'avg CPM', 'cost', 'return', 'range', 'interest', 'assisted sale',
#                       'pcs sold ', 'sales value']
#
#     def __init__(self, clients_list):
#         super().__init__()
#
#         self.clients_list = clients_list
#
#         for count, client in enumerate(self.clients_list):
#             self.click((By.XPATH, f"//*[text()='{client}']"))
#             self.click((By.LINK_TEXT, 'Statystyki'))
#             self.click((By.CSS_SELECTOR, 'div[title="Zmień zakres dat"]'))
#             self.click((By.XPATH, "//*[text()='Wczoraj']"))
#             self.click((By.XPATH, "//*[text()='Aktualizuj']"))
#             self.accounts_data[client] = {}
#             self.accounts_data[client]['sponsored'] = self.scrape_stats(self.sponsored_labels)
#             self.click((By.XPATH, f"//*[text()='Reklama graficzna']"))
#             self.click((By.CSS_SELECTOR, 'div[title="Zmień zakres dat"]'))
#             self.click((By.XPATH, "//*[text()='Wczoraj']"))
#             self.click((By.XPATH, "//*[text()='Aktualizuj']"))
#             self.accounts_data[client]['graphic'] = self.scrape_stats(self.graphic_labels)
#             self.click((By.LINK_TEXT, client))
#             print(f"{count + 1}/{len(self.clients_list)} - {client}")
#
#         wb = Workbook()
#         ws = wb.active
#         row = 1
#         col = 1
#
#         ws.cell(row=row, column=col).value = "wygenerowano"
#         ws.cell(row=row, column=col + 1).value = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
#         row += 2
#         ws.cell(row=row, column=col).value = "konto"
#         col += 2
#
#         for label in self.sponsored_labels:
#             ws.cell(row=row, column=col).value = label
#             col += 1
#         col += 1
#         for label in self.graphic_labels:
#             ws.cell(row=row, column=col).value = label
#             col += 1
#         col = 1
#         row += 1
#
#         for client, data in self.accounts_data.items():
#             ws.cell(row=row, column=col).value = client
#             col += 2
#             for dt in data['sponsored'].values():
#                 ws.cell(row=row, column=col).value = dt
#                 col += 1
#             col += 1
#             for dt in data['graphic'].values():
#                 ws.cell(row=row, column=col).value = dt
#                 col += 1
#             row += 1
#             col = 1
#         yesterday = datetime.date.today() - datetime.timedelta(days=1)
#         yesterday = yesterday.strftime('%d-%m-%Y')
#         wb.save(f'/home/kajetan/Documents/pryzmat/scraped_data/all_accounts/{yesterday}.xlsx')
#
#     def scrape_stats(self, labels):
#         self.sleep()
#         soup = BeautifulSoup(self.driver.page_source, 'html5lib')
#         table = soup.findAll("table")[1]
#         table_body = table.find('tbody')
#         tr1 = table_body.find('tr')
#         tds = tr1.findAll('td')
#         data = {}
#         for label, td in zip(labels, tds):
#             data[label] = float(
#                 td.text.replace(" ", "").replace("%", "").replace("zł", "").replace(",", ".").replace('-', '0'))
#
#         return data
