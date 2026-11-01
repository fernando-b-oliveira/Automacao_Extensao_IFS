﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

idx = code.find("document.getElementById('btn_iniciar').addEventListener")
with open("event_listener_out.txt", "w", encoding="utf-8") as out:
    out.write(code[idx:idx+1500])


