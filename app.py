import streamlit as st
import pandas as pd
from utils import db

st.set_page_config(
    page_title="Inventario CEDI Guayabal",
    page_icon="📦",
    layout="wide",
)

st.title("📦 Triangulación de Inventario — CEDI Guayabal")
st.caption("Sistema de cruce NetSuite · Shopify | Módulos: Triangulación + Resurtido")

if not db.is_configured():
    st.info(
        "**Modo sin historial** — Supabase no está configurado. "
        "El sistema funciona, pero los resultados no se guardarán entre sesiones. "
        "Agrega `SUPABASE_URL` y `SUPABASE_KEY` en `.env` para activar el historial.",
        icon="ℹ️",
    )

# ── Resumen del último run ───────────────────────────────────────────────────
runs = db.get_runs(limit=1)

if not runs:
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Sin runs previos")
        st.write("Ve a **Subir Archivos** para hacer tu primera triangulación.")
    with col2:
        if st.button("➡️ Ir a Subir Archivos", use_container_width=True):
            st.switch_page("pages/1_Upload.py")
else:
    last = runs[0]
    st.markdown("### Último run")
    st.caption(f"📅 {last['created_at'][:19].replace('T',' ')}  |  "
               f"NS: `{last['ns_filename']}`  |  SHO: `{last['sho_filename']}`")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total SKUs",       f"{last['total_skus']:,}")
    col2.metric("✅ OK",            f"{last['ok_count']:,}",
                delta=f"{last['ok_count']/last['total_skus']*100:.1f}%")
    col3.metric("⚠️ Stock oculto",  f"{last['ns_mayor_count']:,}", delta_color="inverse")
    col4.metric("🔴 Sobreventa",    f"{last['sho_mayor_count']:,}", delta_color="inverse")
    col5.metric("📦 Resurtido",     f"{last['resurtido_count']:,}", delta_color="off")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Nuevo run", use_container_width=True):
            st.switch_page("pages/1_Upload.py")
    with col_b:
        if st.button("📊 Ver resultados del último run", use_container_width=True):
            st.session_state["run_id"] = last["id"]
            st.switch_page("pages/2_Resultados.py")

# ── Historial resumido ───────────────────────────────────────────────────────
all_runs = db.get_runs(limit=10)
if len(all_runs) > 1:
    st.markdown("### Historial reciente")
    df_hist = pd.DataFrame(all_runs)[
        ["created_at", "ns_filename", "total_skus", "ok_count",
         "ns_mayor_count", "sho_mayor_count", "resurtido_count"]
    ].rename(columns={
        "created_at":      "Fecha",
        "ns_filename":     "Archivo NS",
        "total_skus":      "Total SKUs",
        "ok_count":        "OK",
        "ns_mayor_count":  "Stock oculto",
        "sho_mayor_count": "Sobreventa",
        "resurtido_count": "Resurtido",
    })
    df_hist["Fecha"] = df_hist["Fecha"].str[:19].str.replace("T", " ")
    st.dataframe(df_hist, use_container_width=True, hide_index=True)
