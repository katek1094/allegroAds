import datetime
import os
from collections import namedtuple
from statistics import mean

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openpyxl import Workbook


def create_session():
    return requests.Session()


def login(s: requests.Session):
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


def get_account_raw_data(s: requests.Session, account_name: str):
    api_url = 'https://niezbedniksprzedawcy.pl/StatystykiAllegro/get_offers_stats?format=json'
    params = {'q': account_name,
              'p': 1,  # pagination control
              'l': 600,  # amount of data on one page
              'f': '1M',  # time range of data requested
              'offerPositionLimit': 600}  # minimum position in accuracy ranking for offer to show; max=600
    r = s.get(api_url, params=params)
    return r.json()


"""
return value structure:
{
    limit: int, the same value as in request
    pages: int, how many pages there are to see
    offset: int, number of page returned
    offers: data about offers, nested deeper
    series: [
        {
            name: offer id
            data: data for 30 days (array) : [
                [
                    timestamp - in miliseconds,
                    value - offer position in accuracy
                ]
            ]
        }
    ]

}
"""

Record = namedtuple('Record', 'date value')
OfferData = namedtuple('OfferData', 'id_number records')


def create_record(record):
    timestamp_in_ms, position = record
    record_date = datetime.datetime.fromtimestamp(timestamp_in_ms / 1000).date()
    return Record(record_date, position)


def format_account_data(data):
    formatted_data = []
    for offer in data['series']:
        records = []
        for record in offer['data']:
            records.append(create_record(record))
        formatted_data.append(OfferData(offer['name'], tuple(records)))

    return formatted_data


def generate_columns_for_dates_dict(skip=1):
    result = {}
    start_date = datetime.date.today()
    day_count = 30
    for index, date in enumerate(start_date - datetime.timedelta(day_count - n) for n in range(day_count)[0::skip]):
        result[date] = index + 2
    return result


columns_for_dates = generate_columns_for_dates_dict()


def get_point_for_day_data(arr):
    points = 0
    for dt in arr:
        if dt == 1:
            points += 14
        elif 4 > dt > 1:
            points += 8
        elif 6 > dt > 3:
            points += 5
        elif 9 > dt > 5:
            points += 3.5
        elif 13 > dt > 8:
            points += 2.5
        elif 21 > dt > 12:
            points += 2
        elif 41 > dt > 20:
            points += 1
        elif 61 > dt > 40:
            points += 0.8
        elif 121 > dt > 60:
            points += 0.4
        elif 181 > dt > 120:
            points += 0.2
        elif 601 > dt > 180:
            points += 0.1
        else:
            raise Exception('wrong value or code "if" ranges')
    return round(points / (len(arr)), 2)


def create_excel(data: [OfferData], username: str):
    wb = Workbook()
    ws = wb.active

    # WRITE DATES
    for date, column in columns_for_dates.items():
        ws.cell(row=1, column=column).value = date.strftime('%d-%m')

    # WRITE DATA
    row = 2
    for offer_data in data:
        ws.cell(row=row, column=1).value = offer_data.id_number
        for record in offer_data.records:
            ws.cell(row=row, column=columns_for_dates[record.date]).value = record.value
        row += 1

    # reformat data into days of records
    days = []
    for _ in range(30):
        days.append([])
    for offer_data in data:
        for index, record in enumerate(offer_data.records):
            days[columns_for_dates[record.date] - 2].append(record.value)

    points = []
    for day in days:
        points.append(get_point_for_day_data(day))

    ws = wb.create_sheet('stats')
    for date, column in columns_for_dates.items():
        ws.cell(row=1, column=column).value = date.strftime('%d-%m')
    for col, point in enumerate(points):
        ws.cell(row=2, column=col + 2).value = point

    for date, column in generate_columns_for_dates_dict(3).items():
        ws.cell(row=5, column=column).value = date.strftime('%d-%m')

    avg_points = []
    for x in range(10):
        print(x)
        print(x * 3, x * 3 + 2)
        avg_points.append(mean(points[x * 3:x * 3 + 2]))
    for col, point in enumerate(avg_points):
        ws.cell(row=6, column=col + 2).value = point

    wb.save(f'/home/kajetan/Desktop/{username}.xlsx')


def create_account_stats_report(s, account_name):
    raw_data = get_account_raw_data(s, account_name)
    results = format_account_data(raw_data)
    create_excel(results, account_name)


session = create_session()
login(session)

create_account_stats_report(session, 'sklep-miszmasz')
