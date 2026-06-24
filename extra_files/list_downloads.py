import os
import time

dl = 'C:/Users/fcama/Downloads'
if not os.path.exists(dl):
    print("Downloads directory does not exist")
    exit()

files = [f for f in os.listdir(dl) if f.lower().endswith('.pdf')]
print(f"Total PDFs in Downloads: {len(files)}")
# Sort files by modification time descending
files_with_time = []
for f in files:
    path = os.path.join(dl, f)
    try:
        mtime = os.path.getmtime(path)
        size = os.path.getsize(path)
        files_with_time.append((f, mtime, size))
    except Exception as e:
        pass

files_with_time.sort(key=lambda x: x[1], reverse=True)

for f, mtime, size in files_with_time[:30]:
    t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    print(f"{f} - Size: {size} bytes - Modified: {t_str}")
