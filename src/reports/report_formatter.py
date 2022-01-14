from openpyxl import load_workbook

# MONTHLY REPORT FORMATTER

from os import listdir

reports_path = '/home/kajetan/Documents/pryzmat/reports'
filenames = listdir(reports_path)

for filename in filenames:
    file_path = reports_path + '/' + filename
    wb = load_workbook(filename=file_path)
    stats_sheet_name = 'Statystyk_2021-11-26_2021-12-25'  # TODO: make it reactive for current date
    del wb[stats_sheet_name]
    ws = wb.active
    ws.delete_cols(1, 2)
    wb.save(file_path)
