filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = [9, 10, 11, 12, 13, 14, 692, 693, 694, 695, 1013, 1017, 1158, 1177, 1264, 3594, 3598, 3939, 3943]
for t in targets:
    if t-1 < len(lines):
        print(f"Line {t}: {repr(lines[t-1])}")
