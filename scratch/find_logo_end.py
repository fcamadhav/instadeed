filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(1700, min(1750, len(lines))):
    line = lines[idx]
    if len(line.strip()) < 200:
        print(f"Line {idx+1}: {line.strip()}")
