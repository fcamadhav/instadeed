with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find index 752118, which is the start of the TM preview rendering logic
start = 752118
end = 837000 # and end of it is around 837000 (after JOINT AFFIDAVIT)

# Find all div starts: <div className=... or comments inside this block
import re
div_matches = re.finditer(r'<div\s+className=["`\{]', content[start:end])
print("Div starts inside the TM preview block:")
for m in list(div_matches)[:40]:
    abs_idx = start + m.start()
    # Print the line containing this div
    line_start = content.rfind('\n', 0, abs_idx) + 1
    line_end = content.find('\n', abs_idx)
    line = content[line_start:line_end].strip()
    # If the line contains "paper-page" or "DOCUMENT" or similar, print it
    if "paper-page" in line or "DOCUMENT" in line or "Page" in line or "PAGE" in line:
        print(f"Index {abs_idx}: {line}")
