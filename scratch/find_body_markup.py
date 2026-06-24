with open("landing.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        line_strip = line.strip()
        if "topbar" in line_strip or "hero-inner" in line_strip or "catalog-section" in line_strip:
            # Print matching lines with line numbers
            print(f"{idx+1}: {line_strip[:120]}")
