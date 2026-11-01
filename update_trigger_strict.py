import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the filter logic in both places to strictly use Diretriz for both
logic_search = """                                    // Strict exclusions that cancel everything (e.g. "sobreaviso 0800" should never be 0800)
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

logic_replace = """                                    // Exclusões estritas
                                    const isStrictIgnore = /troca[r]?\s*(de\s*)?(sobreaviso|plant)|sobreaviso 0800|troca de 0800|reuni[\u00e3a]o/i.test(dir_search) || /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);
                                    const isBlankDir = dir_search.trim() === "";

                                    // Acompanhamento is explicitly in Diretriz
                                    const hasAcompDir = /acomp/i.test(dir_search);
                                    
                                    // 0800 is explicitly in Diretriz
                                    const has0800Dir = /0800|0300/i.test(dir_search) || /emerg[\u00ea]ncia/i.test(dir_search);
                                    
                                    let is0800 = false;
                                    let isAcomp = false;
                                    
                                    if (!isStrictIgnore && !isBlankDir && !isSpecialFilter) {
                                        if (has0800Dir) {
                                            is0800 = true;
                                        }
                                        if (hasAcompDir) {
                                            isAcomp = true;
                                        }
                                    }"""

content = content.replace(logic_search, logic_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated logic strictly to dir_search.")


