import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.metadata import MetadataFactory


def test_language_detection():
    """Verifies the heuristic language detector handles all three target languages."""
    assert MetadataFactory._detect_language("이 문서는 한국어로 작성되었습니다.") == "kr"
    assert MetadataFactory._detect_language("Dieses Dokument enthält Umlaute: ä ö ü") == "de"
    assert MetadataFactory._detect_language("This document is in English.") == "en"
    print("[+] Language detection: OK")


def test_rag_context_format():
    """Verifies that metadata is correctly applied to chunk records."""
    meta = MetadataFactory.create(
        source_path="data/legal/BauGB_Excerpt.pdf",
        chunk_index=0,
        text="§ 34 BauGB regulates the inner area."
    )
    assert meta.legal_context is True, "Legal keywords should trigger legal_context=True"
    assert meta.language == "en"
    assert meta.chunk_index == 0
    print("[+] Metadata creation with legal detection: OK")


def test_korean_legal_detection():
    """Korean text that is in a legal folder path should be tagged as legal/kr."""
    meta = MetadataFactory.create(
        source_path="data/legal/tech_spec_kr.docx",
        chunk_index=1,
        text="이 사양서는 디스플레이 밝기 기준을 정의합니다."
    )
    assert meta.language == "kr"
    assert meta.legal_context is True  # "legal" in path
    print("[+] Korean legal document detection: OK")


if __name__ == "__main__":
    test_language_detection()
    test_rag_context_format()
    test_korean_legal_detection()
    print("\n[OK] All RAG logic tests passed.")
