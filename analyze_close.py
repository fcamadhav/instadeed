f=open('test_script.jsx','r',encoding='utf-8')
s=f.read()
f.close()

sidx = s.find('app-layout-container')
opening = s.find('<div', sidx)
count = 1
pos = opening
while count > 0 and pos < len(s):
    nxt_open = s.find('<div', pos+1)
    nxt_close = s.find('</div>', pos+1)
    if nxt_open != -1 and nxt_open < nxt_close:
        count += 1
        pos = nxt_open
    else:
        count -= 1
        pos = nxt_close

line_num = s[:pos].count('\n') + 1
ctx = s[max(0,pos-80):pos+120]

# Write to file using ascii-safe encoding
o = open('close_ctx.txt','w',encoding='ascii',errors='replace')
o.write(f'Line: {line_num}\n')
o.write(ctx)
o.close()
print("Done")
