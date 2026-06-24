import os

term = "regrentdata"
found_any = False
# Start search from the parent directory: c:\Users\fcama\.gemini\antigravity\scratch
start_dir = r"c:\Users\fcama\.gemini\antigravity\scratch"
for root, dirs, files in os.walk(start_dir):
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
                    for i, line in enumerate(content.splitlines()):
                        if term in line.lower():
                            print(f"  Line {i+1}: {line.strip()}")
            except Exception as e:
                pass

if not found_any:
    print(f"'{term}' not found in any files under {start_dir}.")
