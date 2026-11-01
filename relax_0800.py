import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Expand has0800Dir to include emergency keywords in the Diretriz, and also allow searching description if diretriz has emergency words
logic_search = """                                    // 0800 is explicitly in Diretriz
                                    const has0800Dir = /0800|0300/i.test(dir_search) || /emerg[\u00ea]ncia/i.test(dir_search);"""

logic_replace = """                                    // 0800 is in Diretriz or is a known emergency Diretriz
                                    const has0800Dir = /0800|800|0300|300/i.test(dir_search) || /cheiro|vazamento|press[\u00e3a]o|falta de g[\u00e1a]s|inc[\u00ea]ndio|fogo|trote|emerg[\u00ea]ncia|rompimento|cliente ligou/i.test(dir_search);
                                    
                                    // Sometimes Diretriz is just something else but the falha explains it's an emergency. 
                                    // We will pull it IF it has emergency keywords in text, AS LONG AS it's NOT explicitly an acompanhamento.
                                    const is0800Text = /0800|800|0300|300|cheiro|vazamento|press[\u00e3a]o|falta de g[\u00e1a]s|inc[\u00ea]ndio|fogo|trote|emerg[\u00ea]ncia|rompimento|cliente ligou/i.test(_textToSearch);
"""

content = content.replace(logic_search, logic_replace)

logic_search2 = """                                    if (!isStrictIgnore && !isBlankDir && !isSpecialFilter) {
                                        if (has0800Dir) {
                                            is0800 = true;
                                        }
                                        if (hasAcompDir) {
                                            isAcomp = true;
                                        }
                                    }"""

logic_replace2 = """                                    if (!isStrictIgnore && !isBlankDir && !isSpecialFilter) {
                                        if (hasAcompDir) {
                                            isAcomp = true;
                                        }
                                        if (has0800Dir || (is0800Text && !hasAcompDir)) {
                                            is0800 = true;
                                        }
                                    }"""

content = content.replace(logic_search2, logic_replace2)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated 0800 logic to include emergency keywords and broader search.")


