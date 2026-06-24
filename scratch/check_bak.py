with open("landing.html.bak", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in landing.html.bak: {len(lines)}")
# Find tag counts or specific tags
tags_found = []
for idx, line in enumerate(lines):
    line_strip = line.strip()
    if "<body" in line_strip or "</body" in line_strip or "class=\"topbar" in line_strip or "class=\"hero" in line_strip:
        tags_found.append(f"{idx+1}: {line_strip[:120]}")

print("Tags found:")
for t in tags_found[:20]:
    print(t)
