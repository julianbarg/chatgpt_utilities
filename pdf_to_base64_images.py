import fitz  # PyMuPDF
import base64

def pdf_to_base64_images(pdf_path):
    """
    Convert each page of a PDF to a base64-encoded JPEG string to be used with
    OpenAI API (ChatGPT).

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        List[str]: List of base64-encoded JPEG strings, one per page.
    """
    base64_images = []
    doc = fitz.open(pdf_path)
    for page in doc:
        pix = page.get_pixmap()
        b64 = base64.b64encode(pix.tobytes("jpeg")).decode('utf-8')
        base64_images.append(b64)
    return base64_images



