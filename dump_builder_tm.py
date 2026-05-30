import pypdf

reader = pypdf.PdfReader('builder_tm (1).pdf')
print("Pages in builder_tm (1).pdf:", len(reader.pages))
for i, page in enumerate(reader.pages):
    print(f"\n--- Page {i+1} ---")
    text = page.extract_text()
    if text:
        print(text[:1000])
    else:
        print("[No text extracted]")
