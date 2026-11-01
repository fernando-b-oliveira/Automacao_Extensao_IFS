﻿import re
with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt", "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r'const textoGeral =.*?;', text)
if match:
    print(match.group(0))
else:
    print("textoGeral not found")


