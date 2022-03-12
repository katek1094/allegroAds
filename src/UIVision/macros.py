import datetime
import json

from src.utils import get_all_accounts_from_excel
from .generate_UIVision_JSON import generate_json_script

UI_VISION_MACROS_DIRECTORY_PATH = '/home/kajetan/Documents/pryzmat/uivision/macros'


def generate_macros_by_priority():
    priorities = ((1, 'low'), (2, 'medium'), (3, 'high'))
    for priority in priorities:
        commands_array = generate_json_script('last_month', get_all_accounts_from_excel(priority=priority[0]))
        today = datetime.date.today()
        name = 'last_month-' + str(priority[1])
        full_json = {
            "Name": name,
            "CreationDate": f'{today.year}-{today.month}-{today.day}',
            "Commands": commands_array
        }
        filename = name + '.json'
        with open(UI_VISION_MACROS_DIRECTORY_PATH + '/' + filename, 'w') as f:
            json.dump(full_json, f, ensure_ascii=False)
