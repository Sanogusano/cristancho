import os as _os
from PIL import Image as _PIL_Image
_APP_ICON = _PIL_Image.open(_os.path.join(_os.path.dirname(__file__), '..', 'assets', 'mascot.png'))

import io
import streamlit as st
import pandas as pd
from utils import style
from utils.parser import parse_netsuite

st.set_page_config(page_title="Cristancho · Sincronizar", page_icon=_APP_ICON, layout="wide")
style.apply()
style.header("Sincronizar Shopify — Todas las Tiendas")

# ── Mapeo NetSuite → Shopify ──────────────────────────────────────────────────
LOCATION_MAP = {
    "OFICINA : GUAYABAL":                                   "Inventory Available: CEDI Guayabal",
    "TIENDAS FISICAS : SHOWROOM NUEVO":                     "Inventory Available: Showroom",
    "TIENDAS FISICAS : MST ANDINO BOGOTÁ":                  "Inventory Available: Tienda Andino",
    "TIENDAS FISICAS : MST PLAZA BOCAGRANDE":               "Inventory Available: Tienda Bocagrande Cartagena",
    "TIENDAS FISICAS : MST BUENA VISTA BARRANQUILLA":       "Inventory Available: Tienda Buenavista",
    "TIENDAS FISICAS : MST ALAMEDAS MONTERIA":              "Inventory Available: Tienda C.C. Alamedas",
    "TIENDAS FISICAS : MST TESORO":                         "Inventory Available: Tienda C.C. El Tesoro",
    "TIENDAS FISICAS : MST TESORO MULTIMARCA":              "Inventory Available: Tienda C.C. El Tesoro | Multimarca",
    "TIENDAS FISICAS : MST LOS MOLINOS":                    "Inventory Available: Tienda C.C. Molinos",
    "TIENDAS FISICAS : MST FABRICATO BELLO":                "Inventory Available: Tienda C.C. Parque Fabricato",
    "TIENDAS FISICAS : MST PRIMAVERA URBANA VILLAVICENCIO": "Inventory Available: Tienda C.C. Primavera Urbana",
    "TIENDAS FISICAS : MST SANTA FE MED":                   "Inventory Available: Tienda C.C. Santa Fé - Medellín",
    "TIENDAS FISICAS : MTS GRAN ESTACION NUEVA":            "Inventory Available: Tienda Gran Estacion",
    "TIENDAS FISICAS : MST IPIALES":                        "Inventory Available: Tienda Ipiales",
    "TIENDAS FISICAS : MST JARDÍN PLAZA CÚCUTA":            "Inventory Available: Tienda Jardin Plaza",
    "TIENDAS FISICAS : MTS93 NUEVA":                        "Inventory Available: Tienda la 93",
    "TIENDAS FISICAS : MST OVIEDO MEDELLIN":                "Inventory Available: Tienda Oviedo",
    "TIENDAS FISICAS : MST COLINA":                         "Inventory Available: Tienda Parque Colina",
    "TIENDAS FISICAS : MST UNI PASTO":                      "Inventory Available: Tienda Pasto",
    "TIENDAS FISICAS : MST PITALITO HUILA":                 "Inventory Available: Tienda Pitalito",
    "TIENDAS FISICAS : MST SAN NICOLAS":                    "Inventory Available: Tienda San Nicolas",
    "TIENDAS FISICAS : MST SERREZUELA CARTAGENA":           "Inventory Available: Tienda Serrezuela",
    "TIENDAS FISICAS : MST SOPO NUEVA":                     "Inventory Available: Tienda Sopo",
    "TIENDAS FISICAS : MST UNICO CALI":                     "Inventory Available: Tienda Unico Cali",
    "TIENDAS FISICAS : VENTURA PLAZA CUCUTA":               "Inventory Available: Tienda Ventura Plaza",
    "TIENDAS FISICAS : MST VIVA BARRANQUILLA":              "Inventory Available: Tienda Viva Barranquilla",
    "TIENDAS FISICAS : MST VIVA ENVIGADO":                  "Inventory Available: Tienda Viva Envigado",
    "TIENDAS FISICAS : MST VIVA RIOHACHA":                  "Inventory Available: Tienda Viva Wajiira",
    "TIENDAS FISICAS : MST UNICO BARRANQUILLA":             "Inventory Available: Tienda Único Barranquilla",
}


def parse_netsuite_all_locations(file_bytes: bytes) -> dict:
    """
    Lee el reporte NetSuite y retorna:
        { sku: { 'shopify_col': qty, ... } }
    para todas las ubicaciones del mapeo.
    """
    import xml.etree.ElementTree as ET
    ws_tag  = '{urn:schemas-microsoft-com:office:spreadsheet}Worksheet'
    row_tag = '{urn:schemas-microsoft-com:office:spreadsheet}Row'
    cell_tag= '{urn:schemas-microsoft-com:office:spreadsheet}Cell'
    data_tag= '{urn:schemas-microsoft-com:office:spreadsheet}Data'

    content = file_bytes.decode('utf-8')
    root = ET.fromstring(content)

    for ws in root.iter(ws_tag):
        rows    = list(ws.iter(row_tag))
        headers = [
            ((c.find(data_tag).text or '') if c.find(data_tag) is not None else '')
            for c in rows[6].iter(cell_tag)
        ]
        ns_idx = {h: i for i, h in enumerate(headers)}

        # Advertir columnas del mapa que no están en el archivo
        missing = [k for k in LOCATION_MAP if k not in ns_idx]
        if missing:
            st.warning(
                f"⚠️ {len(missing)} ubicaciones del mapa no encontradas en este archivo NS: "
                + ", ".join(missing),
                icon="⚠️",
            )

        data = {}
        for row in rows[8:]:
            cells = [
                ((c.find(data_tag).text or '') if c.find(data_tag) is not None else '')
                for c in row.iter(cell_tag)
            ]
            while len(cells) < len(headers):
                cells.append('')
            raw = cells[3]
            if not raw:
                continue
            sku = raw.split(':')[-1].strip()
            data[sku] = {
                sho_col: int(float(cells[ns_idx[ns_col]])) if ns_idx.get(ns_col, -1) >= 0 and cells[ns_idx[ns_col]] else 0
                for ns_col, sho_col in LOCATION_MAP.items()
            }
        return data

    raise ValueError("No se encontró hoja en el archivo NetSuite.")


