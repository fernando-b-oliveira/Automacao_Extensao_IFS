﻿with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Fix _techId
old_techId = 'const _techId = (row[_k(row, "Funcion")] || row["[Clocking] CreatedBy"] || "").toUpperCase();'
new_techId = 'const _techId = String(row[_k(row, "Funcion")] || row["[Clocking] CreatedBy"] || "").toUpperCase();'
code = code.replace(old_techId, new_techId)

# Fix _getTec
old_getTec = """                                for (const c of cands) {
                                    if (c && typeof c === 'string') {
                                        const u = c.toUpperCase();
                                        if (u !== "FERNANDOA.ESTAGIO" && u !== "SISTEMA_ERP_EXEMPLOAPP" && u !== "ERP_OPS_CORE" && u.trim() !== "") return c;
                                    }
                                }"""
new_getTec = """                                for (let c of cands) {
                                    if (c) {
                                        c = String(c);
                                        const u = c.toUpperCase();
                                        if (u !== "FERNANDOA.ESTAGIO" && u !== "SISTEMA_ERP_EXEMPLOAPP" && u !== "ERP_OPS_CORE" && u.trim() !== "") return c;
                                    }
                                }"""
code = code.replace(old_getTec, new_getTec)

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed techId string conversion!")



