import xml.etree.ElementTree as ET
import pandas as pd
import io

_NS = "urn:schemas-microsoft-com:office:spreadsheet"
_WS  = f"{{{_NS}}}Worksheet"
_ROW = f"{{{_NS}}}Row"
_CEL = f"{{{_NS}}}Cell"
_DAT = f"{{{_NS}}}Data"

LOC_GUAYABAL     = "OFICINA : GUAYABAL"
LOC_PRINCIPAL    = "OFICINA : PRINCIPAL"
LOC_DISTRIBUIDORES = "RESERVA DISTRIBUIDOR"


def _cell_text(cell):
    d = cell.find(_DAT)
    return (d.text or "").strip() if d is not None else ""


def parse_netsuite(file_bytes: bytes) -> pd.DataFrame:
    """
    Lee el reporte SpreadsheetML de NetSuite 'Inventario Disponible por Ubicación'.
    La fila 6 (0-based) contiene los encabezados.
    El campo Artículo puede tener formato 'PADRE:VARIANTE' — se usa la parte después del colon.
    """
    content = file_bytes.decode("utf-8")
    root = ET.fromstring(content)

    for ws in root.iter(_WS):
        rows = list(ws.iter(_ROW))

        headers = [_cell_text(c) for c in rows[6].iter(_CEL)]

        # Detectar columnas de ubicación
        idx = {}
        for i, h in enumerate(headers):
            if h == LOC_GUAYABAL:
                idx["guayabal"] = i
            elif h == LOC_PRINCIPAL:
                idx["principal"] = i
            elif LOC_DISTRIBUIDORES in h:
                idx["distribuidores"] = i

        if "guayabal" not in idx:
            raise ValueError(
                f"Columna '{LOC_GUAYABAL}' no encontrada. "
                "Verifica que estás subiendo el reporte correcto de NetSuite."
            )

        def _qty(cells, key):
            i = idx.get(key, -1)
            if i < 0 or i >= len(cells):
                return 0.0
            try:
                return float(cells[i])
            except (ValueError, TypeError):
                return 0.0

        records = []
        for row in rows[8:]:
            cells = [_cell_text(c) for c in row.iter(_CEL)]
            while len(cells) < len(headers):
                cells.append("")

            articulo_raw = cells[3]
            if not articulo_raw:
                continue

            # Split por ':' — Shopify usa la variante (parte derecha)
            sku_key = articulo_raw.split(":")[-1].strip() if ":" in articulo_raw else articulo_raw

            records.append({
                "sku":               sku_key,
                "articulo_raw":      articulo_raw,
                "nombre":            cells[5],
                "subtipo":           cells[0],
                "coleccion":         cells[1],
                "linea":             cells[6],
                "genero":            cells[7],
                "color":             cells[8],
                "talla":             cells[9],
                "ns_guayabal":       _qty(cells, "guayabal"),
                "ns_principal":      _qty(cells, "principal"),
                "ns_distribuidores": _qty(cells, "distribuidores"),
            })

        return pd.DataFrame(records)

    raise ValueError("No se encontró hoja de cálculo en el archivo de NetSuite.")


def parse_shopify(file_bytes: bytes) -> pd.DataFrame:
    """
    Lee el export de inventario de Shopify.
    Fuerza dtype=str en Variant SKU para preservar códigos de 15-16 dígitos.
    Agrega por SKU (suma cantidades de variantes duplicadas).
    """
    df = pd.read_excel(io.BytesIO(file_bytes), dtype={"Variant SKU": str})

    cedi_col = next(
        (c for c in df.columns if "CEDI Guayabal" in c),
        None
    )
    if cedi_col is None:
        raise ValueError(
            "Columna 'Inventory Available: CEDI Guayabal' no encontrada. "
            "Verifica que el archivo es el export de inventario de Shopify."
        )

    df = df.rename(columns={
        "Variant SKU": "sku",
        "Title":       "nombre_shopify",
        "Type":        "tipo_shopify",
        cedi_col:      "sho_cedi",
    })

    df["sku"]      = df["sku"].astype(str).str.strip()
    df["sho_cedi"] = pd.to_numeric(df["sho_cedi"], errors="coerce").fillna(0)

    df = (
        df.groupby("sku")
        .agg(nombre_shopify=("nombre_shopify", "first"),
             sho_cedi=("sho_cedi", "sum"))
        .reset_index()
    )

    return df
