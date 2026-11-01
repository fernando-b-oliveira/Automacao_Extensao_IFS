﻿with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix date filter
target_date_ui = """                const fData = document.getElementById('filtro_data_inicio').value;
                if(fData) filterDateApontamento = fData + "T00:00:00Z";"""

new_date_ui = """                const fData = document.getElementById('filtro_data_inicio').value;
                if(fData) filterDateApontamento = fData + "T00:00:00Z";
                const fDataFim = document.getElementById('filtro_data_fim').value;
                if(fDataFim) window.filterDateFim = fDataFim + "T23:59:59Z";
                else window.filterDateFim = null;"""

code = code.replace(target_date_ui, new_date_ui)

target_url = """const urlClockings = `/main/ifsapplications/projection/v1/WorkTaskClockingsHandling.svc/JtTaskClockingSet?$filter=StartTime%20ge%20${filterDateApontamento}`;"""
new_url = """let urlClockings = `/main/ifsapplications/projection/v1/WorkTaskClockingsHandling.svc/JtTaskClockingSet?$filter=StartTime%20ge%20${filterDateApontamento}`;
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                }"""
code = code.replace(target_url, new_url)

# 2. Fix Dados Brutos only containing 0800 and Acomp
target_action = "XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data), \"Dados Brutos\");"
new_action = """
                                // O usuário pediu que 'Dados Brutos' tenha apenas as linhas que foram de 0800 ou Acomp (misturadas, mas apenas o alvo)
                                const dataBrutosAlvo = data.filter(row => {
                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();
                                    const dir_search = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();
                                    const _textToSearch = dF_search + " " + dir_search;
                                    const _techId = _getTec(row);
                                    if (_techId.includes("ERP_OPS_CORE")) return false;
                                    const isIgn = /troca[r]?\\s*(de\\s*)?(sobreaviso|plant)|alarme|port[\\u00e3a]o|seguran[\\u00e7c]a|arrombamento|inspe[\\u00e7c][\\u00e3a]o|inspeq|telemetria|hidrojato|brigada|pintura|ppu|descompress[\\u00e3a]o|cadeado|monitorar|sanar vazamento|verificar press[\\u00e3a]o|verificar vazamento|gaseificar|corte -|encerramento de|simulado|reuni[\\u00e3a]o|produzir aste|quem te ligou|^teste$|teste com modelo|descriiongs|retirada de vazamento|instalar registrador|abrir v[\\u00e1a]lvula|vazamento na conex|vazamento no corpo|vazamento na tampa|v[\\u00e1a]lvula com vazamento|vazamento na uni|adequa[\\u00e7c][\\u00e3a]o|seguradora|ve[i\\u00ed]culo|viatura/i.test(_textToSearch);
                                    if (isIgn) return false;
                                    const is08 = /0800|800|0300|300|cheiro|vazamento|press[\\u00e3a]o|falta de g[\\u00e1a]s|inc[\\u00ea]ndio|fogo|trote|emerg[\\u00ea]ncia|rompimento|cliente ligou/i.test(_textToSearch);
                                    const isAc = dir_search.includes("acomp") || /acomp|\\u00e1guas guariroba|aguas guariroba|prefeitura|sisep|sanesul|empreiteira|escava[\\u00e7c][\\u00e3a]o|implanta[\\u00e7c][\\u00e3a]o|sondagem|drenagem|pavimenta[\\u00e7c][\\u00e3a]o|concession[\\u00e1a]ria|rede de [\\u00e1a]gua|rede de esgoto|reparo na via/i.test(_textToSearch);
                                    return is08 || isAc;
                                });
                                XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataBrutosAlvo), "Dados Brutos");
"""
code = code.replace(target_action, new_action)

# Fix double replace if it happened
with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Applied date filter and restricted Dados Brutos to matching rows!")



