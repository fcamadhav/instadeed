with open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
routes = re.findall(r'@app\.get\([\'"]/[\'"]\)(?:[\s\S]*?def\s+\w+\(.*?\):[\s\S]*?)(?=async\s+def|def|@app\.|\Z)', content)
print("Root routes:")
for r in routes:
    print(r.strip())
