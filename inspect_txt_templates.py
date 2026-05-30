with open('noida_tm_form_full_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("First 2000 chars of noida_tm_form_full_extracted.txt:")
print(text[:2000])

print("\n--- Search for numbered sections or headers ---")
import re
# Let's search for capitalised lines or common headers like "AFFIDAVIT" or "INDEMNITY"
headers = re.findall(r'^[A-Z\s]{5,50}$', text, re.MULTILINE)
print("Potential headers found:", list(set(headers))[:20])
