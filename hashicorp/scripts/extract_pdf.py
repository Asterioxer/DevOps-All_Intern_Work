import sys
from pypdf import PdfReader

try:
    pdf_path = sys.argv[1]
    out_path = sys.argv[2]
    
    reader = PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"\n--- Page {i + 1} ---\n"
        text += page.extract_text() + "\n"
        
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Successfully extracted {len(reader.pages)} pages to {out_path}")
except Exception as e:
    print(f"Error: {e}")
