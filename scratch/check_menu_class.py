with open("landing.html", "r", encoding="utf-8") as f:
    text = f.read()
print(f"class=\"user-menu\" in file: {'class=\"user-menu\"' in text}")
