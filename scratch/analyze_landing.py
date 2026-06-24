import re

with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find sections and key headers
sections = re.findall(r'<!--\s*═════*[\s\S]*?═════*\s*-->', content)
print("=== Sections Comments ===")
for s in sections:
    print(s.strip())

# Find H1, H2, and H3 headers
print("\n=== Header Tags ===")
headers = re.findall(r'<h[1-3][^>]*>[\s\S]*?</h[1-3]>', content)
for h in headers[:20]:
    # clean HTML tags for printing
    clean_h = re.sub('<[^<]+?>', '', h).strip()
    print(f"{h[:4]}: {clean_h}")
