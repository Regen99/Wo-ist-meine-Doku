from src.engine.pipeline import DiscoveryPipeline
import os
import shutil

def test_epic3_pipeline():
    # Setup: Clear old DB if it exists for a fresh test
    db_path = "data/discovery.lancedb"
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    
    pipeline = DiscoveryPipeline(use_gpu=False)
    
    # Files to ingest
    test_pdf = "tests/data/test_pdf.pdf"
    test_docx = "tests/data/test_office.docx"
    
    print("\n--- Phase 1: Initial Ingestion ---")
    pipeline.ingest_file(test_pdf)
    pipeline.ingest_file(test_docx)
    
    print("\n--- Phase 2: Incremental Check (Skip) ---")
    # This should return False (skip)
    re_indexed = pipeline.ingest_file(test_pdf)
    assert re_indexed is False, "Error: Should have skipped already indexed file"
    
    print("\n--- Phase 3: Hybrid Search (German Legal) ---")
    query = "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz"
    results = pipeline.query(query, limit=1)
    
    for res in results:
        print(f"[Result] Score: {res.get('_distance', 'N/A')}")
        print(f"Index: {res['chunk_index']} | Legal: {res['legal_context']}")
        print(f"Content: {res['text'][:100]}...")
        assert res['legal_context'] is True, "Error: Should have detected legal context"

    print("\n--- Phase 4: Korean Search ---")
    results_kr = pipeline.query("다국어 검색 시스템", limit=1)
    print(f"Korean Query executed successfully. Results found: {len(results_kr)}")

    print("\n[SUCCESS] Pipeline integration verified.")

if __name__ == "__main__":
    test_epic3_pipeline()
