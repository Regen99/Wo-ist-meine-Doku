import re
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import os


class ChunkMetadata(BaseModel):
    """
    Standardized metadata for semantic chunks within the Discovery Engine.
    Ensures DACH legal compliance tracking and source provenance.
    """
    source_path: str
    chunk_index: int
    page_label: Optional[str] = None
    legal_context: bool = False
    language: str = "de"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    checksum: Optional[str] = None
    custom_tags: Dict[str, Any] = {}

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MetadataFactory:
    """
    Factory to generate ChunkMetadata objects with automatic legal context
    detection and real language identification. (Fix #6)
    """

    LEGAL_KEYWORDS = ["gesetz", "ordnung", "verordnung", "richtlinie", "§", "artikel"]

    @staticmethod
    def _detect_language(text: str) -> str:
        """
        Lightweight heuristic-based language detection.
        Checks Unicode ranges: Korean (Hangul), German (Umlaut), English (fallback).
        """
        if re.search(r'[\uac00-\ud7a3]', text):
            return "kr"
        elif re.search(r'[äöüßÄÖÜ]', text):
            return "de"
        return "en"

    @staticmethod
    def create(source_path: str, chunk_index: int, text: str, **kwargs) -> ChunkMetadata:
        # Detect legal context based on path or content keywords
        is_legal = (
            any(kw in source_path.lower() for kw in ["gesetze", "legal", "compliance"]) or
            any(kw in text.lower() for kw in MetadataFactory.LEGAL_KEYWORDS)
        )

        # Use real language detection unless explicitly overridden
        lang = kwargs.pop("language", MetadataFactory._detect_language(text))

        return ChunkMetadata(
            source_path=source_path,
            chunk_index=chunk_index,
            legal_context=is_legal,
            language=lang,
            **kwargs
        )
