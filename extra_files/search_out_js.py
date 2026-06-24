import os

term = "regrentdata"
found = False
if os.path.exists("out.js"):
    with open("out.js", 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if term in content.lower():
        found = True
        print("Found in out.js!")
        for i, line in enumerate(content.splitlines()):
            if term in line.lower():
                print(f"  Line {i+1}: {line.strip()[:150]}")
else:
    print("out.js not found!")

if not found:
    print("Not found in out.js.")
