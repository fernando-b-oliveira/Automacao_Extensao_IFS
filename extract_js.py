﻿import json
import re

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"
out_path = r"C:\Users\UsuarioPadrao\Downloads\Extensao_SISTEMA_ERP_EXEMPLO\transcript_js.txt"

with open(transcript_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

blocks = []
for line in lines:
    if "make0800Obj" in line or "iniciarSuperPainel" in line:
        try:
            data = json.loads(line)
            
            # Find in thoughts
            if data.get('type') == 'PLANNER_RESPONSE':
                thought = data.get('thinking', '')
                if 'make0800Obj' in thought or 'iniciarSuperPainel' in thought:
                    blocks.append(thought)
                    
            # Find in tool_calls
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    if 'ReplacementContent' in args:
                        blocks.append(args['ReplacementContent'])
                    if 'CommandLine' in args:
                        blocks.append(args['CommandLine'])
                        
            # Find in generic outputs
            if data.get('type') == 'GENERIC':
                content = data.get('content', '')
                if 'make0800Obj' in content or 'iniciarSuperPainel' in content:
                    blocks.append(content)
        except Exception as e:
            pass

with open(out_path, 'w', encoding='utf-8') as out:
    for i, b in enumerate(blocks):
        out.write(f"--- BLOCK {i} ---\n")
        out.write(b + "\n")


