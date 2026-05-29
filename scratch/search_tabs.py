import re

filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r"setActiveTab\('([^']+)'\)", content)
unique_tabs = sorted(list(set(matches)))
print("Found tabs:", unique_tabs)
