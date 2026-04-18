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

# ── Main UI Layout ────────────────────────────────────────────────────────────

# CSS Variants
light_css = """
    .stApp, .stAppHeader, [data-testid="stSidebar"] { background-color: #faf8f4 !important; }
    h1, h2, h3, h4, h5, h6 { color: #2d2a26 !important; }
    p, span, label, div, .st-markdown { color: #2d2a26 !important; }
    
    /* 💎 UNIFIED CARD DESIGN */
    .result-card { 
        background-color: #ffffff; 
        border: 2px solid #000000; 
        box-shadow: rgba(0, 0, 0, 0.05) 0px 8px 24px; 
    }
    .result-card:hover { border-color: #000000 !important; background-color: #f8f9fb !important; }
    .result-card-text { color: #2d2a26 !important; }
    
    /* 🚀 TOTAL UNIFICATION: Selectbox, Dropdown, Menu, Tooltip & Expander */
    [data-baseweb="select"], [data-baseweb="select"] > div,
    [data-baseweb="popover"], [data-baseweb="popover"] > div,
    [data-baseweb="menu"], [data-baseweb="menu"] *,
    [data-baseweb="tooltip"], [data-baseweb="tooltip"] *,
    [role="listbox"], [role="listbox"] *,
    [role="option"], [role="option"] *,
    .stSelectbox div, .stSelectbox [role="button"],
    [data-testid="stExpander"], [data-testid="stExpander"] summary, 
    [data-testid="stCode"], [data-testid="stCode"] *, [data-testid="stCode"] div, [data-testid="stCode"] pre {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #000000 !important;
    }

    /* Unified Border Logic for Popovers, Menus, & Expanders */
    [data-baseweb="popover"], [data-baseweb="popover"] > div, 
    [data-baseweb="tooltip"], .stTooltipContent,
    [data-testid="stExpander"], [data-testid="stCode"] {
        border: 2px solid #000000 !important;
        border-radius: 12px !important;
        box-shadow: rgba(0, 0, 0, 0.1) 0px 8px 24px !important;
    }
    
    [data-testid="stCode"] { padding: 0px !important; overflow: hidden !important; }
    [data-testid="stCode"] pre { padding: 12px !important; margin: 0 !important; }

    /* Hover States for Menus & Expanders */
    [data-baseweb="menu"] li:hover, [role="option"]:hover, [data-baseweb="popover"] li:hover, [data-testid="stExpander"] summary:hover {
        background-color: #f8f9fb !important;
    }

    /* 💎 UNIFIED INTERACTIVE DESIGN: White Boxes + Black Borders */
    .stTextInput input, .stTextArea textarea, 
    .stSelectbox [data-baseweb="select"], .stSelectbox [role="button"], .stSelectbox div[data-baseweb="input"],
    div[data-testid="stButton"] button, 
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    [data-testid="stStatusWidget"] {
        background-color: #ffffff !important; 
        color: #000000 !important; 
        border: 2px solid #000000 !important;
        border-radius: 12px !important;
        min-height: 42px !important;
        box-shadow: none !important;
    }
    
    /* Hover state for all interactive elements */
    .stTextInput input:hover, .stSelectbox [data-baseweb="select"]:hover, div[data-testid="stButton"] button:hover, [data-testid="stStatusWidget"]:hover {
        background-color: #f8f9fb !important;
    }

    /* Force text color & remove internal gradients */
    .stSelectbox [data-baseweb="select"] *, .stSelectbox [role="button"] * {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] { background-color: #faf8f4 !important; border-right: 2px solid #000000 !important; }
    
    .lang-tag { background-color: #eef6ff !important; color: #2d2a26 !important; border: 1px solid #00000033; }
    .legal-tag { background-color: #f8e6ff !important; color: #2d2a26 !important; border: 1px solid #00000033; }
"""

dark_css = """
    .stApp, .stAppHeader, [data-testid="stSidebar"] { background-color: #1e1e1e !important; }
    h1, h2, h3, h4, h5, h6 { color: #cccccc !important; }
    p, span, label, div, .st-markdown { color: #cccccc !important; }
    .result-card { background-color: #252526; border: 1px solid #3c3c3c; box-shadow: rgba(0, 0, 0, 0.3) 0px 8px 24px; }
    .result-card:hover { border-color: #4fc1ff !important; }
    .result-card-text { color: #cccccc !important; }
    .stTextInput input, .stSelectbox [data-baseweb="select"], .stSelectbox div[role="button"] { background-color: #3c3c3c !important; color: #ffffff !important; border: 1px solid #555555 !important; }
    [data-testid="stSidebar"] { background-color: #252526 !important; border-right: 1px solid #3c3c3c !important; }
    .lang-tag { background-color: #1e2a35 !important; color: #4fc1ff !important; border: 1px solid #4fc1ff33; }
    .legal-tag { background-color: #2d1e35 !important; color: #c586c0 !important; border: 1px solid #c586c033; }
"""

