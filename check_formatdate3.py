﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()
idx = code.find('function formatDate')
if idx == -1:
    idx = code.find('const formatDate')
print(code[idx:idx+400])


