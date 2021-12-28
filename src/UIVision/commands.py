def create_command(command: str, target: str, value: str = "", description: str = "") -> dict:
    return {
        "Command": command,
        "Target": target,
        "Value": value,
        "Description": description
    }


def create_click_command(args) -> dict:
    return create_command('click', *args)


class Commands:
    def __init__(self, account_name):
        self.open_agency_panel = create_command('selectWindow', 'tab=open',
                                                'https://ads.allegro.pl/panel/agency/clients')
        self.open_clients_list = create_click_command('linkText=Przełącz na klienta')
        self.open_client_account = create_click_command(f"xpath=(//*[text()='{account_name}']) ")
        self.open_stats = create_click_command('linkText=linkText=Statystyki')
        self.open_calendar = create_click_command('xpath=//*[@id="layoutBody"]/div/div/div/div[2]/div')

        # calendar range options
        self.select_yesterday = create_click_command("xpath=//*[text()='Wczoraj']")
        self.select_last_week = create_click_command("xpath=//*[text()='Ostatnie 7 dni']")
        self.select_last_month = create_click_command("xpath=//*[text()='Ostatnie 30 dni']")
        self.select_last_billing_month = create_click_command("xpath=//*[text()='Poprzedni okres rozliczeniowy']")
        self.select_current_billing_month = create_click_command("xpath=//*[text()='Bieżący okres rozliczeniowy']")

        self.update = create_click_command("xpath=//*[text()='Aktualizuj']")
