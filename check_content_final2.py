﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content_final.js", "r", encoding="utf-8") as f:
    text = f.read()
idx = text.find('action: function')
print(text[idx:idx+1500])


