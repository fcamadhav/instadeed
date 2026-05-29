import json

def find_original_email():
    log_path = r"C:\Users\fcama\.gemini\antigravity\brain\09be3ae1-8f8d-432b-a4c7-5513355cac8d\.system_generated\logs\transcript.jsonl"
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                step = json.loads(line)
                for tc in step.get('tool_calls', []):
                    args = tc.get('args', {})
                    content = str(args.get('ReplacementContent', '')) or str(args.get('CodeContent', ''))
                    if 'attorney@' in content:
                        print(f"Step {step.get('step_index')}:")
                        print("  Target:", args.get('TargetFile'))
                        # print target vs replacement if available
                        target = str(args.get('TargetContent', ''))
                        if target:
                            print("  Target Content:", target.strip())
                        print("  Replacement Content:", content.strip()[:300])
            except Exception as e:
                pass

if __name__ == '__main__':
    find_original_email()
