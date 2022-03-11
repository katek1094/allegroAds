def create_command(command: str, target: str, value: str = "", description: str = "") -> dict:
    return {
        "Command": command,
        "Target": target,
        "Value": value,
        "Description": description
    }


def create_click_command(*args) -> dict:
    return create_command('click', *args)


def create_xpath_click_command(xpath, *args):
    target = 'xpath=' + xpath
    return create_click_command(target, *args)


class Commands:
    def __init__(self, account_name):
        self.open_agency_panel = create_command('selectWindow', 'tab=open',
                                                'https://ads.allegro.pl/panel/agency/clients')
        self.open_clients_list = create_click_command('linkText=Przełącz na klienta')
        self.open_client_account = create_xpath_click_command(f"(//*[text()='{account_name}']) ")
        self.open_stats = create_xpath_click_command('//*[@id="main"]/div[2]/div/header/div/div/div[2]/div/div/div/div/div[1]/nav/a[2]')
        self.open_calendar = create_xpath_click_command('//*[@id="layoutBody"]/div/div/div/div[2]/div')

        # calendar range options
        self.select_yesterday = create_xpath_click_command("//*[text()='Wczoraj']")
        self.select_today = create_xpath_click_command("//*[text()='Dzisiaj']")
        self.select_last_week = create_xpath_click_command("//*[text()='Ostatnie 7 dni']")
        self.select_last_month = create_xpath_click_command("//*[text()='Ostatnie 30 dni']")
        self.select_last_billing_month = create_xpath_click_command("//*[text()='Poprzedni okres rozliczeniowy']")
        self.select_current_billing_month = create_xpath_click_command("//*[text()='Bieżący okres rozliczeniowy']")
        # updates calendar range
        self.update = create_xpath_click_command("//*[text()='Aktualizuj']")

        # chart dataset options
        self.open_orange_select = create_xpath_click_command(
            '//*[@id="layoutBody"]/div/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/select')
        self.open_grey_select = create_xpath_click_command(
            '//*[@id="layoutBody"]/div/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[4]/div/select')
        self.select_cost_orange = create_xpath_click_command(
            '//*[@id="layoutBody"]/div/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/select/option[5]')
        self.select_return_grey = create_xpath_click_command(
            '//*[@id="layoutBody"]/div/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[4]/div/select/option[5]')

        # reports downloading commands
        self.select_offers_view = create_xpath_click_command(
            '//*[@id="layoutBody"]/div/div/div[4]/div[1]/div/div[3]/button')
        self.open_files = create_xpath_click_command(
            '//*[@id="main"]/div[2]/div/header/div/div/div[2]/div/div/div/div/div[1]/nav/div/a')
        self.click_generate_report = create_xpath_click_command('//*[@id="layoutBody"]/div/div/div[4]/div[2]/button[3]')
        self.click_download_file = create_xpath_click_command(
            '//*[@id="layoutBody"]/div/div[2]/div/div[2]/div/div[6]/div[2]/button[2]')
