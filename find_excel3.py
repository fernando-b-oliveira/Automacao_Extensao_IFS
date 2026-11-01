﻿import json

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    # Check CommandLine for relevant content
                    cmd = args.get('CommandLine', '')
                    if 'make0800Obj' in cmd or 'makeAcompObj' in cmd:
                        print(f"Step {data.get('step_index')}: FOUND IN COMMAND")
                        print(cmd[:3000])
                        print("---")
        except:
            pass


