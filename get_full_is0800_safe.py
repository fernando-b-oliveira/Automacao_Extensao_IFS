﻿import re
with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt", "r", encoding="utf-8") as f:
    text = f.read()

match = re.search(r'const is0800Trigger = /0800\|800.*?is0800 = is0800Trigger.*?;', text, re.DOTALL)
if match:
    with open("is0800_logic.txt", "w", encoding="utf-8") as out:
        out.write(match.group(0))
    print("Saved to is0800_logic.txt")
else:
    print("Not found")


