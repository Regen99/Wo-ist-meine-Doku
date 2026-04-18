import os
import sys

# ── Path Bootstrap ─────────────────────────────────────────────────────────────
# Must happen BEFORE any `from src.*` imports.
# app.py lives at src/ui/app.py → project root is two levels up.
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
import html
import subprocess
import re
from src.engine.pipeline import DiscoveryPipeline
from src.utils.config import ConfigManager
import tkinter as tk
from tkinter import filedialog

# Alias for use in reveal_in_explorer path resolution
project_root = _project_root


# ── Setup & Theme Evaluation ──────────────────────────────────────────────────
@st.cache_resource
def get_config():
    return ConfigManager()

@st.cache_resource
def get_pipeline():
    return DiscoveryPipeline()

config = get_config()

if 'pipeline' not in st.session_state:
    with st.spinner("Initializing Discovery Engine..."):
        st.session_state.pipeline = get_pipeline()

def select_folder():
    """ Opens a native folder selection dialog. """
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    root.attributes('-topmost', True) # Bring dialog to front
    folder_path = filedialog.askdirectory(master=root)
    root.destroy()
    return folder_path

def highlight_text(text: str, query: str) -> str:
    """
    Escapes text and highlights query terms using HTML <mark> tags.
    """
    if not query:
        return html.escape(text)
    
    # Escape the text first to prevent XSS
    escaped_text = html.escape(text)
    
    # Split query into words and escape them for regex
    words = [re.escape(word) for word in query.split() if len(word) > 1]
    if not words:
        return escaped_text
    
    # Create regex pattern for all words (case-insensitive)
    pattern = re.compile(f"({'|'.join(words)})", re.IGNORECASE)
    
    # Wrap matches in <mark> tags
    # We replace with \1 to preserve original case
    return pattern.sub(r'<mark>\1</mark>', escaped_text)

def reveal_in_explorer(file_path: str):
    """
    Opens Windows Explorer and selects the specified file.
    """
    try:
        # Normalize for Windows and ensure absolute path
        # DiscoveryPipeline stores paths like 'data/raw/file.pdf'
        abs_path = os.path.abspath(os.path.join(project_root, file_path))
        if os.path.exists(abs_path):
            # explorer /select selects the file in its folder
            subprocess.run(["explorer", "/select,", abs_path], check=False)
        else:
            # Fallback to directory if file specifically doesn't exist but dir might
            dir_path = os.path.dirname(abs_path)
            if os.path.exists(dir_path):
                os.startfile(dir_path)
            else:
                st.error(f"Path not found: {abs_path}")
    except Exception as e:
        st.error(f"Failed to open explorer: {e}")

# Page Config
st.set_page_config(
    page_title="Wo ist meine Doku | Discovery",
    layout="wide"
)

# ── Theme Selection & Header ──────────────────────────────────────────────────
# Evaluated BEFORE CSS so the style updates instantaneously without a manual rerun.
header_col1, header_col2 = st.columns([5, 1])
with header_col1:
    st.markdown("<h1 style='margin-bottom: 0;'>Search Discovery</h1>", unsafe_allow_html=True)
with header_col2:
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True) # Top spacing
    is_dark = st.toggle("🌙 Dark", key="dark_mode")

# ── Main: Custom CSS (Clay-Inspired) ──────────────────────────────────────────
# CSS Variants
light_css = """
    .stApp, .stAppHeader, [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6 { color: #1e1e1e !important; }
    p, span, label, div, .st-markdown { color: #3b3b3b !important; }
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        box-shadow: rgba(149, 157, 165, 0.1) 0px 8px 24px;
    }
    .result-card:hover { border-color: #005fb8 !important; }
    .result-card-text { color: #3b3b3b !important; }
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #3b3b3b !important;
        border: 1px solid #d1d5da !important;
    }
    [data-testid="stSidebar"] { background-color: #f3f3f3 !important; border-right: 1px solid #e1e4e8 !important; }
    .lang-tag { background-color: #eef6ff !important; color: #005fb8 !important; border: 1px solid #005fb833; }
    .legal-tag { background-color: #f8e6ff !important; color: #af00db !important; border: 1px solid #af00db33; }
"""

