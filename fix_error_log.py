import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

fetch_search = """                    const res = await fetch(nextLink);
                    if (!res.ok) { if (res.status === 404) return []; throw new Error("Erro HTTP: " + res.status); }"""

fetch_replace = """                    const res = await fetch(nextLink);
                    if (!res.ok) { 
                        if (res.status === 404) return []; 
                        const errTxt = await res.text();
                        logStatus(`<span style="color:red">ERRO API HTTP ${res.status} na URL: ${url.split('?')[0]}<br>Detalhe: ${errTxt.substring(0,200)}</span>`);
                        throw new Error(`Erro HTTP: ${res.status}`); 
                    }"""

content = content.replace(fetch_search, fetch_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated error logging for fetchAll.")


