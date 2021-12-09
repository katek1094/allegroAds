import json

from generate_accounts_list import generate_accounts_list

accounts_list = generate_accounts_list()

array = []

for account in accounts_list:
    open_agency_panel = {
        "Command": "selectWindow",
        "Target": "tab=open",
        "Value": "https://ads.allegro.pl/panel/agency/clients",
        "Description": ""
    }
    open_clients_list = {
        "Command": "click",
        "Target": "linkText=Przełącz na klienta",
        "Value": "",
        "Description": ""
    }
    open_client_account = {
        "Command": "click",
        "Target": f"xpath=(//*[text()='{account}']) ",
        "Value": "",
        "Description": ""
    }
    open_stats = {
        "Command": "click",
        "Target": "linkText=Statystyki",
        "Value": "",
        "Description": ""
    }
    open_calendar = {
        "Command": "click",
        "Target": 'xpath=//*[@id="layoutBody"]/div/div/div/div[2]/div',
        "Value": "",
        "Description": ""
    }
    select_yesterday = {
        "Command": "click",
        "Target": "xpath=//*[text()='Wczoraj']",
        "Value": "",
        "Description": ""
    }
    select_last_week = {
        "Command": "click",
        "Target": "xpath=//*[text()='Ostatnie 7 dni']",
        "Value": "",
        "Description": ""
    }
    select_last_month = {
        "Command": "click",
        "Target": "xpath=//*[text()='Ostatnie 30 dni']",
        "Value": "",
        "Description": ""
    }
    select_last_billing_month = {
        "Command": "click",
        "Target": "xpath=//*[text()='Poprzedni okres rozliczeniowy']",
        "Value": "",
        "Description": ""
    }
    select_current_billing_month = {
        "Command": "click",
        "Target": "xpath=//*[text()='Bieżący okres rozliczeniowy']",
        "Value": "",
        "Description": ""
    }

    update = {
        "Command": "click",
        "Target": "xpath=//*[text()='Aktualizuj']",
        "Value": "",
        "Description": ""
    }

    # array.append(open_agency_panel)
    # array.append(open_clients_list)
    # array.append(open_client_account)
    array.append(open_agency_panel)
    array.append(open_clients_list)
    array.append(open_client_account)
    array.append(open_stats)
    array.append(open_calendar)
    array.append(select_last_week)
    array.append(update)

with open('macro.json', 'w', encoding='utf-8') as f:
    json.dump(array, f)
