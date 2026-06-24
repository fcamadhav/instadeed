import sys
import os
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

dl = 'C:/Users/fcama/Downloads'
files = [f for f in os.listdir(dl) if f.lower().endswith('.pdf')]
print(f"Total PDFs to check: {len(files)}")
for f in files:
    path = os.path.join(dl, f)
    try:
        reader = PdfReader(path)
        pages = len(reader.pages)
        print(f"{f}: {pages} pages")
    except Exception as e:
        print(f"Error reading {f}: {e}")
