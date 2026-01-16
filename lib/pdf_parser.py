"""PDF text extraction using pdfplumber."""

import pdfplumber
from io import BytesIO


def extract_text_from_pdf(pdf_file: BytesIO) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_file: A file-like object containing the PDF data.

    Returns:
        Extracted text as a string.
    """
    text_parts = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return "\n\n".join(text_parts)
