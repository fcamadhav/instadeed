import re

with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove all gnidaRegistryData states
pattern = r'\s*const \[gnidaRegistryData, setGnidaRegistryData\] = useState\(\{.*?\}\);'
text = re.sub(pattern, '', text, flags=re.DOTALL)

with open('Madhav_Drafting_Hub_Final_Registry.html', 'r', encoding='utf-8') as f:
    src_lines = f.readlines()
state_code = "".join(src_lines[685:738])

# Insert exactly one instance before defaultATSData
text = text.replace('            const defaultATSData = {', state_code + '\n            const defaultATSData = {')

with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned up duplicate states!")
