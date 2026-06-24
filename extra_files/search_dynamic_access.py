import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's search for "regRent" or "REG_RENT" in test_script.jsx
with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- Searching for REG_RENT ---")
for i, line in enumerate(lines):
    if "REG_RENT" in line:
        print(f"Line {i+1}: {line.strip()}")

print("--- Searching for regData or regRent ---")
for i, line in enumerate(lines):
    if "regData" in line or "regrent" in line.lower():
        print(f"Line {i+1}: {line.strip()}")
