﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('action: function ( e, dt, node, config ) {')
end = code.find('XLSX.writeFile(wb, "Relatorio_Separado_SISTEMA_ERP_EXEMPLO.xlsx");', idx)
print(code[idx:end+50])


