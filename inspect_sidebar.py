import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's search for "flex h-screen" or similar root container structure
# Often it is around the render function start, let's print lines 2000-2600 to find it
# Actually, let's write a script to search for the sidebar HTML.
# A sidebar is typically a column like <div className="w-80 or w-96 or w-1/4
# Let's search for classes with width in the outer layout.

for i, line in enumerate(lines):
    if 'w-80' in line or 'w-96' in line or 'sidebar' in line or 'aside' in line or 'flex flex-col' in line:
        if 'className=' in line and ('w-' in line or 'flex' in line) and i > 2000 and i < 4000:
            print(f"Line {i+1}: {line.strip()}")
