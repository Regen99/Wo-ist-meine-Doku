# Antigravity Knowledge Map

## Entities
- [MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) - Optimized multilingual embedding engine for FastEmbed (384-dim).
- [FastEmbed](https://github.com/qdrant/fastembed) - Light-weight, high-performance Python library for CPU-optimized embeddings.
- [LanceDB](https://lancedb.com/) - High-performance local vector database with hybrid FTS integration.
- [Discovery Dashboard](src/ui/app.py) - Streamlit-based interface for document exploration.
- [Discovery Engine](src/engine/pipeline.py) - Orchestrator for parsing, chunking, and indexing logic.


- [Discovery DB](src/engine/database.py) - LanceDB storage for hybrid search.
- [RapidOCR](src/engine/ocr.py) - ONNX-based lightweight OCR engine for scanned PDF discovery.
- [Discovery Text Parser](src/parsers/text.py) - Lightweight string-based parser for .md, .txt, and .csv.
- [ConfigManager](src/utils/config.py) - Persistent configuration system for favorites and last-used states.

## Concepts
- [Turbo-Lite Architecture](src/engine/pipeline.py) - Radical optimization: Removed PyTorch/Transformers for ONNX-based inference.
- [Warm Enterprise UX](src/ui/app.py) - Professional aesthetic: Beige backdrop (#faf8f4) with High-Contrast White Box components.
- [Multimodal Raw Ingestion](src/engine/pipeline.py) - Unified pipeline for Office, PDF, Markdown, and Plain Text discovery.
- [ONNX-OCR Fallback](src/parsers/pdf.py) - Automatic optical character recognition for scanned/blank documents using RapidOCR.
- [PDF Visual Previews](src/engine/pipeline.py) - High-fidelity thumbnail generation for first-page visual confirmation.
- [Project Favorites](src/ui/app.py) - Multi-path management system for switching between document sources.
- [Night Clay / Dark Mode](src/ui/app.py) - High-fidelity dual-theme system with dynamic top-right toggle.
- [Exact Match Search](src/ui/app.py) - Hybrid toggle for switching between Semantic (Vector) and Literal (FTS) search.
- [Native Folder Picker](src/ui/app.py) - Windows directory selection via `tkinter` with state-sync fix.
- [Recursive Chunking](src/engine/chunker.py) - Balanced document splitting using RecursiveCharacterTextSplitter for zero ML overhead during ingestion.
- [Zero-AI Discovery](wiki/status_report.md) - Optimized retrieval strategy focusing on 100% data fidelity.
- [Runtime Hardening](src/ui/app.py) - Graceful degradation and lazy loading | Stability | 2026-04-18
- [Top NAV Toolbar](src/ui/app.py) - Centralized project controls for better UX | UI | 2026-04-18

## Sources
- [research.md](wiki/research.md) - Strategic Architectural Blueprint for Integrated Multimodal Semantic Search.
- [Jira.md](wiki/Jira.md) - Project roadmap and technical backlog.
- [Status Report](wiki/status_report.md) - Current state and capability matrix.

## Projects
- [Wo ist meine Doku](wiki/status_report.md) - **Alpha State | Epic 4 Complete**. Semantic discovery system for German and English document corpora.
- [Pre-Development Report](wiki/pre_dev_report.md) - Phase 0 planning report.
