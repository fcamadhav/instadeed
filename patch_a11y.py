import re
file_path = r'C:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\frontend\src\App.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix img without alt
def fix_img(match):
    tag = match.group(0)
    if 'alt=' not in tag:
        return tag.replace('<img', '<img alt="Decorative image"')
    return tag

content = re.sub(r'<img\b[^>]*>', fix_img, content)

# Fix button without aria-label
def fix_button(match):
    tag = match.group(0)
    if 'aria-label=' not in tag:
        title_match = re.search(r'title=["\']([^"\']+)["\']', tag)
        label = title_match.group(1) if title_match else 'Action button'
        return tag.replace('<button', f'<button aria-label="{label}"')
    return tag

content = re.sub(r'<button\b[^>]*>', fix_button, content)

# Fix SVG missing aria-hidden
def fix_svg(match):
    tag = match.group(0)
    if 'aria-hidden=' not in tag:
        return tag.replace('<svg', '<svg aria-hidden="true"')
    return tag

content = re.sub(r'<svg\b[^>]*>', fix_svg, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched App.jsx for accessibility')
