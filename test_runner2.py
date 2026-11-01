﻿import json

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('action: function ( e, dt, node, config ) {')
end = code.find('} : { extend:', idx)
action_code = code[idx:end]

test_code = """
const XLSX = { utils: { book_new: () => ({}), json_to_sheet: () => ({}), book_append_sheet: () => {} }, writeFile: () => {} };
const dt = { rows: () => ({ data: () => ({ toArray: () => [{
    "Descri\u00e7\u00e3o da Falha (Completa)": "Vazamento",
    "Descri\u00e7\u00e3o da Tarefa": "Verificar",
    "ID Funcion\u00e1rio": "TEST",
    "Status OS": "WORKDONE"
}] }) }) };

const obj = {
""" + action_code + """
};
obj.action(null, dt, null, null);
console.log("Success!");
"""

with open("test.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body><script>{test_code}</script></body></html>")
print("Done")


