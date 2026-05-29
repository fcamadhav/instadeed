import re

def find_madhav(filepath):
    print(f"\n--- Occurrences of 'Madhav' in {filepath} ---")
    with open(filepath, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            if 'madhav' in line.lower():
                print(f"{idx}: {line.strip()}")

find_madhav('c:\\Users\\fcama\\.gemini\\antigravity\\scratch\\madhav-legal-drafter\\Madhav_Drafting_Hub.html')
find_madhav('c:\\Users\\fcama\\.gemini\\antigravity\\scratch\\madhav-legal-drafter\\landing.html')
