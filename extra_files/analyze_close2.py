f=open('test_script.jsx','r',encoding='utf-8')
s=f.read()
f.close()

# Find the first app-layout-container and the second one (since we now have 2 - landing is first, layout is second)
first = s.find('app-layout-container')
second = s.find('app-layout-container', first+1)
print(f"First layout container at line {s[:first].count(chr(10))+1}")
print(f"Second layout container at line {s[:second].count(chr(10))+1}")

# Find the matching close for the second one
# The second one opens a div AFTER it, not at it. Let me find the exact opening
opening = s.rfind('<div', second-10, second+10)

# Count from there
count = 1
pos = opening
while count > 0 and pos < len(s):
    nxt_open = s.find('<div', pos+1)
    nxt_close = s.find('</div>', pos+1)
    if nxt_open != -1 and nxt_open < nxt_close:
        count += 1
        pos = nxt_open
    else:
        if count == 1 and nxt_close != -1:
            # This is the closing of our div
            pos = nxt_close
            break
        count -= 1
        pos = nxt_close

line_num = s[:pos].count(chr(10)) + 1
ctx = s[max(0,pos-100):pos+150]

o = open('close_ctx2.txt','w',encoding='ascii',errors='replace')
o.write(f'Line: {line_num}, Char: {pos}\n')
o.write(ctx)
o.write(f'\n---\nTotal lines: {s[:pos].count(chr(10))+1}')
o.close()
print("Done")
