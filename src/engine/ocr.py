import logging

logger = logging.getLogger(__name__)


class DiscoveryOCR:
    """
    Lightweight ONNX-based OCR for discovery.
    Uses RapidOCR for German and English support without heavy framework deps.
    All heavy imports (fitz, rapidocr) are lazy — the app starts even if
    these packages are not yet installed.
    """

    def __init__(self):
        self.engine = None
        self._fitz = None
        try:
            from rapidocr_onnxruntime import RapidOCR
            self.engine = RapidOCR()
        except ImportError:
            logger.warning("rapidocr_onnxruntime not installed — OCR disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize RapidOCR: {e}")

        try:
            import fitz
            self._fitz = fitz
        except ImportError:
            logger.warning("PyMuPDF (fitz) not installed — OCR page rendering disabled.")

    def ocr_pdf(self, pdf_path: str, max_pages: int = 5) -> str:
        """
        Extracts text from a scanned PDF via OCR.
        Converts each page to an image then runs RapidOCR on the bytes.
        """
        if not self.engine or not self._fitz:
            return ""

        fitz = self._fitz
        full_text = []
        try:
            with fitz.open(pdf_path) as doc:
                pages_to_ocr = min(len(doc), max_pages)
                for page_num in range(pages_to_ocr):
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_bytes = pix.tobytes("png")

                    result, _ = self.engine(img_bytes)
                    if result:
                        page_text = "\n".join([line[1] for line in result])
                        full_text.append(page_text)

            return "\n\n".join(full_text)
        except Exception as e:
            logger.error(f"OCR Error for {pdf_path}: {e}")
            return ""

    def ocr_image(self, img_path: str) -> str:
        """Runs OCR on a single image file (PNG/JPG/etc.)."""
        if not self.engine:
            return ""
        try:
            result, _ = self.engine(img_path)
            if result:
                return "\n".join([line[1] for line in result])
            return ""
        except Exception as e:
            logger.error(f"OCR Error for image {img_path}: {e}")
            return ""
