filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(1700, 1712):
    print(f"{idx+1}: {lines[idx].strip()}")
