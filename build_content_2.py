﻿import re

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

excel_logic = r"""
                              const txt = ((row["Descri\u00e7\u00e3o da Tarefa"]||"") + " " + (row["Descri\u00e7\u00e3o da Falha (Completa)"]||"")).toLowerCase();
                              const tecnico = (row["ID do funcion\u00e1rio"] || row["ID Funcion\u00e1rio"] || "").toUpperCase();
                              
                              let isIgnored = tecnico.includes("ERP_OPS_CORE");
                              
                              const regex0800 = /(?:^|\s)(0800|800|plantao)(?:\s|$)/i;
                              const is0800Trigger = regex0800.test(txt) || txt.includes("0800");
                              
                              const isAcompTrigger = txt.includes("acompanhamento") || txt.includes("acomp");
                              
                              if (is0800Trigger && !isIgnored) {
                                  data0800.push(cleanRow);
                              } else if (isAcompTrigger && !isIgnored) {
                                  dataAcomp.push(cleanRow);
                              } else {
"""

# Just find the exact substring to replace
target = """const txt = ((row["Descrio da Tarefa"]||"") + " " + (row["Descrio da Falha (Completa)"]||"")).toLowerCase();
                                if (txt.includes("0800")) {
                                    data0800.push(cleanRow);
                                } else if (txt.includes("acompanhamento")) {
                                    dataAcomp.push(cleanRow);
                                } else {"""

code = code.replace(target, excel_logic)

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)

print("Pached excel logic")



