from pathlib import Path
from typing import Optional
from .office import OfficeParser
from .pdf import PDFParser
from .text import TextParser


class ParserFactory:
    """
    Unified entry point for document parsing.
    Detects file formats and routes to the specialized parser (Office, PDF, or Text).
    """

    OFFICE_EXTENSIONS = {'.docx', '.pptx', '.xlsx', '.doc', '.ppt', '.xls'}
    PDF_EXTENSIONS = {'.pdf'}
    TEXT_EXTENSIONS = {'.txt', '.md', '.csv', '.log'}

    def __init__(self, ocr_engine=None):
        # Lazy initialization for consistent pattern
        self._office_parser = None
        self._pdf_parser = None
        self._text_parser = None
        self.ocr_engine = ocr_engine

    @property
    def office_parser(self):
        if self._office_parser is None:
            self._office_parser = OfficeParser()
        return self._office_parser

    @property
    def pdf_parser(self):
        if self._pdf_parser is None:
            self._pdf_parser = PDFParser(ocr_engine=self.ocr_engine)
        return self._pdf_parser

    @property
    def text_parser(self):
        if self._text_parser is None:
            self._text_parser = TextParser()
        return self._text_parser

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
        elif suffix in self.TEXT_EXTENSIONS:
            return self.text_parser
        else:
            raise ValueError(f"Unsupported file type: {suffix} for {file_path}")
