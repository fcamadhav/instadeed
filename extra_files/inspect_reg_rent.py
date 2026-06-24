import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_around(line_num, count=10):
    print(f"=== Around line {line_num} ===")
    start = max(0, line_num - count)
    end = min(len(lines), line_num + count)
    for idx in range(start, end):
        print(f"{idx+1}: {lines[idx]}", end="")

print_around(2914)
print_around(3334)
print_around(3354)
print_around(3379)
