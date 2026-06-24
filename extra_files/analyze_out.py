import re
f=open('out.js','r',encoding='utf-8')
s=f.read()
f.close()

# Find how the sidebar renders content based on activeTab
# Look for the pattern where it checks activeTab === 'HOME' or similar
patterns = [
    "activeTab === 'HOME'",
    "activeTab==='HOME'",
    '"HOME"',
]
for p in patterns:
    idx = s.find(p)
    if idx > 0:
        ctx = s[max(0,idx-200):idx+300]
        print(f"=== Found pattern '{p}' at {idx} ===")
        print(ctx)
        print()

# Also look for where the left sidebar renders form fields vs doc grid
idx = s.find('instadeed-authority-selector')
if idx > 0:
    # Find what wraps this - look backwards for a conditional
    before = s[max(0,idx-1500):idx]
    print("=== Before authority selector ===")
    print(before)
