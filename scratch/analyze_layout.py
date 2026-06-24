import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("landing.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
# Find tag lines and their line numbers starting from line 1100 to 2402
for idx, line in enumerate(lines[1180:]):
    line_idx = idx + 1181
    line_strip = line.strip()
    if line_strip.startswith("<body") or line_strip.startswith("<nav") or line_strip.startswith("<section") or line_strip.startswith("<footer") or line_strip.startswith("<!--"):
        print(f"{line_idx}: {line_strip[:120]}")
