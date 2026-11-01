﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\excel_logic_found3.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("lines_out.txt", "w", encoding="utf-8") as out:
    for i in range(100, 140):
        if i < len(lines):
            out.write(f"{i}: {lines[i].strip()}\n")


