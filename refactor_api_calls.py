import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the fetching logic to pull both clockings and tasks as root
fetch_search = """                // Carrega TODOS os apontamentos a partir de 01/04/2026
                let urlClockings = `/main/ifsapplications/projection/v1/WorkTaskClockingsHandling.svc/JtTaskClockingSet?$filter=StartTime%20ge%20${filterDateApontamento}`;
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                }

                logStatus(`> Passo 1/4: Buscando todos os Apontamentos desde ${document.getElementById('filtro_data_inicio').value || '01/04/2026'}...`);
                const clockings = await fetchAll(urlClockings);

                if (!clockings || clockings.length === 0) {
                    logStatus("Nenhum apontamento encontrado no período!");
                    document.getElementById('btn_iniciar').innerHTML = '✅ Extrair Dados do SISTEMA_ERP_EXEMPLO';
                    return;
                }

                // Extrai as Tarefas exclusivas
                const taskSeqs = [...new Set(clockings.map(c => c.TaskSeq).filter(Boolean))];
                let tasks = [];
                
                if (taskSeqs.length > 0) {
                    logStatus(`> Passo 2/4: Puxando dados das ${taskSeqs.length} Tarefas em lotes paralelos seguros...`);
                    const taskPromises = [];
                    for (let i = 0; i < taskSeqs.length; i += BATCH_SIZE) {
                        const lote = taskSeqs.slice(i, i + BATCH_SIZE);
                        const filtro = lote.map(t => `TaskSeq eq ${t}`).join(' or ').replace(/ /g, '%20');
                        const urlTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${filtro}`;
                        taskPromises.push(fetchAll(urlTasks));
                    }
                    const tasksResult = await Promise.all(taskPromises);
                    tasksResult.forEach(res => tasks = tasks.concat(res));
                }"""

fetch_replace = """                // Passo 1: Busca Apontamentos E Tarefas baseadas na data
                let urlClockings = `/main/ifsapplications/projection/v1/WorkTaskClockingsHandling.svc/JtTaskClockingSet?$filter=StartTime%20ge%20${filterDateApontamento}`;
                let taskFiltroDate = `ActualStart ge ${filterDateApontamento} or ReportedDate ge ${filterDateApontamento}`;
                
                if (window.filterDateFim) {
                    urlClockings += `%20and%20StartTime%20le%20${window.filterDateFim}`;
                    taskFiltroDate = `(ActualStart ge ${filterDateApontamento} and ActualStart le ${window.filterDateFim}) or (ReportedDate ge ${filterDateApontamento} and ReportedDate le ${window.filterDateFim})`;
                }
                
                let urlBaseTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${taskFiltroDate.replace(/ /g, '%20')}`;

                logStatus(`> Passo 1/4: Buscando Apontamentos E Tarefas Órfãs desde ${document.getElementById('filtro_data_inicio').value || '01/04/2026'}...`);
                
                const [clockings, baseTasks] = await Promise.all([
                    fetchAll(urlClockings),
                    fetchAll(urlBaseTasks)
                ]);

                if ((!clockings || clockings.length === 0) && (!baseTasks || baseTasks.length === 0)) {
                    logStatus("Nenhum dado encontrado no período!");
                    document.getElementById('btn_iniciar').innerHTML = '✅ Extrair Dados do SISTEMA_ERP_EXEMPLO';
                    return;
                }

                // Junta as Tarefas dos Apontamentos com as Tarefas base
                const taskSeqsSet = new Set();
                clockings.forEach(c => { if(c.TaskSeq) taskSeqsSet.add(c.TaskSeq); });
                
                const fetchedTaskSeqs = new Set();
                baseTasks.forEach(t => { 
                    if(t.TaskSeq) {
                        taskSeqsSet.add(t.TaskSeq);
                        fetchedTaskSeqs.add(t.TaskSeq);
                    }
                });

                const taskSeqs = [...taskSeqsSet];
                const taskSeqsToFetch = taskSeqs.filter(seq => !fetchedTaskSeqs.has(seq));
                
                let tasks = [...baseTasks];
                
                if (taskSeqsToFetch.length > 0) {
                    logStatus(`> Passo 2/4: Puxando dados de ${taskSeqsToFetch.length} Tarefas extras ligadas aos Apontamentos...`);
                    const taskPromises = [];
                    for (let i = 0; i < taskSeqsToFetch.length; i += BATCH_SIZE) {
                        const lote = taskSeqsToFetch.slice(i, i + BATCH_SIZE);
                        const filtro = lote.map(t => `TaskSeq eq ${t}`).join(' or ').replace(/ /g, '%20');
                        const urlTasks = `/main/ifsapplications/projection/v1/WorkTasksHandling.svc/JtTaskSet?$filter=${filtro}`;
                        taskPromises.push(fetchAll(urlTasks));
                    }
                    const tasksResult = await Promise.all(taskPromises);
                    tasksResult.forEach(res => tasks = tasks.concat(res));
                } else {
                    logStatus(`> Passo 2/4: Todas as Tarefas já foram capturadas! (${tasks.length} total)`);
                }"""

