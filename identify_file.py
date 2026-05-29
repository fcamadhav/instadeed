
import sys

def read_header(path):
    try:
        with open(path, 'rb') as f:
            header = f.read(20)
            print(f"Header: {header}")
            
            f.seek(0)
            content = f.read()
            # simple strings implementation
            import re
            strings = re.findall(b"[a-zA-Z0-9\s\.,;:\-_\(\)]{4,}", content)
            print("--- First 20 strings ---")
            for s in strings[:20]:
                try:
                    print(s.decode('utf-8'))
                except:
                    pass
    except Exception as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        read_header(sys.argv[1])
