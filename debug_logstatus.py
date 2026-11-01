﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# Find the exact text around 'btn_iniciar' addEventListener
import re

# Inject logStatus right before the setTimeout that has btn_iniciar
# Pattern: find setTimeout that contains btn_iniciar
pattern = r'(        setTimeout\(\(\) => \{\n(?:.|\n)*?btn_iniciar.*?\n)'
m = re.search(pattern, code)
if m:
    print("Found at:", m.start(), m.group()[:80])
else:
    # Find the SECOND setTimeout
    positions = [i for i in range(len(code)) if code[i:i+20] == "        setTimeout(("]
    print("All setTimeout positions:", positions)
    for pos in positions:
        print(f"  pos {pos}: {repr(code[pos:pos+120])[:150]}")


