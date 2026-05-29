with open('c:\\Users\\fcama\\.gemini\\antigravity\\scratch\\madhav-legal-drafter\\landing.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if 'out.js' in line:
            print(f"{idx}: {line.strip()}")
