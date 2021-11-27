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
    array.append(open_agency_panel)
    array.append(open_clients_list)
    array.append(open_client_account)
    array.append(open_agency_panel)
    array.append(open_clients_list)
    array.append(open_client_account)
    array.append(open_stats)

with open('macro.json', 'w', encoding='utf-8') as f:
    json.dump(array, f)
