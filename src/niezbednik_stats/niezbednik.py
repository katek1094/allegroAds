import os
import requests
import datetime

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openpyxl import Workbook


def create_session():
    return requests.Session()


def login(s):
    load_dotenv()

    password = os.getenv('NIEZBEDNIK_PASSWORD')

    s.headers.update({'referer': 'https://niezbedniksprzedawcy.pl/accounts/login/'})

    soup = BeautifulSoup(s.get('https://niezbedniksprzedawcy.pl/accounts/login/').content, 'html5lib')
    csrftoken = soup.find('input', dict(name='csrfmiddlewaretoken'))['value']

    r = s.post('https://niezbedniksprzedawcy.pl/accounts/login/', {
        'csrfmiddlewaretoken': csrftoken,
        'login': 'info@pryzmat.media',
        'password': password
    })

    if r.status_code != 200:
        raise Exception('CAN NOT LOGIN INTO NIEZBEDNIK SPRZEDAWCY')


def get_account_raw_data(s: requests.Session, account_name):
    api_url = 'https://niezbedniksprzedawcy.pl/StatystykiAllegro/get_offers_stats?format=json'
    """
    params
    q - account_name
    p - page number
    l - 
    f - 1M, 2M, 3M, 1y
    offerPositionLimit - 
    """
    #     'https://niezbedniksprzedawcy.pl/StatystykiAllegro/get_offers_stats?format=json&q=handlowiec-rs-pl&p=1&l=10&f=1M&offerPositionLimit=600')
    r = s.get(api_url, params={'q': account_name, 'p': 1, 'l': 600, 'f': '1M', 'offerPositionLimit': 600})
    return r.json()


def format_account_data(data):
    formatted_data = []
    for dt in data['series']:
        arr = []
        for record in dt['data']:
            arr.append(record[1])
        formatted_data.append((dt['name'], arr))
    return formatted_data


def create_excel(data):
    wb = Workbook()
    ws = wb.active
    row = 1
    col = 2

    start_date = datetime.date.today()
    day_count = 30
    for date in (start_date - datetime.timedelta(day_count - n) for n in range(day_count)):
        ws.cell(row=row, column=col).value = date.strftime('%d-%m')
        col += 1
    row += 1
    col = 1
    for id_number, records in data:
        ws.cell(row=row, column=col).value = id_number
        col += 1
        for record in records:
            ws.cell(row=row, column=col).value = record
            col += 1
        row += 1
        col = 1
    wb.save('/home/kajetan/Desktop/handlowiec-rs-pl.xlsx')


s = create_session()
login(s)
raw_data = get_account_raw_data(s, 'handlowiec-rs-pl')
results = format_account_data(raw_data)
create_excel(results)
