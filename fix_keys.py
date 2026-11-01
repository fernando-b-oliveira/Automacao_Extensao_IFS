﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the _make0800 and _makeAcomp functions to use dynamic keys
target = '                            const _make0800 = (row) => {'
idx = code.find(target)

if idx != -1:
    end_idx = code.find('// ======= FIM HELPERS =======', idx)
    
    new_helpers = """                            const _k = (row, search) => Object.keys(row).find(k => k.toLowerCase().includes(search.toLowerCase())) || search;
                            
                            const _make0800 = (row) => {
                                _seq++;
                                const dF = row[_k(row, "Falha")] || "";
                                const dT = row[_k(row, "Tarefa")] || "";
                                const all = dF + " | " + dT;
                                const hI = row[_k(row, "Hora In")] || "";
                                const hF = row[_k(row, "Hora Fim")] || "";
                                const chegada = _ext(all, /Cheg(?:ada|uei)[^\\d]*([\\d]{2}:[\\d]{2})/i) || hI;
                                const conclusao = _ext(all, /T[e\\u00ea]rmino[^:]*:\\s*([\\d:]+)/i) || _ext(all, /Finalizado[^\\d]*([\\d]{2}:[\\d]{2})/i) || hF;
                                const local = _ext(all, /Endere[\\u00e7c]o:\\s*([^|]+)/i) || _ext(all, /Local:\\s*([^|]+)/i) || row["[OS] MchCodeDescription"] || "";
                                const cliente = _ext(all, /(?:Cliente|Empresa|Condom\\u00ednio|Edif\\u00edcio):\\s*([^|]+)/i);
                                const autor = _ext(all, /Autor[:]?\\s*([^|]+)/i) || _ext(all, /Respons\\u00e1vel[:]?\\s*([^|]+)/i);
                                const tel = _ext(all, /(?:Tel|Fone|Celular)[.\\s]?(?:Autor)?[:\\s]?((?:[\\d\\s\\(\\)\\-]){7,})/i);
                                const ocorr = _ext(all, /Ocorr[e\\u00ea]ncia[:]?\\s*([^|]+)/i) || dT.split('|')[0].trim();
                                
                                const obj = {
                                    "Dados/Sequ\\u00eancia": _seq,
                                    "Data": row[_k(row, "Data In")] || "",
                                    "N\\u00ba Ordem": row[_k(row, "OS")] || "",
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
                                    "Situa\\u00e7\\u00e3o": _transSit(row[_k(row, "Status OS")]),
                                    "Diretiva": row[_k(row, "Diretiva")] || ""
                                };
                                const miss = !obj["N\\u00ba Ordem"] || !obj["T\\u00e9cnico"] || !obj["Local"];
                                if (miss) obj["AVISO"] = "\\u26a0\\ufe0f FALTAM DADOS NESSA LINHA";
                                return obj;
                            };

                            const _makeAcomp = (row) => {
                                _seq++;
                                const dF = row[_k(row, "Falha")] || "";
                                const dT = row[_k(row, "Tarefa")] || "";
                                const all = dF + " | " + dT;
                                const hI = row[_k(row, "Hora In")] || "";
                                const hF = row[_k(row, "Hora Fim")] || "";
                                const chegada = _ext(all, /Cheg(?:ada|uei)[^\\d]*([\\d]{2}:[\\d]{2})/i) || hI;
                                const conclusao = _ext(all, /T[e\\u00ea]rmino[^:]*:\\s*([\\d:]+)/i) || _ext(all, /Finalizado[^\\d]*([\\d]{2}:[\\d]{2})/i) || hF;
                                const local = _ext(all, /Endere[\\u00e7c]o:\\s*([^|]+)/i) || _ext(all, /Local:\\s*([^|]+)/i) || row["[OS] MchCodeDescription"] || "";
                                const cliente = _ext(all, /(?:Cliente|Empresa):\\s*([^|]+)/i);
                                
                                const obj = {
                                    "Dados/Sequ\\u00eancia": _seq,
                                    "Data": row[_k(row, "Data In")] || "",
                                    "N\\u00ba Ordem": row[_k(row, "OS")] || "",
                                    "Hora chamada": hI,
                                    "Cliente": cliente,
                                    "Local": local,
                                    "T\\u00e9cnico": _getTec(row),
                                    "chegada": chegada,
                                    "at\\u00e9": conclusao,
                                    "Tempo de trabalho": _calcDur(chegada, conclusao),
                                    "Descri\\u00e7\\u00e3o": dF,
                                    "Situa\\u00e7\\u00e3o": _transSit(row[_k(row, "Status OS")]),
                                    "Diretiva": row[_k(row, "Diretiva")] || ""
                                };
                                const miss = !obj["N\\u00ba Ordem"] || !obj["T\\u00e9cnico"];
                                if (miss) obj["AVISO"] = "\\u26a0\\ufe0f FALTAM DADOS NESSA LINHA";
                                return obj;
                            };
                            """
    
    code = code[:idx] + new_helpers + code[end_idx:]
    print("Replaced!")
else:
    print("Not found")

# Fix _getTec because it's also using exact keys
target_tec = 'const cands = [\n                                    row["ID Funcion\\u00e1rio"], row["ID do funcion\\u00e1rio"],'
if target_tec in code:
    new_tec = 'const cands = [\n                                    row[_k(row, "Funcion")], '
    code = code.replace(target_tec, new_tec, 1)

target_tec2 = 'return row["ID Funcion\\u00e1rio"] || "";\n                            };'
if target_tec2 in code:
    new_tec2 = 'return row[_k(row, "Funcion")] || "";\n                            };'
    code = code.replace(target_tec2, new_tec2, 1)

# Fix the forEach part
target_forEach = 'const _dirTxt = (row["Diretiva"] || "").toLowerCase();\n                                const _techId = (row["ID Funcion\\u00e1rio"] || row["[Clocking] CreatedBy"] || "").toUpperCase();'
if target_forEach in code:
    new_forEach = 'const _dirTxt = (row[_k(row, "Diretiva")] || "").toLowerCase();\n                                const _techId = (row[_k(row, "Funcion")] || row["[Clocking] CreatedBy"] || "").toUpperCase();'
    code = code.replace(target_forEach, new_forEach, 1)

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved!")


