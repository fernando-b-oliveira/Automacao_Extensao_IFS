﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('window.masterData =')
if idx != -1:
    print(code[idx-500:idx+500])
else:
    print("masterData not found")


