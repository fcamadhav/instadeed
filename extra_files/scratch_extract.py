import re

with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    text = f.read()

script = re.search(r'<script type="text/babel">(.*?)</script>', text, re.DOTALL)
if script:
    with open('test_script.jsx', 'w', encoding='utf-8') as f:
        f.write(script.group(1))
    print('Script extracted.')
