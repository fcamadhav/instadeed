import json
import os

def search_transcript(log_path, query):
    if not os.path.exists(log_path):
        print(f"Log path does not exist: {log_path}")
        return
        
    print(f"Searching for '{query}' in transcript...")
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                step = json.loads(line)
                content = step.get('content', '')
                tool_calls = step.get('tool_calls', [])
                
                # Check query in content or tool calls
                found = False
                if query.lower() in content.lower():
                    found = True
                for tc in tool_calls:
                    if query.lower() in str(tc).lower():
                        found = True
                        
                if found:
                    print(f"Step {step.get('step_index')}: {step.get('type')} from {step.get('source')}")
                    # Print a snippet of content
                    if content:
                        print("  Content snippet:", content[:200].replace('\n', ' '))
            except Exception as e:
                pass

if __name__ == '__main__':
    log_path = r"C:\Users\fcama\.gemini\antigravity\brain\09be3ae1-8f8d-432b-a4c7-5513355cac8d\.system_generated\logs\transcript.jsonl"
    search_transcript(log_path, "Rohan")
    search_transcript(log_path, "attorney")
