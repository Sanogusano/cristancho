import pandas as pd
from typing import Tuple

STATUS_OK          = "ok"
STATUS_NS_MAYOR    = "ns_mayor"       # Stock en bodega, Shopify en 0 → venta perdida
STATUS_SHO_MAYOR   = "sho_mayor"      # Shopify promete más de lo que hay → sobreventa
STATUS_SIN_NS      = "sin_match_ns"   # SKU en Shopify pero no en NetSuite
STATUS_SIN_SHO     = "sin_match_sho"  # SKU en NetSuite GUAYABAL pero no publicado en Shopify

STATUS_LABELS = {
    STATUS_OK:       "✅  OK — coinciden",
    STATUS_NS_MAYOR: "⚠️  Stock oculto (NS > Shopify)",
    STATUS_SHO_MAYOR:"🔴  Sobreventa (Shopify > NS)",
    STATUS_SIN_NS:   "❓  Sin match en NetSuite",
    STATUS_SIN_SHO:  "📦  En NS sin publicar en Shopify",
}

STATUS_COLORS = {
    STATUS_OK:       "#d4edda",
    STATUS_NS_MAYOR: "#fff3cd",
    STATUS_SHO_MAYOR:"#f8d7da",
    STATUS_SIN_NS:   "#e2e3e5",
    STATUS_SIN_SHO:  "#cce5ff",
}


def triangulate(
    df_ns: pd.DataFrame,
    df_sho: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cruza NetSuite y Shopify por SKU.

    Retorna:
        results  — una fila por SKU con status de triangulación
        resurtido — subset donde GUAYABAL=0 y hay stock en PRINCIPAL o DISTRIBUIDORES
    """
    ns_cols = ["sku", "articulo_raw", "nombre", "subtipo", "coleccion",
               "linea", "genero", "color", "talla",
               "ns_guayabal", "ns_principal", "ns_distribuidores"]
    sho_cols = ["sku", "nombre_shopify", "sho_cedi"]

    merged = pd.merge(
        df_ns[ns_cols],
        df_sho[sho_cols],
        on="sku",
        how="outer",
    )

    # Rellenar nulos numéricos
    for col in ("ns_guayabal", "ns_principal", "ns_distribuidores", "sho_cedi"):
        merged[col] = merged[col].fillna(0)

    # Nombre: preferir NetSuite; fallback a Shopify
    merged["nombre"] = merged["nombre"].fillna(merged["nombre_shopify"])

    merged["diff"] = merged["ns_guayabal"] - merged["sho_cedi"]

    # Flags para identificar presencia en cada sistema
    merged["_en_ns"]  = merged["articulo_raw"].notna()
    merged["_en_sho"] = merged["nombre_shopify"].notna()

    def _classify(row):
        if not row["_en_ns"]:
            return STATUS_SIN_NS
        if not row["_en_sho"]:
            # Solo reportar como "sin publicar" si hay stock en Guayabal
            return STATUS_SIN_SHO if row["ns_guayabal"] > 0 else STATUS_OK
        if row["ns_guayabal"] == row["sho_cedi"]:
            return STATUS_OK
        if row["ns_guayabal"] > row["sho_cedi"]:
            return STATUS_NS_MAYOR
        return STATUS_SHO_MAYOR

    merged["status"] = merged.apply(_classify, axis=1)
    merged.drop(columns=["_en_ns", "_en_sho"], inplace=True)

    # Resurtido: GUAYABAL vacío pero hay fuente disponible
    mask_resurtido = (
        (merged["ns_guayabal"] == 0)
        & ((merged["ns_principal"] > 0) | (merged["ns_distribuidores"] > 0))
        & (merged["status"] != STATUS_SIN_NS)
    )
    resurtido = merged[mask_resurtido].copy()

    resurtido["fuente"] = resurtido.apply(
        lambda r: "PRINCIPAL" if r["ns_principal"] > 0 else "DISTRIBUIDORES",
        axis=1,
    )
    resurtido["qty_sugerida"] = resurtido.apply(
        lambda r: r["ns_principal"] if r["ns_principal"] > 0 else r["ns_distribuidores"],
        axis=1,
    )

    return merged, resurtido


def summary_stats(results: pd.DataFrame) -> dict:
    counts = results["status"].value_counts().to_dict()
    total  = len(results)
    return {
        "total":      total,
        "ok":         counts.get(STATUS_OK, 0),
        "ns_mayor":   counts.get(STATUS_NS_MAYOR, 0),
        "sho_mayor":  counts.get(STATUS_SHO_MAYOR, 0),
        "sin_ns":     counts.get(STATUS_SIN_NS, 0),
        "sin_sho":    counts.get(STATUS_SIN_SHO, 0),
        "pct_ok":     round(counts.get(STATUS_OK, 0) / total * 100, 1) if total else 0,
    }
