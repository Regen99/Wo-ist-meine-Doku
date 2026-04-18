import lancedb
import pandas as pd
import os

# Connect to the local LanceDB
db_path = "data/discovery.lancedb"
if not os.path.exists(db_path):
    print(f"Error: Database path {db_path} does not exist.")
    exit(1)

db = lancedb.connect(db_path)
table_name = "chunks"

if table_name not in db.table_names():
    print(f"Error: Table {table_name} not found in database.")
    exit(1)

table = db.open_table(table_name)
df = table.to_pandas()

print(f"Total chunks in database: {len(df)}")
if len(df) > 0:
    sources = df['source_path'].unique()
    print(f"Unique source files indexed: {len(sources)}")
    print("\nFile types distribution:")
    extensions = [os.path.splitext(s)[1].lower() for s in sources]
    from collections import Counter
    print(Counter(extensions))
    
    print("\nLast 5 indexed files:")
    for s in sources[-5:]:
        print(f" - {s}")
else:
    print("Database is empty.")
