import os as _os
from PIL import Image as _PIL_Image
_APP_ICON = _PIL_Image.open(_os.path.join(_os.path.dirname(__file__), "assets", "mascot.png"))

import streamlit as st
import pandas as pd
from utils import db
from utils import style

st.set_page_config(
    page_title="Cristancho",
    page_icon=_APP_ICON,
    layout="wide",
)
style.apply()
style.header()

if not db.is_configured():
    st.info(
        "**Modo sin historial** — Supabase no configurado. "
        "Agrega SUPABASE_URL y SUPABASE_KEY en .env para activar el historial.",
        icon="ℹ️",
    )

runs = db.get_runs(limit=1)

style.section_title("📦", "Estado del inventario")

if not runs:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            '<div style="font-family:VT323,monospace;font-size:20px;color:#AAAAAA">'
            'Sin runs previos. Sube los archivos para iniciar la primera triangulación.'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("▶  SUBIR ARCHIVOS", use_container_width=True):
            st.switch_page("pages/1_Upload.py")
else:
    last = runs[0]
    st.caption(
        f"📅 {last['created_at'][:19].replace('T',' ')}  ·  "
        f"NS: {last['ns_filename']}  ·  SHO: {last['sho_filename']}"
    )

    total = last["total_skus"] or 1
    pct_ok = round(last["ok_count"] / total * 100, 1)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: style.slot_card("🗂", "Total SKUs",   f"{last['total_skus']:,}")
    with c2: style.slot_card("✅", "OK",           f"{last['ok_count']:,}",        color="#55FF55")
    with c3: style.slot_card("⚠️", "Stock oculto", f"{last['ns_mayor_count']:,}",  color="#FFB800")
    with c4: style.slot_card("🔴", "Sobreventa",   f"{last['sho_mayor_count']:,}", color="#FF5555")
    with c5: style.slot_card("📦", "Resurtido",    f"{last['resurtido_count']:,}", color="#3EEBD0")

    st.markdown("<br>", unsafe_allow_html=True)
    style.xp_bar(pct_ok, label="Salud del inventario (% SKUs sincronizados)", color="#55A038")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⛏  NUEVO RUN", use_container_width=True):
            st.switch_page("pages/1_Upload.py")
    with col_b:
        if st.button("📊  VER RESULTADOS", use_container_width=True):
            st.session_state["run_id"] = last["id"]
            st.switch_page("pages/2_Resultados.py")

all_runs = db.get_runs(limit=8)
if len(all_runs) > 1:
    style.section_title("📜", "Historial reciente")
    df_hist = pd.DataFrame(all_runs)[[
        "created_at", "ns_filename", "total_skus",
        "ok_count", "ns_mayor_count", "sho_mayor_count", "resurtido_count"
    ]].rename(columns={
        "created_at": "Fecha", "ns_filename": "Archivo NS",
        "total_skus": "Total", "ok_count": "OK",
        "ns_mayor_count": "Stock oculto",
        "sho_mayor_count": "Sobreventa", "resurtido_count": "Resurtido",
    })
    df_hist["Fecha"] = df_hist["Fecha"].str[:19].str.replace("T", " ")
    st.dataframe(df_hist, use_container_width=True, hide_index=True)