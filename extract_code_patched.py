﻿import json

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"
out_path = r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content_final.js"

content = ""

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    if 'content.js' in args.get('TargetFile', ''):
                        if 'CodeContent' in args:
                            content = args['CodeContent']
                        elif 'ReplacementContent' in args:
                            target = args['TargetContent']
                            replacement = args['ReplacementContent']
                            content = content.replace(target, replacement)
        except Exception as e:
            pass

with open(out_path, 'w', encoding='utf-8') as out:
    out.write(content)
print("Applied all patches!")


