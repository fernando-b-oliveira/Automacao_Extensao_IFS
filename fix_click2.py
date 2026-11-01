﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the exact pattern
target = 'filterDateApontamento = fData + "T00:00:00Z";\n\n                \n\n                document.body.innerHTML = `'
replacement = '''filterDateApontamento = fData + "T00:00:00Z";

                const do0800 = document.getElementById('chk_0800')?.checked ?? true;
                const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;
                window.isFiltroDuplo = do0800 && doAcomp;
                window.selectedTypes = { do0800: do0800, doAcomp: doAcomp };

                document.body.innerHTML = `'''

if target in code:
    code = code.replace(target, replacement, 1)
    print("Fix applied!")
else:
    # Just inject the lines before document.body.innerHTML
    pos = code.find('document.body.innerHTML = `\n\n                    <div style="font-family: \'Segoe UI\', sans-serif; background: #fff; min')
    if pos > 0:
        inject = """const do0800 = document.getElementById('chk_0800')?.checked ?? true;
                const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;
                window.isFiltroDuplo = do0800 && doAcomp;
                window.selectedTypes = { do0800: do0800, doAcomp: doAcomp };

                """
        code = code[:pos] + inject + code[pos:]
        print("Injected before body.innerHTML!")
    else:
        print("STILL NOT FOUND")

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved!")


