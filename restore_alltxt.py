﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

target = """                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();
                                    const _textToSearch = dF_search + " " + dir_search;"""

replacement = """                                    const _allTxt = Object.values(row).join(" ").toLowerCase();
                                    const _textToSearch = _allTxt;
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();"""

if target in code:
    code = code.replace(target, replacement)
    with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
        f.write(code)
    print("Restored full row search!")
else:
    print("Not found.")


