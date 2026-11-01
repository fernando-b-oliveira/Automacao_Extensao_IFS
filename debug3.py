﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# The setTimeout is at around 26800. Find the start of it.
pos_listener = 26863
# Go backwards to find the start of setTimeout
start = code.rfind('setTimeout', 0, pos_listener)
print(f"setTimeout at: {start}")
print(repr(code[start:start+200]))


