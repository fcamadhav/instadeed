
import sys
import re

def extract_strings(path):
    try:
        with open(path, 'rb') as f:
            content = f.read()
            # Extract strings of length 3+
            strings = re.findall(b"[a-zA-Z0-9\s\.,;:\-_\(\)\[\]\/]{3,}", content)
            
            full_text = []
            for s in strings:
                try:
                    decoded = s.decode('utf-8').strip()
                    if decoded:
                        full_text.append(decoded)
                except:
                    pass
            
            return '\n'.join(full_text)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(extract_strings(sys.argv[1]))
