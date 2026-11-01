﻿import json
import re

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content_final.js", 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix fetchAll 404 crash
code = code.replace(
    'if (!res.ok) throw new Error("Erro HTTP: " + res.status);',
    'if (!res.ok) { if (res.status === 404) return []; throw new Error("Erro HTTP: " + res.status); }'
)

# 2. Fix the %20 space URL bug in TaskSeq
code = code.replace(
    "const filtro = lote.map(t => `TaskSeq eq ${t}`).join(' or ');",
    "const filtro = lote.map(t => `TaskSeq eq ${t}`).join(' or ').replace(/ /g, '%20');"
)

# 3. Fix the %20 space URL bug in WoNo (Active)
code = code.replace(
    "const filtro = lote.map(w => `WoNo eq ${w}`).join(' or ');",
    "const filtro = lote.map(w => `WoNo eq ${w}`).join(' or ').replace(/ /g, '%20');"
)

# 4. We need to add the beautiful UI inside the SUPER_PAINEL if block
ui_html = """
        document.title = "ERP Ops - Painel de Gestão e Extração";
        document.body.innerHTML = `
            <div style="background: #f4f6f8; min-height: 100vh; padding-top: 40px; box-sizing: border-box;">
                <div style="font-family: 'Segoe UI', Arial, sans-serif; background: #fff; max-width: 650px; margin: 0 auto; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,67,139,0.1); border-top: 8px solid #3b82f6;">
                    
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #1e293b; margin: 0; font-size: 48px; font-weight: 900; letter-spacing: -2px;">ERP <span style="color: #3b82f6;">Ops</span></h1>
                        <h2 style="color: #555; margin-top: 5px; font-size: 20px; font-weight: 400;">Super Painel de Operações</h2>
                        <p style="color: #888; font-size: 14px; margin-top: 10px;">Defina os filtros abaixo para extrair os dados do SISTEMA_ERP_EXEMPLO.</p>
                    </div>
                    
                    <div style="margin-bottom: 25px;">
                        <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #1e293b;">Data Inicial dos Apontamentos:</label>
                        <input type="date" id="filtro_data_inicio" value="2026-04-01" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 6px; box-sizing: border-box; font-size: 16px; outline: none; transition: 0.3s;" onfocus="this.style.borderColor='#1e293b'" onblur="this.style.borderColor='#e0e0e0'">
                    </div>

                    <div style="margin-bottom: 25px;">
                        <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #1e293b;">Data Final (Opcional):</label>
                        <input type="date" id="filtro_data_fim" style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 6px; box-sizing: border-box; font-size: 16px; outline: none; transition: 0.3s;" onfocus="this.style.borderColor='#1e293b'" onblur="this.style.borderColor='#e0e0e0'">
                    </div>

                    <div style="margin-bottom: 35px; background: #f8fbff; padding: 20px; border-radius: 8px; border: 1px solid #dce8f4;">
                        <label style="font-weight: bold; display: block; margin-bottom: 15px; color: #1e293b; font-size: 16px;">Filtros de Extração (Selecione o que deseja baixar):</label>
                        
                        <div style="display: flex; gap: 30px; margin-bottom: 20px; background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0;">
                            <label style="cursor: pointer; font-size: 16px; display: flex; align-items: center; color: #333; font-weight: 500;">
                                <input type="checkbox" id="chk_0800" value="0800" checked style="width: 22px; height: 22px; margin-right: 10px; cursor: pointer; accent-color: #3b82f6;"> 🚨 Plantão 0800
                            </label>
                            <label style="cursor: pointer; font-size: 16px; display: flex; align-items: center; color: #333; font-weight: 500;">
                                <input type="checkbox" id="chk_acomp" value="acompanhamento" checked style="width: 22px; height: 22px; margin-right: 10px; cursor: pointer; accent-color: #3b82f6;"> 🚧 Acompanhamentos
                            </label>
                        </div>
                        
                        <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #1e293b; font-size: 16px;">Telas / APIs para Extração Adicional (Opcional):</label>
                        <div style="margin-bottom: 20px; background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0; position: relative;">
                            <input type="text" id="api_search" placeholder="Pesquisar tela (ex: Equipamento, Estoque)..." autocomplete="off" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px; font-size: 14px;">
                            <div id="api_suggestions" style="display: none; position: absolute; top: 52px; left: 15px; right: 15px; background: #fff; border: 1px solid #ccc; border-radius: 4px; max-height: 150px; overflow-y: auto; z-index: 10; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></div>
                            <label style="font-size: 13px; color: #666; font-weight: bold; margin-bottom: 8px; display: block;">APIs Selecionadas para o Relatório:</label>
                            <div id="api_selected_list" style="display: flex; flex-direction: column; gap: 8px;">
                                <label style="display:flex; align-items:center; font-size: 13px; color: #333;"><input type="checkbox" checked disabled style="margin-right: 6px; accent-color: #1e293b;"> Apontamentos de Tempo (Usado no 0800)</label>
                                <label style="display:flex; align-items:center; font-size: 13px; color: #333;"><input type="checkbox" checked disabled style="margin-right: 6px; accent-color: #1e293b;"> Tarefas de Serviço (Usado no 0800)</label>
                                <label style="display:flex; align-items:center; font-size: 13px; color: #333;"><input type="checkbox" checked disabled style="margin-right: 6px; accent-color: #1e293b;"> Ordens de Serviço Ativas (Usado no 0800)</label>
                                <label style="display:flex; align-items:center; font-size: 13px; color: #333;"><input type="checkbox" checked disabled style="margin-right: 6px; accent-color: #1e293b;"> Histórico de Ordens de Serviço (Usado no 0800)</label>
                            </div>
                        </div>

                        <label style="font-weight: bold; display: block; margin-bottom: 8px; color: #555; font-size: 14px;">Palavra-chave extra (Opcional):</label>
                        <input type="text" id="filtro_palavra" placeholder="Ex: manutenção, vazamento, corretiva..." style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 6px; box-sizing: border-box; font-size: 16px; outline: none; transition: 0.3s;" onfocus="this.style.borderColor='#1e293b'" onblur="this.style.borderColor='#e0e0e0'">
                    </div>

                    <button id="btn_iniciar" style="width: 100%; background: #3b82f6; color: white; border: none; padding: 18px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(122, 193, 66, 0.4);" onmouseover="this.style.backgroundColor='#2563eb'" onmouseout="this.style.backgroundColor='#3b82f6'">🚀 Extrair Dados do SISTEMA_ERP_EXEMPLO</button>
                    
                    <p style="text-align: center; color: #999; font-size: 13px; margin-top: 25px;">Desenvolvido exclusivamente para as operações da EMPRESA_EXEMPLO.</p>
                </div>
            </div>
        `;
        
        setTimeout(() => {
            document.getElementById('btn_iniciar').addEventListener('click', () => {
                const fData = document.getElementById('filtro_data_inicio').value;
                if(fData) filterDateApontamento = fData + "T00:00:00Z";
                
                document.body.innerHTML = `
                    <div style="font-family: 'Segoe UI', sans-serif; text-align: center; margin-top: 50px;">
                        <h1 style="color: #107c41;">⚙️ Construindo o Super Painel SISTEMA_ERP_EXEMPLO...</h1>
                        <p>O robô está cruzando as APIs em tempo real. Isso pode levar alguns segundos...</p>
                        <div id="status-log" style="background: #2b2b2b; color: #0f0; font-family: monospace; padding: 20px; width: 60%; margin: auto; text-align: left; height: 300px; overflow-y: auto; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                            > Conectando ao Banco de Dados do SISTEMA_ERP_EXEMPLO...<br>
                        </div>
                    </div>
                `;
                iniciarSuperPainel();
            });
        }, 500);
"""

