import os

term = "regrentdata"
found = False
for file in os.listdir('.'):
    if file.endswith('.html'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        if term in content.lower():
            found = True
            print(f"Found in html file: {file}")
            for i, line in enumerate(content.splitlines()):
                if term in line.lower():
                    print(f"  Line {i+1}: {line.strip()}")

if not found:
    print("Not found in any HTML files in current directory.")
