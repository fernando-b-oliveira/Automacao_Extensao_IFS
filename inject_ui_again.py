import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Find the end of the chk_acomp div
pattern = r'(<input type="checkbox" id="chk_acomp"[^>]*>.*?</label>\s*</div>)'

new_html = r"""\1

                        <!-- Status Checkboxes -->
                        <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0;">
                            <label style="font-weight: bold; width: 100%; text-align: left; color: #1e293b; font-size: 14px; margin-bottom: 5px;">Filtrar por Situação (Status OS):</label>
                            
                            <label style="cursor: pointer; font-size: 14px; display: flex; align-items: center; color: #333;">
                                <input type="checkbox" id="chk_status_concluida" value="concluida" checked style="margin-right: 6px; accent-color: #1e293b;"> Concluídas / Finalizadas / Histórico
                            </label>
                            
                            <label style="cursor: pointer; font-size: 14px; display: flex; align-items: center; color: #333;">
                                <input type="checkbox" id="chk_status_andamento" value="andamento" checked style="margin-right: 6px; accent-color: #1e293b;"> Em Andamento / Liberado
                            </label>

                            <label style="cursor: pointer; font-size: 14px; display: flex; align-items: center; color: #333;">
                                <input type="checkbox" id="chk_status_cancelada" value="cancelada" style="margin-right: 6px; accent-color: #1e293b;"> Canceladas
                            </label>
                        </div>"""

if 'id="chk_status_concluida"' not in content:
    content, count = re.subn(pattern, new_html, content, flags=re.DOTALL)
    print(f"Injected UI HTML. Match count: {count}")
    with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
        f.write(content)
else:
    print("UI HTML already present.")



