import streamlit as st
import pandas as pd
from datetime import datetime
from utils.parser import parse_netsuite, parse_shopify
from utils.triangulate import triangulate, summary_stats, STATUS_LABELS
from utils.export import export_triangulation, export_resurtido
from utils import db

st.set_page_config(page_title="Subir Archivos", page_icon="⬆️", layout="wide")
st.title("⬆️ Subir Archivos — Nueva Triangulación")

st.markdown(
    "Sube los dos archivos para iniciar el cruce. "
    "Los resultados se mostrarán de inmediato en esta página."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("NetSuite")
    st.caption("Reporte: **Inventario Disponible por Ubicación - Digital**")
    ns_file = st.file_uploader(
        "Archivo NetSuite (.xls / .xlsx)",
        type=["xls", "xlsx"],
        key="ns_upload",
    )

with col2:
    st.subheader("Shopify")
    st.caption("Export de inventario desde Shopify Admin → Inventario → Exportar")
    sho_file = st.file_uploader(
        "Archivo Shopify (.xlsx)",
        type=["xlsx"],
        key="sho_upload",
    )

st.markdown("---")

if ns_file and sho_file:
    with st.spinner("Leyendo archivos y ejecutando triangulación..."):
        try:
            df_ns  = parse_netsuite(ns_file.read())
            df_sho = parse_shopify(sho_file.read())
            results, resurtido = triangulate(df_ns, df_sho)
            stats = summary_stats(results)
        except Exception as e:
            st.error(f"❌ Error al procesar los archivos: {e}")
            st.stop()

    # ── Métricas resumen ─────────────────────────────────────────────────────
    st.subheader("Resultados de la triangulación")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total SKUs",        f"{stats['total']:,}")
    c2.metric("✅ OK",             f"{stats['ok']:,}",
              delta=f"{stats['pct_ok']}%")
    c3.metric("⚠️ Stock oculto",   f"{stats['ns_mayor']:,}", delta_color="inverse")
    c4.metric("🔴 Sobreventa",     f"{stats['sho_mayor']:,}", delta_color="inverse")
    c5.metric("❓ Sin match NS",   f"{stats['sin_ns']:,}",  delta_color="off")
    c6.metric("📦 Resurtido",      f"{len(resurtido):,}",   delta_color="off")

    # ── Guardar en Supabase ──────────────────────────────────────────────────
    run_id = db.save_run(ns_file.name, sho_file.name, results, resurtido)
    if run_id:
        st.success(f"✅ Run guardado en historial (ID: `{run_id[:8]}...`)")
        st.session_state["run_id"] = run_id
    else:
        st.session_state["results"]  = results
        st.session_state["resurtido"] = resurtido
        st.info("Supabase no configurado — resultados en memoria de esta sesión.", icon="ℹ️")

    # ── Tabla de discrepancias ───────────────────────────────────────────────
    st.markdown("### Vista rápida de discrepancias")

    status_filter = st.selectbox(
        "Filtrar por estado",
        options=["Todos"] + list(STATUS_LABELS.values()),
        index=0,
    )

    label_to_key = {v: k for k, v in STATUS_LABELS.items()}
    df_view = results.copy()
    if status_filter != "Todos":
        df_view = df_view[df_view["status"] == label_to_key[status_filter]]

    df_view["status_label"] = df_view["status"].map(STATUS_LABELS)
    df_display = df_view[[
        "sku", "nombre", "subtipo", "ns_guayabal", "sho_cedi", "diff", "status_label"
    ]].rename(columns={
        "sku":          "SKU",
        "nombre":       "Nombre",
        "subtipo":      "Subtipo",
        "ns_guayabal":  "NS Guayabal",
        "sho_cedi":     "Shopify CEDI",
        "diff":         "Diferencia",
        "status_label": "Estado",
    })

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=400,
    )

    # ── Descargas ────────────────────────────────────────────────────────────
    st.markdown("### Descargar resultados")
    meta = {
        "ns_filename":  ns_file.name,
        "sho_filename": sho_file.name,
        "fecha":        datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    dl1, dl2 = st.columns(2)
    with dl1:
        excel_tri = export_triangulation(results, meta)
        st.download_button(
            label="📥 Descargar triangulación completa (.xlsx)",
            data=excel_tri,
            file_name=f"triangulacion_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with dl2:
        if len(resurtido) > 0:
            excel_res = export_resurtido(resurtido, meta)
            st.download_button(
                label=f"📦 Descargar orden de resurtido ({len(resurtido)} SKUs) (.xlsx)",
                data=excel_res,
                file_name=f"resurtido_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        else:
            st.info("No hay SKUs para resurtido en este run.", icon="ℹ️")

else:
    st.info("👆 Sube los dos archivos para iniciar la triangulación.", icon="📎")
