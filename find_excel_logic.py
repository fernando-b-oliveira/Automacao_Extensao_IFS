﻿import json

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"

results = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    code = args.get('CodeContent', '') or args.get('ReplacementContent', '')
                    if 'make0800Obj' in code or 'makeAcompObj' in code:
                        results.append((data.get('step_index'), code[:3000]))
        except:
            pass

if results:
    step, code = results[-1]  # Get the last (most recent) version
    print(f"Step {step}:")
    print(code)
else:
    print("Not found")


