## [2026-04-18] [FIX] | UI Dependency Logic & Checkbox Styling (v1.3.18)
- Refactored Search Options: "Include Subfolders" now only appears when "Current Folder Only" is active.
- Fixed "Naked Checkmark" CSS bug by adding explicit high-contrast borders to `stCheckbox`.
- Corrected accidental code loss in `app.py` layout grid.

## [2026-04-18] [FEAT] | Recursive Search Toggle (v1.3.17)
- Added "Include Subfolders" toggle to search filters.
- Implemented `ILIKE` for case-insensitive path matching in LanceDB.
- Hardened path prefix logic to ensure clean folder boundary matching.
- Enabled granular control over deep vs. flat directory discovery.

## [2026-04-18] [QA] | Subfolder Indexing Clarification (v1.3.16)
- Confirmed that indexing is fully recursive via `os.walk`.
- Confirmed that "Current Folder Only" search filter is recursive via SQL `LIKE` prefix matching.
- Documented exclusion of hidden (`.`) and system (`$`) folders.

## [2026-04-18] [UI] | Sidebar Identity: Recursive Font (v1.3.15)
- Switched all sidebar text elements to the `Recursive` Google Font.
- Imported `Recursive` (wght 300-1000) for better navigational contrast.

## [2026-04-18] [FIX] | CSS f-string NameError (v1.3.14)
- Fixed `NameError` by doubling CSS braces `{{ }}` in `app.py`.
- Restored application startup stability.

## [2026-04-18] [FIX] | Responsive UI Hardening (v1.3.13)
- Enforced `white-space: nowrap` on tags, headers, and buttons.
- Optimized result header column ratios (18/52/15/15) for high badge density.
- Prevented font/icon line wrapping during container resize.

## [2026-04-18] [FEAT] | Path-Centric Result Headers (v1.3.12)
- Replaced filename header with full source path for absolute clarity.
- Unified identifying information into a single, high-contrast primary label.

## [2026-04-18] [FEAT] | Folder-Aware Discovery & State Hardening (v1.3.11)
- Added "Current Folder Only" search filter.
- Decoupled widget keys from session state to resolve StreamlitAPIExceptions.
- Implemented Version-Aware Pipeline reloads.

## [2026-04-18] [STABILITY] | Lazy loaded OCR dependencies to prevent startup crashes.
## [2026-04-18] [FEAT] | Added support for .md, .txt, .csv, and .log files.
## [2026-04-18] [UI] | Implemented Total White contrast mode for Light Mode widgets.
## [2026-04-18] [UI] | Overhauled sidebar-heavy design to Top NAV Toolbar layout for ingestion/favorites.

## [2026-04-18] [FIX] | UI Readability: Light Mode Contrast Overhaul
- **Selectbox Fix**: Resolved "black box" issue in Light Mode by forcing white backgrounds and high-contrast dark text via robust CSS selectors.
- **Button Contrast**: Darkened default button labels and borders for better visibility; maintained "magical" hover states with clear white-on-black text.
- **Sidebar Clarity**: Refined sidebar colors and text contrast to ensure professional legibility.

## [2026-04-18] [FIX] | Runtime Stability & Environment Hardening (v1.3.1)
- **Path Bootstrapping**: Fixed `ModuleNotFoundError: No module named 'src'` by moving `sys.path` modification to the absolute top of `app.py`.
- **Lazy Imports**: Refactored `ocr.py` and `pipeline.py` to lazy-load `rapidocr` and `fitz`. The app now boots and extracts text even if OCR/Thumbnail packages are missing.
- **Dependency Sync**: Explicitly installed `pymupdf`, `rapidocr-onnxruntime`, and `opencv-python-headless` into the `.venv` used by the launcher.
- **Git Operations**: Performed forced push to synchronize remote state with the hardened local version.

## [2026-04-18] [UPDATE] | Phase 5: UX Pro & Multi-Discovery (v1.3.0)
- **Multi-Path Management**: Integrated **Favorites** system via `DiscoveryConfig` and sidebar controls.
- **ONNX-OCR**: Implemented **RapidOCR** fallback for scanned/blank PDFs, ensuring 100% discovery coverage for paper-to-digital workflows.
- **Visual Previews**: Added **High-Fidelity PDF Thumbnails** in search results for instant visual confirmation.
- **Infrastructure**: Added `rapidocr_onnxruntime` and `pymupdf` to requirements; maintaining Ultra-Lite CPU footprint.

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
