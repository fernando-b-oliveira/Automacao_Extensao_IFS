﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

target = 'const is0800Trigger = /0800|0300|\\bvazamento\\b|\\bcheiro\\b|press\\u00e3o|pressao|falta de g\\u00e1s|falta de gas|inc\\u00eandio|incendio|\\bfogo\\b|emerg\\u00eancia|emergencia|rompimento|cliente ligou/i.test(_allTxt);'

if target in code:
    replacement = """
                                    const is0800Trigger = /0800|800|0300|300|cheiro|vazamento|press[\\u00e3a]o|falta de g[\\u00e1a]s|inc[\\u00eandio|fogo|trote|emerg[\\u00eancia|rompimento|cliente ligou/i.test(_allTxt);
                                    const isAcompTrigger = _dirTxt.includes("acomp") || /acomp|\\u00e1guas guariroba|aguas guariroba|prefeitura|sisep|sanesul|empreiteira|escava[\\u00e7c][\\u00e3a]o|implanta[\\u00e7c][\\u00e3a]o|sondagem|drenagem|pavimenta[\\u00e7c][\\u00e3a]o|concession[\\u00e1a]ria|rede de [\\u00e1a]gua|rede de esgoto|reparo na via/i.test(_allTxt);
                                    const isIgnoredText = /troca[r]?\\s*(de\\s*)?(sobreaviso|plant)|alarme|port[\\u00e3a]o|seguran[\\u00e7c]a|arrombamento|inspe[\\u00e7c][\\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\\u00e1a]lvula com vazamento|vazamento na uni|adequa[\\u00e7c][\\u00e3a]o|seguradora|ve[\\u00ed\\i]culo/i.test(_allTxt);

                                    if (isIgnoredText) return; // Ignora as excecoes 
"""
    # Replace is0800Trigger and the next line (isAcompTrigger)
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if 'const is0800Trigger =' in line:
            lines[i] = replacement
            lines[i+1] = '' # clear old isAcompTrigger
            break
    code = '\n'.join(lines)
    
    with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
        f.write(code)
    print("Replaced filters!")
else:
    print("Not found!")