content = content.replace(fetch_search, fetch_replace)

# 2. Update the masterData building logic
build_search = """                // Constrói a tabela cruzada
                const masterData = [];
                clockings.forEach(clock => {
                    const task = mapTasks[clock.TaskSeq] || {};
                    const os = mapOS[task.WoNo] || {};

                    const start = formatDate(clock.StartTime);
                    const stop = formatDate(clock.StopTime);

                    const cleanText = (txt) => (txt || "").replace(/\r?\n/g, ' | ');

                    const row = {
                        "Nº OS": task.WoNo || os.WoNo || "",
                        "ID Tarefa": clock.TaskSeq || task.TaskSeq || "",
                        "Instância Execução": clock.ExecutionInstanceSeq || "",
                        "Tipo Demanda": os.DemandType || "",
                        "Tipo Apontamento": clock.ClockingType || "",
                        "Categoria": clock.ClockingCategory || "",
                        "Seq Grupo Recurso": clock.ResourceGroupSeq || "",
                        "Seq Recurso": clock.ResourceSeq || "",
                        "Técnico": clock.EmployeeId || task.ExecutedBy || clock.CreatedBy || "",
                        "Data Início": start.data,
                        "Hora Início": start.hora,
                        "Data Fim": stop.data,
                        "Hora Fim": stop.hora,
                        "Horas Trab.": clock.WorkHours || "",
                        "ID Tipo Tempo": clock.TimeTypeId || "",
                        "Site": clock.Site || task.Site || os.Site || "",
                        "Empresa": clock.Company || task.Company || os.Company || "",
                        "Comentário Saída": cleanText(clock.ClockoutComment),
                        "ID Transação": clock.TransactionId || "",
                        "Criado Por": clock.CreatedBy || "",
                        "Data de Criação": formatDate(clock.CreatedDate).data,
                        "Descrição da Tarefa": cleanText(task.Description),
                        "Grupo de Recurso": clock.ResourceGroup || "",
                        "Desc. Grupo Recurso": cleanText(clock.ResourceGroupDesc),
                        "ID Recurso": clock.ResourceId || "",
                        "Descrição Recurso": cleanText(clock.ResourceDescription),
                        "ID Organização": clock.OrganizationId || task.OrganizationId || os.OrganizationId || "",
                        "Nome Funcionário": cleanText(clock.EmployeeName),
                        
                        "Descrição da Falha (Completa)": cleanText(os.ErrDescr || ""),
                        "Status OS": os.Objstate || os.State || (os.IsHistorical ? 'Historical' : ''),
                        "Status Tarefa": task.Objstate || task.State || "",
                        "Diretiva": cleanText(os.Directive || ""),
                        
                        // Campos Extras OS para 0800
                        "Hora chamada": formatDate(os.RegDate).hora,
                        "Cliente": cleanText(os.CustomerNo),
                        "Autor": cleanText(os.ReportedBy),
                        "Tel. Autor": cleanText(os.PhoneNo),
                        "Local": cleanText(os.MchCodeDescription || os.MchCode)
                    };
                    masterData.push(row);
                });"""

