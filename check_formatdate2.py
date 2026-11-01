﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()
import re
match = re.search(r'function format.*?\([\s\S]*?\}', code)
if match:
    print(match.group(0))
else:
    print("not found format date")


