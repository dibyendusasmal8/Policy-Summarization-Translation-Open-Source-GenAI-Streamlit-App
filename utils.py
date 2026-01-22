import pdfplumber
from docx import Document as DocxDocument
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_stream):
    text = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)

def extract_text_from_docx(file_stream):
    doc = DocxDocument(file_stream)
    full = []
    for para in doc.paragraphs:
        full.append(para.text)
    return "\n".join(full)

def ocr_image(file_stream):
    im = Image.open(file_stream)
    return pytesseract.image_to_string(im)

def chunk_text(text, max_chars=3000):
    import re
    sentences = re.split(r'(?<=[.؟!])\s+', text)
    chunks = []
    cur = ''
    for s in sentences:
        if len(cur) + len(s) < max_chars:
            cur += ' ' + s
        else:
            if cur.strip():
                chunks.append(cur.strip())
            cur = s
    if cur.strip():
        chunks.append(cur.strip())
    return chunks
