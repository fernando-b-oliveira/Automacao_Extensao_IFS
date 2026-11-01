import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the duplicate UI injection issue by clearing existing UI before injecting
ui_search = """    function iniciarInterface() {
        if (document.getElementById('super-painel-ifs')) return;"""

ui_replace = """    function iniciarInterface() {
        // Remove ANY existing interface to prevent duplicate IDs
        const existing = document.querySelectorAll('#super-painel-ifs');
        existing.forEach(e => e.remove());"""

content = content.replace(ui_search, ui_replace)

# Fix the date value extraction to get from the specific newly injected element
# Actually, since we remove existing, getElementById will now correctly get the visible one.

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UI injection to prevent duplicate IDs.")


