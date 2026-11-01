﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("textoGeral_out.txt", "w", encoding="utf-8") as out:
    for i in range(1682, 1695):
        if i < len(lines):
            out.write(lines[i])


