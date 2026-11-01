﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('const _make0800')
idx2 = code.find('data.forEach(row => {')
end = code.find('const wb = XLSX.utils', idx2)
print(code[idx2:end])


