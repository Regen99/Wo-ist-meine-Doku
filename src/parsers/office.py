import sharepoint2text
from typing import Generator

class OfficeParser:
    """
    Layout-aware parser for Microsoft Office documents (.docx, .pptx, .xlsx, .doc, .ppt, .xls).
    Uses the pure-Python sharepoint-to-text library to ensure compatibility without Java/LibreOffice.
    """

    def parse(self, file_path: str) -> str:
        """
        Parses an Office file and returns full text content.
        
        Args:
            file_path: Absolute path to the document.
            
        Returns:
            Extracted text content formatted as a string.
        """
        try:
            # sharepoint2text.read_file returns a Reader object
            reader = next(sharepoint2text.read_file(file_path))
            
            # Combine units into a single string for semantic chunking
            chunks = []
            for unit in reader.iterate_units():
                text = unit.get_text().strip()
                if text:
                    chunks.append(text)
            
            return "\n\n".join(chunks)
        except Exception as e:
            print(f"[OfficeParser] Error parsing {file_path}: {str(e)}")
            return ""

if __name__ == "__main__":
    # Quick sanity check interface
    import sys
    if len(sys.argv) > 1:
        parser = OfficeParser()
        for chunk in parser.parse(sys.argv[1]):
            print(f"--- Chunk ---\n{chunk}\n")
