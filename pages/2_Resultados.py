from PIL import Image as _PIL_Image
_APP_ICON = _PIL_Image.open("assets/mascot.png")
import streamlit as st
import pandas as pd
from utils import db, style
from utils.triangulate import STATUS_LABELS, STATUS_COLORS

st.set_page_config(page_title="Resultados", page_icon=_APP_ICON, layout="wide")
style.apply()
st.title("📊 Resultados — Triangulación")

# ── Determinar fuente de datos ───────────────────────────────────────────────
run_id   = st.session_state.get("run_id")
results  = st.session_state.get("results")  # Fallback si no hay Supabase

if run_id and db.is_configured():
    raw = db.get_results(run_id)
    if raw:
        results = pd.DataFrame(raw).rename(columns={
            "ns_qty":  "ns_guayabal",
            "sho_qty": "sho_cedi",
        })

if results is None:
    st.warning("No hay resultados cargados. Ve a **Subir Archivos** para ejecutar una triangulación.")
    if st.button("➡️ Ir a Subir Archivos"):
        st.switch_page("pages/1_Upload.py")
    st.stop()

# ── Resumen de conteos ───────────────────────────────────────────────────────
counts = results["status"].value_counts().to_dict()
total  = len(results)

cols = st.columns(5)
metrics = [
    ("✅ OK",           "ok",          "#28a745"),
    ("⚠️ Stock oculto", "ns_mayor",    "#ffc107"),
    ("🔴 Sobreventa",   "sho_mayor",   "#dc3545"),
    ("❓ Sin match NS", "sin_match_ns","#6c757d"),
    ("📦 Sin publicar", "sin_match_sho","#17a2b8"),
]
for col, (label, key, _) in zip(cols, metrics):
    col.metric(label, f"{counts.get(key, 0):,}")

st.markdown("---")

# ── Tabs por tipo de anomalía ────────────────────────────────────────────────
tab_labels = [
    "⚠️ Stock oculto",
    "🔴 Sobreventa",
    "❓ Sin match NS",
    "📦 Sin publicar",
    "✅ OK",
    "Todos",
]
tabs = st.tabs(tab_labels)
status_keys = ["ns_mayor", "sho_mayor", "sin_match_ns", "sin_match_sho", "ok", None]

DISPLAY_COLS = {
    "sku":         "SKU",
    "nombre":      "Nombre",
    "subtipo":     "Subtipo",
    "ns_guayabal": "NS Guayabal",
    "sho_cedi":    "Shopify CEDI",
    "diff":        "Diferencia",
}

for tab, status_key in zip(tabs, status_keys):
    with tab:
        if status_key:
            subset = results[results["status"] == status_key]
            friendly = STATUS_LABELS.get(status_key, status_key)

            if status_key == "ns_mayor":
                st.info(
                    "**Stock oculto:** NetSuite registra unidades en GUAYABAL, "
                    "pero Shopify muestra 0. Productos que podrías estar vendiendo hoy.",
                    icon="⚠️",
                )
            elif status_key == "sho_mayor":
                st.error(
                    "**Sobreventa:** Shopify promete más stock del que existe en NetSuite. "
                    "Riesgo de cancelar pedidos.",
                    icon="🔴",
                )
            elif status_key == "sin_match_ns":
                st.warning(
                    "**Sin match en NetSuite:** SKUs en Shopify que no tienen contraparte en NetSuite. "
                    "Puede ser productos nuevos no dados de alta, o diferencia de formato.",
                    icon="❓",
                )
            elif status_key == "sin_match_sho":
                st.info(
                    "**Sin publicar:** Productos con stock físico en GUAYABAL que no están en Shopify. "
                    "Oportunidad de venta inmediata.",
                    icon="📦",
                )
        else:
            subset = results

        # Búsqueda
        search = st.text_input("🔍 Buscar SKU o nombre", key=f"search_{status_key}", placeholder="ej: SOFIA, 041080...")
        if search:
            mask = (
                subset["sku"].astype(str).str.contains(search, case=False, na=False)
                | subset["nombre"].astype(str).str.contains(search, case=False, na=False)
            )
            subset = subset[mask]

        if len(subset) == 0:
            st.success("Sin registros en esta categoría. ✅")
        else:
            # Columnas disponibles
            avail_cols = [c for c in DISPLAY_COLS if c in subset.columns]
            display = subset[avail_cols].rename(columns=DISPLAY_COLS)

            # Ordenar por diferencia absoluta
            if "Diferencia" in display.columns:
                display = display.reindex(
                    display["Diferencia"].abs().sort_values(ascending=False).index
                )

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True,
                height=min(600, max(200, len(display) * 36 + 40)),
            )

            st.caption(f"{len(subset):,} registros")
