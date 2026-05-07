"""
Cristancho — Minecraft UI skin
Inyecta el CSS y provee helpers visuales para todas las páginas.
"""
import streamlit as st

# ── Fuentes ──────────────────────────────────────────────────────────────────
_FONTS = """
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
"""

# ── Paleta Minecraft ─────────────────────────────────────────────────────────
C = {
    "grass":       "#55A038",
    "grass_light": "#7BC95E",
    "stone":       "#8B8B8B",
    "stone_dark":  "#3A3A3A",
    "stone_light": "#C8C8C8",
    "dirt":        "#866043",
    "wood":        "#A0782A",
    "diamond":     "#3EEBD0",
    "gold":        "#FFB800",
    "redstone":    "#FF3030",
    "lapis":       "#4A6FE3",
    "bg":          "#1A1A1A",
    "bg2":         "#2D2D2D",
    "bg3":         "#3C3C3C",
    "text":        "#FFFFFF",
    "text_dim":    "#AAAAAA",
}

# ── CSS principal ─────────────────────────────────────────────────────────────
_CSS = f"""
<style>
/* === BASE === */
html, body, [class*="css"], p, span, div, td, th, label {{
    font-family: 'VT323', monospace !important;
    font-size: 17px !important;
    letter-spacing: 0.5px;
}}

/* === HEADINGS === */
h1, h2, h3, h4, .stTitle {{
    font-family: 'Press Start 2P', monospace !important;
    text-shadow: 3px 3px #000000 !important;
    line-height: 1.6 !important;
    letter-spacing: 1px;
}}
h1 {{ font-size: 18px !important; color: {C['grass_light']} !important; }}
h2 {{ font-size: 13px !important; color: #FFFFFF !important; }}
h3 {{ font-size: 11px !important; color: {C['text_dim']} !important; }}

/* === BUTTONS === */
.stButton > button,
button[kind="primary"],
button[kind="secondary"] {{
    font-family: 'VT323', monospace !important;
    font-size: 20px !important;
    background-color: {C['stone']} !important;
    color: #FFFFFF !important;
    text-shadow: 2px 2px #000 !important;
    border-radius: 0 !important;
    border: none !important;
    box-shadow:
        inset -4px -4px 0px {C['stone_dark']},
        inset  4px  4px 0px {C['stone_light']} !important;
    padding: 8px 18px !important;
    min-height: 42px !important;
    transition: none !important;
}}
.stButton > button:hover {{
    background-color: #9E9E9E !important;
    filter: brightness(1.15) !important;
    box-shadow:
        inset -4px -4px 0px #2A2A2A,
        inset  4px  4px 0px #D8D8D8 !important;
}}
.stButton > button:active {{
    box-shadow:
        inset  4px  4px 0px {C['stone_dark']},
        inset -4px -4px 0px {C['stone_light']} !important;
}}

/* === DOWNLOAD BUTTONS === */
[data-testid="stDownloadButton"] > button {{
    font-family: 'VT323', monospace !important;
    font-size: 20px !important;
    background-color: #1E5C1E !important;
    color: #FFFFFF !important;
    border-radius: 0 !important;
    border: none !important;
    box-shadow:
        inset -4px -4px 0px #0D3A0D,
        inset  4px  4px 0px #3A9A3A !important;
    text-shadow: 2px 2px #000 !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
    background-color: #2A7A2A !important;
    filter: brightness(1.2) !important;
}}

/* === METRICS (inventory slots) === */
[data-testid="metric-container"] {{
    background: {C['bg3']} !important;
    border-radius: 0 !important;
    box-shadow:
        inset -3px -3px 0px #1E1E1E,
        inset  3px  3px 0px #5A5A5A !important;
    padding: 12px 14px !important;
}}
[data-testid="stMetricLabel"] {{
    font-family: 'VT323', monospace !important;
    font-size: 15px !important;
    color: {C['text_dim']} !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Press Start 2P', monospace !important;
    font-size: 18px !important;
    text-shadow: 2px 2px #000 !important;
}}
[data-testid="stMetricDelta"] {{
    font-family: 'VT323', monospace !important;
    font-size: 15px !important;
}}

/* === FILE UPLOADER === */
[data-testid="stFileUploader"] {{
    background: {C['bg2']} !important;
    border: 3px dashed {C['grass']} !important;
    border-radius: 0 !important;
    padding: 8px !important;
}}
[data-testid="stFileUploader"] label {{
    font-family: 'VT323', monospace !important;
    font-size: 17px !important;
    color: {C['text_dim']} !important;
}}

/* === TEXT INPUT === */
input[type="text"], input[type="number"], textarea {{
    border-radius: 0 !important;
    background: {C['bg2']} !important;
    border: 2px solid {C['grass']} !important;
    color: #FFFFFF !important;
    font-family: 'VT323', monospace !important;
    font-size: 17px !important;
}}

/* === SELECTBOX === */
[data-testid="stSelectbox"] > div > div {{
    border-radius: 0 !important;
    background: {C['bg2']} !important;
    border: 2px solid {C['grass']} !important;
    font-family: 'VT323', monospace !important;
    font-size: 17px !important;
}}

/* === TABS === */
[data-baseweb="tab-list"] {{
    background: {C['bg2']} !important;
    border-bottom: 3px solid {C['stone_dark']} !important;
    gap: 0 !important;
}}
[data-baseweb="tab"] {{
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    border-radius: 0 !important;
    background: {C['bg3']} !important;
    color: {C['text_dim']} !important;
    border: none !important;
    padding: 8px 16px !important;
    box-shadow: inset -2px -2px 0px #1E1E1E, inset 2px 2px 0px #5A5A5A !important;
}}
[data-baseweb="tab"][aria-selected="true"] {{
    background: {C['bg']} !important;
    color: {C['grass_light']} !important;
    box-shadow: none !important;
    border-bottom: 3px solid {C['grass']} !important;
}}

/* === ALERTS === */
[data-testid="stAlert"] {{
    border-radius: 0 !important;
    border-left-width: 5px !important;
    font-family: 'VT323', monospace !important;
    font-size: 17px !important;
}}

/* === DATAFRAME === */
[data-testid="stDataFrame"] > div {{
    border: 2px solid {C['stone_dark']} !important;
    border-radius: 0 !important;
}}
[data-testid="stDataFrame"] th {{
    background: {C['bg2']} !important;
    font-family: 'VT323', monospace !important;
    font-size: 16px !important;
    color: {C['grass_light']} !important;
    border-bottom: 2px solid {C['grass']} !important;
}}
[data-testid="stDataFrame"] td {{
    font-family: 'VT323', monospace !important;
    font-size: 16px !important;
    background: {C['bg3']} !important;
}}

/* === SPINNER === */
[data-testid="stSpinner"] p {{
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    color: {C['grass']} !important;
}}

/* === SIDEBAR === */
[data-testid="stSidebar"] {{
    background: #111111 !important;
    border-right: 4px solid {C['stone_dark']} !important;
}}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    border-radius: 0 !important;
    letter-spacing: 1px;
}}
[data-testid="stSidebarNavSeparator"] {{
    border-color: {C['stone_dark']} !important;
}}

/* === DIVIDERS === */
hr {{
    border: none !important;
    height: 4px !important;
    background: repeating-linear-gradient(
        90deg,
        {C['stone_dark']} 0px, {C['stone_dark']} 8px,
        {C['bg']}   8px,  {C['bg']}  16px
    ) !important;
    margin: 1rem 0 !important;
}}

/* === MAIN CONTAINER === */
.block-container {{
    padding-top: 1rem !important;
    max-width: 1100px !important;
}}

/* === CAPTION === */
[data-testid="stCaptionContainer"] p {{
    font-family: 'VT323', monospace !important;
    font-size: 15px !important;
    color: {C['text_dim']} !important;
}}

/* === NUMBER INPUT ARROWS === */
[data-testid="stNumberInput"] input {{
    border-radius: 0 !important;
}}
[data-testid="stNumberInput"] button {{
    border-radius: 0 !important;
    background: {C['bg3']} !important;
    border: none !important;
    box-shadow: inset -2px -2px 0px #1E1E1E, inset 2px 2px 0px #5A5A5A !important;
}}
</style>
"""

