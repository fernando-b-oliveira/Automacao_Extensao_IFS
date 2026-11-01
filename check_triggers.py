﻿import re
with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\excel_logic_found3.txt", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split('\n')
for i, line in enumerate(lines):
    if 'is0800' in line or 'isAcomp' in line:
        print(f"{i}: {line.strip()}")


