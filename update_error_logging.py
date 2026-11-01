import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace fetchAll to log HTTP errors with response text
fetch_search = """        async function fetchAll(url) {
            let data = [];
            let nextLink = url;
            let page = 1;
            while(nextLink) {
                try {
                    const response = await fetch(nextLink);
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status} - ${response.statusText}`);
                    }
                    const jsonStr = await response.text();"""

fetch_replace = """        async function fetchAll(url) {
            let data = [];
            let nextLink = url;
            let page = 1;
            while(nextLink) {
                try {
                    const response = await fetch(nextLink);
                    if (!response.ok) {
                        const errTxt = await response.text();
                        logStatus(`<span style="color:red">ERRO API HTTP ${response.status} na URL: ${url.split('?')[0]}<br>Detalhe: ${errTxt.substring(0,200)}</span>`);
                        throw new Error(`HTTP ${response.status}`);
                    }
                    const jsonStr = await response.text();"""

content = content.replace(fetch_search, fetch_replace)

# Modify the task root query to be simpler to avoid OData parsing errors
task_search = """                let taskFiltroDate = `ActualStart ge ${filterDateApontamento} or ReportedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `(ActualStart ge ${filterDateApontamento} and ActualStart le ${window.filterDateFim}) or (ReportedDate ge ${filterDateApontamento} and ReportedDate le ${window.filterDateFim})`;
                }
                
                let urlBaseTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${taskFiltroDate.replace(/ /g, '%20')}`;"""

task_replace = """                let taskFiltroDate = `CreatedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `CreatedDate ge ${filterDateApontamento} and CreatedDate le ${window.filterDateFim}`;
                }
                
                let urlBaseTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${taskFiltroDate.replace(/ /g, '%20')}`;"""

content = content.replace(task_search, task_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated to use CreatedDate and catch API errors.")


