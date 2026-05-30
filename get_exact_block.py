import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = 3889 - 1
end_idx = 4203

block = "".join(lines[start_idx:end_idx])
print("BLOCK LENGTH:", len(block))
print("START 100 CHARS:")
print(repr(block[:100]))
print("END 100 CHARS:")
print(repr(block[-100:]))
