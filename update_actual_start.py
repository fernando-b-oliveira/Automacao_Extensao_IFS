import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

task_search = """                let taskFiltroDate = `CreatedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `CreatedDate ge ${filterDateApontamento} and CreatedDate le ${window.filterDateFim}`;
                }"""

task_replace = """                // Usa ActualStart e ReportedDate para não perder tarefas antigas executadas agora
                let taskFiltroDate = `ActualStart ge ${filterDateApontamento} or ReportedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `(ActualStart ge ${filterDateApontamento} and ActualStart le ${window.filterDateFim}) or (ReportedDate ge ${filterDateApontamento} and ReportedDate le ${window.filterDateFim})`;
                }"""

content = content.replace(task_search, task_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated to use ActualStart and ReportedDate.")


