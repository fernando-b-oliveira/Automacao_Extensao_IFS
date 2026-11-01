﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

target = """                                    const _allTxt = Object.values(row).join(" ").toLowerCase();
                                    const _textToSearch = _allTxt;
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();"""

replacement = """                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();
                                    const dT_search = String(_krx(row, /Descri..o da Tarefa/i, "")).toLowerCase();
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();
                                    const _textToSearch = dF_search + " " + dT_search + " " + dir_search;"""

if target in code:
    code = code.replace(target, replacement)
    
    # Fix the regexes to avoid false positives!
    old_ign = "/troca[r]?\\s*(de\\s*)?(sobreaviso|plant)|alarme|port[\\u00e3a]o|seguran[\\u00e7c]a|arrombamento|inspe[\\u00e7c][\\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\\u00e1a]lvula com vazamento|vazamento na uni|adequa[\\u00e7c][\\u00e3a]o|seguradora|ve[i\\u00ed]culo|viatura/i"
    new_ign = "/troca[r]?\\s*(de\\s*)?(sobreaviso|plant)|alarme|port[\\u00e3a]o|seguran[\\u00e7c]a|arrombamento|inspe[\\u00e7c][\\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\\u00e1a]lvula com vazamento|vazamento na uni|adequa[\\u00e7c][\\u00e3a]o|seguradora|ve[i\\u00ed]culo|viatura|bancada|calib|end-point/i"
    code = code.replace(old_ign, new_ign)
    
    old_0800 = "/0800|800|0300|300|cheiro|vazamento|press[\\u00e3a]o|falta de g[\\u00e1a]s|inc[\\u00ea]ndio|fogo|trote|emerg[\\u00ea]ncia|rompimento|cliente ligou/i"
    new_0800 = "/\\b0800\\b|\\b800\\b|\\b0300\\b|\\b300\\b|\\bcheiro\\b|vazamento|\\bpress[\\u00e3a]o\\b|falta de g[\\u00e1a]s|inc[\\u00ea]ndio|fogo|trote|emerg[\\u00ea]ncia|rompimento|cliente ligou/i"
    code = code.replace(old_0800, new_0800)
    
    # ensure it is applied properly for Brutos too!
    code = code.replace("const _textToSearch = dF_search + \" \" + dir_search;", "const dT_search = String(_krx(row, /Descri..o da Tarefa/i, \"\")).toLowerCase();\n                                    const _textToSearch = dF_search + \" \" + dT_search + \" \" + dir_search;")
    code = code.replace(old_ign, new_ign)
    code = code.replace(old_0800, new_0800)
    
    with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
        f.write(code)
    print("Replaced and tightened filters!")
else:
    print("Not found.")


