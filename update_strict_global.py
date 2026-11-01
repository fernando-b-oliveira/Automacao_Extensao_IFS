import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Fix isStrictIgnore to apply to textToSearch so it catches "Troca de plantão" in tasks too
logic_search = """                                    // Exclus\u00f5es estritas
                                      const isStrictIgnore = /troca[r]?\s*(de\s*)?(sobreaviso|plant)|sobreaviso 0800|troca de 0800|reuni[\u00e3a]o/i.test(dir_search) || /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);"""

logic_replace = """                                    // Exclus\u00f5es estritas (aplicadas no texto geral para limpar lixo como "Troca de plant\u00e3o 0800")
                                      const isStrictIgnore = /troca[r]?\s*(de\s*)?(sobreaviso|plant)|sobreaviso 0800|troca de 0800|reuni[\u00e3a]o|simulado/i.test(_textToSearch) || /manuten[\u00e7c][\u00e3a]o completa/i.test(_textToSearch);"""

content = content.replace(logic_search, logic_replace)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated strict ignore to textToSearch.")


