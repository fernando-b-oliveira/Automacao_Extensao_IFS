﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Find ALL btn_iniciar occurrences
idx = 0
while True:
    pos = code.find("btn_iniciar", idx)
    if pos == -1:
        break
    print(f"pos {pos}: {repr(code[max(0,pos-50):pos+60])}")
    idx = pos + 1


