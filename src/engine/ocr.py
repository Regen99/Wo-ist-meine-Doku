import logging
import fitz  # PyMuPDF for PDF-to-image rendering

logger = logging.getLogger(__name__)


class DiscoveryOCR:
    """
    Lightweight ONNX-based OCR for discovery.
    Uses RapidOCR for German and English support without heavy framework deps.
    """

    def __init__(self):
        # Lazy import to avoid crash when rapidocr is not yet installed
        try:
            from rapidocr_onnxruntime import RapidOCR
            self.engine = RapidOCR()
        except Exception as e:
            logger.error(f"Failed to initialize RapidOCR: {e}")
            self.engine = None

    def ocr_pdf(self, pdf_path: str, max_pages: int = 5) -> str:
        """
        Extracts text from a scanned PDF via OCR.
        Converts each page to an image then runs RapidOCR on the bytes.
        """
        if not self.engine:
            return ""

        full_text = []
        try:
            # Context manager ensures doc is always closed, even on error
            with fitz.open(pdf_path) as doc:
                pages_to_ocr = min(len(doc), max_pages)
                for page_num in range(pages_to_ocr):
                    page = doc.load_page(page_num)
                    # 2x scale improves OCR accuracy on small text
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_bytes = pix.tobytes("png")

                    result, _ = self.engine(img_bytes)
                    if result:
                        # result format: [[box, text, score], ...]
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
