# Antigravity Project Log

## [2026-04-18] [DEPLOY] | Final Release Preparation (v1.2.0)
- Dependencies: Standardized `requirements.txt` and `requirements-cpu.txt` with `tantivy` for FTS.
- Search: Integrated **Hybrid Toggle** (Semantic vs. Exact Match) into the UI.
- Docs: Drafted LinkedIn marketing copy and created a Deployment Checklist.
- Readiness: Completed deep stability audit of batch scripts and environment activations.

## [2026-04-18] [UPDATE] | UI/UX Overhaul: Clay System & Folder Integration
- UI: Implemented **Reveal in Explorer**, **Search Term Highlighting**, and **Native Folder Picker**.
- UX: Added **Night Clay (Dark Mode)** with a dynamic top-right toggle.
- Stability: Implemented **Pending Update Pattern** to resolve Streamlit widget state-sync conflicts during folder selection.
- Engine: Standardized on **MiniLM-L12-v2** for optimal FastEmbed/ONNX compatibility.
- Documentation: Fully synchronized README (EN/DE) and internal Wiki to current state.

## [2026-04-18] [RELEASE] | Turbo-Lite Engine deployed.
- Optimization: Replaced PyTorch/Transformers stack with **FastEmbed (ONNX)**.
- Stability: Replaced IBM Docling with **pdfplumber** to eliminate system freezes.
- Speed: Installation reduced from 15 minutes to 2 minutes; RAM usage cut by 60%.
- Reliability: Custom recursive splitting eliminates ML overhead during ingestion.

## [2026-04-18] [FIX] | Fixed install error by changing --index-url to --extra-index-url.
## [2026-04-18] [REFACTOR] | Applied Ultra-Lite refactor: replaced docling/langchain with pdfplumber/simple-splitter to resolve freezing.

## [2026-04-17] [REBRAND] | Wo ist meine Doku Pivot
- Rebranding: Renamed project to "Wo ist meine Doku".
- Sanitization: Removed all emojis and legacy "Senior" branding from UI and scripts.
- Optimization: Switched to CPU-Only mode with Multilingual-E5-Small (384-dim).
- UI Cleanup: Professional, text-only Streamlit dashboard for stable deployment.

## [2026-04-17] [PIVOT] | Shifted to Search-Only Dashboard
- Decision: Removed Ollama/Gemma 4 dependencies to minimize disk footprint and eliminate hallucination risks.
- Achievement: Implemented Discovery Dashboard as a high-fidelity semantic tool.

## [2026-04-17] [INGEST] | Vector DB & Hybrid Search (Epic 3 Complete)
- Implementation: Integrated LanceDB with hybrid FTS integration.
- Logic: Implemented DiscoveryDB with FTS index support for hybrid keyword + semantic retrieval.
- Incremental Ingestion: Implemented duplicate check logic in the discovery pipeline.

## [2026-04-17] [INGEST] | Semantic Engine (Epic 2 Complete)
- Implementation: Deployed high-efficiency multilingual embeddings.
- Logic: Implemented Discovery Chunker using semantic breakpoint analysis.

## [2026-04-17] [INGEST] | Multilingual Parsing (Epic 1 Complete)
- Implementation: Developed ParserFactory supporting PDF, DOCX, XLSX, and PPTX.
- Output: Standardized on Markdown strings for optimal chunking down the stream.

## [2026-04-05] [INIT] | Antigravity Wiki initialized.
- Setup: Initialized index.md and log.md following core architecture rules.
