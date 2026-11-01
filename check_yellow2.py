﻿import openpyxl
wb = openpyxl.load_workbook(r"C:\Users\UsuarioPadrao\Downloads\Relatorio_Separado_SISTEMA_ERP_EXEMPLO (1).xlsx", data_only=True)
ws = wb["0800"]
yellow_rows = []
for row in ws.iter_rows(min_row=2):
    # Check fill color of any cell
    is_yellow = any(cell.fill.start_color.index != '00000000' and cell.fill.start_color.index != 0 for cell in row)
    if is_yellow:
        yellow_rows.append((row[0].row, row[1].value, row[13].value, row[15].value))

print("Yellow rows in 0800:", yellow_rows[:10])

ws2 = wb["Acompanhamento"]
yellow_rows2 = []
for row in ws2.iter_rows(min_row=2):
    is_yellow = any(cell.fill.start_color.index != '00000000' and cell.fill.start_color.index != 0 for cell in row)
    if is_yellow:
        yellow_rows2.append((row[0].row, row[1].value, row[13].value, row[15].value))

print("Yellow rows in Acomp:", yellow_rows2[:10])


