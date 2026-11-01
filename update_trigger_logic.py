import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the filter logic in both places
logic_search = """                                    const isIgnoredText = /troca[r]?\s*(de\s*)?(sobreaviso|plant)|sobreaviso 0800|troca de 0800|alarme|port[\u00e3a]o|seguran[\u00e7c]a|arrombamento|inspe[\u00e7c][\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\u00e1a]lvula com vazamento|vazamento na uni|adequa[\u00e7c][\u00e3a]o|seguradora|ve[i\u00ed]culo|patrulheiro|preventiva|prevpeq|calibrar/i.test(_textToSearch);

                                    // 0800 trigger: must have 0800, cheiro, vazamento, etc.
                                    const is0800Trigger = /0800|800|0300|300|cheiro|vazamento|press[\u00e3a]o|falta de g[\u00e1a]s|inc[\u00ea]ndio|fogo|trote|emerg[\u00ea]ncia|rompimento|cliente ligou/i.test(_textToSearch);
                                    
                                    // Acompanhamento trigger: user requested ONLY items with "acomp" in name
                                    const isAcompTrigger = /acomp/i.test(_textToSearch);

                                    const tipoManut = String(_krx(row, /Tipo de Manuten/i, "")).toUpperCase();
                                    const isPlanned = (tipoManut === "PREV" || tipoManut === "COPR" || tipoManut === "CONP") && !/0800|0300|300|800/i.test(_textToSearch);
                                    const isManutencaoCompleta = /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);
                                    
                                    const isBlankDir = dir_search.trim() === "";

                                    const is0800 = is0800Trigger && !isIgnoredText && !isPlanned && !isManutencaoCompleta && !isSpecialFilter && !isBlankDir;
                                    const isAcomp = isAcompTrigger && !isSpecialFilter && !isBlankDir;"""

logic_replace = """                                    // Strict exclusions that cancel everything (e.g. "sobreaviso 0800" should never be 0800)
                                    const isStrictIgnore = /troca[r]?\s*(de\s*)?(sobreaviso|plant)|sobreaviso 0800|troca de 0800|reuni[\u00e3a]o/i.test(dir_search) || /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);
                                    const isBlankDir = dir_search.trim() === "";

                                    // Acompanhamento is explicitly in Diretriz
                                    const hasAcompDir = /acomp/i.test(dir_search);
                                    
                                    // 0800 is explicitly in Diretriz
                                    const has0800Dir = /0800|800|0300|300/i.test(dir_search);
                                    
                                    // Alternative emergency triggers if diretriz is weak (optional, but requested focus on diretriz)
                                    const isEmerg = /cheiro|vazamento|press[\u00e3a]o|falta de g[\u00e1a]s|inc[\u00ea]ndio|fogo|trote|emerg[\u00ea]ncia|rompimento|cliente ligou/i.test(dir_search) || /cheiro|vazamento/i.test(dF_search);
                                    
                                    let is0800 = false;
                                    let isAcomp = false;
                                    
                                    if (!isStrictIgnore && !isBlankDir && !isSpecialFilter) {
                                        if (has0800Dir || isEmerg) {
                                            is0800 = true;
                                        }
                                        if (hasAcompDir) {
                                            isAcomp = true;
                                        }
                                    }"""

content = content.replace(logic_search, logic_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated trigger logic based on Diretriz.")



