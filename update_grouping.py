import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the generation of "Dados Brutos Completos"
logic_search = """                                  if (isRawOnly) {
                                      // Se os dois tiverem desmarcados, puxa todas as colunas brutas (absolutamente todas)
                                      XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data), "Dados Brutos Completos");
                                  }"""

logic_replace = """                                  if (isRawOnly) {
                                      // Clonar e agrupar
                                      let rawData = JSON.parse(JSON.stringify(data));
                                      
                                      // Ordenar por OS e depois por Tarefa
                                      rawData.sort((a, b) => {
                                          const osA = _krx(a, /^N. OS$/i, "") || "";
                                          const osB = _krx(b, /^N. OS$/i, "") || "";
                                          if (osA !== osB) return osA.localeCompare(osB);
                                          
                                          const tA = _krx(a, /^N. Tarefa$/i, "") || "";
                                          const tB = _krx(b, /^N. Tarefa$/i, "") || "";
                                          return tA.localeCompare(tB);
                                      });
                                      
                                      let lastOs = null;
                                      
                                      const groupedData = rawData.map(row => {
                                          const currentOs = _krx(row, /^N. OS$/i, "");
                                          const rowCopy = { ...row };
                                          
                                          // Find the exact key for OS to blank it out
                                          const osKey = Object.keys(rowCopy).find(key => /^N. OS$/i.test(key));
                                          
                                          if (currentOs && currentOs === lastOs) {
                                              if (osKey) rowCopy[osKey] = ""; // Blank out for visual grouping
                                          } else {
                                              lastOs = currentOs;
                                          }
                                          
                                          return rowCopy;
                                      });
                                      
                                      // Optional: Reorder keys to match user preference: OS, Tarefa, Tipo, Tecnico, Data/Hora, Descricao
                                      const reorderedData = groupedData.map(row => {
                                          const newRow = {};
                                          const osK = Object.keys(row).find(k => /^N. OS$/i.test(k));
                                          const tK = Object.keys(row).find(k => /^N. Tarefa$/i.test(k));
                                          const tipoK = Object.keys(row).find(k => /Tipo.*Apontamento/i.test(k));
                                          const tecK = Object.keys(row).find(k => /^T[e\u00e9]cnico$/i.test(k));
                                          const dInK = Object.keys(row).find(k => /^Data In.cio$/i.test(k));
                                          const hInK = Object.keys(row).find(k => /^Hora In.cio$/i.test(k));
                                          const dFimK = Object.keys(row).find(k => /^Data Fim$/i.test(k));
                                          const hFimK = Object.keys(row).find(k => /^Hora Fim$/i.test(k));
                                          const descK = Object.keys(row).find(k => /Descri..o da Tarefa/i.test(k)) || Object.keys(row).find(k => /Descri..o/i.test(k));
                                          
                                          if (osK) newRow[osK] = row[osK];
                                          if (tK) newRow[tK] = row[tK];
                                          if (tipoK) newRow[tipoK] = row[tipoK];
                                          if (tecK) newRow[tecK] = row[tecK];
                                          if (dInK) newRow[dInK] = row[dInK];
                                          if (hInK) newRow[hInK] = row[hInK];
                                          if (dFimK) newRow[dFimK] = row[dFimK];
                                          if (hFimK) newRow[hFimK] = row[hFimK];
                                          if (descK) newRow[descK] = row[descK];
                                          
                                          // Add the rest
                                          for (const k in row) {
                                              if (!(k in newRow)) newRow[k] = row[k];
                                          }
                                          return newRow;
                                      });
                                      
                                      XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(reorderedData), "Dados Brutos Completos");
                                  }"""

content = content.replace(logic_search, logic_replace)

# Also apply this grouping logic to `dataBrutosAlvo` if both 0800 and acomp are selected
logic_search2 = """                                      return (is0800 && window.selectedTypes.do0800) || (isAcomp && window.selectedTypes.doAcomp);
                                      });
                                      XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataBrutosAlvo), "Dados Brutos");"""

logic_replace2 = """                                      return (is0800 && window.selectedTypes.do0800) || (isAcomp && window.selectedTypes.doAcomp);
                                      });
                                      
                                      // Clonar e agrupar para Dados Brutos filtrados
                                      let rawDataAlvo = JSON.parse(JSON.stringify(dataBrutosAlvo));
                                      
                                      rawDataAlvo.sort((a, b) => {
                                          const osA = _krx(a, /^N. OS$/i, "") || "";
                                          const osB = _krx(b, /^N. OS$/i, "") || "";
                                          if (osA !== osB) return osA.localeCompare(osB);
                                          
                                          const tA = _krx(a, /^N. Tarefa$/i, "") || "";
                                          const tB = _krx(b, /^N. Tarefa$/i, "") || "";
                                          return tA.localeCompare(tB);
                                      });
                                      
                                      let lastOsAlvo = null;
                                      
                                      const groupedDataAlvo = rawDataAlvo.map(row => {
                                          const currentOs = _krx(row, /^N. OS$/i, "");
                                          const rowCopy = { ...row };
                                          const osKey = Object.keys(rowCopy).find(key => /^N. OS$/i.test(key));
                                          
                                          if (currentOs && currentOs === lastOsAlvo) {
                                              if (osKey) rowCopy[osKey] = "";
                                          } else {
                                              lastOsAlvo = currentOs;
                                          }
                                          return rowCopy;
                                      });
                                      
                                      const reorderedDataAlvo = groupedDataAlvo.map(row => {
                                          const newRow = {};
                                          const osK = Object.keys(row).find(k => /^N. OS$/i.test(k));
                                          const tK = Object.keys(row).find(k => /^N. Tarefa$/i.test(k));
                                          const tipoK = Object.keys(row).find(k => /Tipo.*Apontamento/i.test(k));
                                          const tecK = Object.keys(row).find(k => /^T[e\u00e9]cnico$/i.test(k));
                                          const dInK = Object.keys(row).find(k => /^Data In.cio$/i.test(k));
                                          const hInK = Object.keys(row).find(k => /^Hora In.cio$/i.test(k));
                                          const dFimK = Object.keys(row).find(k => /^Data Fim$/i.test(k));
                                          const hFimK = Object.keys(row).find(k => /^Hora Fim$/i.test(k));
                                          const descK = Object.keys(row).find(k => /Descri..o da Tarefa/i.test(k)) || Object.keys(row).find(k => /Descri..o/i.test(k));
                                          
                                          if (osK) newRow[osK] = row[osK];
                                          if (tK) newRow[tK] = row[tK];
                                          if (tipoK) newRow[tipoK] = row[tipoK];
                                          if (tecK) newRow[tecK] = row[tecK];
                                          if (dInK) newRow[dInK] = row[dInK];
                                          if (hInK) newRow[hInK] = row[hInK];
                                          if (dFimK) newRow[dFimK] = row[dFimK];
                                          if (hFimK) newRow[hFimK] = row[hFimK];
                                          if (descK) newRow[descK] = row[descK];
                                          
                                          for (const k in row) {
                                              if (!(k in newRow)) newRow[k] = row[k];
                                          }
                                          return newRow;
                                      });
                                      
                                      XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(reorderedDataAlvo), "Dados Brutos");"""

content = content.replace(logic_search2, logic_replace2)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated grouping logic.")


