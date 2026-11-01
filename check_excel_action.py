﻿import sys
import py_compile

# We can't compile JS with python, but we can search for obvious syntax errors manually.
with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('action: function ( e, dt, node, config ) {')
end = code.find('} : { extend: \'excelHtml5\'', idx)
print(code[idx:end])


