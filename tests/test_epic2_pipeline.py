from src.engine.chunker import DiscoveryChunker
from src.utils.metadata import ChunkMetadata
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_pipeline():
    print("=== Wo ist meine Doku: Chunker Integration Test ===")
    
    # 1. Initialize Chunker (No ML model loaded during chunking)
    print("Initializing Recursive Chunker...")
    chunker = DiscoveryChunker()
    
    # 2. Test German (Legal Context)
    print("\n--- Testing German (Legal Context) ---")
    de_text = (
        "Das Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz ist ein Gesetz zur Regelung der Überwachung. "
        "Es wurde in Mecklenburg-Vorpommern am 19. Januar 2000 verkündet. "
        "Dieser Text sollte als legal_context=True markiert werden."
    )
    de_chunks = chunker.chunk_document("tests/data/legal_test.txt", de_text)
    
    for text, meta in de_chunks:
        print(f"Chunk [{meta.chunk_index}] (Legal: {meta.legal_context}): {text[:100]}...")

    # 3. Test Korean
    print("\n--- Testing Korean ---")
    ko_text = (
        "이 시스템은 다국어 시맨틱 검색 시스템입니다. "
        "독일어와 한국어를 동시에 지원하며, E5-Small 모델을 사용하여 고성능 검색을 지원합니다. "
        "이 텍스트는 한국어로 정상적으로 청킹되어야 합니다."
    )
    ko_chunks = chunker.chunk_document("tests/data/ko_test.txt", ko_text)
    
    for text, meta in ko_chunks:
        print(f"Chunk [{meta.chunk_index}] (Lang: {meta.language}): {text[:100]}...")

    print("\n=== Test Completed Successfully ===")

if __name__ == "__main__":
    test_pipeline()
