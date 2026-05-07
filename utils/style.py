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

/* === CRISTANCHO SPLASH ANIMATIONS === */
@keyframes cri-blink  {{ 0%,100%{{opacity:1}} 50%{{opacity:0}} }}
@keyframes cri-slide  {{ from{{transform:translateX(60px);opacity:0}} to{{transform:translateX(0);opacity:1}} }}
@keyframes cri-drop   {{ from{{transform:translateY(-20px);opacity:0}} to{{transform:translateY(0);opacity:1}} }}
@keyframes cri-flicker{{ 0%,100%{{opacity:1}} 92%{{opacity:1}} 93%{{opacity:.7}} 95%{{opacity:1}} 97%{{opacity:.8}} }}
.cri-blink  {{ animation: cri-blink  1.1s step-start infinite; }}
.cri-mascot {{ animation: cri-slide  .5s  ease-out both; }}
.cri-title  {{ animation: cri-drop   .4s  ease-out both; }}
.cri-screen {{ animation: cri-flicker 6s  ease-in-out infinite; }}
</style>
"""



# ── SPLASH HEADER ─────────────────────────────────────────────────────────────

def _build_headers(b64: str):
    """Build header HTML strings at import time — avoids f-string/CSS brace conflicts."""
    img_tag = (
        '<img class="cri-mascot" '
        'src="data:image/png;base64,' + b64 + '" '
        'style="position:absolute;right:32px;bottom:0;height:280px;'
        'image-rendering:pixelated;z-index:3;'
        'filter:drop-shadow(0 0 22px rgba(255,200,0,.4)) '
        'drop-shadow(-6px 0 10px rgba(0,0,0,.95))" alt="Cristancho">'
    )
    img_small = (
        '<img src="data:image/png;base64,' + b64 + '" '
        'style="height:52px;image-rendering:pixelated;flex-shrink:0" alt="Cristancho">'
    )

    header = (
        '<div class="cri-screen" style="'
        'background:#111;'
        'background-image:'
        'repeating-linear-gradient(0deg,transparent,transparent 31px,#1A1A1A 31px,#1A1A1A 32px),'
        'repeating-linear-gradient(90deg,transparent,transparent 31px,#1A1A1A 31px,#1A1A1A 32px);'
        'border:4px solid #2A2A2A;box-shadow:inset 0 0 0 2px #333;'
        'position:relative;overflow:hidden;min-height:300px;'
        'display:flex;align-items:flex-end;margin-bottom:14px;">'

        '<div style="position:absolute;inset:0;pointer-events:none;z-index:2;'
        'background:repeating-linear-gradient('
        '180deg,transparent 0,transparent 3px,rgba(0,0,0,.18) 3px,rgba(0,0,0,.18) 4px)"></div>'

        '<div style="position:absolute;right:0;bottom:0;width:360px;height:360px;'
        'background:radial-gradient(ellipse at 60% 90%,rgba(255,200,0,.14) 0%,transparent 65%);'
        'pointer-events:none;z-index:0"></div>'

        '<div style="position:absolute;top:0;left:0;right:0;height:3px;'
        'background:linear-gradient(90deg,transparent,#FFD700 30%,#FFD700 70%,transparent);'
        'z-index:3;opacity:.4"></div>'
        + img_tag +

        '<div style="position:relative;z-index:4;padding:28px;">'

        '<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
        'color:#444;letter-spacing:3px;margin-bottom:12px">[ INVENTORY SYS v1.0 ]</div>'

        '<div class="cri-title" style="font-family:\'Press Start 2P\',monospace;font-size:34px;'
        'color:#FFD700;text-shadow:5px 5px #000,-2px -2px #8B6914;'
        'letter-spacing:4px;line-height:1.25;margin-bottom:16px">CRIS<br>TANCHO</div>'

        '<div style="font-family:VT323,monospace;font-size:19px;'
        'color:#7BC95E;letter-spacing:2px;margin-bottom:4px">&#9654; OPERADOR DE INVENTARIO</div>'

        '<div style="font-family:VT323,monospace;font-size:16px;'
        'color:#3A7A2A;letter-spacing:2px;margin-bottom:22px">CEDI GUAYABAL &middot; MONASTERY</div>'

        '<div style="font-family:\'Press Start 2P\',monospace;font-size:9px;'
        'color:#FFF;letter-spacing:2px">'
        '<span class="cri-blink">&#9632;</span> SUBE LOS ARCHIVOS PARA INICIAR'
        '</div></div></div>'
    )

    subheader_tpl = (
        '<div style="background:#2D2D2D;'
        'box-shadow:inset -4px -4px 0 #1A1A1A,inset 4px 4px 0 #4A4A4A;'
        'padding:10px 16px;display:flex;align-items:center;gap:14px;'
        'margin-bottom:14px;border-left:5px solid #FFD700;">'
        + img_small +
        '<div>'
        '<div style="font-family:\'Press Start 2P\',monospace;font-size:10px;'
        'color:#FFD700;text-shadow:2px 2px #000;letter-spacing:2px">CRISTANCHO</div>'
        '<div style="font-family:VT323,monospace;font-size:18px;'
        'color:#7BC95E;letter-spacing:1px;margin-top:3px">&#187; {subtitle}</div>'
        '</div></div>'
    )

    return header, subheader_tpl


_HEADER_HTML, _SUBHEADER_HTML_TPL = _build_headers(
    __import__('base64').b64encode(
        open(__import__('os').path.join(__import__('os').path.dirname(__file__),
             '..', 'assets', 'mascot.png'), 'rb').read()
    ).decode()
)



# ── Aplicar todo ──────────────────────────────────────────────────────────────
def apply():
    st.markdown(_FONTS, unsafe_allow_html=True)
    st.markdown(_CSS,   unsafe_allow_html=True)


def header(subtitle: str = ""):
    if subtitle:
        st.markdown(
            _SUBHEADER_HTML_TPL.format(subtitle=subtitle.upper()),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(_HEADER_HTML, unsafe_allow_html=True)


# ── Sección title ─────────────────────────────────────────────────────────────
def section_title(icon: str, text: str):
    st.markdown(
        f'<div style="font-family:\'Press Start 2P\',monospace;font-size:11px;'
        f'color:#7BC95E;text-shadow:2px 2px #000;margin:18px 0 10px;'
        f'letter-spacing:1px;border-left:4px solid #55A038;padding-left:10px;">'
        f'{icon} {text.upper()}</div>',
        unsafe_allow_html=True,
    )


# ── Slot card ─────────────────────────────────────────────────────────────────
def slot_card(icon: str, label: str, value, color: str = "#FFFFFF", sublabel: str = ""):
    sub = (f"<div style='font-family:VT323,monospace;font-size:14px;color:#777;"
           f"margin-top:4px'>{sublabel}</div>") if sublabel else ""
    st.markdown(
        f'<div style="background:#3C3C3C;'
        f'box-shadow:inset -3px -3px 0px #1E1E1E,inset 3px 3px 0px #5A5A5A;'
        f'padding:14px 16px;margin:4px 0;">'
        f'<div style="font-family:VT323,monospace;font-size:14px;color:#AAAAAA;">'
        f'{icon} {label.upper()}</div>'
        f'<div style="font-family:\'Press Start 2P\',monospace;font-size:20px;'
        f'color:{color};text-shadow:3px 3px #000;margin-top:6px">{value}</div>'
        f'{sub}</div>',
        unsafe_allow_html=True,
    )


# ── XP bar ────────────────────────────────────────────────────────────────────
def xp_bar(pct: float, label: str = "", color: str = "#55A038"):
    bar_w = min(max(pct, 0), 100)
    st.markdown(
        f'<div style="margin:8px 0">'
        f'<div style="font-family:VT323,monospace;font-size:15px;color:#AAAAAA;margin-bottom:3px">{label}</div>'
        f'<div style="background:#1E1E1E;box-shadow:inset 2px 2px 0px #111,inset -2px -2px 0px #333;'
        f'height:18px;position:relative;">'
        f'<div style="background:{color};width:{bar_w}%;height:100%;'
        f'box-shadow:inset -2px -2px 0px rgba(0,0,0,0.4),inset 2px 2px 0px rgba(255,255,255,0.15)"></div>'
        f'<div style="position:absolute;top:0;left:0;right:0;bottom:0;'
        f'font-family:VT323,monospace;font-size:14px;color:#FFF;'
        f'text-align:center;line-height:18px;text-shadow:1px 1px #000">{bar_w:.1f}%</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
