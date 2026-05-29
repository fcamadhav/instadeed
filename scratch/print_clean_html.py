import re

filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(1698, 1715):
    line = lines[idx]
    cleaned = re.sub(r'src="data:image/[^;]+;base64,[^"]+"', 'src="data:image/png;base64,..."', line)
    print(f"{idx+1}: {cleaned}", end='')
