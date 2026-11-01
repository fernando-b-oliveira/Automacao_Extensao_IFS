import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

task_search = """                let taskFiltroDate = `ActualStart ge ${filterDateApontamento} or ReportedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `(ActualStart ge ${filterDateApontamento} and ActualStart le ${window.filterDateFim}) or (ReportedDate ge ${filterDateApontamento} and ReportedDate le ${window.filterDateFim})`;
                }"""

task_replace = """                let taskFiltroDate = `ReportedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `ReportedDate ge ${filterDateApontamento} and ReportedDate le ${window.filterDateFim}`;
                }"""

content = content.replace(task_search, task_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated to use only ReportedDate to prevent API errors.")


