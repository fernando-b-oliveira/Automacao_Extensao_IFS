﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()
if 'fDataFim' in code:
    print("fDataFim IS in code!")
else:
    print("fDataFim IS NOT in code!")


