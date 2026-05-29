import re
import sys

def check_jsx_tags(code):
    tag_regex = re.compile(r'(</?[a-zA-Z][a-zA-Z0-9.-]*(?:\s+[^>]*?)?/?>|{/\*.*?\*/})')
    
    stack = []
    lines = code.split('\n')
    
    print("Scanning for unclosed JSX tags...")
    errors = 0
    for i, line in enumerate(lines, 1):
        for match in tag_regex.finditer(line):
            tag_str = match.group(1)
            if tag_str.startswith('{/*') and tag_str.endswith('*/}'):
                continue
                
            if tag_str.endswith('/>') or tag_str.startswith('<input') or tag_str.startswith('<img') or tag_str.startswith('<br') or tag_str.startswith('<hr'):
                if not tag_str.endswith('/>') and not tag_str.startswith('</'):
                    continue
            
            if tag_str.startswith('</'):
                tag_name = tag_str[2:].strip()[:-1].strip()
                if not stack:
                    print(f"Error at line {i}: Closing tag {tag_str} without opening tag")
                    errors += 1
                else:
                    open_tag, open_line, open_str = stack.pop()
                    if open_tag != tag_name:
                        print(f"Mismatched tag at line {i}: Found {tag_str}, expected closing for {open_str} from line {open_line}")
                        errors += 1
                        stack.append((open_tag, open_line, open_str))
            elif tag_str.startswith('<') and not tag_str.endswith('/>'):
                parts = tag_str[1:-1].split()
                if parts:
                    tag_name = parts[0]
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9.-]*$', tag_name):
                        stack.append((tag_name, i, tag_str))
                        
    if stack:
        print("\nUnclosed tags remaining in stack:")
        for tag_name, line, tag_str in reversed(stack):
            print(f"Line {line}: {tag_str}")
        errors += len(stack)
    else:
        print("\nAll tags matched!")
    return errors

if __name__ == '__main__':
    with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
        content = f.read()

    script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    if not script_match:
        print("No Babel script found")
        sys.exit(1)

    errors = check_jsx_tags(script_match.group(1))
    if errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)
