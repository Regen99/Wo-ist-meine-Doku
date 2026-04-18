import os, sys
sys.path.insert(0, os.path.abspath('.'))

from src.engine.database import DiscoveryDB

db = DiscoveryDB()

test_paths = [
    'data/raw/test_readme.md',
    'data\\raw\\test_readme.md',
    os.path.abspath('data/raw/test_readme.md'),
]

print("--- Path Normalization Fix Test ---")
for p in test_paths:
    result = db.file_exists(p)
    short = (p if len(p) < 60 else p[:57] + "...")
    print(f"exists({short!r}) = {result}")

print("\n--- Full DB type distribution ---")
import lancedb
ldb = lancedb.connect("data/discovery.lancedb")
table = ldb.open_table("chunks")
import pandas as pd
df = table.to_pandas()
from collections import Counter
exts = [os.path.splitext(s)[1].lower() for s in df['source_path'].unique()]
for ext, count in Counter(exts).most_common():
    print(f"  {ext}: {count} files")
