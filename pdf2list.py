#!/usr/bin/env python3

from popplerqt5 import Poppler
import base64
import tempfile
import sys

def pdf2list(pdf_path):
    """
    Convert a PDF file into a list of base64-encoded PNG images using
    python-poppler-qt5 with default rendering settings.

    Parameters:
      pdf_path (str): The file path to the PDF.
      
    Returns:
      list[str]: A list of base64-encoded PNG strings, one per page.
    """
    document = Poppler.Document.load(pdf_path)
    if document is None:
        raise Exception("Could not load PDF file: " + pdf_path)

    num_pages = document.numPages()
    base64_images = []

    for i in range(num_pages):
        page = document.page(i)
        image = page.renderToImage()
        
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            image.save(tmp.name, "PNG")
            tmp.seek(0)
            img_bytes = tmp.read()
            b64_img = base64.b64encode(img_bytes).decode("utf-8")
            base64_images.append(b64_img)

    return base64_images

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python poppler_to_base64.py <pdf_file>", file=sys.stderr)
        sys.exit(1)

    pdf_file = sys.argv[1]
    
    try:
        images = pdf2list(pdf_file)
        # Print the base64 images, one per line.
        print("\n".join(images))
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)
