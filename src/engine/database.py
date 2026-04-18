import lancedb
import pyarrow as pa
from lancedb.pydantic import LanceModel, Vector
from typing import List, Optional, Dict, Any
import os
from datetime import datetime

# Vector dimension for Multilingual-E5-Small
VECTOR_DIM = 384


class ChunkModel(LanceModel):
    """LanceDB Schema for Discovery Engine chunks"""
    vector: Vector(VECTOR_DIM)
    text: str
    source_path: str
    chunk_index: int
    language: str
    legal_context: bool
    timestamp: str


class DiscoveryDB:
    def __init__(self, db_dir: str = "data/discovery.lancedb"):
        self.db_dir = db_dir
        os.makedirs(os.path.dirname(db_dir), exist_ok=True)
        self.db = lancedb.connect(db_dir)
        self.table_name = "chunks"
        self._table = None

    def _get_table(self):
        if self._table is None:
            if self.table_name in self.db.table_names():
                self._table = self.db.open_table(self.table_name)
            else:
                self._table = self.db.create_table(self.table_name, schema=ChunkModel)
                self._table.create_fts_index("text", replace=True)
        return self._table

    def file_exists(self, source_path: str) -> bool:
        """Check if a file's chunks already exist in the database.
        Handles both old relative-path records and new absolute-path records.
        """
        if self.table_name not in self.db.table_names():
            return False

        table = self._get_table()

        # Normalize to absolute forward-slash (for new records)
        abs_path = os.path.abspath(source_path).replace("\\", "/")
        # Also check the raw forward-slash version (for legacy records)
        rel_path = source_path.replace("\\", "/")

        for path in set([abs_path, rel_path]):
            safe = path.replace("'", "''")
            result = table.search().where(
                f"source_path = '{safe}'", prefilter=True
            ).to_list()
            if result:
                return True
        return False

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """Add multiple chunks to the database."""
        table = self._get_table()
        table.add(chunks)

    def create_fts_index(self):
        """Rebuild the Full-Text Search index. Call after batch ingestion. (Fix #3)"""
        table = self._get_table()
        table.create_fts_index("text", replace=True)

    def search(self,
               query_vector: Optional[List[float]],
               query_text: str,
               limit: int = 5,
               language: Optional[str] = None,
               legal_only: bool = False,
               exact_match: bool = False) -> List[Dict[str, Any]]:
        """
        Hybrid search (Semantic Vector + Full-Text Search).
        Supports language and legal context filtering.
        """
        table = self._get_table()

        filters = []
        if language:
            filters.append(f"language = '{language}'")
        if legal_only:
            filters.append("legal_context = true")

        filter_str = " AND ".join(filters) if filters else None

        if exact_match:
            query = table.search(query_text, query_type="fts")
        else:
            query = table.search(query_vector)

        if filter_str:
            query = query.where(filter_str, prefilter=True)

        return query.limit(limit).to_list()
