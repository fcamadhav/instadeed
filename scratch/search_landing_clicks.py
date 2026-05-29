filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\landing.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if 'initiateRazorpayPayment' in line:
        print(f"Line {idx}: {line.strip()}")
