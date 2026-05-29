import sys

filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_lines(start, end):
    for i in range(start - 1, min(end, len(lines))):
        print(f"{i+1}: {lines[i]}", end='')

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        print_lines(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("Usage: python view_lines.py <start> <end>")
