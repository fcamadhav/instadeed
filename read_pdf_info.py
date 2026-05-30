import os
import pypdf

pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
print("Found PDFs:", pdf_files)

for pdf in pdf_files:
    print(f"\n=== Inspecting {pdf} ===")
    try:
        reader = pypdf.PdfReader(pdf)
        print(f"Number of pages: {len(reader.pages)}")
        # Print first 500 chars of page 1 text
        text = reader.pages[0].extract_text()
        print("Page 1 preview:")
        print(text[:800])
    except Exception as e:
        print(f"Error reading {pdf}: {e}")
