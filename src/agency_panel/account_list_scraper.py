import time

from bs4 import BeautifulSoup

from src.agency_panel.agency_driver import AgencyDriver


def scrape_accounts():
    driver = AgencyDriver(False)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    layout_body = soup.find('div', {'id': 'layoutBody'})
    clients = layout_body.find('div', {'class': 't1szo'})
    children = clients.contents[1:-1]

    results = []

    for child in children:
        status = child.div.contents[3].contents[1].contents[1].text
        budget = float(child.div.contents[6].contents[1].text.replace("zł", "").replace(",", '.').replace(' ', ''))
        if status == 'Aktywny' and budget > 0:
            name = child.div.contents[4].contents[1].find('button').text
            results.append(name)

    print(len(results))
    return results
