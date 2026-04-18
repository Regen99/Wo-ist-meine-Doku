# Wo ist meine Doku

**Local Semantic Discovery Engine for Private Documents**

---

### 🌐 Select Language / Sprache wählen
[English](#-english-version) | [Deutsch](#-deutsche-version)

---

## 🇺🇸 English Version

Your system has been optimized for **Maximum Speed and Stability** on your local PC.

### How to Start
1.  **First Time ONLY**: Double-click **`install.bat`**. 
    *   This will create a lightweight virtual environment and install exactly what you need for CPU mode.
2.  **To Use the App**: Double-click **`Launch-Doku.bat`**.
    *   This will start the dashboard and automatically open your web browser.

### Features
- **Semantic Search**: Find paragraphs by *meaning*, not just keywords.
- **100% Offline**: Zero data leakage. All processing happens on your core.
- **Hybrid Retrieval**: Combines Vektor Search with FTS5 Keyword matching.
- **Ultra-Lite Engine**: CPU-optimized using ONNX/FastEmbed. No freezing.
- **Clay Design**: Handcrafted professional UI with Night Clay (Dark Mode).

---

<details>
<summary><b>🇩🇪 Deutsche Version (Klicken zum Aufklappen / Click to Expand)</b></summary>

## 🇩🇪 Deutsche Version

Wo ist meine Doku ist eine leistungsstarke Suchmaschine für Rechtsexperten und Forscher, die eine 100%ige Offline-Dokumentenanalyse benötigen.

### Erste Schritte
1. **Nur beim ersten Mal**: Doppelklicken Sie auf **`install.bat`**.
   * Dies erstellt eine virtuelle Umgebung und installiert die CPU-optimierten Bibliotheken.
2. **App starten**: Doppelklicken Sie auf **`Launch-Doku.bat`**.
   * Das Dashboard startet und öffnet automatisch Ihren Browser.

### Hauptfunktionen
- **Semantische Suche**: Finden Sie Textstellen nach *Bedeutung* (§), nicht nur nach Stichworten.
- **100% Offline**: Keine Cloud, kein Datenabfluss. Maximale Datensouveränität.
- **Hybride Suche**: Kombiniert Vektorähnlichkeit 서비스와 FTS5-Volltextsuche.
- **Ultra-Lite Engine**: Minimale Systemlast, optimiert für Standard-Hardware.
- **Clay Design System**: Taktiles Design mit Night Clay (Dunkelmodus).

### Unterstützte Formate
`.pdf`, `.docx`, `.xlsx`, `.pptx`, `.txt`, `.md`

---

</details>

---

## Technical Details

### Architecture
| Component | Technology Stack |
|------|------|
| **Interface** | Streamlit |
| **Vector Engine** | LanceDB |
| **Embeddings** | FastEmbed (MiniLM-L12-v2) |
| **Parsing** | pdfplumber / sharepoint-to-text |

### Security & Privacy
| Feature | Data Location | External Transmission |
|------|------------|----------|
| Indexing | Local SQLite / LanceDB | None |
| Semantic Search | Local Vector Index | None |
| Telemetry | Disabled | None |

---

## License & Support
Copyright 2025-2026 Wo ist meine Doku. Developed by the Antigravity Agent.
- **Repository**: [Regen99/Wo-ist-meine-Doku](https://github.com/Regen99/Wo-ist-meine-Doku)
- **Contact**: sungwoo.kim@gmx.de
