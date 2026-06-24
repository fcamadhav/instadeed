import os

project_dir = 'c:/Users/fcama/.gemini/antigravity/scratch/madhav-legal-drafter'
for root, dirs, files in os.walk(project_dir):
    for f in files:
        if f.endswith('.txt') or f.endswith('.docx') or f.endswith('.doc'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if 'CAUTION' in content or 'deponents understand that receipt' in content:
                        print("Found keyword in:", path)
            except Exception as e:
                pass
