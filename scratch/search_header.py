filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if 'header' in line.lower() or 'navigation' in line.lower() or 'nav' in line.lower():
        if len(line.strip()) < 150:
            print(f"Line {idx}: {line.strip()}")
