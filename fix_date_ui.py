﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

import re
code = re.sub(
    r"const fData = document\.getElementById\('filtro_data_inicio'\)\.value;\s+if\(fData\) filterDateApontamento = fData \+ \"T00:00:00Z\";",
    "const fData = document.getElementById('filtro_data_inicio').value;\n                if(fData) filterDateApontamento = fData + \"T00:00:00Z\";\n                const fDataFim = document.getElementById('filtro_data_fim').value;\n                if(fDataFim) window.filterDateFim = fDataFim + \"T23:59:59Z\";\n                else window.filterDateFim = null;",
    code
)

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed date UI!")