with st.sidebar:
    st.title("Wo ist meine Doku")
    is_dark = st.toggle("🌙 Dark Mode", key="dark_mode")
    st.divider()
    st.markdown("### System Status")
    st.info("CPU-Only Mode")
    st.success("100% Offline & GDPR Safe")

# ── Header & NAV Toolbar ──────────────────────────────────────────────────────
st.markdown("<h1 style='margin-bottom: -15px; margin-top: -60px; font-size: 2.75rem !important;'>Wo ist meine Doku</h1>", unsafe_allow_html=True)

base_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&family=Space+Mono&display=swap');
    
    h1, h2, h3, h4, h5, h6, p, span, div, label {{ font-family: 'Outfit', sans-serif; }}
    .result-card {{ border-radius: 24px; padding: 32px; margin-bottom: 24px; transition: all 0.25s; }}
    .result-card-text {{ font-size: 1.13rem; line-height: 1.6; white-space: pre-wrap; }}
    
    /* 🔒 GIGANTIC INTERACTIVE LOCK: Global Height, Border, Radius */
    div[data-testid="stButton"] button, 
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"],
    .stTextInput input, .stTextArea textarea, 
    .stSelectbox [data-baseweb="select"], 
    .stSelectbox [role="button"], 
    .stSelectbox div[data-baseweb="input"] {{
        height: 42px !important;
        min-height: 42px !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }}

    mark {{ background-color: #fbbd41 !important; color: #000000 !important; border-radius: 4px; padding: 2px 6px; }}
    .lang-tag, .legal-tag {{ font-family: 'Space Mono', monospace !important; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.08px; padding: 6px 12px; border-radius: 11px; margin-right: 8px; }}
    .file-tag {{ font-family: 'Space Mono', monospace !important; font-size: 0.75rem; color: #9f9b93 !important; }}

    {dark_css if is_dark else light_css}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)

# ── TOP TOOLBAR (The Nav Section) ───────────────────────────────────────────
st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)
with st.container():
    # Split Layout: Left (Inputs) | Right (Actions)
    n_left, n_right = st.columns([6.2, 3.8])
    
    favorites = config.get_favorites()
    if '_dir_widget' not in st.session_state:
        st.session_state._dir_widget = config.get_last_used_path()

    with n_left:
        l1, l2, l3 = st.columns([2.5, 5, 1.3], vertical_alignment="bottom")
        with l1:
            st.markdown("<small><b>Project Favorites</b></small>", unsafe_allow_html=True)
            fav_options = ["-- Favorites --"] + (favorites if favorites else [])
            selected_fav = st.selectbox("fav", fav_options, label_visibility="collapsed", key="nav_fav_sel")
            if selected_fav != "-- Favorites --" and selected_fav != st.session_state._dir_widget:
                st.session_state._dir_widget = selected_fav
                st.rerun()
        with l2:
            st.markdown("<small><b>Ingestion Path</b></small>", unsafe_allow_html=True)
            current_path = st.text_input("path", value=st.session_state._dir_widget, label_visibility="collapsed", key="nav_path_val")
            st.session_state._dir_widget = current_path
        with l3:
            st.markdown("<small><b>&nbsp;</b></small>", unsafe_allow_html=True) 
            if st.button("📁 Browse", help="Pick Folder", key="nav_picker", use_container_width=True):
                path = select_folder()
                if path:
                    st.session_state._dir_widget = path
                    st.rerun()

    with n_right:
        r1, r2 = st.columns([1.5, 3.5], vertical_alignment="bottom")
        with r1:
            st.markdown("<small><b>&nbsp;</b></small>", unsafe_allow_html=True) 
            is_fav = (current_path or "").replace("\\", "/") in [f.replace("\\", "/") for f in favorites]
            btn_text = "⭐ Fav" if not is_fav else "🗑️ Unfav"
            if st.button(btn_text, help="Add/Remove Favorite", key="nav_fav_toggle", use_container_width=True):
                if is_fav: config.remove_favorite(current_path)
                else: config.add_favorite(current_path)
                st.rerun()
        with r2:
            st.markdown("<small><b>&nbsp;</b></small>", unsafe_allow_html=True) 
            sync_triggered = st.button("Sync & Re-index", key="sync_btn", use_container_width=True)

# Status Container (Outside columns to prevent height fragmentation)
status_placeholder = st.empty()
if sync_triggered:
    config.set_last_used_path(st.session_state._dir_widget)
    with status_placeholder.status("Indexing...", expanded=True) as status:
        new_files = st.session_state.pipeline.run_incremental_pipeline(st.session_state._dir_widget)
        status.update(label=f"Done! +{new_files} files", state="complete", expanded=False)
    st.rerun()

st.divider()

# ── Main: Search Area ────────────────────────────────────────────────────────
st.markdown("<h3 style='margin-bottom: -5px; margin-top: -20px;'>Search Discovery</h3>", unsafe_allow_html=True)
st.caption("Locate exact paragraphs from German legal texts and technical documents.")

s_col1, s_col2 = st.columns([4, 1.2], vertical_alignment="bottom")
with s_col1:
    search_query = st.text_input("What are you looking for?", placeholder="e.g., §34 BauGB inner area...", key="main_search_val")
with s_col2:
    st.markdown("<div style='text-align: right;'><small><b>Language</b></small></div>", unsafe_allow_html=True)
    lang_filter = st.selectbox("lang", ["All", "DE", "EN"], label_visibility="collapsed", key="lang_sel_val")

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
col_opt1, col_opt2 = st.columns([0.4, 0.6])
with col_opt1:
    legal_only = st.checkbox("Focus on Legal Context")
with col_opt2:
    exact_match = st.checkbox("Exact Keyword Match")

if search_query:
    st.divider()
    filter_lang = lang_filter.lower() if lang_filter != "All" else None
    try:
        results = st.session_state.pipeline.query(search_query, limit=10, language=filter_lang, legal_only=legal_only, exact_match=exact_match)
    except Exception as e:
        results = None
        st.error(f"Search failed: {e}")

    if results is None: pass
    elif not results: st.warning("No matches found.")
    else:
        st.write(f"**{len(results)} matches found:**")
        for idx, res in enumerate(results):
            full_source_path = res.get("source_path", "Unknown")
            filename = os.path.basename(full_source_path)
            content = highlight_text(res.get("text", ""), search_query)
            lang = html.escape(res.get("language", "und").upper())
            is_legal = res.get("legal_context", False)
            legal_badge = f"<span class='legal-tag'>LEGAL §</span>" if is_legal else ""

            # Result Card Container
            with st.container():
                # ENTERPRISE UX: Clear text labels for actions, consistent left alignment
                h_col1, h_col2, h_col3, _ = st.columns([0.2, 0.12, 0.12, 0.56], vertical_alignment="center")
                with h_col1:
                    st.markdown(f"<span class='lang-tag'>{lang}</span>{legal_badge}", unsafe_allow_html=True)
                with h_col2:
                    if st.button("📂 Open", key=f"q_open_{idx}", help="Open in Explorer"):
                        reveal_in_explorer(full_source_path)
                with h_col3:
                    if st.button("📋 Copy", key=f"q_copy_{idx}", help="Copy Path"):
                        st.toast("Path copied!", icon="📎")
                
                # CONTENT CARD (Strict Left)
                card_html = (
                    f'<div class="result-card" style="margin-top: -5px;">'
                    f'<div style="text-align: left; margin-bottom: 8px;"><small class="file-tag">FILE: {html.escape(filename)}</small></div>'
                    f'<div class="result-card-text">{content}</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
                
                # REMAINDER: Visual Preview (Left Aligned content)
                with st.expander(f"👁️ View Preview"):
                    p_col1, p_col2 = st.columns([1, 2])
                    with p_col1:
                        if filename.lower().endswith(".pdf"):
                            thumb_bytes = st.session_state.pipeline.generate_thumbnail(full_source_path)
                            if thumb_bytes: st.image(thumb_bytes, use_container_width=True)
                            else: st.info("Loading preview...")
                        else: st.warning("PDF only")
                    with p_col2:
                        st.markdown("**Local Source Path:**")
                        st.code(full_source_path, language="text")
                        st.caption("Engine: Ultra-Lite ONNX • Left-aligned grid V1.3")

st.divider()
st.caption("Wo ist meine Doku v1.3.2 — High-fidelity retrieval. 100% offline.")
