﻿with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the entire action block with a fail-safe one
target_start = "action: function ( e, dt, node, config ) {"
target_end = "XLSX.writeFile(wb, \"Relatorio_Separado_SISTEMA_ERP_EXEMPLO.xlsx\");"

idx_start = code.find(target_start)
idx_end = code.find(target_end, idx_start)

if idx_start != -1 and idx_end != -1:
    end_of_block = idx_end + len(target_end)
    # also include the closing bracket and comma if they exist
    while code[end_of_block] in ['\n', '\r', ' ', '\t']:
        end_of_block += 1
    if code[end_of_block] == '}':
        end_of_block += 1
        
    old_block = code[idx_start:end_of_block]
    
    new_block = """action: function ( e, dt, node, config ) {
                            try {
                                const data = dt.rows({ search: 'applied' }).data().toArray();
                                const data0800 = [];
                                const dataAcomp = [];

                                let _seq = 0;

                                const _calcDur = (h1, h2) => {
                                    if (!h1 || !h2) return "";
                                    try {
                                        const p = s => { const [h,m] = String(s).split(':').map(Number); return (h||0)*60+(m||0); };
                                        let d = p(h2) - p(h1); if (d < 0) d += 1440;
                                        return Math.floor(d/60) + ':' + String(d%60).padStart(2,'0');
                                    } catch(err) { return ""; }
                                };

                                const _krx = (row, rx, fallback) => {
                                    const k = Object.keys(row).find(key => rx.test(key));
                                    return k ? row[k] : fallback;
                                };

                                const _getTec = (row) => {
                                    const val = _krx(row, /^ID Funcion.rio$/i, null) || _krx(row, /Funcion.rio/i, null) || row["[Clocking] CreatedBy"] || row["[Task] ExecutedBy"] || "";
                                    return String(val).toUpperCase();
                                };

                                const _transSit = (s) => {
                                    const m = {"WORKDONE":"Trabalho Realizado","FINISHED":"Finalizado","RELEASED":"Liberado","STARTED":"Iniciado","CANCELED":"Cancelado","Historical":"Hist\\u00f3rico","PREPARED":"Preparado","REPORTED":"Reportado"};
                                    return m[s] || s || "";
                                };

                                const _ext = (txt, pat) => { const m = String(txt).match(pat); return m ? m[1].trim() : ''; };

                                const _make0800 = (row) => {
                                    _seq++;
                                    const dF = String(_krx(row, /Descri..o da Falha/i, ""));
                                    const dT = String(_krx(row, /Descri..o da Tarefa/i, ""));
                                    const all = dF + " | " + dT;
                                    const hI = String(_krx(row, /^Hora In.cio$/i, ""));
                                    const hF = String(_krx(row, /^Hora Fim$/i, ""));
                                    const chegada = _ext(all, /Cheg(?:ada|uei)[^\\d]*([\\d]{2}:[\\d]{2})/i) || hI;
                                    const conclusao = _ext(all, /T[e\\u00ea]rmino[^:]*:\\s*([\\d:]+)/i) || _ext(all, /Finalizado[^\\d]*([\\d]{2}:[\\d]{2})/i) || hF;
                                    const local = _ext(all, /Endere[\\u00e7c]o:\\s*([^|]+)/i) || _ext(all, /Local:\\s*([^|]+)/i) || row["[OS] MchCodeDescription"] || "";
                                    const cliente = _ext(all, /(?:Cliente|Empresa|Condom\\u00ednio|Edif\\u00edcio):\\s*([^|]+)/i);
                                    const autor = _ext(all, /Autor[:]?\\s*([^|]+)/i) || _ext(all, /Respons\\u00e1vel[:]?\\s*([^|]+)/i);
                                    const tel = _ext(all, /(?:Tel|Fone|Celular)[.\\s]?(?:Autor)?[:\\s]?((?:[\\d\\s\\(\\)\\-]){7,})/i);
                                    const ocorr = _ext(all, /Ocorr[e\\u00ea]ncia[:]?\\s*([^|]+)/i) || dT.split('|')[0].trim();
                                    
                                    const obj = {
                                        "Dados/Sequ\\u00eancia": _seq,
                                        "Data": _krx(row, /^Data In.cio$/i, ""),
                                        "N\\u00ba Ordem": _krx(row, /^N. OS$/i, ""),
                                        "Hora chamada": hI,
                                        "Cliente": cliente,
                                        "Autor": autor,
                                        "Tel. Autor": tel,
                                        "Local": local,
                                        "T\\u00e9cnico": _getTec(row),
                                        "Ocorr\\u00eancia": ocorr,
                                        "chegada": chegada,
                                        "at\\u00e9": conclusao,
                                        "Tempo de trabalho": _calcDur(chegada, conclusao),
                                        "Descri\\u00e7\\u00e3o": dF,
                                        "Situa\\u00e7\\u00e3o": _transSit(_krx(row, /^Status OS$/i, "")),
                                        "Diretiva": _krx(row, /^Diretiva$/i, "")
                                    };
                                    const miss = !obj["N\\u00ba Ordem"] || !obj["T\\u00e9cnico"] || !obj["Local"];
                                    if (miss) obj["[ AVISO ]"] = "\\u26a0\\ufe0f FALTAM DADOS NESSA LINHA";
                                    return obj;
                                };

                                const _makeAcomp = (row) => {
                                    _seq++;
                                    const dF = String(_krx(row, /Descri..o da Falha/i, ""));
                                    const dT = String(_krx(row, /Descri..o da Tarefa/i, ""));
                                    const all = dF + " | " + dT;
                                    const hI = String(_krx(row, /^Hora In.cio$/i, ""));
                                    const hF = String(_krx(row, /^Hora Fim$/i, ""));
                                    const chegada = _ext(all, /Cheg(?:ada|uei)[^\\d]*([\\d]{2}:[\\d]{2})/i) || hI;
                                    const conclusao = _ext(all, /T[e\\u00ea]rmino[^:]*:\\s*([\\d:]+)/i) || _ext(all, /Finalizado[^\\d]*([\\d]{2}:[\\d]{2})/i) || hF;
                                    const local = _ext(all, /Endere[\\u00e7c]o:\\s*([^|]+)/i) || _ext(all, /Local:\\s*([^|]+)/i) || row["[OS] MchCodeDescription"] || "";
                                    const cliente = _ext(all, /(?:Cliente|Empresa):\\s*([^|]+)/i);
                                    
                                    const obj = {
                                        "Dados/Sequ\\u00eancia": _seq,
                                        "Data": _krx(row, /^Data In.cio$/i, ""),
                                        "N\\u00ba Ordem": _krx(row, /^N. OS$/i, ""),
                                        "Hora chamada": hI,
                                        "Cliente": cliente,
                                        "Local": local,
                                        "T\\u00e9cnico": _getTec(row),
                                        "chegada": chegada,
                                        "at\\u00e9": conclusao,
                                        "Tempo de trabalho": _calcDur(chegada, conclusao),
                                        "Descri\\u00e7\\u00e3o": dF,
                                        "Situa\\u00e7\\u00e3o": _transSit(_krx(row, /^Status OS$/i, "")),
                                        "Diretiva": _krx(row, /^Diretiva$/i, "")
                                    };
                                    const miss = !obj["N\\u00ba Ordem"] || !obj["T\\u00e9cnico"];
                                    if (miss) obj["[ AVISO ]"] = "\\u26a0\\ufe0f FALTAM DADOS NESSA LINHA";
                                    return obj;
                                };

                                data.forEach(row => {
                                    const _allTxt = Object.values(row).join(" ").toLowerCase();
                                    const _dirTxt = String(_krx(row, /^Diretiva$/i, "")).toLowerCase();
                                    const _techId = _getTec(row);

                                    if (_techId.includes("ERP_OPS_CORE")) return; 

                                    const is0800Trigger = /0800|0300|\\bvazamento\\b|\\bcheiro\\b|press\\u00e3o|pressao|falta de g\\u00e1s|falta de gas|inc\\u00eandio|incendio|\\bfogo\\b|emerg\\u00eancia|emergencia|rompimento|cliente ligou/i.test(_allTxt);
                                    const isAcompTrigger = _dirTxt.includes("acomp") || /acompanhamento|escava\\u00e7\\u00e3o|implanta\\u00e7\\u00e3o|sondagem|drenagem|pavimenta\\u00e7\\u00e3o|concession\\u00e1ria|\\u00e1guas guariroba|aguas guariroba/i.test(_allTxt);

                                    if (is0800Trigger) {
                                        data0800.push(_make0800(row));
                                    } else if (isAcompTrigger) {
                                        dataAcomp.push(_makeAcomp(row));
                                    }
                                });

                                const wb = XLSX.utils.book_new();
                                if(data0800.length > 0) XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data0800), "0800");
                                if(dataAcomp.length > 0) XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataAcomp), "Acompanhamento");
                                XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data), "Dados Brutos");

                                XLSX.writeFile(wb, "Relatorio_Separado_SISTEMA_ERP_EXEMPLO.xlsx");
                            } catch (error) {
                                alert("Erro ao gerar Excel: " + error.message);
                                console.error(error);
                            }
                        }"""
    code = code[:idx_start] + new_block + code[end_of_block:]
    
    with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
        f.write(code)
    print("Action block successfully rewritten!")
else:
    print("Could not find the target bounds.")



