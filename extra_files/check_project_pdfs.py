import os
import time

project_dir = 'c:/Users/fcama/.gemini/antigravity/scratch/madhav-legal-drafter'
files = [f for f in os.listdir(project_dir) if f.lower().endswith('.pdf')]
print("Project PDFs:")
for f in files:
    path = os.path.join(project_dir, f)
    size = os.path.getsize(path)
    mtime = os.path.getmtime(path)
    t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    print(f"{f} - Size: {size} bytes - Modified: {t_str}")
