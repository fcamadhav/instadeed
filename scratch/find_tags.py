with open("landing.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        line_strip = line.strip()
        # Find any line that contains an HTML opening tag like <div, <nav, etc.
        if line_strip.startswith("<") and not line_strip.startswith("</") and not line_strip.startswith("<!--"):
            # print first 50 tag matches to inspect
            print(f"{idx+1}: {line_strip}")
