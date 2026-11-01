﻿with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

logStatusFn = """        function logStatus(msg) {
            const logDiv = document.getElementById('status-log');
            if(logDiv) {
                logDiv.innerHTML += '> ' + msg + '<br>';
                logDiv.scrollTop = logDiv.scrollHeight;
            }
        }

        """

# Find the exact start of the setTimeout (8 spaces before)
target = "setTimeout(() => {\n\n            document.getElementById('btn_iniciar').addEventListener('click', () => {"
if target in code:
    # Find how many spaces precede it
    pos = code.find(target)
    # Go back to find the newline
    start = code.rfind('\n', 0, pos) + 1
    prefix = code[start:pos]
    full_target = prefix + target
    code = code.replace(full_target, logStatusFn + full_target, 1)
    print("Injected!")
else:
    print("Not found. Trying simpler match...")
    target2 = "document.getElementById('btn_iniciar').addEventListener"
    pos = code.find(target2)
    # Find start of containing setTimeout
    start = code.rfind("setTimeout", 0, pos)
    # Find the newline before setTimeout
    nl_before = code.rfind('\n', 0, start) + 1
    insert_at = nl_before
    code = code[:insert_at] + logStatusFn + code[insert_at:]
    print("Injected at", insert_at)

with open(r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved!")


