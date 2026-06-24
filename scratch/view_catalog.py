import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("landing.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(2613, 2645):
    print(f"{idx+1}: {lines[idx].strip()}")
