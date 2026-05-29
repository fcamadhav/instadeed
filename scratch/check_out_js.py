filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

if 'out.js' in content.lower():
    print("Found reference to out.js")
else:
    print("No references to out.js")
