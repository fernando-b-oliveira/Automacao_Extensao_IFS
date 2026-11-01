﻿import json

transcript_path = r"C:\Users\UsuarioPadrao\.gemini\antigravity\brain\b42e1e42-5568-4858-98c3-14f28a5dd672\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for tc in data['tool_calls']:
                    args = tc.get('args', {})
                    if 'content.js' in str(args.get('TargetFile', '')) or 'content.js' in str(args.get('CommandLine', '')):
                        if 'uiHtml' in str(args) or 'Telas' in str(args):
                            print("FOUND IN STEP", data.get('step_index'))
                            print(json.dumps(args, indent=2, ensure_ascii=False))
        except Exception:
            pass


