try:
    from german_compound_splitter import comp_split
except ImportError:
    comp_split = None

try:
    from split_words import Splitter as CharSplitter
except ImportError:
    CharSplitter = None

from typing import List

class GermanNLP:
    """
    NLP utilities focused on the German language.
    Handles compound word splitting, which is critical for German semantic search.
    """

    def __init__(self):
        # Statistical splitter (CharSplit) - No dictionary needed
        self.char_splitter = CharSplitter() if CharSplitter else None
        # Dictionary-based splitter
        self.dict_splitter = comp_split if comp_split else None

    def split_compound(self, word: str) -> List[str]:
        """
        Splits a German compound word into its atomic parts.
        Example: "Donaudampfschifffahrt" -> ["Donau", "dampf", "schiff", "fahrt"]
        
        Args:
            word: The German word to split.
            
        Returns:
            A list of component words.
        """
        # Strategy 1: Statistical splitting (CharSplit)
        if self.char_splitter:
            try:
                # split_words returns a list of components
                result = self.char_splitter.split(word)
                if result and len(result) > 1:
                    return [r for r in result if r]
            except Exception:
                pass

        # Strategy 2: Dictionary-based (requires manual dictionary setup)
        # Note: This is left as a placeholder until a large dictionary is provided.
        
        return [word]

if __name__ == "__main__":
    # Test cases for German compound words
    nlp = GermanNLP()
    test_words = [
        "Donaudampfschifffahrtsgesellschaft",
        "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz",
        "Hausmeister"
    ]
    for w in test_words:
        print(f"{w} -> {nlp.split_compound(w)}")
