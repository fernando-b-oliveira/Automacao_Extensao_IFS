﻿import re
with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt", "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r'const textoGeral = \([\s\S]*?\);', text)
if match:
    with open("textoGeral_out.txt", "w", encoding="utf-8") as out:
        out.write(match.group(0))
else:
    print("textoGeral not found")


