﻿import json
import sys

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"
out_path = r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_reconstruct2.txt"

with open(transcript_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(out_path, 'w', encoding='utf-8') as out:
    for line in lines:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    if tc['name'] == 'replace_file_content':
                        out.write("--- REPLACE ---\n")
                        out.write(tc['args'].get('ReplacementContent', '') + "\n")
        except:
            pass


