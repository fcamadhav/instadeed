filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    line_num = idx + 1
    if 'useeffect' in line.lower():
        print(f"Line {line_num}: {line.strip()[:120]}")
