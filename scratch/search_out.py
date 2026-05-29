with open('c:\\Users\\fcama\\.gemini\\antigravity\\scratch\\madhav-legal-drafter\\Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("out.js in html:", "out.js" in content)
print("test_script.jsx in html:", "test_script.jsx" in content)
print("type=\"text/babel\" in html:", 'type="text/babel"' in content)