# ── ASCII / Header art ────────────────────────────────────────────────────────
_HEADER_HTML = """
<div style="padding: 16px 0 8px;">
  <div style="
      font-family: 'Press Start 2P', monospace;
      font-size: 22px;
      color: #7BC95E;
      text-shadow: 4px 4px #000000;
      letter-spacing: 3px;
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
  ">
    &#9935;&#65039; CRISTANCHO
  </div>
  <div style="
      font-family: 'VT323', monospace;
      font-size: 17px;
      color: #888;
      letter-spacing: 2px;
      margin-top: 6px;
  ">
    ▶ TRIANGULACION DE INVENTARIO · CEDI GUAYABAL
  </div>
</div>
"""

# ── Slot card (imita un inventario de Minecraft) ──────────────────────────────
def slot_card(icon: str, label: str, value, color: str = "#FFFFFF", sublabel: str = ""):
    """Renders an inventory-slot-style metric card."""
    st.markdown(f"""
    <div style="
        background: #3C3C3C;
        box-shadow: inset -3px -3px 0px #1E1E1E, inset 3px 3px 0px #5A5A5A;
        padding: 14px 16px;
        margin: 4px 0;
        position: relative;
    ">
        <div style="font-family:VT323,monospace;font-size:14px;color:#AAAAAA;letter-spacing:1px">{icon} {label.upper()}</div>
        <div style="font-family:'Press Start 2P',monospace;font-size:20px;color:{color};text-shadow:3px 3px #000;margin-top:6px">{value}</div>
        {"<div style='font-family:VT323,monospace;font-size:14px;color:#777;margin-top:4px'>" + sublabel + "</div>" if sublabel else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Status badge ─────────────────────────────────────────────────────────────
STATUS_BADGE_STYLES = {
    "ok":           ("✔", "#55FF55", "#1E4A1E", "#2A8A2A"),
    "ns_mayor":     ("⚠", "#FFB800", "#3A2A00", "#9A7000"),
    "sho_mayor":    ("✖", "#FF5555", "#4A1A1A", "#9A2A2A"),
    "sin_match_ns": ("?", "#AAAAAA", "#2A2A2A", "#666666"),
    "sin_match_sho":("◉", "#55AAFF", "#1A1A3A", "#3A4A8A"),
}

def status_html(status: str) -> str:
    icon, fg, bg, border = STATUS_BADGE_STYLES.get(status, ("?","#FFF","#333","#666"))
    return (
        f'<span style="background:{bg};color:{fg};'
        f'border:2px solid {border};'
        f'font-family:VT323,monospace;font-size:16px;'
        f'padding:1px 8px;white-space:nowrap">{icon}</span>'
    )


# ── Barra XP / salud ──────────────────────────────────────────────────────────
def xp_bar(pct: float, label: str = "", color: str = "#55A038"):
    """Renders a Minecraft-style XP/health bar."""
    bar_w = min(max(pct, 0), 100)
    st.markdown(f"""
    <div style="margin:8px 0">
        <div style="font-family:VT323,monospace;font-size:15px;color:#AAAAAA;margin-bottom:3px">{label}</div>
        <div style="background:#1E1E1E;box-shadow:inset 2px 2px 0px #111,inset -2px -2px 0px #333;height:18px;position:relative">
            <div style="background:{color};width:{bar_w}%;height:100%;
                        box-shadow:inset -2px -2px 0px rgba(0,0,0,0.4),inset 2px 2px 0px rgba(255,255,255,0.15)">
            </div>
            <div style="position:absolute;top:0;left:0;right:0;bottom:0;
                        font-family:VT323,monospace;font-size:14px;color:#FFF;
                        text-align:center;line-height:18px;text-shadow:1px 1px #000">
                {bar_w:.1f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Sección title ─────────────────────────────────────────────────────────────
def section_title(icon: str, text: str):
    st.markdown(f"""
    <div style="
        font-family:'Press Start 2P',monospace;
        font-size:11px;
        color:#7BC95E;
        text-shadow:2px 2px #000;
        margin:18px 0 10px;
        letter-spacing:1px;
        border-left:4px solid #55A038;
        padding-left:10px;
    ">{icon} {text.upper()}</div>
    """, unsafe_allow_html=True)


# ── Aplicar todo ──────────────────────────────────────────────────────────────
def apply():
    """Llamar al inicio de cada página."""
    st.markdown(_FONTS, unsafe_allow_html=True)
    st.markdown(_CSS,   unsafe_allow_html=True)


def header(subtitle: str = ""):
    """Renderiza el logo CRISTANCHO."""
    st.markdown(_HEADER_HTML, unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f'<div style="font-family:VT323,monospace;font-size:19px;'
            f'color:#888;margin-bottom:12px;letter-spacing:1px">» {subtitle}</div>',
            unsafe_allow_html=True,
        )
