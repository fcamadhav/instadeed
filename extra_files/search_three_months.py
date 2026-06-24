with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("three months")
if pos != -1:
    print("Found 'three months' at index:", pos)
    print(repr(content[pos-200:pos+200]))
else:
    print("'three months' not found")
