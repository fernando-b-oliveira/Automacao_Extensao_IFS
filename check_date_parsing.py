﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('const _make0800')
idx2 = code.find('return {', idx)
end = code.find('};', idx2)
print(code[idx2:end])


