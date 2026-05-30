import pdfplumber
import pypdfium2 as pdfium
import os

print("--- Extracting text using pdfplumber ---")
with pdfplumber.open("builder_tm (1).pdf") as pdf:
    print("Total pages:", len(pdf.pages))
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"Page {i+1} character count:", len(text) if text else 0)
        if text:
            print(f"Page {i+1} first 200 chars:")
            print(repr(text[:200]))

print("\n--- Rendering Page 1 to Image ---")
try:
    pdf = pdfium.PdfDocument("builder_tm (1).pdf")
    page = pdf[0]
    bitmap = page.render(scale=2)
    pil_img = bitmap.to_pil()
    # Save the image to the artifacts folder
    artifact_dir = "C:/Users/fcama/.gemini/antigravity/brain/09be3ae1-8f8d-432b-a4c7-5513355cac8d"
    dest_path = os.path.join(artifact_dir, "builder_tm_p1.png")
    pil_img.save(dest_path)
    print("Page 1 saved to:", dest_path)
except Exception as e:
    print("Error rendering page:", e)
