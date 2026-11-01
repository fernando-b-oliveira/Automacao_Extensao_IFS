﻿with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# === FIX 1: Logo - change uppercase Á to lowercase á and add translate=no ===
code = code.replace(
    'ERP <span style="color: #3b82f6;">Ops</span></h1>',
    '<span translate="no">ERP <span style="color: #3b82f6;">Ops</span></span></h1>'
)

# === FIX 2: Set window.isFiltroDuplo and window.selectedTypes in the click handler ===
old_click = """document.getElementById('btn_iniciar').addEventListener('click', () => {
                const fData = document.getElementById('filtro_data_inicio').value;
                if(fData) filterDateApontamento = fData + "T00:00:00Z";
                
                document.body.innerHTML = `"""

new_click = """document.getElementById('btn_iniciar').addEventListener('click', () => {
                const fData = document.getElementById('filtro_data_inicio').value;
                if(fData) filterDateApontamento = fData + "T00:00:00Z";

                const do0800 = document.getElementById('chk_0800')?.checked ?? true;
                const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;
                window.isFiltroDuplo = do0800 && doAcomp;
                window.selectedTypes = { do0800: do0800, doAcomp: doAcomp };
                
                document.body.innerHTML = `"""

if old_click in code:
    code = code.replace(old_click, new_click, 1)
    print("Fix 2 (window.isFiltroDuplo) applied!")
else:
    print("Fix 2 NOT applied - target not found")

# === FIX 3: Better filter logic in the Excel action ===
old_filter = """                              const txt = ((row["Descri\\u00e7\\u00e3o da Tarefa"]||\"\") + \" \" + (row["Descri\\u00e7\\u00e3o da Falha (Completa)"]||\"\")).toLowerCase();
                              const tecnico = (row["ID do funcion\\u00e1rio"] || row["ID Funcion\\u00e1rio"] || \"\").toUpperCase();
                              
                              let isIgnored = tecnico.includes(\"ERP_OPS_CORE\");
                              
                              const regex0800 = /(?:^|\\s)(0800|800|plantao)(?:\\s|$)/i;
                              const is0800Trigger = regex0800.test(txt) || txt.includes(\"0800\");
                              
                              const isAcompTrigger = txt.includes(\"acompanhamento\") || txt.includes(\"acomp\");
                              
                              if (is0800Trigger && !isIgnored) {
                                  data0800.push(cleanRow);
                              } else if (isAcompTrigger && !isIgnored) {
                                  dataAcomp.push(cleanRow);
                              } else {
                              
                              
                                    dataAcomp.push(cleanRow); // Fallback"""

new_filter = """                              const _allTxt = Object.values(cleanRow).join(" ").toLowerCase();
                              const _dirTxt = (cleanRow["Diretiva"] || "").toLowerCase();
                              const _techId = (cleanRow["ID Funcion\\u00e1rio"] || cleanRow["ID do funcion\\u00e1rio"] || "").toUpperCase();
                              
                              // Ignorar se t\\u00e9cnico for o sistema ERP_OPS_CORE
                              if (_techId.includes("ERP_OPS_CORE")) { return; }

                              // Detecta 0800: palavras-chave de emerg\\u00eancia/atendimento
                              const is0800Trigger = /0800|0300|\\bvazamento\\b|\\bcheiro\\b|press\\u00e3o|pressao|falta de g\\u00e1s|falta de gas|inc\\u00eandio|incendio|\\bfogo\\b|\\btrote\\b|emerg\\u00eancia|emergencia|rompimento|cliente ligou/i.test(_allTxt);

                              // Detecta Acompanhamento: campo Diretiva ou palavras-chave de obra
                              const isAcompTrigger = _dirTxt.includes("acomp") || 
                                  /acompanhamento|\\u00e1guas guariroba|aguas guariroba|\\bprefeitura\\b|sanesul|empreiteira|escava\\u00e7\\u00e3o|escavacao|implanta\\u00e7\\u00e3o|implantacao|sondagem|drenagem|pavimenta\\u00e7\\u00e3o|concession\\u00e1ria|rede de \\u00e1gua|rede de esgoto|reparo na via/i.test(_allTxt);

                              if (is0800Trigger) {
                                  data0800.push(cleanRow);
                              } else if (isAcompTrigger) {
                                  dataAcomp.push(cleanRow);
                              } else {
                                    // n\\u00e3o classificado - n\\u00e3o adiciona"""

if old_filter in code:
    code = code.replace(old_filter, new_filter, 1)
    print("Fix 3 (better filters) applied!")
else:
    print("Fix 3 NOT applied. Doing a simpler replacement...")
    # Try to find and replace just the isIgnored/is0800Trigger block
    target_simple = 'let isIgnored = tecnico.includes("ERP_OPS_CORE");'
    if target_simple in code:
        idx = code.find(target_simple)
        # find the else { block after
        else_start = code.find('} else {', idx)
        fallback_end = code.find('dataAcomp.push(cleanRow); // Fallback', idx)
        if fallback_end > 0:
            end_pos = code.find('\n', fallback_end) + 1
            old_block = code[idx:end_pos]
            new_block = """let isIgnored = _techId.includes("ERP_OPS_CORE");
                              const is0800Trigger = /0800|0300|\\bvazamento\\b|\\bcheiro\\b|press\\u00e3o|pressao|falta de g\\u00e1s|falta de gas|inc\\u00eandio|incendio|\\bfogo\\b|emerg\\u00eancia|emergencia|rompimento|cliente ligou/i.test(_allTxt);
                              const isAcompTrigger = _dirTxt.includes("acomp") || /acompanhamento|escava\\u00e7\\u00e3o|implanta\\u00e7\\u00e3o|sondagem|drenagem|pavimenta\\u00e7\\u00e3o|concession\\u00e1ria/i.test(_allTxt);
                              if (is0800Trigger && !isIgnored) {
                                  data0800.push(cleanRow);
                              } else if (isAcompTrigger && !isIgnored) {
                                  dataAcomp.push(cleanRow);
                              } else {
                                    // nao classificado\n"""
            code = code[:idx] + new_block + code[end_pos:]
            print("Simpler fix 3 applied!")

# Also add _allTxt and _techId before the block since old code had txt/tecnico
# Make sure the old txt/tecnico variables don't crash
code = code.replace(
    'const txt = ((row["Descri\\u00e7\\u00e3o da Tarefa"]||\"\") + \" \" + (row["Descri\\u00e7\\u00e3o da Falha (Completa)"]||\"\")).toLowerCase();\n\n                              const tecnico = (row["ID do funcion\\u00e1rio"] || row["ID Funcion\\u00e1rio"] || \"\").toUpperCase();',
    'const _allTxt = Object.values(cleanRow).join(" ").toLowerCase();\n\n                              const _dirTxt = (cleanRow["Diretiva"] || "").toLowerCase();\n\n                              const _techId = (cleanRow["ID Funcion\\u00e1rio"] || cleanRow["ID do funcion\\u00e1rio"] || "").toUpperCase();'
)

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved!")



