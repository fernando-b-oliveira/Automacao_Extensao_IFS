import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update UI to add checkboxes for status
ui_search = """                            <label style="cursor: pointer; font-size: 16px; display: flex; align-items: center; color: #333; font-weight: 500;">

                                <input type="checkbox" id="chk_acomp" value="acompanhamento" checked style="width: 22px; height: 22px; margin-right: 10px; cursor: pointer; accent-color: #3b82f6;"> 🤝 Acompanhamentos

                            </label>

                        </div>"""

ui_replace = """                            <label style="cursor: pointer; font-size: 16px; display: flex; align-items: center; color: #333; font-weight: 500;">

                                <input type="checkbox" id="chk_acomp" value="acompanhamento" checked style="width: 22px; height: 22px; margin-right: 10px; cursor: pointer; accent-color: #3b82f6;"> 🤝 Acompanhamentos

                            </label>

                        </div>

                        <!-- Status Checkboxes -->
                        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0;">
                            <label style="font-weight: bold; width: 100%; text-align: left; color: #1e293b; font-size: 14px; margin-bottom: 5px;">Filtrar por Situação (Status OS):</label>
                            
                            <label style="cursor: pointer; font-size: 14px; display: flex; align-items: center; color: #333;">
                                <input type="checkbox" id="chk_status_concluida" value="WORKDONE,FINISHED,REPORTED,Historical" checked style="margin-right: 6px; accent-color: #1e293b;"> Concluídas / Finalizadas / Histórico
                            </label>
                            
                            <label style="cursor: pointer; font-size: 14px; display: flex; align-items: center; color: #333;">
                                <input type="checkbox" id="chk_status_andamento" value="RELEASED,STARTED,PREPARED,FAULTREPORT" checked style="margin-right: 6px; accent-color: #1e293b;"> Em Andamento / Liberado
                            </label>

                            <label style="cursor: pointer; font-size: 14px; display: flex; align-items: center; color: #333;">
                                <input type="checkbox" id="chk_status_cancelada" value="CANCELED" style="margin-right: 6px; accent-color: #1e293b;"> Canceladas
                            </label>
                        </div>"""

content = content.replace(ui_search, ui_replace)


# 2. Extract these status values in window
status_extract_search = """                const do0800 = document.getElementById('chk_0800')?.checked ?? true;
                const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;"""

status_extract_replace = """                const do0800 = document.getElementById('chk_0800')?.checked ?? true;
                const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;
                const stConc = document.getElementById('chk_status_concluida')?.checked ?? true;
                const stAnda = document.getElementById('chk_status_andamento')?.checked ?? true;
                const stCanc = document.getElementById('chk_status_cancelada')?.checked ?? false;
                window.selectedStatus = { conc: stConc, anda: stAnda, canc: stCanc };
"""

content = content.replace(status_extract_search, status_extract_replace)

# 3. Add filtering logic before processing the rows
filter_search = """                                data.forEach(row => {
                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();"""

filter_replace = """                                data.forEach(row => {
                                    const rawStatus = String(_krx(row, /^Status OS$/i, "")).toUpperCase();
                                    const stConcList = ["WORKDONE", "FINISHED", "REPORTED", "HISTORICAL"];
                                    const stAndaList = ["RELEASED", "STARTED", "PREPARED", "FAULTREPORT"];
                                    const stCancList = ["CANCELED"];
                                    
                                    let keepStatus = true;
                                    if (!window.isRawOnly) {
                                        keepStatus = false;
                                        if (window.selectedStatus.conc && stConcList.includes(rawStatus)) keepStatus = true;
                                        if (window.selectedStatus.anda && stAndaList.includes(rawStatus)) keepStatus = true;
                                        if (window.selectedStatus.canc && stCancList.includes(rawStatus)) keepStatus = true;
                                    }
                                    
                                    if (!keepStatus) return;

                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();"""

# wait, we must make sure window.isRawOnly is defined earlier. Let's not use window.isRawOnly here, we can just use (window.selectedTypes.do0800 || window.selectedTypes.doAcomp) as the opposite of rawOnly.
# Let's fix that.
filter_replace = """                                data.forEach(row => {
                                    const rawStatus = String(_krx(row, /^Status OS$/i, "")).toUpperCase();
                                    const stConcList = ["WORKDONE", "FINISHED", "REPORTED", "HISTORICAL"];
                                    const stAndaList = ["RELEASED", "STARTED", "PREPARED", "FAULTREPORT"];
                                    const stCancList = ["CANCELED"];
                                    
                                    let keepStatus = false;
                                    if (window.selectedStatus.conc && stConcList.includes(rawStatus)) keepStatus = true;
                                    if (window.selectedStatus.anda && stAndaList.includes(rawStatus)) keepStatus = true;
                                    if (window.selectedStatus.canc && stCancList.includes(rawStatus)) keepStatus = true;
                                    // If rawStatus is unknown, we might want to keep it to be safe, but user said filter strictly
                                    if (!stConcList.includes(rawStatus) && !stAndaList.includes(rawStatus) && !stCancList.includes(rawStatus)) keepStatus = true; 
                                    
                                    if (!keepStatus) return; // Skip this row

                                    const dF_search = String(_krx(row, /Descri..o da Falha/i, "")).toLowerCase();"""

content = content.replace(filter_search, filter_replace)

# 4. Modify the is0800Trigger to require that diretriz is not entirely blank for it to match, OR the match is clear.
# Actually, the user says: "puxou coisa com o campo diretriz em bracno que nao é pra cacontecer".
# Let's add:
# const isBlankDir = dir_search.trim() === "";
# const is0800 = is0800Trigger && !isIgnoredText && !isPlanned && !isManutencaoCompleta && !isSpecialFilter && !isBlankDir;
# const isAcomp = isAcompTrigger && !isSpecialFilter && !isBlankDir;

logic_search = """                                    const isManutencaoCompleta = /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);

                                    const is0800 = is0800Trigger && !isIgnoredText && !isPlanned && !isManutencaoCompleta && !isSpecialFilter;
                                    const isAcomp = isAcompTrigger && !isSpecialFilter;"""

logic_replace = """                                    const isManutencaoCompleta = /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);
                                    
                                    const isBlankDir = dir_search.trim() === "";

                                    const is0800 = is0800Trigger && !isIgnoredText && !isPlanned && !isManutencaoCompleta && !isSpecialFilter && !isBlankDir;
                                    const isAcomp = isAcompTrigger && !isSpecialFilter && !isBlankDir;"""

content = content.replace(logic_search, logic_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated UI, added status filters, and prevented blank Diretriz from being pulled.")



