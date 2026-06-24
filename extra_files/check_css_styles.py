with open('Madhav_Drafting_Hub_dev.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Find style block
style_pos = html.find("<style>")
style_end = html.find("</style>", style_pos)
if style_pos != -1:
    print("CSS Style Block snippet:")
    styles = html[style_pos:style_end]
    for line in styles.splitlines():
        if 'paper-page' in line or 'page' in line or 'print' in line or 'h-' in line or 'height' in line:
            print(line.strip())
else:
    print("No style block found in HTML dev file")
