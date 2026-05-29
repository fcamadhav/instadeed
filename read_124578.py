import sys
from pypdf import PdfReader

path = 'C:/Users/fcama/Downloads/124578.pdf'
try:
    reader = PdfReader(path)
    print(f"Number of pages: {len(reader.pages)}")
    with open('124578_extracted.txt', 'w', encoding='utf-8') as f:
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            f.write(f"--- PAGE {idx+1} ---\n")
            f.write(text)
            f.write("\n\n")
    print("Successfully extracted text to 124578_extracted.txt")
except Exception as e:
    print(f"Error: {e}")
