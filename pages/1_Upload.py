import streamlit as st
import pandas as pd
from datetime import datetime
from utils.parser import parse_netsuite, parse_shopify
from utils.triangulate import triangulate, summary_stats, STATUS_LABELS
from utils.export import export_triangulation, export_resurtido
from utils import db, style

st.set_page_config(page_title="Cristancho · Subir", page_icon="⛏️", layout="wide")
style.apply()
style.header("Subir Archivos — Nueva Triangulacion")

st.markdown('<div style="font-family:VT323,monospace;font-size:18px;color:#888;margin-bottom:16px">Sube los dos archivos para iniciar el cruce de inventario.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    style.section_title("📗", "NetSuite")
    st.caption("Inventario Disponible por Ubicacion - Digital")
    ns_file = st.file_uploader("Archivo NetSuite (.xls / .xlsx)", type=["xls","xlsx"], key="ns_up")
with col2:
    style.section_title("🛒", "Shopify")
    st.caption("Export de inventario · Admin → Inventario → Exportar")
    sho_file = st.file_uploader("Archivo Shopify (.xlsx)", type=["xlsx"], key="sho_up")

st.markdown("---")

if ns_file and sho_file:
    with st.spinner("Minando los datos..."):
        try:
            df_ns  = parse_netsuite(ns_file.read())
            df_sho = parse_shopify(sho_file.read())
            results, resurtido = triangulate(df_ns, df_sho)
            stats = summary_stats(results)
        except Exception as e:
            st.error(f"ERROR: {e}")
            st.stop()

    style.section_title("💎", "Resultados")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: style.slot_card("🗂","Total",    f"{stats['total']:,}")
    with c2: style.slot_card("✅","OK",       f"{stats['ok']:,}", color="#55FF55", sublabel=f"{stats['pct_ok']}%")
    with c3: style.slot_card("⚠","Oculto",   f"{stats['ns_mayor']:,}", color="#FFB800")
    with c4: style.slot_card("🔴","Sobreventa",f"{stats['sho_mayor']:,}", color="#FF5555")
    with c5: style.slot_card("?","Sin match", f"{stats['sin_ns']:,}", color="#AAAAAA")
    with c6: style.slot_card("📦","Resurtido", f"{len(resurtido):,}", color="#3EEBD0")

    st.markdown("<br>", unsafe_allow_html=True)
    style.xp_bar(stats["pct_ok"], "Sincronía del inventario", color="#55A038")

    run_id = db.save_run(ns_file.name, sho_file.name, results, resurtido)
    if run_id:
        st.success(f"Run guardado — ID: {run_id[:8]}...")
        st.session_state["run_id"] = run_id
    else:
        st.session_state["results"]   = results
        st.session_state["resurtido"] = resurtido
        st.info("Supabase no configurado — resultados en memoria.", icon="ℹ️")

    style.section_title("🗃", "Vista de discrepancias")
    label_to_key = {v: k for k, v in STATUS_LABELS.items()}
    status_filter = st.selectbox("Filtrar", ["Todos"] + list(STATUS_LABELS.values()))
    df_view = results.copy()
    if status_filter != "Todos":
        df_view = df_view[df_view["status"] == label_to_key[status_filter]]
    df_view["estado"] = df_view["status"].map(STATUS_LABELS)
    cols_show = [c for c in ["sku","nombre","subtipo","ns_guayabal","sho_cedi","diff","estado"] if c in df_view.columns]
    st.dataframe(df_view[cols_show].rename(columns={"sku":"SKU","nombre":"Nombre","subtipo":"Subtipo","ns_guayabal":"NS Guayabal","sho_cedi":"Shopify CEDI","diff":"Diferencia","estado":"Estado"}), use_container_width=True, hide_index=True, height=380)

    style.section_title("💾", "Descargar resultados")
    meta = {"ns_filename": ns_file.name, "sho_filename": sho_file.name, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")}
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button("📥  TRIANGULACION COMPLETA (.xlsx)", data=export_triangulation(results, meta), file_name=f"cristancho_tri_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with dl2:
        if len(resurtido):
            st.download_button(f"📦  ORDEN RESURTIDO — {len(resurtido)} SKUs (.xlsx)", data=export_resurtido(resurtido, meta), file_name=f"cristancho_resurtido_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        else:
            st.info("Sin SKUs para resurtido en este run.", icon="ℹ️")
else:
    st.markdown('<div style="font-family:VT323,monospace;font-size:20px;color:#55A038;border:3px dashed #3A3A3A;padding:28px;text-align:center;margin-top:16px">▲ Sube los dos archivos para iniciar la triangulacion</div>', unsafe_allow_html=True)
