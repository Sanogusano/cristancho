import streamlit as st
import pandas as pd
from utils import db, style

st.set_page_config(page_title="Historial", page_icon="📈", layout="wide")
style.apply()
st.title("📈 Historial de Runs")

if not db.is_configured():
    st.warning(
        "Historial no disponible sin Supabase. "
        "Configura `SUPABASE_URL` y `SUPABASE_KEY` en `.env` para activar esta función.",
        icon="⚠️",
    )
    st.stop()

runs = db.get_runs(limit=30)

if not runs:
    st.info("No hay runs guardados todavía. Ve a **Subir Archivos** para crear el primero.")
    st.stop()

df = pd.DataFrame(runs)
df["fecha"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d %H:%M")
df["pct_ok"] = (df["ok_count"] / df["total_skus"] * 100).round(1)

# ── Métricas del run más reciente vs anterior ────────────────────────────────
if len(df) >= 2:
    curr, prev = df.iloc[0], df.iloc[1]
    st.subheader("Comparación: último run vs anterior")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total SKUs",    f"{curr['total_skus']:,}", delta=int(curr['total_skus'] - prev['total_skus']))
    c2.metric("% OK",          f"{curr['pct_ok']}%",   delta=f"{curr['pct_ok']-prev['pct_ok']:.1f}%")
    c3.metric("Stock oculto",  f"{curr['ns_mayor_count']:,}", delta=int(curr['ns_mayor_count']-prev['ns_mayor_count']), delta_color="inverse")
    c4.metric("Sobreventa",    f"{curr['sho_mayor_count']:,}", delta=int(curr['sho_mayor_count']-prev['sho_mayor_count']), delta_color="inverse")
    st.markdown("---")

# ── Gráfica de tendencia ─────────────────────────────────────────────────────
st.subheader("Tendencia de discrepancias")

df_chart = df[["fecha", "ok_count", "ns_mayor_count", "sho_mayor_count", "resurtido_count"]].copy()
df_chart = df_chart.sort_values("fecha")
df_chart = df_chart.rename(columns={
    "ok_count":        "OK",
    "ns_mayor_count":  "Stock oculto",
    "sho_mayor_count": "Sobreventa",
    "resurtido_count": "Resurtido",
}).set_index("fecha")

st.line_chart(df_chart[["Stock oculto", "Sobreventa"]], use_container_width=True, height=250)

# ── Tabla de todos los runs ──────────────────────────────────────────────────
st.subheader("Todos los runs")

df_table = df[[
    "fecha", "ns_filename", "total_skus",
    "ok_count", "ns_mayor_count", "sho_mayor_count", "resurtido_count", "id"
]].rename(columns={
    "fecha":           "Fecha",
    "ns_filename":     "Archivo NS",
    "total_skus":      "Total",
    "ok_count":        "OK",
    "ns_mayor_count":  "Stock oculto",
    "sho_mayor_count": "Sobreventa",
    "resurtido_count": "Resurtido",
    "id":              "Run ID",
})

st.dataframe(df_table, use_container_width=True, hide_index=True)

# ── Cargar un run histórico ──────────────────────────────────────────────────
st.markdown("---")
st.subheader("Cargar run histórico")

run_options = {f"{r['created_at'][:19].replace('T',' ')} — {r['ns_filename']}": r["id"] for r in runs}
selected_label = st.selectbox("Seleccionar run", options=list(run_options.keys()))

if st.button("📊 Ver resultados de este run", use_container_width=False):
    st.session_state["run_id"] = run_options[selected_label]
    st.switch_page("pages/2_Resultados.py")
