import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace DataTable initialization
dt_search = r"(dom:\s*'Brtip',)"
dt_replace = r"dom: 'Bfrtip',\n                  paging: window.usePagination !== undefined ? window.usePagination : true,\n                  pageLength: 50,\n                  "
content = re.sub(dt_search, dt_replace, content)

# Replace the language setting to add search translation
lang_search = r"(language:\s*\{\s*url:\s*'//cdn\.datatables\.net/plug-ins/1\.13\.6/i18n/pt-BR\.json'\s*\})"
lang_replace = r"language: { url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json', search: '🔍 Pesquisar em toda a tabela:' }"
content = re.sub(lang_search, lang_replace, content)

# Check if injection worked
if "window.usePagination !== undefined" not in content:
    print("WARNING: Replacement failed!")
else:
    print("DataTable init updated successfully.")

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)


