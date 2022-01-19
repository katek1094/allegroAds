from bs4 import BeautifulSoup

from src.agency_panel.agency_driver import AgencyDriver


def scrape_accounts():
    driver = AgencyDriver(False)
    soup = BeautifulSoup(driver.page_source)
    layout_body = soup.find('div', {'id': 'layoutBody'})
    clients = layout_body.find('div', {'class': 't1szo'})
    children = clients.contents[1:-1]

    results = []

    for child in children:
        status = child.div.contents[3].contents[1].contents[1].text
        if status == 'Aktywny':
            name = child.div.contents[4].contents[1].find('button').text
            results.append(name)

    print(len(results))
    return results


accounts = scrape_accounts()
print(accounts)
