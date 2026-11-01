﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('const row = {')
end_idx = code.find('};', idx)
print(repr(code[idx:end_idx]))


