﻿import pandas as pd
df = pd.read_excel(r"C:\Users\UsuarioPadrao\Downloads\Relatorio_Separado_SISTEMA_ERP_EXEMPLO (1).xlsx", sheet_name="0800")
print("0800 Dates out of range?")
print(df['Data'].head(10))

# Can we see what was painted yellow using openpyxl?
import openpyxl
wb = openpyxl.load_workbook(r"C:\Users\UsuarioPadrao\Downloads\Relatorio_Separado_SISTEMA_ERP_EXEMPLO (1).xlsx", data_only=True)
ws = wb["0800"]
yellow_rows = []
for row in ws.iter_rows(min_row=2):
    # Check fill color of the first cell
    if row[0].fill.start_color.index != '00000000' and row[0].fill.start_color.index != 0:
        yellow_rows.append((row[0].row, row[3].value, row[15].value)) # Row, Ocorrência, Diretiva

print("Yellow rows in 0800:", yellow_rows[:10])

ws2 = wb["Acompanhamento"]
yellow_rows2 = []
for row in ws2.iter_rows(min_row=2):
    if row[0].fill.start_color.index != '00000000' and row[0].fill.start_color.index != 0:
        yellow_rows2.append((row[0].row, row[3].value, row[15].value))

print("Yellow rows in Acomp:", yellow_rows2[:10])


