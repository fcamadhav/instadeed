import os

workspace = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter"
keywords = ['madhav', 'madhav legal']

for root, dirs, files in os.walk(workspace):
    # Skip only sub-scratch folder and node_modules
    rel_path = os.path.relpath(root, workspace)
    rel_parts = rel_path.split(os.sep)
    if 'node_modules' in rel_parts or '.git' in rel_parts or 'scratch' in rel_parts:
        continue
    for file in files:
        if file.endswith(('.html', '.js', '.py')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                matches = []
                for kw in keywords:
                    if kw in content.lower():
                        matches.append(kw)
                if matches:
                    print(f"File {file}: contains keywords {matches}")
            except Exception as e:
                pass
