import pypdfium2 as pdfium
import os

pdf = pdfium.PdfDocument("builder_tm (1).pdf")
artifact_dir = "C:/Users/fcama/.gemini/antigravity/brain/09be3ae1-8f8d-432b-a4c7-5513355cac8d"

for i in range(len(pdf)):
    page = pdf[i]
    bitmap = page.render(scale=1.5)
    pil_img = bitmap.to_pil()
    dest_path = os.path.join(artifact_dir, f"builder_tm_p{i+1}.png")
    pil_img.save(dest_path)
    print(f"Page {i+1} saved to: {dest_path}")
