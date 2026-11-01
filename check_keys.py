﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Check what the actual key text looks like in the make0800 function
idx = code.find('_make0800')
segment = code[idx:idx+1500]
print(repr(segment[:500]))


