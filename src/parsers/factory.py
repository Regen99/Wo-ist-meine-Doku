from pathlib import Path
from .office import OfficeParser
from .pdf import PDFParser


class ParserFactory:
    """
    Unified entry point for document parsing.
    Detects file formats and routes to the specialized parser (Office or PDF).
    Fix #10: Removed dead generator-based parse() method.
    """

    OFFICE_EXTENSIONS = {'.docx', '.pptx', '.xlsx', '.doc', '.ppt', '.xls'}
    PDF_EXTENSIONS = {'.pdf'}

    def __init__(self):
        # Lazy initialization for consistent pattern
        self._office_parser = None
        self._pdf_parser = None

    @property
    def office_parser(self):
        if self._office_parser is None:
            self._office_parser = OfficeParser()
        return self._office_parser

    @property
    def pdf_parser(self):
        if self._pdf_parser is None:
            self._pdf_parser = PDFParser()
        return self._pdf_parser

    def get_parser(self, file_path: str):
        """
        Determines the appropriate parser based on the file extension.
        Raises ValueError for unsupported types (caller should catch).
        """
        suffix = Path(file_path).suffix.lower()
        if suffix in self.OFFICE_EXTENSIONS:
            return self.office_parser
        elif suffix in self.PDF_EXTENSIONS:
            return self.pdf_parser
        else:
            raise ValueError(f"Unsupported file type: {suffix} for {file_path}")
