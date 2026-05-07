import streamlit as st
import pandas as pd
from datetime import datetime
from utils import db, style
from utils.export import export_resurtido

st.set_page_config(page_title="Resurtido", page_icon="📦", layout="wide")
style.apply()
st.title("📦 Orden de Resurtido")
st.caption("Productos para transferir desde Bodega Principal o solicitar a Distribuidores → CEDI Guayabal")

# ── Obtener datos ────────────────────────────────────────────────────────────
run_id    = st.session_state.get("run_id")
resurtido = st.session_state.get("resurtido")

if run_id and db.is_configured():
    raw = db.get_resurtido_lines(run_id)
    if raw:
        resurtido = pd.DataFrame(raw).rename(columns={
            "qty_guayabal":      "ns_guayabal",
            "qty_principal":     "ns_principal",
            "qty_distribuidores":"ns_distribuidores",
        })

if resurtido is None or (isinstance(resurtido, pd.DataFrame) and len(resurtido) == 0):
    st.info("No hay datos de resurtido. Ejecuta una triangulación primero.", icon="📎")
    if st.button("➡️ Ir a Subir Archivos"):
        st.switch_page("pages/1_Upload.py")
    st.stop()

# ── Métricas ─────────────────────────────────────────────────────────────────
from_principal    = resurtido[resurtido["fuente"] == "PRINCIPAL"]
from_distribuidores = resurtido[resurtido["fuente"] == "DISTRIBUIDORES"]

c1, c2, c3 = st.columns(3)
c1.metric("Total SKUs a resurtir",          f"{len(resurtido):,}")
c2.metric("🏭 Desde Bodega Principal",       f"{len(from_principal):,}",
          delta=f"{int(from_principal['qty_sugerida'].sum()):,} unidades")
c3.metric("🚚 Desde Distribuidores",         f"{len(from_distribuidores):,}",
          delta=f"{int(from_distribuidores['qty_sugerida'].sum()):,} unidades")

st.markdown("---")

# ── Filtros ──────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([2, 1, 1])

with col_f1:
    search = st.text_input("🔍 Buscar por SKU o nombre", placeholder="ej: CAP, 600001...")

with col_f2:
    fuente_filter = st.selectbox("Fuente", ["Todas", "PRINCIPAL", "DISTRIBUIDORES"])

with col_f3:
    min_qty = st.number_input("Cantidad mínima sugerida", min_value=0, value=0, step=1)

# Aplicar filtros
df_view = resurtido.copy()

if search:
    mask = (
        df_view["sku"].astype(str).str.contains(search, case=False, na=False)
        | df_view["nombre"].astype(str).str.contains(search, case=False, na=False)
    )
    df_view = df_view[mask]

if fuente_filter != "Todas":
    df_view = df_view[df_view["fuente"] == fuente_filter]

if min_qty > 0:
    df_view = df_view[df_view["qty_sugerida"] >= min_qty]

df_view = df_view.sort_values("qty_sugerida", ascending=False)

# ── Tabla ────────────────────────────────────────────────────────────────────
st.subheader(f"SKUs para resurtir ({len(df_view):,})")

display_cols = {
    "sku":               "SKU",
    "nombre":            "Nombre",
    "subtipo":           "Subtipo",
    "ns_guayabal":       "Stock CEDI actual",
    "ns_principal":      "Disponible Principal",
    "ns_distribuidores": "Disponible Distribuidor",
    "qty_sugerida":      "Qty sugerida",
    "fuente":            "Fuente",
}
avail = [c for c in display_cols if c in df_view.columns]
st.dataframe(
    df_view[avail].rename(columns=display_cols),
    use_container_width=True,
    hide_index=True,
    height=450,
    column_config={
        "Qty sugerida": st.column_config.NumberColumn(format="%d"),
        "Stock CEDI actual": st.column_config.NumberColumn(format="%d"),
        "Disponible Principal": st.column_config.NumberColumn(format="%d"),
        "Disponible Distribuidor": st.column_config.NumberColumn(format="%d"),
    }
)

# ── Descarga ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Generar orden de resurtido")

col_d1, col_d2 = st.columns([2, 1])
with col_d1:
    st.write(
        "Descarga el Excel listo para entregar a Bodega o Distribuidores. "
        "El archivo incluye SKU, nombre, cantidades disponibles y origen recomendado."
    )
with col_d2:
    meta = {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M")}
    excel_bytes = export_resurtido(df_view if len(df_view) < len(resurtido) else resurtido, meta)
    st.download_button(
        label=f"📥 Descargar orden ({len(df_view):,} SKUs)",
        data=excel_bytes,
        file_name=f"resurtido_CEDI_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