# Replace the direct call to iniciarSuperPainel() with the UI
code = re.sub(
    r"document\.body\.innerHTML = `[\s\S]*?<div id=\"status-log\"[\s\S]*?</div>[\s\S]*?`;[\s\S]*?async function fetchAll",
    lambda m: ui_html + "\n\n        let filterDateApontamento = \"2026-04-01T00:00:00Z\";\n\n        async function fetchAll",
    code,
    flags=re.IGNORECASE
)

# Replace the hardcoded filterDateApontamento inside iniciarSuperPainel
code = code.replace(
    'const filterDateApontamento = "2026-04-01T00:00:00Z";',
    '// filterDateApontamento gets value from UI'
)

# Remove the automatic call to iniciarSuperPainel() at the end
code = code.replace(
    '        iniciarSuperPainel();\n    } \n    //',
    '    } \n    //'
)

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

pattern = r'const txt = \(\(row\["Descri\S+o da Tarefa"\]\|\|""\) \+ " " \+ \(row\["Descri\S+o da Falha \(Completa\)"\]\|\|""\)\)\.toLowerCase\(\);\s+if \(txt\.includes\("0800"\)\) \{\s+data0800\.push\(cleanRow\);\s+\} else if \(txt\.includes\("acompanhamento"\)\) \{\s+dataAcomp\.push\(cleanRow\);\s+\} else \{'

code = re.sub(pattern, lambda m: excel_logic, code, flags=re.IGNORECASE)

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)

print("Generated PERFECT content.js!")



