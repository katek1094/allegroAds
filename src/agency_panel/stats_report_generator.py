from openpyxl import Workbook


class StatsReportGenerator:
    def __init__(self, stats: list):
        for account_stats in stats:
            self.generate_stats_for_account(account_stats)

    def generate_stats_for_account(self, account_stats):
        wb = Workbook()
        ws = wb.active  # TODO: change sheet name
        self.write_column_labels(ws)
        row = 2
        col = 1


    def write_column_labels(self, ws):
        pass  # TODO: write this
