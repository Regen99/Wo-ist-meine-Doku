# Project Roadmap: Wo ist meine Doku

This document outlines the strategic direction and technical implementation plan for a high-performance local semantic search system.

## 🏁 Completed Milestones (Turbo-Lite Refactor)

*   **[DONE] FastEmbed Integration**: Replaced Torch/Transformers with ONNX for 10x faster startup and 60% less RAM.
*   **[DONE] Lightweight Parsing**: Replaced Docling with `pdfplumber` to eliminate system freezes on complex PDFs.
*   **[DONE] Recursive Splitting**: Switched from Semantic Chunker to Recursive splitting for deterministic ingestion speed.
*   **[DONE] Rebranding**: Fully rebranded to "Wo ist meine Doku".

---

## Technical Implementation Backlog

### Epic 1: Advanced Hybrid Retrieval & Analytics
*Goal: Enhance the quality and transparency of search results.*

#### Task 1.1: Reciprocal Rank Fusion (RRF) Reranking
- **Description**: Implement RRF to better merge Vector and BM25 scores.
- **Status**: [BACKLOG]

#### Task 1.2: German Compound Decomposition Analytics
- **Description**: Use `split-words` to highlight which parts of a compound word matched a query.
- **Status**: [BACKLOG]

---

### Epic 2: Productivity & Export Features
*Goal: Enable users to take data out of the system.*

#### Task 2.1: CSV/Excel Result Export
- **Description**: Allow users to export the current search view to a spreadsheet.
- **Status**: [IN_PROGRESS]

#### Task 2.2: Cross-Document Comparison View
- **Description**: Side-by-side view for comparing two found documents.
- **Status**: [BACKLOG]

---

### Epic 3: Deployment & Stability
*Goal: Professional-grade local deployment.*

#### Task 3.1: Portable Python Environment
- **Description**: Package the app with an embedded Python interpreter to avoid 'install.bat' requirements for end users.
- **Status**: [FUTURE]

#### Task 3.2: Optional OCR Plugin
- **Description**: Add OCR as an optional download/module to keep the core "Turbo-Lite" engine small.
- **Status**: [RESEARCH]

---

## 🛠️ Technical Stack (Current)
- **Engine**: FastEmbed (ONNX)
- **DB**: LanceDB
- **UI**: Streamlit
- **Parsers**: pdfplumber, sharepoint-to-text
- **Language**: Python 3.10+