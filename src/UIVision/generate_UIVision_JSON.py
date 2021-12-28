import json

from .commands import Commands

possible_modes = (
    'campaigns',
    'last_week'
)


def generate_json_script(mode: str, accounts_list: list):
    if mode not in possible_modes:
        raise ValueError(f'mode : "{mode}" is not allowed. Please select from one of possible modes: {possible_modes}')

    commands_array = []

    for account_name in accounts_list:
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
        commands_array.extend(account_commands_array)

    with open('../../macro.json', 'w', encoding='utf-8') as f:
        json.dump(commands_array, f)
