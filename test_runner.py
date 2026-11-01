﻿import json

code = """
const dt = { rows: () => ({ data: () => ({ toArray: () => [{
    "Descri\u00e7\u00e3o da Falha (Completa)": "Vazamento",
    "Descri\u00e7\u00e3o da Tarefa": "Verificar",
    "ID Funcion\u00e1rio": "TEST",
    "Status OS": "WORKDONE"
}] }) }) };

const action = function() {
    const data = dt.rows({ search: 'applied' }).data().toArray();
    const data0800 = [];
    const dataAcomp = [];

    let _seq = 0;

    const _calcDur = (h1, h2) => {
        if (!h1 || !h2) return "";
        try {
            const p = s => { const [h,m] = s.split(':').map(Number); return h*60+m; };
            let d = p(h2) - p(h1); if (d < 0) d += 1440;
            return Math.floor(d/60) + ':' + String(d%60).padStart(2,'0');
        } catch(e) { return ""; }
    };

    const _k = (row, search) => Object.keys(row).find(k => k.toLowerCase().includes(search.toLowerCase())) || search;

    const _getTec = (row) => {
        const cands = [
            row[_k(row, "Funcion")], row["ID do funcion\u00e1rio"],
            row["[Clocking] CreatedBy"], row["[Task] SignId"],
            row["[Task] ExecutedBy"], row["[Task] ReportedBy"],
            row["[OS] PreparedBy"], row["[OS] CreatedBy"]
        ];
        for (const c of cands) {
            if (c && typeof c === 'string') {
                const u = c.toUpperCase();
                if (u !== "FERNANDOA.ESTAGIO" && u !== "SISTEMA_ERP_EXEMPLOAPP" && u !== "ERP_OPS_CORE" && u.trim() !== "") return c;
            }
        }
        return row[_k(row, "Funcion")] || "";
    };

    const _transSit = (s) => {
        const m = {"WORKDONE":"Trabalho Realizado","FINISHED":"Finalizado","RELEASED":"Liberado","STARTED":"Iniciado","CANCELED":"Cancelado","Historical":"Hist\u00f3rico","PREPARED":"Preparado","REPORTED":"Reportado"};
        return m[s] || s || "";
    };

    const _ext = (txt, pat) => { const m = txt.match(pat); return m ? m[1].trim() : ''; };

    const _make0800 = (row) => {
        _seq++;
        const dF = row[_k(row, "Falha")] || "";
        const dT = row[_k(row, "Tarefa")] || "";
        const all = dF + " | " + dT;
        const hI = row[_k(row, "Hora In")] || "";
        const hF = row[_k(row, "Hora Fim")] || "";
        const chegada = _ext(all, /Cheg(?:ada|uei)[^\d]*([\d]{2}:[\d]{2})/i) || hI;
        const conclusao = _ext(all, /T[e\u00ea]rmino[^:]*:\s*([\d:]+)/i) || _ext(all, /Finalizado[^\d]*([\d]{2}:[\d]{2})/i) || hF;
        const local = _ext(all, /Endere[\u00e7c]o:\s*([^|]+)/i) || _ext(all, /Local:\s*([^|]+)/i) || row["[OS] MchCodeDescription"] || "";
        const cliente = _ext(all, /(?:Cliente|Empresa|Condom\u00ednio|Edif\u00edcio):\s*([^|]+)/i);
        const autor = _ext(all, /Autor[:]?\s*([^|]+)/i) || _ext(all, /Respons\u00e1vel[:]?\s*([^|]+)/i);
        const tel = _ext(all, /(?:Tel|Fone|Celular)[.\s]?(?:Autor)?[:\s]?((?:[\d\s\(\)\-]){7,})/i);
        const ocorr = _ext(all, /Ocorr[e\u00ea]ncia[:]?\s*([^|]+)/i) || dT.split('|')[0].trim();
        
        const obj = {
            "Dados/Sequ\u00eancia": _seq,
            "Data": row[_k(row, "Data In")] || "",
            "N\u00ba Ordem": row[_k(row, "OS")] || "",
            "Hora chamada": hI,
            "Cliente": cliente,
            "Autor": autor,
            "Tel. Autor": tel,
            "Local": local,
            "T\u00e9cnico": _getTec(row),
            "Ocorr\u00eancia": ocorr,
            "chegada": chegada,
            "at\u00e9": conclusao,
            "Tempo de trabalho": _calcDur(chegada, conclusao),
            "Descri\u00e7\u00e3o": dF,
            "Situa\u00e7\u00e3o": _transSit(row[_k(row, "Status OS")]),
            "Diretiva": row[_k(row, "Diretiva")] || ""
        };
        const miss = !obj["N\u00ba Ordem"] || !obj["T\u00e9cnico"] || !obj["Local"];
        if (miss) obj["AVISO"] = "\u26a0\ufe0f FALTAM DADOS NESSA LINHA";
        return obj;
    };

    const _makeAcomp = (row) => {
        _seq++;
        const dF = row[_k(row, "Falha")] || "";
        const dT = row[_k(row, "Tarefa")] || "";
        const all = dF + " | " + dT;
        const hI = row[_k(row, "Hora In")] || "";
        const hF = row[_k(row, "Hora Fim")] || "";
        const chegada = _ext(all, /Cheg(?:ada|uei)[^\d]*([\d]{2}:[\d]{2})/i) || hI;
        const conclusao = _ext(all, /T[e\u00ea]rmino[^:]*:\s*([\d:]+)/i) || _ext(all, /Finalizado[^\d]*([\d]{2}:[\d]{2})/i) || hF;
        const local = _ext(all, /Endere[\u00e7c]o:\s*([^|]+)/i) || _ext(all, /Local:\s*([^|]+)/i) || row["[OS] MchCodeDescription"] || "";
        const cliente = _ext(all, /(?:Cliente|Empresa):\s*([^|]+)/i);
        
        const obj = {
            "Dados/Sequ\u00eancia": _seq,
            "Data": row[_k(row, "Data In")] || "",
            "N\u00ba Ordem": row[_k(row, "OS")] || "",
            "Hora chamada": hI,
            "Cliente": cliente,
            "Local": local,
            "T\u00e9cnico": _getTec(row),
            "chegada": chegada,
            "at\u00e9": conclusao,
            "Tempo de trabalho": _calcDur(chegada, conclusao),
            "Descri\u00e7\u00e3o": dF,
            "Situa\u00e7\u00e3o": _transSit(row[_k(row, "Status OS")]),
            "Diretiva": row[_k(row, "Diretiva")] || ""
        };
        const miss = !obj["N\u00ba Ordem"] || !obj["T\u00e9cnico"];
        if (miss) obj["AVISO"] = "\u26a0\ufe0f FALTAM DADOS NESSA LINHA";
        return obj;
    };

    data.forEach(row => {
        const _allTxt = Object.values(row).join(" ").toLowerCase();
        const _dirTxt = (row[_k(row, "Diretiva")] || "").toLowerCase();
        const _techId = (row[_k(row, "Funcion")] || row["[Clocking] CreatedBy"] || "").toUpperCase();

        if (_techId.includes("ERP_OPS_CORE")) return; // ignora ERP_OPS_CORE

        const is0800Trigger = /0800|0300|\bvazamento\b|\bcheiro\b|press\u00e3o|pressao|falta de g\u00e1s|falta de gas|inc\u00eandio|incendio|\bfogo\b|emerg\u00eancia|emergencia|rompimento|cliente ligou/i.test(_allTxt);
        const isAcompTrigger = _dirTxt.includes("acomp") || /acompanhamento|escava\u00e7\u00e3o|implanta\u00e7\u00e3o|sondagem|drenagem|pavimenta\u00e7\u00e3o|concession\u00e1ria|\u00e1guas guariroba|aguas guariroba/i.test(_allTxt);

        if (is0800Trigger) {
            data0800.push(_make0800(row));
        } else if (isAcompTrigger) {
            dataAcomp.push(_makeAcomp(row));
        }
    });

    console.log("0800:", data0800.length);
    console.log("Acomp:", dataAcomp.length);
};

action();
"""

with open("test.html", "w", encoding="utf-8") as f:
    f.write(f"<html><body><script>{code}</script></body></html>")
print("Done")



