from pathlib import Path

class TextParser:
    """
    Standard parser for plain text files (.txt, .md, .csv, .log).
    Simply reads the content as a string with UTF-8 encoding (fallback to ignore errors).
    """

    def parse(self, file_path: str) -> str:
        """
        Reads the file and returns its content as a string.
        """
        try:
            # We use errors='ignore' to handle cases where there might be binary artifacts 
            # or mixed encoding in raw logs/scraps.
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file at {file_path}: {e}")
