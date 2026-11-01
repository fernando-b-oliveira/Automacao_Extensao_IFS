﻿import json
with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find('const masterData = clockings.map')
if idx != -1:
    end_idx = code.find('return {', idx)
    end_obj = code.find('};', end_idx)
    print("masterData row:")
    print(code[end_idx:end_obj+2])


