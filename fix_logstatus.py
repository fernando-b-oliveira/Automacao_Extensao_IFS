﻿with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'r', encoding='utf-8') as f:
    code = f.read()

# First, fix all double \r\r\n to \r\n
code = code.replace('\r\r\n', '\r\n')

logStatusFn = "        function logStatus(msg) {\r\n            const logDiv = document.getElementById('status-log');\r\n            if(logDiv) {\r\n                logDiv.innerHTML += '> ' + msg + '<br>';\r\n                logDiv.scrollTop = logDiv.scrollHeight;\r\n            }\r\n        }\r\n\r\n        "

# Find where btn_iniciar listener is set and inject logStatus before it
target = "        setTimeout(() => {\r\n            document.getElementById('btn_iniciar').addEventListener('click', () => {"
replacement = logStatusFn + target

if target in code:
    code = code.replace(target, replacement, 1)
    print("logStatus injected!")
else:
    # Try without \r
    target2 = "        setTimeout(() => {\n            document.getElementById('btn_iniciar').addEventListener('click', () => {"
    if target2 in code:
        code = code.replace(target2, logStatusFn.replace('\r\n', '\n') + target2, 1)
        print("logStatus injected (unix)!")
    else:
        print("TARGET NOT FOUND. Searching...")
        idx = code.find("setTimeout(() => {")
        print("setTimeout found at index:", idx)
        print("Context:", repr(code[idx-5:idx+100]))

with open(r"C:\\Projetos\\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content.js", 'w', encoding='utf-8') as f:
    f.write(code)

print("Done!")



