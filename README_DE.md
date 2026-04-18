# Wo ist meine Doku

**Lokale semantische Suchmaschine für private Dokumente**

Finden Sie genau das, was Sie suchen, anhand der *Bedeutung*, nicht nur anhand von Schlüsselwörtern. Ganz gleich, wo es in Ihren lokalen Dateien versteckt ist.

[English Version](README.md) | **Deutsch**

---

## Übersicht

Wo ist meine Doku ist eine leistungsstarke, professionelle Suchmaschine für Rechtsexperten, Forscher und technische Prüfer, die eine 100%ige Offline-Dokumentenanalyse benötigen. Durch den Einsatz modernster Embedding-Modelle und Vektor-Datenbanken wird Ihr lokaler PC indexiert, sodass Sie Dokumente mit natürlicher Sprache abfragen und exakte Textstellen sofort finden können.

- **Kein Datenabfluss**: Alle Operationen erfolgen ausschließlich lokal. Keine Cloud, keine externen Server.
- **Hohe Genauigkeit**: Spezialisiert auf deutsche Rechtstexte (§) und technische Anforderungen.
- **Stabilität**: Optimiert für Standard-Windows-Hardware (nur CPU).

---

## Hauptfunktionen

### Semantische Inhaltssuche
Indexieren Sie Ordner und Unterordner automatisch. Suchen Sie nach Konzepten wie "Brandschutzvorschriften für innerstädtische Wohngebiete" statt nur nach "Brandschutz". Das System versteht den Kontext und findet relevante Absätze in Tausenden von Dateien.

### Hybride Suche
Kombiniert leistungsstarke Volltextsuche (FTS5) mit semantischer Vektorähnlichkeit. Dies stellt sicher, dass exakte Stichworttreffer genauso zuverlässig gefunden werden wie konzeptionelle Übereinstimmungen.

### UI/UX: Clay Design System
Ein handgefertigtes "Clay"-Design mit warmen Farbtönen (Night Clay für den Dunkelmodus), taktilen Hover-Animationen und markanten Schatten. Inklusive der Schaltfläche **"Im Explorer anzeigen"** und einer **nativen Ordnerauswahl** für eine intuitive Bedienung.

### Ultra-Lite Parsing (NEU)
Nutzt extrem schnelle, CPU-effiziente Parser (`pdfplumber`), um Text aus Dokumenten sofort zu extrahieren, ohne schwere neuronale Layout-Engines laden zu müssen. Dies verhindert System-Freezes, die zuvor durch komplexe KI-Verarbeitung verursacht wurden.

### Unterstützung mehrerer Formate
Leistungsstarke Parser verarbeiten eine Vielzahl von Dokumenttypen unter Beibehaltung der Dokumentstruktur.

| Format | Erweiterungen | Anmerkungen |
|------|--------|------|
| Portable Document | `.pdf` | Strukturierte Textextraktion |
| Textverarbeitung | `.docx` `.doc` | Strukturelle Hierarchie bleibt erhalten |
| Tabellenkalkulation | `.xlsx` `.xls` | Verfolgung bis auf Zellenebene (Zeile/Spalte) |
| Präsentationen | `.pptx` | Folienbasierte semantische Indexierung |
| Reiner Text | `.txt` `.md` | Automatische Erkennung der Kodierung |

---

## Installation & Bereitstellung

### 1. Voraussetzungen
- **Windows 10/11 x64**
- **Python 3.10 oder höher**
- RAM: 8 GB (Minimum), 16 GB (empfohlen)
- Festplatte: 1 GB freier Speicherplatz für Indizes und Modelle

### 2. Einrichtung
Doppelklicken Sie auf **`install.bat`** im Hauptverzeichnis.
Dies bewirkt Folgendes:
- Erstellung einer lokalen virtuellen Umgebung (VENV).
- Installation der **FastEmbed** Bibliothek und ONNX Runtime (CPU-optimiert).
- Herunterladen des Embedding-Modells (~150 MB, einmaliger Vorgang).

### 3. Starten
Doppelklicken Sie auf **`Launch-Doku.bat`**, um das Discovery Dashboard zu starten.
Ihr Browser öffnet sich automatisch unter `http://localhost:8501`.

---

## Sicherheit & Datenschutz

Das System ist für maximale Compliance und Datensouveränität ausgelegt. Wenn KI-Funktionen deaktiviert sind, findet **keinerlei Netzwerkkommunikation** statt.

| Funktion | Datenspeicherort | Externe Übertragung |
|------|------------|----------|
| Indexierung | Lokale SQLite / LanceDB | Keine |
| Semantische Suche | Lokaler Vektor-Index | Keine |
| Embedding-Operationen | Lokales ONNX/Torch-Modell | Keine |
| Dokumentvorschau | In-Memory-Cache | Keine |
| Telemetrie | Deaktiviert | Keine |

---

## Architektur

```mermaid
graph TD
    UI[Streamlit Dashboard] --> Pipeline[Discovery Pipeline]
    
    subgraph "Engine Layer"
        Pipeline --> Chunker[Rekursiver Chunker]
        Pipeline --> Embedder[MiniLM-L12-v2 Embedder]
        Pipeline --> DB[LanceDB Hybrid Store]
    end
    
    subgraph "Parsing Layer"
        ParserFactory[Parser Factory] --> PDF[pdfplumber]
        ParserFactory --> Office[Office Parsers]
    end
    
    subgraph "Storage Layer"
        DB --> FTS[FTS5 Indizes]
        DB --> Vector[Vektor-Index (HNSW)]
    end
    
    Source[Benutzerdokumente] --> ParserFactory
```

| Komponente | Technologie-Stack |
|------|------|
| **Benutzeroberfläche** | Streamlit |
| **Orchestrierung** | Python 3.10+ |
| **Vector Engine** | LanceDB (LCA) |
| **Embeddings** | FastEmbed (paraphrase-multilingual-MiniLM-L12-v2) |
| **Parsing** | pdfplumber / python-docx / openpyxl |
| **Inference** | ONNX Runtime (CPU-optimiert) |

---

## Lizenz & Kontakt

Copyright 2025-2026 Wo ist meine Doku. Entwickelt durch den Antigravity Agent.

- **Entwickler**: sungwoo.kim@gmx.de
- **Repository**: [Regen99/Wo-ist-meine-Doku](https://github.com/Regen99/Wo-ist-meine-Doku)

Für Support, Fehlermeldungen oder Anfragen zur Integration in juristische Arbeitsprozesse kontaktieren Sie den Entwickler bitte per E-Mail.
