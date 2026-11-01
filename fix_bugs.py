﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: Add logStatus function before the setTimeout block
logStatusFn = """
        function logStatus(msg) {
            const logDiv = document.getElementById('status-log');
            if(logDiv) {
                logDiv.innerHTML += '> ' + msg + '<br>';
                logDiv.scrollTop = logDiv.scrollHeight;
            }
        }

        """

code = code.replace(
    "        setTimeout(() => {\r\n            document.getElementById('btn_iniciar')",
    logStatusFn + "        setTimeout(() => {\r\n            document.getElementById('btn_iniciar')"
)

# Fix 2: White background on loading screen
code = code.replace(
    '<div style="font-family: \'Segoe UI\', sans-serif; text-align: center; margin-top: 50px;">',
    '<div style="font-family: \'Segoe UI\', sans-serif; background: #fff; min-height: 100vh; text-align: center; padding-top: 50px;">'
)

# Fix 3: const masterData -> let masterData (so it can be reassigned in filter)
code = code.replace(
    "                const masterData = [];\r\n",
    "                let masterData = [];\r\n"
)

# Fix 4: Remove the selectedStatuses filter block that crashes everything
oldBlock = """                // Aplica o filtro de Status
                if (selectedStatuses) {
                    masterData = masterData.filter(row => {
                        const status = (row["OsStatus"] || "").toUpperCase();
                        
                        // Categorização dos status
                        const isFechada = ["FINISHED", "WORKDONE", "REPORTED", "HISTORICAL"].includes(status);
                        const isCancelada = ["CANCELED", "CANCELLED"].includes(status);
                        // Consideramos Ativas todas as que não estão Fechadas nem Canceladas
                        const isAtiva = !isFechada && !isCancelada;

                        if (selectedStatuses.ativas && isAtiva) return true;
                        if (selectedStatuses.fechadas && isFechada) return true;
                        if (selectedStatuses.canceladas && isCancelada) return true;

                        return false;
                    });
                    
                    if (masterData.length === 0) {
                        logStatus(`<span style='color:red'>Nenhum dado sobrou após aplicar os filtros de Status.</span>`);
                        return;
                    }
                }"""

# Normalize line endings for comparison
code_normalized = code.replace('\r\n', '\n')
oldBlock_normalized = oldBlock.replace('\r\n', '\n')

if oldBlock_normalized in code_normalized:
    code = code_normalized.replace(oldBlock_normalized, '').replace('\n', '\r\n')
    print("Removed selectedStatuses block")
else:
    print("Block not found, checking partial...")
    if 'if (selectedStatuses)' in code:
        print("Found partial - manual fix needed")
    else:
        print("selectedStatuses not found, maybe already fixed")

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)

print("Done!")


