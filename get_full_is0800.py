﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt", "r", encoding="utf-8") as f:
    text = f.read()
import re
match = re.search(r'const is0800Trigger = /0800\|800.*?is0800 = is0800Trigger.*?;', text, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("Not found")


