import json

from .commands import Commands

possible_modes = (
    'campaigns',
    'last_week',
    'last_month',
    'last_month_graphic',
    'generate_reports',
    'download_reports',
)


def generate_json_script(mode: str, accounts_list: list, dump: bool = False):
    if mode not in possible_modes:
        raise ValueError(f'mode : "{mode}" is not allowed. Please select from one of possible modes: {possible_modes}')

    commands_array = []

    for account_name in [account.name for account in accounts_list]:
        commands = Commands(account_name)

        account_commands_array = [  # the same for every mode, campaigns mode
            commands.open_agency_panel,
            commands.open_clients_list,
            commands.open_client_account,
        ]

        if mode == possible_modes[1]:  # last week mode
            account_commands_array.extend([
                commands.open_stats,
                commands.open_calendar,
                commands.select_last_week,
                commands.update,
            ])
        if mode == possible_modes[2]:  # last month mode
            account_commands_array.extend([
                commands.open_stats,
                commands.open_calendar,
                commands.select_last_month,
                commands.update,
            ])

        if mode == possible_modes[3]:  # last month graphic mode
            account_commands_array.extend([
                commands.open_stats,
                commands.open_graphic,
                commands.open_calendar,
                commands.select_last_month,
                commands.update,
            ])

        if mode == possible_modes[4]:  # generate reports mode
            account_commands_array.extend([
                commands.open_stats,
                commands.open_calendar,
                commands.select_last_billing_month,
                commands.update,
                commands.select_offers_view,
                commands.click_generate_report,
                commands.open_client_account,
            ])

        if mode == possible_modes[5]:  # download reports mode
            account_commands_array.extend([
                commands.open_files,
                commands.click_download_file,
                commands.open_client_account,
            ])

        commands_array.extend(account_commands_array)

    if dump:
        with open('../macro.json', 'w') as f:
            json.dump(commands_array, f, ensure_ascii=False)
    else:
        return commands_array
