import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Inject UI checkbox right before "Data Inicial dos Apontamentos" div
ui_search = r'(<div style="margin-bottom: 25px;">\s*<label style="font-weight: bold; display: block; margin-bottom: 8px; color: #1e293b;">Data Inicial dos Apontamentos:)'
ui_replace = r'''<div style="background: #f0f8ff; padding: 15px; border-radius: 8px; border: 1px solid #b3d4fc; margin-bottom: 25px;">
                        <p style="margin-top:0; font-weight: bold; color: #1e293b; font-size:16px;">Tabela (Infinito ou Páginas?):</p>
                        <label style="font-size: 15px; cursor: pointer; display: flex; align-items: center; color: #333; font-weight: 500;">
                            <input type="checkbox" id="chk_paginacao" style="width: 20px; height: 20px; margin-right: 10px; accent-color: #1e293b;"> 
                            Exibir em páginas separadas (Desmarque para ROLAGEM INFINITA numa página só)
                        </label>
                    </div>
                    \1'''
content = re.sub(ui_search, ui_replace, content)

# 2. Extract state
js_search = r'(const do0800 = document\.getElementById\(\'chk_0800\'\)\?\.checked \?\? true;)'
js_replace = r'''window.usePagination = document.getElementById('chk_paginacao')?.checked ?? false;
                  \1'''
content = re.sub(js_search, js_replace, content)

# 3. Update DataTables initialization
dt_search = r"(dom:\s*'Bfrtip',\s*buttons: \[)"
dt_replace = r"language: { search: '🔍 Pesquisar na Tabela Toda:' },\n                paging: window.usePagination,\n                pageLength: window.usePagination ? 50 : undefined,\n                \1"
content = re.sub(dt_search, dt_replace, content)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Successfully injected UI and logic.")



