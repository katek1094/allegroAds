import datetime
import os
import time

from bs4 import BeautifulSoup
from openpyxl import load_workbook
from selenium.webdriver.common.by import By

from .agency_driver import AgencyDriver


def generate_default_report_name():
    # today = datetime.date.today()  # TODO: uncomment when using for real
    today = datetime.date(2021, 12, 28)  # TODO: comment when using for real
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    last_month_number = last_month.strftime("%m")
    last_year_number = last_month.strftime("%Y")
    current_month_number = today.strftime("%m")
    current_year_number = today.strftime("%Y")
    return f'statystyki_oferty_26-{last_month_number}-{last_year_number}_25-{current_month_number}-{current_year_number}.xlsx'


def generate_stats_sheet_default_name():
    # today = datetime.date.today()  # TODO: uncomment when using for real
    today = datetime.date(2021, 12, 27)  # TODO: comment when using for real
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    last_month_number = last_month.strftime("%m")
    last_year_number = last_month.strftime("%Y")
    current_month_number = today.strftime("%m")
    current_year_number = today.strftime("%Y")
    return f'Statystyk_{last_year_number}-{last_month_number}-26_{current_year_number}-{current_month_number}-25'


default_report_name = generate_default_report_name()
stats_sheet_default_name = generate_stats_sheet_default_name()
reports_path = '/home/kajetan/Documents/pryzmat/reports/'


def click_to_generate_report(username, driver):
    print(f'generate report for account: {username}')
    driver.open_client_and_stats(username)
    driver.set_ads_type('sponsored')
    driver.set_date_range('last_billing_month')
    driver.set_detail_level('offers')
    driver.click((By.XPATH, '//*[@id="layoutBody"]/div/div/div[3]/div[2]/button[3]'))


def generate_reports(accounts_list):
    print('function generate reports started')
    # if datetime.date.today().day < 26:
    #     raise Exception("It is too early for generating reports for previous billing month")
    driver = AgencyDriver()
    for account in accounts_list:
        click_to_generate_report(account, driver)
    print('function generate reports finished, reports are now generated')


def check_for_report(username, driver):
    print(f'check for report for account: {username}')
    driver.open_client(username)
    driver.open_my_files()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    tags = soup.findAll(string=default_report_name)
    for tag in tags:
        if tag.parent.name != 'strong':
            parent = tag.parent.parent
            status = parent.findAll('div')[3].text.strip('Status')
            return status == 'Gotowe'


def check_for_reports(accounts_list):
    print(f'function check for reports started')
    driver = AgencyDriver()
    ready = 0
    for account in accounts_list:
        if check_for_report(account, driver):
            ready += 1
        else:
            return False
    print(f'function check for reports finished')
    return ready == len(accounts_list)


def rename_and_format_file(username):
    file_path = reports_path + default_report_name
    wb = load_workbook(filename=file_path)
    stats_sheet_name = 'Statystyk_' + stats_sheet_default_name
    del wb[stats_sheet_name]
    ws = wb.active
    ws.delete_cols(1, 2)
    # TODO: sort data
    # TODO: add default columns width
    new_file_path = reports_path + f'raport-{username}.xlsx'
    wb.save(new_file_path)
    os.remove(file_path)


def download_report(username, driver):
    print(f'download report for account: {username}')
    driver.open_client(username)
    driver.open_my_files()
    time.sleep(1)
    driver.click((By.CSS_SELECTOR, 'button[title="Pobierz plik"]'))
    time.sleep(2)
    rename_and_format_file(username)


def download_reports(accounts_list):
    print(f'function download reports started')
    driver = AgencyDriver()
    for account in accounts_list:
        download_report(account, driver)
    print(f'function download reports finished')


def run_reports_downloader(accounts_list):
    print(f'started reports downloader for {len(accounts_list)} accounts')
    generate_reports(accounts_list)
    sleep_time = 60 * 2
    reports_ready = False
    while not reports_ready:
        time.sleep(sleep_time)
        time_now = datetime.datetime.now().strftime("%H:%M:S")
        print(f'{time_now}, next check if reports are ready in: {sleep_time / 60} minutes')
        reports_ready = check_for_reports(accounts_list)
    download_reports(accounts_list)

