import re

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as f:
    content = f.read()

# Add orphanOrders to baseOrders and mapOrders
search_logic = """                    const orphanTaskResults = await Promise.all(orphanTaskPromises);
                    const orphanTasks = orphanTaskResults.flat();
                    
                    // Merge tasks
                    tasks = [...tasks, ...orphanTasks];"""

replace_logic = """                    const orphanTaskResults = await Promise.all(orphanTaskPromises);
                    const orphanTasks = orphanTaskResults.flat();
                    
                    // ADD THE ORPHAN ORDERS TO THE MAIN DICTIONARY SO THEY CAN BE FILTERED PROPERLY!
                    orphanOrders.forEach(o => {
                        if (o.WoNo) {
                            mapOrders[o.WoNo] = o;
                        }
                    });
                    
                    // Merge tasks
                    tasks = [...tasks, ...orphanTasks];"""

content = content.replace(search_logic, replace_logic)

with open(r"C:\Automacao\Codigosf\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated to map orphan orders properly!")


