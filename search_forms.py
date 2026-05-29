import sys

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = []
for idx, line in enumerate(lines):
    if "NoidaTransferForm" in line or "renderNoidaTransfer" in line:
        targets.append((idx + 1, "NameMatch"))
    if "activeTab === 'NOIDA_TRANSFER'" in line:
        targets.append((idx + 1, "ActiveTabMatch"))

with open('search_forms_output.txt', 'w', encoding='utf-8') as out:
    out.write(f"Targets found: {targets}\n\n")
    for target, match_type in targets:
        out.write(f"--- Around Line {target} ({match_type}) ---\n")
        start = max(1, target - 10)
        end = min(len(lines), target + 50)
        for i in range(start, end + 1):
            out.write(f"{i}: {lines[i-1]}")
        out.write("\n\n")