build_replace = """                // Constrói a tabela cruzada baseada em TAREFAS (para não perder OS sem reloginho)
                const masterData = [];
                tasks.forEach(task => {
                    const os = mapOS[task.WoNo] || {};
                    const cleanText = (txt) => (txt || "").replace(/\r?\n/g, ' | ');
                    
                    const taskClockings = clockings.filter(c => c.TaskSeq === task.TaskSeq);
                    
                    if (taskClockings.length === 0) {
                        // Sem apontamento (reloginho), cria uma linha apenas com a Tarefa e a OS
                        const start = formatDate(task.ActualStart); // Usa o Início Real da tarefa como fallback
                        const stop = formatDate(task.ActualFinish);
                        
                        masterData.push({
                            "Nº OS": task.WoNo || os.WoNo || "",
                            "ID Tarefa": task.TaskSeq || "",
                            "Instância Execução": "",
                            "Tipo Demanda": os.DemandType || "",
                            "Tipo Apontamento": "Manual (Sem Relógio)",
                            "Categoria": "",
                            "Seq Grupo Recurso": "",
                            "Seq Recurso": "",
                            "Técnico": task.ExecutedBy || "",
                            "Data Início": start.data,
                            "Hora Início": start.hora,
                            "Data Fim": stop.data,
                            "Hora Fim": stop.hora,
                            "Horas Trab.": task.Duration || "",
                            "ID Tipo Tempo": "",
                            "Site": task.Site || os.Site || "",
                            "Empresa": task.Company || os.Company || "",
                            "Comentário Saída": "",
                            "ID Transação": "",
                            "Criado Por": task.CreatedBy || "",
                            "Data de Criação": formatDate(task.CreatedDate).data,
                            "Descrição da Tarefa": cleanText(task.Description),
                            "Grupo de Recurso": "",
                            "Desc. Grupo Recurso": "",
                            "ID Recurso": "",
                            "Descrição Recurso": "",
                            "ID Organização": task.OrganizationId || os.OrganizationId || "",
                            "Nome Funcionário": "",
                            
                            "Descrição da Falha (Completa)": cleanText(os.ErrDescr || ""),
                            "Status OS": os.Objstate || os.State || (os.IsHistorical ? 'Historical' : ''),
                            "Status Tarefa": task.Objstate || task.State || "",
                            "Diretiva": cleanText(os.Directive || ""),
                            
                            "Hora chamada": formatDate(os.RegDate).hora,
                            "Cliente": cleanText(os.CustomerNo),
                            "Autor": cleanText(os.ReportedBy),
                            "Tel. Autor": cleanText(os.PhoneNo),
                            "Local": cleanText(os.MchCodeDescription || os.MchCode)
                        });
                    } else {
                        // Com apontamento (com reloginho)
                        taskClockings.forEach(clock => {
                            const start = formatDate(clock.StartTime);
                            const stop = formatDate(clock.StopTime);

                            masterData.push({
                                "Nº OS": task.WoNo || os.WoNo || "",
                                "ID Tarefa": clock.TaskSeq || task.TaskSeq || "",
                                "Instância Execução": clock.ExecutionInstanceSeq || "",
                                "Tipo Demanda": os.DemandType || "",
                                "Tipo Apontamento": clock.ClockingType || "",
                                "Categoria": clock.ClockingCategory || "",
                                "Seq Grupo Recurso": clock.ResourceGroupSeq || "",
                                "Seq Recurso": clock.ResourceSeq || "",
                                "Técnico": clock.EmployeeId || task.ExecutedBy || clock.CreatedBy || "",
                                "Data Início": start.data,
                                "Hora Início": start.hora,
                                "Data Fim": stop.data,
                                "Hora Fim": stop.hora,
                                "Horas Trab.": clock.WorkHours || "",
                                "ID Tipo Tempo": clock.TimeTypeId || "",
                                "Site": clock.Site || task.Site || os.Site || "",
                                "Empresa": clock.Company || task.Company || os.Company || "",
                                "Comentário Saída": cleanText(clock.ClockoutComment),
                                "ID Transação": clock.TransactionId || "",
                                "Criado Por": clock.CreatedBy || "",
                                "Data de Criação": formatDate(clock.CreatedDate).data,
                                "Descrição da Tarefa": cleanText(task.Description),
                                "Grupo de Recurso": clock.ResourceGroup || "",
                                "Desc. Grupo Recurso": cleanText(clock.ResourceGroupDesc),
                                "ID Recurso": clock.ResourceId || "",
                                "Descrição Recurso": cleanText(clock.ResourceDescription),
                                "ID Organização": clock.OrganizationId || task.OrganizationId || os.OrganizationId || "",
                                "Nome Funcionário": cleanText(clock.EmployeeName),
                                
                                "Descrição da Falha (Completa)": cleanText(os.ErrDescr || ""),
                                "Status OS": os.Objstate || os.State || (os.IsHistorical ? 'Historical' : ''),
                                "Status Tarefa": task.Objstate || task.State || "",
                                "Diretiva": cleanText(os.Directive || ""),
                                
                                "Hora chamada": formatDate(os.RegDate).hora,
                                "Cliente": cleanText(os.CustomerNo),
                                "Autor": cleanText(os.ReportedBy),
                                "Tel. Autor": cleanText(os.PhoneNo),
                                "Local": cleanText(os.MchCodeDescription || os.MchCode)
                            });
                        });
                    }
                });"""

content = content.replace(build_search, build_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated architecture to pull OS without clockings!")


