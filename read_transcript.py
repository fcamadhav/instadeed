import json

log_file = "C:/Users/fcama/.gemini/antigravity/brain/09be3ae1-8f8d-432b-a4c7-5513355cac8d/.system_generated/logs/transcript.jsonl"
steps = []
with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            steps.append(json.loads(line))
        except:
            pass

print("Total steps in transcript:", len(steps))

with open("transcript_filtered.txt", "w", encoding="utf-8") as out:
    for idx, step in enumerate(steps):
        content = str(step.get('content', ''))
        # Let's search for user input or content related to PDF mismatch
        is_relevant = False
        if step.get('type') == 'USER_INPUT':
            is_relevant = True
        elif 'builder_tm' in content:
            is_relevant = True
        elif 'pdf is not' in content:
            is_relevant = True
        elif 'render_all_pdf' in content:
            is_relevant = True
        
        if is_relevant:
            out.write(f"Step {idx}: Type={step.get('type')}, Source={step.get('source')}\n")
            out.write(content + "\n")
            out.write("=" * 80 + "\n")
print("Filtered transcript written to transcript_filtered.txt")
