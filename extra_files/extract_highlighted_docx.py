
import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def read_docx_with_highlights(file_path):
    if not zipfile.is_zipfile(file_path):
        return "Error: Not a valid zip/docx file."

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'word/document.xml' not in z.namelist():
                return "Error: word/document.xml not found using zip method."
            
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Namespaces
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            full_text = []
            
            # Iterate paragraphs
            for p in root.findall('.//w:p', namespaces):
                para_text = ""
                for r in p.findall('.//w:r', namespaces):
                    text_elem = r.find('.//w:t', namespaces)
                    if text_elem is not None and text_elem.text is not None:
                        text_val = text_elem.text
                        
                        # Check for highlight
                        rPr = r.find('w:rPr', namespaces)
                        is_highlighted = False
                        if rPr is not None:
                            highlight = rPr.find('w:highlight', namespaces)
                            if highlight is not None:
                                val = highlight.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                                if val == 'yellow':
                                    is_highlighted = True
                        
                        if is_highlighted:
                             para_text += f"__VAR__{text_val}__VAR__"
                        else:
                             para_text += text_val
                
                full_text.append(para_text)
            
            return '\n'.join(full_text)

    except Exception as e:
        return f"Error processing file: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_highlighted_docx.py <file_path>")
    else:
        print(read_docx_with_highlights(sys.argv[1]))
