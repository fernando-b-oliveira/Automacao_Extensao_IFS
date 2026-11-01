import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Inject the orphan loop immediately after the clockings loop finishes building masterData
loop_search = """                    masterData.push(row);
                });"""

loop_replace = """                    masterData.push(row);
                });
                
                // NEW: Process tasks that have NO clockings!
                const processedTasks = new Set(clockings.map(c => c.TaskSeq));
                tasks.forEach(task => {
                    if (!processedTasks.has(task.TaskSeq)) {
                        const os = mapOS[task.WoNo] || {};
                        const start = formatDate(task.ActualStart || os.RealSDate || task.ReportedDate || os.RegDate);
                        const stop = formatDate(task.ActualFinish || os.RealFDate || task.ReportedDate || os.RegDate);
                        
                        const row = {
                            "Nº OS": task.WoNo || os.WoNo || "",
                            "ID Tarefa": task.TaskSeq || "",
                            "Categoria": task.DemandType || "Work",
                            "ID Funcionário": os.ReportedBy || "",
                            "Data Início": start.data,
                            "Hora Início": start.hora,
                            "Data Fim": stop.data,
                            "Hora Fim": stop.hora,
                            "Horas Trab.": "",
                            "Descrição da Tarefa": task.Description || task.TaskDescription || "",
                            "Descrição da Falha (Completa)": os.ErrDescrLo || "",
                            "Diretiva": os.ErrDescr || "",
                            "Status do SO": os.State || os.Objstate || "",
                            "Status": task.State || task.Objstate || "",
                            "Organização": task.OrganizationId || os.OrgCode || "",
                            "Tipo de Apontamento": "Manual (Sem Relógio)",
                            "Tipo de Manutenção": task.WorkTypeId || os.WorkTypeId || ""
                        };
                        
                        for (let k in os) {
                            if (typeof os[k] !== 'object' && !k.startsWith('@') && k !== 'WoNo' && k !== 'WorkTypeId' && k !== 'ErrDescr' && k !== 'ErrDescrLo' && k !== 'Objstate' && k !== 'State') {
                                row['[OS] ' + k] = os[k];
                            }
                        }
                        for (let k in task) {
                            if (typeof task[k] !== 'object' && !k.startsWith('@') && k !== 'WoNo' && k !== 'TaskSeq' && k !== 'Description' && k !== 'TaskDescription' && k !== 'OrganizationId' && k !== 'WorkTypeId' && k !== 'Objstate' && k !== 'State') {
                                row['[Task] ' + k] = task[k];
                            }
                        }
                        masterData.push(row);
                    }
                });"""

content = content.replace(loop_search, loop_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Added loop for orphan tasks!")


