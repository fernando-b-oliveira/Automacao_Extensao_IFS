﻿import subprocess
with open("test.js", "w", encoding="utf-8") as f:
    f.write("var WScript = {Echo: function(){}}; \n")
    with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", "r", encoding="utf-8") as js:
        f.write(js.read())

result = subprocess.run(["cscript", "//E:JScript", "test.js"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)