dark_css = """
    .stApp, .stAppHeader, [data-testid="stSidebar"] {
        background-color: #1e1e1e !important;
    }
    h1, h2, h3, h4, h5, h6 { color: #cccccc !important; }
    p, span, label, div, .st-markdown { color: #cccccc !important; }
    .result-card {
        background-color: #252526;
        border: 1px solid #3c3c3c;
        box-shadow: rgba(0, 0, 0, 0.3) 0px 8px 24px;
    }
    .result-card:hover { border-color: #4fc1ff !important; }
    .result-card-text { color: #cccccc !important; }
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #3c3c3c !important;
        color: #cccccc !important;
        border: 1px solid #555555 !important;
    }
    [data-testid="stSidebar"] { background-color: #252526 !important; border-right: 1px solid #3c3c3c !important; }
    .lang-tag { background-color: #1e2a35 !important; color: #4fc1ff !important; border: 1px solid #4fc1ff33; }
    .legal-tag { background-color: #2d1e35 !important; color: #c586c0 !important; border: 1px solid #c586c033; }
"""

# Global Styles (shared)
base_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&family=Space+Mono&display=swap');

    /* Typography */
    h1, h2, h3, h4, h5, h6, p, span, div, label {{ font-family: 'Outfit', sans-serif; }}
    h1 {{ font-weight: 600 !important; letter-spacing: -3.2px !important; font-size: 3.75rem !important; }}
    h2, h3 {{ font-weight: 600 !important; letter-spacing: -1.32px !important; }}

    /* Result Cards */
    .result-card {{
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 32px;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    .result-card:hover {{
        transform: translateY(-2px);
    }}
    .result-card-text {{
        font-size: 1.13rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }}

    /* Tags */
    .lang-tag {{
        font-family: 'Space Mono', monospace !important;
        font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.08px;
        background-color: #f0f8ff; padding: 6px 12px; border-radius: 11px; color: #3859f9 !important; margin-right: 8px;
    }}
    .legal-tag {{
        font-family: 'Space Mono', monospace !important;
        font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.08px;
        background-color: #fc798122; padding: 6px 12px; border-radius: 11px; color: #fc7981 !important; border: 1px solid #fc7981;
    }}
    .file-tag {{ font-family: 'Space Mono', monospace !important; font-size: 0.75rem; color: #9f9b93 !important; }}

    /* Buttons */
    .stButton>button {{
        background-color: transparent !important; color: #717989 !important; border: 1px solid #717989 !important;
        border-radius: 12px !important; font-weight: 500 !important; padding: 6.4px 12.8px !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}
    .stButton>button:hover {{
        background-color: #078a52 !important; color: #ffffff !important; border-color: #000000 !important;
        transform: rotateZ(-3deg) translateY(-8px) !important; box-shadow: #000000 -7px 7px 0px !important;
    }}

    /* Highlighting */
    mark {{
        background-color: #fbbd41 !important; color: #000000 !important; border-radius: 4px; padding: 2px 6px;
        font-weight: 500; box-shadow: rgba(0,0,0,0.1) 0px 1px 1px inset;
    }}
    
    /* Input Rounding */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {{ border-radius: 8px !important; }}

    /* Theme Specific Injections */
    {dark_css if is_dark else light_css}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)

# Initialize Backend Pipeline (cached in session)
# Redundant block removed (already initialized at top)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Wo ist meine Doku")
    st.subheader("Discovery Engine")
    st.divider()

    # ── Multi-Path Management (Favorites) ───────────────────────────────────
    st.markdown("### Project Favorites")
    favorites = config.get_favorites()
    
    if favorites:
        selected_fav = st.selectbox(
            "Select a favorite project",
            ["-- Choose a Favorite --"] + favorites,
            label_visibility="collapsed",
            key="fav_dropdown"
        )
        # Use _pending_dir pattern — same as folder picker — to avoid
        # Streamlit widget state conflicts (cannot write to a widget key
        # after it has already been rendered in the current run).
        if selected_fav != "-- Choose a Favorite --" and selected_fav != st.session_state.get("_dir_widget"):
            st.session_state._pending_dir = selected_fav
            config.set_last_used_path(selected_fav)
            st.rerun()
    else:
        st.info("No favorite paths saved yet.")

    st.divider()
    st.markdown("### Document Ingestion")

    if '_pending_dir' in st.session_state:
        st.session_state._dir_widget = st.session_state._pending_dir
        config.set_last_used_path(st.session_state._pending_dir)
        del st.session_state._pending_dir

    # Initialize widget state from config if not existing
    if '_dir_widget' not in st.session_state:
        st.session_state._dir_widget = config.get_last_used_path()

    st.caption("Current Source Path")
    col_path, col_btn_pick, col_btn_fav = st.columns([4, 1, 1])
    
    with col_path:
        current_path = st.text_input(
            "Source Directory",
            key="_dir_widget",
            label_visibility="collapsed"
        )
    
    with col_btn_pick:
        if st.button("📁", help="Select Source Folder"):
            picked_path = select_folder()
            if picked_path:
                st.session_state._pending_dir = picked_path
                st.rerun()

    with col_btn_fav:
        is_fav = current_path.replace("\\", "/") in favorites
        if st.button("⭐" if not is_fav else "🗑️", help="Add/Remove Favorite"):
            if is_fav:
                config.remove_favorite(current_path)
            else:
                config.add_favorite(current_path)
            st.rerun()

    if st.button("Sync & Re-index", use_container_width=True):
        config.set_last_used_path(current_path)
        with st.status("Ingesting Documents...", expanded=True) as status:
            new_files = st.session_state.pipeline.run_incremental_pipeline(st.session_state._dir_widget)
            status.update(
                label=f"Sync Complete! Indexed {new_files} new file(s).",
                state="complete",
                expanded=False,
            )
        st.success("Knowledge index is up to date.")

    st.divider()
    st.markdown("### System Status")
    st.info("Multilingual-E5-Small (Lite)")
    st.info("CPU-Only Mode")
    st.info("LanceDB (Hybrid Search)")
    st.success("100% Offline & GDPR Safe")

# ── Main: Search ──────────────────────────────────────────────────────────────
st.caption("Locate exact paragraphs from German legal texts and technical documents.")

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<b>What are you looking for?</b>", unsafe_allow_html=True)
    search_query = st.text_input(
        "query",
        placeholder="e.g., §34 BauGB inner area or Display thermal limits...",
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<b>Language</b>", unsafe_allow_html=True)
    lang_filter = st.selectbox("lang", ["All", "DE", "EN"], label_visibility="collapsed")

# Fix #7: legal_only is now wired and forwarded through the pipeline
col_opt1, col_opt2 = st.columns([0.4, 0.6])
with col_opt1:
    legal_only = st.checkbox("Focus on Legal Context only")
with col_opt2:
    exact_match = st.checkbox("Exact Keyword Match only")

if search_query:
    st.divider()

    filter_lang = lang_filter.lower() if lang_filter != "All" else None
    
    try:
        results = st.session_state.pipeline.query(
            search_query,
            limit=10,
            language=filter_lang,
            legal_only=legal_only,  # Fix #7: was dead code before
            exact_match=exact_match,
        )
    except Exception as e:
        results = None
        if exact_match and ("tantivy" in str(e).lower() or "fts" in str(e).lower()):
            st.error("Exact Match requires the 'tantivy' package or a recreated index. Please run `pip install tantivy` then re-sync directory.")
        else:
            st.error(f"Search failed: {e}")

    if results is None:
        pass # Error already shown
    elif not results:
        st.warning("No matches found. Try adding documents via Sync & Re-index first, or verify Exact Match keywords.")
    else:
        st.write(f"**{len(results)} matches found:**")

        for idx, res in enumerate(results):
            full_source_path = res.get("source_path", "Unknown")
            filename = os.path.basename(full_source_path)
            content = highlight_text(res.get("text", ""), search_query)
            source_path = html.escape(full_source_path)
            lang = html.escape(res.get("language", "und").upper())
            is_legal = res.get("legal_context", False)
            legal_badge = f"<span class='legal-tag'>LEGAL §</span>" if is_legal else ""

            # Define the card HTML
            card_html = (
                f'<div class="result-card">'
                f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px dashed #dad4c8; padding-bottom: 16px;">'
                f'<div><span class="lang-tag">{lang}</span>{legal_badge}</div>'
                f'<span class="file-tag">FILE: {html.escape(filename)}</span>'
                f'</div>'
                f'<div class="result-card-text">{content}</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Expansion for Preview and Actions
            with st.expander(f"👁️ Preview & Actions: {filename}"):
                col_prev, col_act = st.columns([1, 2])
                with col_prev:
                    if filename.lower().endswith(".pdf"):
                        thumb_bytes = st.session_state.pipeline.generate_thumbnail(full_source_path)
                        if thumb_bytes:
                            st.image(thumb_bytes, use_container_width=True, caption="First Page Preview")
                        else:
                            st.info("No preview available")
                    else:
                        st.info("Preview support only for PDF")
                
                with col_act:
                    st.write(f"**Full Path:**")
                    st.code(full_source_path, language="text")
                    if st.button("📂 Open in Explorer", key=f"open_{idx}_{filename}"):
                        reveal_in_explorer(full_source_path)
                    
                    st.caption("Tip: Use 'Open in Explorer' to locate the document instantly.")
else:
    st.info("Tip: Try searching for specific legal concepts or technical requirements.")

# Footer
st.divider()
st.caption("Wo ist meine Doku v1.0 — High-fidelity retrieval. 100% offline.")
