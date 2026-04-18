import pdfplumber
from src.engine.ocr import DiscoveryOCR
import logging


class PDFParser:
    """
    Lightweight PDF parser using pdfplumber with OCR fallback.
    Handles text-based PDFs with pdfplumber, and switches to
    RapidOCR for scanned documents.
    """

    def __init__(self, ocr_engine: DiscoveryOCR = None):
        self.logger = logging.getLogger(__name__)
        self.ocr_engine = ocr_engine

    def parse(self, file_path: str) -> str:
        """
        Parses a PDF file and returns full text content.
        Uses pdfplumber first; falls back to OCR if empty.
        """
        text_parts = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            clean_text = "\n\n".join(text_parts).strip()
            
            # If native text is empty and OCR is available, try OCR
            if not clean_text and self.ocr_engine:
                self.logger.info(f"[PDFParser] No native text in {file_path}. Running OCR fallback...")
                clean_text = self.ocr_engine.ocr_pdf(file_path)
            
            return clean_text
        except Exception as e:
            self.logger.error(f"[PDFParser] Failed to parse {file_path}: {e}")
            return ""


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        parser = PDFParser()
        result = parser.parse(sys.argv[1])
        print(result[:2000])
