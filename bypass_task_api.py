import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# I am completely removing the URL that crashes JtTaskSet, and replacing it with 
# a direct query to ActiveSeparateSet using RegDate, which is 100% safe and indexed.
task_search = """                let taskFiltroDate = `ReportedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `ReportedDate ge ${filterDateApontamento} and ReportedDate le ${window.filterDateFim}`;
                }
                
                let urlBaseTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${taskFiltroDate.replace(/ /g, '%20')}`;"""

task_replace = """                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                }
                // NO LONGER FETCHING ORPHAN TASKS DIRECTLY DUE TO API CRASHES
                let urlBaseTasks = null;"""

content = content.replace(task_search, task_replace)

# Now, instead of pushing urlBaseTasks, we skip it
push_search = """                        const urlTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${filtro}`;
                        taskPromises.push(fetchAll(urlTasks));
                    }
                    taskPromises.push(fetchAll(urlBaseTasks));"""

push_replace = """                        const urlTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${filtro}`;
                        taskPromises.push(fetchAll(urlTasks));
                    }"""

content = content.replace(push_search, push_replace)

# To find orphans, we will fetch Orders directly by RegDate!
orders_search = """                    // TAREFAS FALTANTES: Agora precisamos buscar as tarefas que vieram dos Apontamentos 
                    // mas não vieram do urlBaseTasks.
                    const taskSeqsFromClockings = [...new Set(clockings.map(c => c.TaskSeq))];"""

orders_replace = """                    
                    // NEW ORPHAN LOGIC: Fetch Orders directly by RegDate to bypass JtTaskSet crashes!
                    let orderFiltroDate = `RegDate ge ${filterDateApontamento}`;
                    if (window.filterDateFim) {
                        orderFiltroDate = `RegDate ge ${filterDateApontamento} and RegDate le ${window.filterDateFim}`;
                    }
                    const urlOrphanActive = `/main/ifsapplications/projection/v1/ActiveSeparateHandling.svc/ActiveSeparateSet?$filter=${orderFiltroDate.replace(/ /g, '%20')}`;
                    const urlOrphanHist = `/main/ifsapplications/projection/v1/HistoricalWorkOrdersHandling.svc/HistoricalSeparateSet?$filter=${orderFiltroDate.replace(/ /g, '%20')}`;
                    
                    logStatus(`Passo Extra: Buscando Ordens Órfãs (sem relógio) criadas no período...`);
                    const orphanActive = await fetchAll(urlOrphanActive);
                    const orphanHist = await fetchAll(urlOrphanHist);
                    const orphanOrders = [...orphanActive, ...orphanHist];
                    
                    // Fetch tasks for these orphan orders
                    const orphanWoNos = [...new Set(orphanOrders.map(o => o.WoNo))];
                    const orphanTaskPromises = [];
                    for (let i = 0; i < orphanWoNos.length; i += 25) {
                        const chunk = orphanWoNos.slice(i, i + 25);
                        const filtro = chunk.map(seq => `WoNo eq ${seq}`).join(' or ');
                        const urlTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${filtro.replace(/ /g, '%20')}`;
                        orphanTaskPromises.push(fetchAll(urlTasks));
                    }
                    const orphanTaskResults = await Promise.all(orphanTaskPromises);
                    const orphanTasks = orphanTaskResults.flat();
                    
                    // Merge tasks
                    tasks = [...tasks, ...orphanTasks];
                    
                    // TAREFAS FALTANTES: Agora precisamos buscar as tarefas que vieram dos Apontamentos 
                    // mas não vieram do urlBaseTasks.
                    const taskSeqsFromClockings = [...new Set(clockings.map(c => c.TaskSeq))];"""

content = content.replace(orders_search, orders_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated to fetch orphan OS directly from RegDate.")


