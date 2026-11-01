﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'textoGeral =' in line or 'textoGeral' in line:
        print(f"{i}: {line.strip()}")