def apply_ns_to_shopify(df_sho: pd.DataFrame, ns_data: dict) -> tuple:
    """
    Aplica las cantidades de NS sobre el DataFrame de Shopify.
    Retorna (df_actualizado, stats_dict)
    """
    inv_cols = [c for c in df_sho.columns if c.startswith('Inventory Available:')]
    for c in inv_cols:
        df_sho[c] = pd.to_numeric(df_sho[c], errors='coerce').fillna(0).astype(int)

    matched = unmatched = 0
    location_totals = {c: 0 for c in inv_cols}

    for idx, row in df_sho.iterrows():
        sku = str(row['Variant SKU']).strip()
        if sku in ns_data:
            for sho_col, qty in ns_data[sku].items():
                if sho_col in df_sho.columns:
                    df_sho.at[idx, sho_col] = qty
            matched += 1
        else:
            unmatched += 1

    for c in inv_cols:
        location_totals[c] = int(df_sho[c].sum())

    return df_sho, {
        'matched':   matched,
        'unmatched': unmatched,
        'totals':    location_totals,
    }


# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="font-family:VT323,monospace;font-size:18px;color:#888;margin-bottom:16px">'
    'Sube los dos archivos · el sistema actualiza TODAS las ubicaciones y genera el Excel listo para importar en Shopify.'
    '</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)
with col1:
    style.section_title("📗", "NetSuite")
    st.caption("Inventario Disponible por Ubicación - Digital")
    ns_file = st.file_uploader("Archivo NetSuite (.xls / .xlsx)", type=["xls", "xlsx"], key="sync_ns")
with col2:
    style.section_title("🛒", "Shopify Export actual")
    st.caption("Admin → Inventario → Exportar inventario")
    sho_file = st.file_uploader("Archivo Shopify Export (.xlsx)", type=["xlsx"], key="sync_sho")

st.markdown("---")

if ns_file and sho_file:
    with st.spinner("⛏  Procesando todas las ubicaciones..."):
        try:
            ns_data = parse_netsuite_all_locations(ns_file.read())
            df_sho  = pd.read_excel(
                io.BytesIO(sho_file.read()),
                dtype={'Variant SKU': str},
            )
            df_sho['Variant SKU'] = df_sho['Variant SKU'].astype(str).str.strip()
            df_updated, stats = apply_ns_to_shopify(df_sho, ns_data)
        except Exception as e:
            st.error(f"ERROR: {e}")
            st.stop()

    # ── Métricas ──────────────────────────────────────────────────────────────
    style.section_title("💎", "Resultado")
    c1, c2, c3 = st.columns(3)
    with c1: style.slot_card("✅", "SKUs actualizados", f"{stats['matched']:,}", color="#55FF55")
    with c2: style.slot_card("❓", "Sin match NS",      f"{stats['unmatched']:,}", color="#AAAAAA",
                              sublabel="quedan con valor anterior")
    with c3: style.slot_card("🏪", "Ubicaciones",       f"{len(LOCATION_MAP)}", color="#3EEBD0")

    # ── Totales por tienda ────────────────────────────────────────────────────
    style.section_title("🏪", "Unidades por ubicación")
    totals = stats['totals']
    rows_display = [
        {"Ubicación Shopify": col.replace("Inventory Available: ", ""), "Unidades": qty}
        for col, qty in sorted(totals.items(), key=lambda x: -x[1])
        if qty > 0
    ]
    if rows_display:
        df_totals = pd.DataFrame(rows_display)
        st.dataframe(df_totals, use_container_width=True, hide_index=True, height=400)

    # ── Descarga ──────────────────────────────────────────────────────────────
    st.markdown("---")
    style.section_title("💾", "Descargar e Importar en Shopify")
    st.markdown(
        '<div style="font-family:VT323,monospace;font-size:16px;color:#888;margin-bottom:12px">'
        '1. Descarga el archivo &nbsp;·&nbsp; '
        '2. Shopify Admin → Inventario → Importar &nbsp;·&nbsp; '
        '3. Sube este archivo'
        '</div>',
        unsafe_allow_html=True,
    )

    output = io.BytesIO()
    df_updated.to_excel(output, index=False)
    output.seek(0)

    st.download_button(
        label=f"📥  DESCARGAR SHOPIFY INVENTORY UPDATE — {stats['matched']:,} SKUs · {len(LOCATION_MAP)} tiendas",
        data=output.getvalue(),
        file_name=f"shopify_inventory_update_{ns_file.name.replace('.xls','').replace('.xlsx','')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

else:
    st.markdown(
        '<div style="font-family:VT323,monospace;font-size:20px;color:#55A038;'
        'border:3px dashed #3A3A3A;padding:28px;text-align:center;margin-top:16px">'
        '▲ Sube los dos archivos para generar el inventario sincronizado'
        '</div>',
        unsafe_allow_html=True,
    )
