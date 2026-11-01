﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\excel_logic_found3.txt", "r", encoding="utf-8") as f:
    text = f.read()
    
idx = text.find("const isIgnored = ")
end = text.find("ve[", idx)
print(text[idx:end+15])


