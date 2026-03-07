import fitz
import io
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_bytes):
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            page_text = page.get_text().strip()
            if page_text:
                text += page_text + "\n"
            else:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes()))
                text += pytesseract.image_to_string(img) + "\n"
    except Exception as e:
        return f"Error extracting text: {e}"
    return text