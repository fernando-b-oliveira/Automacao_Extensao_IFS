﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('function processarDados')
if idx == -1:
    idx = code.find('processarDados')
print(code[idx:idx+2500])


