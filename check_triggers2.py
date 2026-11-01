﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\excel_logic_found3.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(110, 140):
    if i < len(lines):
        print(f"{i}: {lines[i].strip()}")


