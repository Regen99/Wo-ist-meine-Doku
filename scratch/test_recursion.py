import os
import sys

# Path Bootstrap
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.engine.pipeline import DiscoveryPipeline

def test_recursion():
    # Create a test directory structure
    base_dir = os.path.join(_project_root, "scratch", "test_recursion")
    sub_dir = os.path.join(base_dir, "depth1", "depth2")
    os.makedirs(sub_dir, exist_ok=True)
    
    test_file = os.path.join(sub_dir, "recurse_test.txt")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("This is a file deep in a subfolder for testing recursion.")
        
    pipeline = DiscoveryPipeline()
    # Index the base_dir
    indexed = pipeline.run_incremental_pipeline(base_dir)
    print(f"Indexed {indexed} files from {base_dir}")
    
    # Query for the content
    results = pipeline.query("recursion", limit=5)
    print(f"Results for 'recursion': {len(results)}")
    for r in results:
        print(f" - Found in: {r.get('source_path')}")

    # Query with path filter
    results_filtered = pipeline.query("recursion", path_prefix=base_dir)
    print(f"Filtered results for 'recursion': {len(results_filtered)}")

if __name__ == "__main__":
    test_recursion()
