import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update UI label
ui_search = "Data Inicial dos Apontamentos:"
ui_replace = "Data Inicial da Execução (Início Real):"
content = content.replace(ui_search, ui_replace)

# 2. Update orphan fetching to pull 90 days backwards
fetch_search = """                    // NEW ORPHAN LOGIC: Fetch Orders directly by RegDate to bypass JtTaskSet crashes!
                    let orderFiltroDate = `RegDate ge ${filterDateApontamento}`;
                    if (window.filterDateFim) {
                        orderFiltroDate = `RegDate ge ${filterDateApontamento} and RegDate le ${window.filterDateFim}`;
                    }"""

fetch_replace = """                    // NEW ORPHAN LOGIC: Fetch Orders directly by RegDate to bypass JtTaskSet crashes!
                    // To ensure we catch old OSs executed recently, we fetch 90 days BEFORE the selected date!
                    let dtRegSafe = new Date(filterDateApontamento);
                    dtRegSafe.setDate(dtRegSafe.getDate() - 90);
                    let safeRegDateStr = dtRegSafe.toISOString().split('.')[0] + 'Z';
                    
                    let orderFiltroDate = `RegDate ge ${safeRegDateStr}`;
                    if (window.filterDateFim) {
                        orderFiltroDate = `RegDate ge ${safeRegDateStr} and RegDate le ${window.filterDateFim}`;
                    }"""
content = content.replace(fetch_search, fetch_replace)

# 3. Add memory filtering in the orphan loop
loop_search = """                        const start = formatDate(task.ActualStart || os.RealSDate || task.ReportedDate || os.RegDate);
                        const stop = formatDate(task.ActualFinish || os.RealFDate || task.ReportedDate || os.RegDate);"""

loop_replace = """                        const rawStart = task.ActualStart || os.RealSDate || task.ReportedDate || os.RegDate;
                        const actualStartDate = new Date(rawStart);
                        const filterDate = new Date(filterDateApontamento);
                        if (actualStartDate < filterDate) return; // Ignore if executed before UI date
                        
                        if (window.filterDateFim) {
                            const filterFimDate = new Date(window.filterDateFim);
                            if (actualStartDate > filterFimDate) return; // Ignore if executed after UI end date
                        }
                        
                        const start = formatDate(rawStart);
                        const stop = formatDate(task.ActualFinish || os.RealFDate || task.ReportedDate || os.RegDate);"""
content = content.replace(loop_search, loop_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated to fetch 90 days back and filter execution dates in memory.")


