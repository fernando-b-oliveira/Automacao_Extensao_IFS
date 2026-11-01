import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Modify the extraction logic for both places
def replace_logic(match):
    return """
                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();
                                    const dT_search = String(_krx(row, /Descri..o da Tarefa/i, "")).toLowerCase();
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();
                                    const _textToSearch = (dT_search + " " + dF_search + " " + dir_search).toLowerCase();
                                    
                                    const _techId = _getTec(row);
                                    const isSpecialFilter = _techId.toUpperCase().includes("ERP_OPS_CORE");

                                    // Ignore list expanded to clearly reject "sobreaviso 0800" etc.
                                    const isIgnoredText = /troca[r]?\s*(de\s*)?(sobreaviso|plant)|sobreaviso 0800|troca de 0800|alarme|port[\u00e3a]o|seguran[\u00e7c]a|arrombamento|inspe[\u00e7c][\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\u00e1a]lvula com vazamento|vazamento na uni|adequa[\u00e7c][\u00e3a]o|seguradora|ve[i\u00ed]culo|patrulheiro|preventiva|prevpeq|calibrar/i.test(_textToSearch);

                                    // 0800 trigger: must have 0800, cheiro, vazamento, etc.
                                    const is0800Trigger = /0800|800|0300|300|cheiro|vazamento|press[\u00e3a]o|falta de g[\u00e1a]s|inc[\u00ea]ndio|fogo|trote|emerg[\u00ea]ncia|rompimento|cliente ligou/i.test(_textToSearch);
                                    
                                    // Acompanhamento trigger: user requested ONLY items with "acomp" in name
                                    const isAcompTrigger = /acomp/i.test(_textToSearch);

                                    const tipoManut = String(_krx(row, /Tipo de Manuten/i, "")).toUpperCase();
                                    const isPlanned = (tipoManut === "PREV" || tipoManut === "COPR" || tipoManut === "CONP") && !/0800|0300|300|800/i.test(_textToSearch);
                                    const isManutencaoCompleta = /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);

                                    const is0800 = is0800Trigger && !isIgnoredText && !isPlanned && !isManutencaoCompleta && !isSpecialFilter;
                                    const isAcomp = isAcompTrigger && !isIgnoredText && !isSpecialFilter;
"""

# Replace the first block
content = re.sub(r'(\s+const dF_search = String\(_krx\(row,\s*/Descri\.\.o da Falha/i.*?const isAcomp = isAcompTrigger && !isSpecialFilter;)', replace_logic, content, flags=re.DOTALL)

# Add logic to check for window.selectedTypes
block = """
                                const wb = XLSX.utils.book_new();
                                if(data0800.length > 0) XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data0800), "0800");
                                if(dataAcomp.length > 0) XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataAcomp), "Acompanhamento");
                                
                                // O usu\u00e1rio pediu que 'Dados Brutos' tenha apenas as linhas que foram de 0800 ou Acomp (misturadas, mas apenas o alvo)
                                const dataBrutosAlvo = data.filter(row => {"""

replacement_block = """
                                const wb = XLSX.utils.book_new();
                                const isRawOnly = (!window.selectedTypes.do0800 && !window.selectedTypes.doAcomp);
                                
                                if (isRawOnly) {
                                    // Se os dois tiverem desmarcados, puxa todas as colunas brutas (absolutamente todas)
                                    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data), "Dados Brutos Completos");
                                } else {
                                    if(data0800.length > 0 && window.selectedTypes.do0800) XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data0800), "0800");
                                    if(dataAcomp.length > 0 && window.selectedTypes.doAcomp) XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataAcomp), "Acompanhamento");
                                    
                                    const dataBrutosAlvo = data.filter(row => {"""

content = content.replace(block, replacement_block)

block2 = """
                                    return is0800 || isAcomp;
                                });
                                XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataBrutosAlvo), "Dados Brutos");


                                XLSX.writeFile(wb, "Relatorio_Separado_SISTEMA_ERP_EXEMPLO.xlsx");"""

replacement_block2 = """
                                    return (is0800 && window.selectedTypes.do0800) || (isAcomp && window.selectedTypes.doAcomp);
                                    });
                                    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataBrutosAlvo), "Dados Brutos");
                                }

                                XLSX.writeFile(wb, "Relatorio_Separado_SISTEMA_ERP_EXEMPLO.xlsx");"""

content = content.replace(block2, replacement_block2)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Modified content.js successfully.")



