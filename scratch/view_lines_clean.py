import sys

filepath = r"c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_lines_clean(start, end):
    for i in range(start - 1, min(end, len(lines))):
        line = lines[i]
        if len(line) > 150:
            truncated = line[:150].strip() + " ... [TRUNCATED]"
            print(f"{i+1}: {truncated}")
        else:
            print(f"{i+1}: {line}", end='')

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        print_lines_clean(int(sys.argv[1]), int(sys.argv[2]))
    else:
        print("Usage: python view_lines_clean.py <start> <end>")
