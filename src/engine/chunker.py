from src.engine.embeddings import DiscoveryEmbedder
from src.utils.metadata import MetadataFactory, ChunkMetadata
import logging


class DiscoveryChunker:
    """
    Lightweight text chunker for the Discovery Engine.
    Uses recursive character splitting — zero ML calls during chunking.
    This replaces the heavy SemanticChunker (LangChain) which called the
    embedding model hundreds of times per document.
    """

    def __init__(self, embedder: DiscoveryEmbedder = None,
                 chunk_size: int = 512, chunk_overlap: int = 64):
        # Embedder is kept for API compatibility with pipeline,
        # but is NOT called during chunking anymore.
        self.embedder = embedder or DiscoveryEmbedder(use_gpu=False)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Separators ordered by priority: paragraphs > lines > sentences > words
        self.separators = ["\n\n", "\n", ". ", " ", ""]

    def _split_text(self, text: str) -> list[str]:
        """Recursively split text using a hierarchy of separators."""
        chunks: list[str] = []
        self._recursive_split(text, self.separators, chunks)
        return chunks

    def _recursive_split(self, text: str, separators: list[str], chunks: list[str]):
        """Core recursive logic: try coarse splits first, refine if needed."""
        if len(text) <= self.chunk_size:
            if text.strip():
                chunks.append(text.strip())
            return

        separator = separators[0] if separators else ""
        remaining = separators[1:] if len(separators) > 1 else [""]

        # Base case: no separator left, hard-split by character count
        if separator == "":
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunk = text[i:i + self.chunk_size]
                if chunk.strip():
                    chunks.append(chunk.strip())
            return

        parts = text.split(separator)
        current = ""

        for part in parts:
            candidate = (current + separator + part).strip() if current else part.strip()

            if len(candidate) <= self.chunk_size:
                current = candidate
            else:
                # Flush what we have
                if current.strip():
                    chunks.append(current.strip())
                # If this part alone is too big, recurse with finer separator
                if len(part) > self.chunk_size:
                    self._recursive_split(part, remaining, chunks)
                    current = ""
                else:
                    current = part.strip()

        if current.strip():
            chunks.append(current.strip())

    def chunk_document(self, source_path: str, full_text: str) -> list[tuple[str, ChunkMetadata]]:
        """
        Splits text into chunks and attaches metadata.
        No embedding model is called during this step.
        """
        if not isinstance(full_text, str):
            full_text = "\n\n".join(list(full_text))

        logging.info(f"Chunking document: {source_path}")

        chunks = self._split_text(full_text)

        processed_chunks = []
        for i, chunk_text in enumerate(chunks):
            metadata = MetadataFactory.create(
                source_path=source_path,
                chunk_index=i,
                text=chunk_text
            )
            processed_chunks.append((chunk_text, metadata))

        logging.info(f"Generated {len(processed_chunks)} chunks.")
        return processed_chunks
