﻿import json

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"

results = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            content = data.get('content', '')
            if 'make0800Obj' in content or 'makeAcompObj' in content:
                results.append((data.get('step_index'), content[:5000]))
        except:
            pass

print(f"Found {len(results)} results")
if results:
    step, code = results[-1]
    print(f"Step {step}:")
    print(code)


