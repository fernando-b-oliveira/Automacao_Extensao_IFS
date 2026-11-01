﻿with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

target_start = 'data.forEach(row => {'
target_end = 'if (is0800Trigger) {'

idx_start = code.find(target_start)
idx_end = code.find(target_end, idx_start)

if idx_start != -1 and idx_end != -1:
    old_block = code[idx_start:idx_end]
    
    new_block = """data.forEach(row => {
                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();
                                    const _textToSearch = dF_search + " " + dir_search;
                                    
                                    const _techId = _getTec(row);

                                    if (_techId.includes("ERP_OPS_CORE")) return; 

                                    const isIgnoredText = /troca[r]?\\s*(de\\s*)?(sobreaviso|plant)|alarme|port[\\u00e3a]o|seguran[\\u00e7c]a|arrombamento|inspe[\\u00e7c][\\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\\u00e1a]lvula com vazamento|vazamento na uni|adequa[\\u00e7c][\\u00e3a]o|seguradora|ve[i\\u00ed]culo|viatura/i.test(_textToSearch);

                                    if (isIgnoredText) return; // Ignora as excecoes 

                                    const is0800Trigger = /0800|800|0300|300|cheiro|vazamento|press[\\u00e3a]o|falta de g[\\u00e1a]s|inc[\\u00ea]ndio|fogo|trote|emerg[\\u00ea]ncia|rompimento|cliente ligou/i.test(_textToSearch);
                                    const isAcompTrigger = dir_search.includes("acomp") || /acomp|\\u00e1guas guariroba|aguas guariroba|prefeitura|sisep|sanesul|empreiteira|escava[\\u00e7c][\\u00e3a]o|implanta[\\u00e7c][\\u00e3a]o|sondagem|drenagem|pavimenta[\\u00e7c][\\u00e3a]o|concession[\\u00e1a]ria|rede de [\\u00e1a]gua|rede de esgoto|reparo na via/i.test(_textToSearch);

                                    const osNum = _krx(row, /^N. OS$/i, "");
                                    
                                    """
    
    code = code[:idx_start] + new_block + code[idx_end:]
    
    with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
        f.write(code)
    print("Replaced filters to only check Diretiva and Descricao da Falha!")
else:
    print("Not found!")



