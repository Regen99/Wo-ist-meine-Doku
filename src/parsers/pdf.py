import pdfplumber
import logging


class PDFParser:
    """
    Lightweight PDF parser using pdfplumber.
    Handles text-based PDFs with fast, low-memory extraction.
    No AI models loaded — pure Python text extraction.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, file_path: str) -> str:
        """
        Parses a PDF file and returns full text content.

        Args:
            file_path: Absolute path to the PDF.

        Returns:
            Extracted text content as a single string.
        """
        try:
            text_parts = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            return "\n\n".join(text_parts)
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
