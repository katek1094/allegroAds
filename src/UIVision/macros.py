import datetime
import json

from src.utils import get_all_accounts_from_excel
from .generate_UIVision_JSON import generate_json_script

UI_VISION_MACROS_DIRECTORY_PATH = '/home/kajetan/Documents/pryzmat/uivision/macros'


def generate_macro(mode: str, accounts_list: list, name: str):
    commands_array = generate_json_script(mode, accounts_list)
    today = datetime.date.today()
    full_json = {
        "Name": name,
        "CreationDate": f'{today.year}-{today.month}-{today.day}',
        "Commands": commands_array
    }
    filename = name + '.json'
    with open(UI_VISION_MACROS_DIRECTORY_PATH + '/' + filename, 'w') as f:
        json.dump(full_json, f, ensure_ascii=False)


def generate_macros_by_priority():
    priorities = ((1, 'low'), (2, 'medium'), (3, 'high'))
    for priority in priorities:
        generate_macro('last_month', get_all_accounts_from_excel(priority=priority[0]),
                       'last_month-' + str(priority[1]))


def generate_all_graphic_macro():
    generate_macro('last_month_graphic', get_all_accounts_from_excel(only_graphic=True), 'last month graphic')


def generate_all_sponsored_macro():
    generate_macro('last_month', get_all_accounts_from_excel(), 'last month all')


def generate_all_macros():
    generate_macros_by_priority()
    generate_all_sponsored_macro()
    generate_all_graphic_macro()
