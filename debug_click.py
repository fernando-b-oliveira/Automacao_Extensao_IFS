﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Find the click handler for btn_iniciar
idx = code.find("document.getElementById('btn_iniciar').addEventListener")
print(f"Found at {idx}: {repr(code[idx:idx+200])}")


