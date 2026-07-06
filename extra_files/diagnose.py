import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract babel block
start = content.find('<script type="text/babel">') + len('<script type="text/babel">')
end = content.rfind('</script>')
babel = content[start:end]

# Try to find issues by looking for common Babel-breaking patterns
# that our paren counter can't catch:

lines = babel.split('\n')

# 1. Check for arrow functions with wrong syntax
# e.g. => without proper params
import re
for i, l in enumerate(lines):
    # Look for `=> {` that isn't preceded by ) or a variable name
    if '=>' in l:
        idx = l.index('=>')
        before = l[:idx].rstrip()
        if before and before[-1] not in ')}]_ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
            print(f"Suspicious arrow at line {i+347}: {l.strip()[:80]}")

# 2. Check for missing commas in object literals (very common JSX error)
# Look for lines like: key: value\n key: value (missing comma)
print()
print("=== Checking for the SPECIFIC onerror handler ===")
for i, l in enumerate(lines):
    if 'window.onerror' in l or 'onerror' in l.lower():
        for j in range(max(0,i-2), min(len(lines), i+12)):
            print(f"  babel-line {j+1} (file {j+347}): {lines[j].rstrip()[:100]}")
        break

# 3. THE KEY CHECK: Is window.onerror INSIDE the babel block?
print()
if 'window.onerror' in babel:
    print("WARNING: window.onerror IS inside the Babel block!")
else:
    print("OK: window.onerror is NOT in the Babel block")

# 4. Check for the exact script tag structure
print()
print("=== Script tags in the file ===")
for m in re.finditer(r'<script[^>]*>', content, flags=re.IGNORECASE):
    line_num = content[:m.start()].count('\n') + 1
    print(f"  Line {line_num}: {m.group()}")

print()
print("=== </script> tags ===")
for m in re.finditer(r'</script>', content, flags=re.IGNORECASE):
    line_num = content[:m.start()].count('\n') + 1
    print(f"  Line {line_num}: </script>")
