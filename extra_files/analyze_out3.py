import sys
f=open('test_script.jsx','r',encoding='utf-8')
s=f.read()
f.close()

# Find the layout container and its closing
idx = s.find('app-layout-container')
print("Layout container starts at char", idx)
print("Line:", s[:idx].count("\n") + 1)

# Find the matching close by counting divs
open_div = s.find('<div', idx)
count = 1
pos = open_div
while count > 0 and pos < len(s):
    nxt_open = s.find('<div', pos+1)
    nxt_close = s.find('</div>', pos+1)
    if nxt_open != -1 and nxt_open < nxt_close:
        count += 1
        pos = nxt_open
    else:
        count -= 1
        pos = nxt_close

line_num = s[:pos].count("\n") + 1
print("Layout container closes at char", pos, "line", line_num)

# Print context around the closing
ctx_start = max(0, pos-100)
ctx_end = min(len(s), pos+200)
print("\nContext around closing:")
sys.stdout.reconfigure(encoding='utf-8')
print(s[ctx_start:ctx_end].encode('ascii', errors='replace').decode('ascii'))
