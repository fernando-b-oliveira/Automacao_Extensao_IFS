﻿import json

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"
out_path = r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\content_from_transcript.js"

last_code = None

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    if args.get('TargetFile') == 'C:\\Users\\usuario_padrao\\Downloads\\Extensao_SISTEMA_ERP_EXEMPLO\\content.js':
                        if 'CodeContent' in args:
                            last_code = args['CodeContent']
                        elif 'ReplacementContent' in args:
                            # It's a patch, we need the full file... let's just save the last CodeContent for now
                            pass
        except Exception:
            pass

if last_code:
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(last_code)
    print("Extracted CodeContent!")
else:
    print("No CodeContent found")


