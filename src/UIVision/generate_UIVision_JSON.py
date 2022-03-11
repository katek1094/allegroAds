import json

from .commands import Commands

possible_modes = (
    'campaigns',
    'last_week',
    'last_month',
    'generate_reports',
    'download_reports',
)


def generate_json_script(mode: str, accounts_list: list):
    if mode not in possible_modes:
        raise ValueError(f'mode : "{mode}" is not allowed. Please select from one of possible modes: {possible_modes}')

    commands_array = []

    if mode == possible_modes[3] or mode == possible_modes[4]:
        cmd = Commands('empty')
        commands_array.append(cmd.open_agency_panel)
        commands_array.append(cmd.open_clients_list)

    for account_name in [account.name for account in accounts_list]:
        commands = Commands(account_name)

        account_commands_array = [
            commands.open_agency_panel,
            commands.open_clients_list,
            commands.open_client_account,
        ]

        if mode == possible_modes[1]:
            account_commands_array.extend([
                commands.open_stats,
                commands.open_calendar,
                commands.select_last_week,
                commands.update,
            ])
        if mode == possible_modes[2]:
            account_commands_array.extend([
                commands.open_stats,
                commands.open_calendar,
                commands.select_last_month,
                commands.update,
            ])
        if mode == possible_modes[3]:
            account_commands_array = account_commands_array[2:]

            account_commands_array.extend([
                commands.open_stats,
                commands.open_calendar,
                commands.select_last_billing_month,
                commands.update,
                commands.select_offers_view,
                commands.click_download_report,
                commands.open_client_account, # in this situation list
            ])

        if mode == possible_modes[4]:
            account_commands_array = account_commands_array[2:]
            account_commands_array.extend([
                commands.open_files,
                commands.click_download_file,
                commands.open_client_account,  # in this situation list
            ])



        commands_array.extend(account_commands_array)

    with open('../macro.json', 'w') as f:
        json.dump(commands_array, f, ensure_ascii=False)
