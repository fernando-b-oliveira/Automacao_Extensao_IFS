with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Fix isAcomp
content = content.replace("const isAcomp = isAcompTrigger && !isIgnoredText && !isSpecialFilter;", "const isAcomp = isAcompTrigger && !isSpecialFilter;")

# Also make sure the first occurrence (since it is repeated) is replaced
with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed isAcomp.")



