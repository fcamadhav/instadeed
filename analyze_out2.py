f=open('test_script.jsx','r',encoding='utf-8')
s=f.read()
f.close()

# Find the right panel area - the one that shows document preview
# Search for the preview container
idx = s.find('bg-dot-pattern')
if idx > 0:
    start = max(0, idx-500)
    end = min(len(s), idx+2000)
    print("=== Right panel (preview area) ===")
    open('analysis_output.txt','w',encoding='utf-8').write(s[start:end])

# Also find the closing of the whole layout
idx2 = s.find('app-layout-container')
if idx2 > 0:
    layout_end = s.find('</div>', idx2+30000)
    print("\n=== Layout end ===")
    print(s[layout_end-200:layout_end+50])
    
print("\nTotal file length:", len(s))
