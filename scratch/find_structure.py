with open("landing.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        line_strip = line.strip()
        # Find structural tags or classes
        if any(term in line_strip for term in ["<nav", "<section", "<footer", "<header", "class=\"topbar", "class=\"hero", "class=\"stats-bar", "class=\"catalog-section"]):
            print(f"{idx+1}: {line_strip}")
