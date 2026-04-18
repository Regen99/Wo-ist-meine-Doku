from src.parsers.factory import ParserFactory
from src.engine.chunker import DiscoveryChunker
from src.engine.embeddings import DiscoveryEmbedder
from src.engine.database import DiscoveryDB
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DiscoveryPipeline:
    def __init__(self, use_gpu: bool = False):
        self.factory = ParserFactory()
        # Create ONE embedder, inject into chunker to share memory
        self.embedder = DiscoveryEmbedder(use_gpu=use_gpu)
        self.chunker = DiscoveryChunker(embedder=self.embedder)
        self.db = DiscoveryDB()

    def ingest_file(self, file_path: str) -> bool:
        """
        Process a single file and store it in the vector database.
        Returns True if newly indexed, False if skipped.
        """
        # 1. Incremental check: skip already-indexed files
        if self.db.file_exists(file_path):
            logger.info(f"Skipping {os.path.basename(file_path)}: Already indexed.")
            return False

        logger.info(f"Ingesting {os.path.basename(file_path)}...")

        # 2. Parse (Factory routes by extension)
        try:
            parser = self.factory.get_parser(file_path)
        except ValueError as e:
            logger.warning(f"Unsupported file type, skipping: {e}")
            return False

        markdown_content = parser.parse(file_path)

        if not markdown_content or not markdown_content.strip():
            logger.warning(f"Skipping {os.path.basename(file_path)}: Empty content after parsing.")
            return False

        # 3. Semantic chunking & metadata enrichment
        chunks_with_meta = self.chunker.chunk_document(file_path, markdown_content)

        # 4. Generate embeddings & prepare records
        data_to_store = []
        for text, meta in chunks_with_meta:
            # E5-Small requirement: prefix with 'passage: ' for indexing
            vector = self.embedder.embed([f"passage: {text}"])[0]
            record = {
                "vector": vector,
                "text": text,
                "source_path": file_path.replace("\\", "/"),
                "chunk_index": meta.chunk_index,
                "language": meta.language,
                "legal_context": meta.legal_context,
                "timestamp": meta.timestamp,
            }
            data_to_store.append(record)

        # 5. Persist to LanceDB
        if data_to_store:
            self.db.add_chunks(data_to_store)
            logger.info(f"Indexed {len(data_to_store)} chunks from {os.path.basename(file_path)}.")
            return True

        return False

    def run_incremental_pipeline(self, directory_path: str) -> int:
        """
        Scans a directory for supported files and ingests new ones.
        Returns the number of newly indexed files.
        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            return 0

        total_indexed = 0
        supported = {".pdf", ".docx", ".xlsx", ".pptx"}

        for root, _, files in os.walk(directory_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported:
                    full_path = os.path.join(root, file)
                    if self.ingest_file(full_path):
                        total_indexed += 1

        self.db.create_fts_index()
        return total_indexed

    def query(self, text: str, limit: int = 5,
               language: str = None, legal_only: bool = False,
               exact_match: bool = False) -> List[Dict[str, Any]]:
        """
        Multilingual search (Semantic or FTS).
        """
        if exact_match:
            query_vector = None
        else:
            # E5-Small requirement: prefix with 'query: ' for search
            query_vector = self.embedder.embed([f"query: {text}"])[0]
            
        return self.db.search(
            query_vector=query_vector,
            query_text=text,
            limit=limit,
            language=language,
            legal_only=legal_only,
            exact_match=exact_match
        )
