import os
import glob

html_files = glob.glob('c:\\Users\\fcama\\.gemini\\antigravity\\scratch\\madhav-legal-drafter\\*.html')
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'out.js' in content:
        print(f"out.js is referenced in {os.path.basename(fpath)}")
    if 'test_script' in content:
        print(f"test_script is referenced in {os.path.basename(fpath)}")
