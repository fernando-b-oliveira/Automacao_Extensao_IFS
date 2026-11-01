﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Find the exact click handler and inject isFiltroDuplo logic
target = "if(fData) filterDateApontamento = fData + \"T00:00:00Z\";\n\n                document.body.innerHTML = `"

injection = """if(fData) filterDateApontamento = fData + "T00:00:00Z";

                const do0800 = document.getElementById('chk_0800')?.checked ?? true;
                const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;
                window.isFiltroDuplo = do0800 && doAcomp;
                window.selectedTypes = { do0800: do0800, doAcomp: doAcomp };

                document.body.innerHTML = `"""

if target in code:
    code = code.replace(target, injection, 1)
    print("Fix 2 applied!")
else:
    print("Not found. Checking context...")
    idx = code.find("filterDateApontamento = fData")
    print(repr(code[idx:idx+200]))

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved!")


