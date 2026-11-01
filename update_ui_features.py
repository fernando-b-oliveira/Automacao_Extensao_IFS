import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Checkbox to the UI
ui_search = """                      <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 25px;">
                          <p style="margin-top:0; font-weight: bold; color: #1e293b;">Filtros Opcionais de Extração:</p>"""

ui_replace = """                      <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 25px;">
                          <p style="margin-top:0; font-weight: bold; color: #1e293b;">Exibição da Tabela:</p>
                          <label style="font-size: 14px; margin-bottom: 10px; display: block; cursor: pointer;">
                              <input type="checkbox" id="chk_paginacao" checked> Habilitar Paginação (Desmarque para mostrar tudo em rolagem infinita)
                          </label>
                      </div>

                      <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 25px;">
                          <p style="margin-top:0; font-weight: bold; color: #1e293b;">Filtros Opcionais de Extração:</p>"""

content = content.replace(ui_search, ui_replace)

# 2. Read the checkbox state
btn_search = """                  const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;"""

btn_replace = """                  const doAcomp = document.getElementById('chk_acomp')?.checked ?? true;
                  window.usePagination = document.getElementById('chk_paginacao')?.checked ?? true;"""

content = content.replace(btn_search, btn_replace)

# 3. Apply pagination to DataTables
dt_search = """            $('#super-table').DataTable({
                dom: 'Bfrtip',
                buttons: ["""

dt_replace = """            $('#super-table').DataTable({
                dom: 'Bfrtip',
                paging: window.usePagination,
                pageLength: window.usePagination ? 50 : undefined,
                language: { search: "🔍 Pesquisar em toda a tabela:" },
                buttons: ["""

content = content.replace(dt_search, dt_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Added infinite scroll option and custom search label.")



