# Antigravity Knowledge Map

## Entities
- [MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) - Optimized multilingual embedding engine for FastEmbed (384-dim).
- [FastEmbed](https://github.com/qdrant/fastembed) - Light-weight, high-performance Python library for CPU-optimized embeddings.
- [LanceDB](https://lancedb.com/) - High-performance local vector database with hybrid FTS integration.
- [Discovery Dashboard](src/ui/app.py) - Streamlit-based interface for document exploration.
- [Discovery Engine](src/engine/pipeline.py) - Orchestrator for parsing, chunking, and indexing logic.


## Concepts
- [Turbo-Lite Architecture](src/engine/pipeline.py) - Radical optimization: Removed PyTorch/Transformers for ONNX-based inference.
- [MiniLM-L12-v2 Embedding](src/engine/embeddings.py) - Multilingual vector model optimized for speed and compatibility with FastEmbed.
- [Reveal in Explorer](src/ui/app.py) - Windows system integration for direct file discovery.
- [Search Term Highlighting](src/ui/app.py) - Visual markers using `<mark>` for query term identification.
- [Night Clay / Dark Mode](src/ui/app.py) - High-fidelity dual-theme system with dynamic top-right toggle.
- [Exact Match Search](src/ui/app.py) - Hybrid toggle for switching between Semantic (Vector) and Literal (FTS) search.
- [Native Folder Picker](src/ui/app.py) - Windows directory selection via `tkinter` with state-sync fix.
- [Discovery DB](src/engine/database.py) - LanceDB storage for hybrid search.
- [Recursive Chunking](src/engine/chunker.py) - Balanced document splitting using RecursiveCharacterTextSplitter for zero ML overhead during ingestion.
- [Zero-AI Discovery](wiki/status_report.md) - Optimized retrieval strategy focusing on 100% data fidelity.

## Sources
- [research.md](wiki/research.md) - Strategic Architectural Blueprint for Integrated Multimodal Semantic Search.
- [Jira.md](wiki/Jira.md) - Project roadmap and technical backlog.
- [Status Report](wiki/status_report.md) - Current state and capability matrix.

## Projects
- [Wo ist meine Doku](wiki/status_report.md) - **Alpha State | Epic 4 Complete**. Semantic discovery system for German and English document corpora.
- [Pre-Development Report](wiki/pre_dev_report.md) - Phase 0 planning report.
