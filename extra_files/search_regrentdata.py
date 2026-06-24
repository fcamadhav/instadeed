import os

term = "regrentdata"
found_any = False
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.jsx', '.json', '.txt')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if term in content.lower():
                    found_any = True
                    print(f"Found '{term}' (case-insensitive) in file: {path}")
                    # Find line number
                    for i, line in enumerate(content.splitlines()):
                        if term in line.lower():
                            print(f"  Line {i+1}: {line.strip()}")
            except Exception as e:
                pass

if not found_any:
    print(f"'{term}' not found in any files (case-insensitive).")
