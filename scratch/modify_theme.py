import re

file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Google Font link
old_font_link = """    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&family=Libre+Baskerville:wght@700&family=Plus+Jakarta+Sans:wght@700;800;900&display=swap"
        rel="stylesheet">"""

new_font_link = """    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,700&family=Merriweather:wght@300;400;700&family=Libre+Baskerville:wght@700&display=swap" rel="stylesheet">"""

if old_font_link in content:
    content = content.replace(old_font_link, new_font_link)
else:
    # try with different spaces
    pattern = r'<link\s+href="https://fonts.googleapis.com/css2\?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&family=Libre\+Baskerville:wght@700&family=Plus\+Jakarta\+Sans:wght@700;800;900&display=swap"\s+rel="stylesheet">'
    content = re.sub(pattern, new_font_link, content, flags=re.DOTALL)

# 2. Replace Tailwind config fontFamily.ui
old_tailwind_ui = "ui: ['\"Inter\"', 'sans-serif'],"
new_tailwind_ui = "ui: ['\"Plus Jakarta Sans\"', '\"Inter\"', 'sans-serif'],"
content = content.replace(old_tailwind_ui, new_tailwind_ui)

# 3. Replace body font family
old_body_font = 'font-family: "Inter", sans-serif;'
new_body_font = 'font-family: "Plus Jakarta Sans", "Inter", sans-serif;'
content = content.replace(old_body_font, new_body_font)

# 4. Replace Title to match landing page style
old_title = '<title>INSTADEED - Legal Drafting Hub</title>'
new_title = '<title>INSTADEED – Legal Drafting Suite | Draft, eSign & Deliver</title>'
content = content.replace(old_title, new_title)

# 5. Replace indigo theme classes with blue theme classes to match landing page
content = content.replace('bg-indigo-600', 'bg-blue-600')
content = content.replace('hover:bg-indigo-700', 'hover:bg-blue-700')
content = content.replace('text-indigo-600', 'text-blue-600')
content = content.replace('text-indigo-700', 'text-blue-700')
content = content.replace('text-indigo-800', 'text-blue-800')
content = content.replace('bg-indigo-50', 'bg-blue-50')
content = content.replace('border-indigo-100', 'border-blue-100')
content = content.replace('hover:border-indigo-100', 'hover:border-blue-100')
content = content.replace('hover:bg-indigo-50', 'hover:bg-blue-50')
content = content.replace('focus:border-indigo-500', 'focus:border-blue-500')
content = content.replace('shadow-indigo-200', 'shadow-blue-200')
content = content.replace('shadow-indigo-100', 'shadow-blue-100')
content = content.replace('indigo-500/10', 'blue-500/10')
content = content.replace('indigo-400/20', 'blue-400/20')
content = content.replace('text-indigo-300', 'text-blue-300')
content = content.replace('bg-indigo-600/10', 'bg-blue-600/10')
content = content.replace('border-indigo-50', 'border-blue-50')
content = content.replace('from-indigo-500/10', 'from-blue-500/10')
content = content.replace('to-blue-500/10', 'to-blue-600/10')
content = content.replace('border-indigo-500', 'border-blue-600')
content = content.replace('ring-indigo-100', 'ring-blue-100')
content = content.replace('bg-indigo-100', 'bg-blue-100')
content = content.replace('text-indigo-500', 'text-blue-500')
content = content.replace('text-indigo-800', 'text-blue-800')
content = content.replace('hover:text-indigo-600', 'hover:text-blue-600')
content = content.replace('from-slate-900 via-indigo-950 to-slate-950', 'from-slate-900 via-blue-950 to-slate-950')
content = content.replace('bg-indigo-600/10', 'bg-blue-600/10')
content = content.replace('bg-purple-600/10', 'bg-sky-600/10')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Theme updated successfully!")
