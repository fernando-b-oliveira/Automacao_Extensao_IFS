﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

target = """                                    if (is0800Trigger) {
                                        data0800.push(_make0800(row));
                                    } else if (isAcompTrigger) {
                                        dataAcomp.push(_makeAcomp(row));
                                    }"""

if target in code:
    replacement = """
                                    const osNum = _krx(row, /^N. OS$/i, "");
                                    
                                    if (is0800Trigger) {
                                        if (osNum && !osVistas0800.has(osNum)) {
                                            osVistas0800.add(osNum);
                                            data0800.push(_make0800(row));
                                        }
                                    } 
                                    if (isAcompTrigger) {
                                        dataAcomp.push(_makeAcomp(row));
                                    }"""
    code = code.replace(target, replacement)
    
    # Need to declare osVistas0800 at the top of action
    code = code.replace('const dataAcomp = [];', 'const dataAcomp = [];\n                                const osVistas0800 = new Set();')
    
    with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
        f.write(code)
    print("Replaced with non-else-if and added deduplication!")
else:
    print("Target not found! Searching for alternative...")


