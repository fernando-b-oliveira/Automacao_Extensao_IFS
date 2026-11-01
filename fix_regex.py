﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("inc[\\u00eandio", "inc[\\u00ea]ndio")
code = code.replace("emerg[\\u00eancia", "emerg[\\u00ea]ncia")

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed regex syntax!")


