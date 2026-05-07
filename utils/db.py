import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        try:
            from supabase import create_client
            url = os.environ.get("SUPABASE_URL", "")
            key = os.environ.get("SUPABASE_KEY", "")
            if not url or not key:
                return None
            _client = create_client(url, key)
        except Exception:
            return None
    return _client


def is_configured() -> bool:
    return get_client() is not None


def save_run(
    ns_filename: str,
    sho_filename: str,
    results: pd.DataFrame,
    resurtido: pd.DataFrame,
) -> str | None:
    """
    Guarda un run en Supabase.
    Retorna el run_id si tuvo éxito, None si Supabase no está configurado.
    """
    client = get_client()
    if client is None:
        return None

    counts = results["status"].value_counts().to_dict()

    run_resp = client.table("runs").insert({
        "ns_filename":     ns_filename,
        "sho_filename":    sho_filename,
        "total_skus":      int(len(results)),
        "ok_count":        int(counts.get("ok", 0)),
        "ns_mayor_count":  int(counts.get("ns_mayor", 0)),
        "sho_mayor_count": int(counts.get("sho_mayor", 0)),
        "sin_match_count": int(counts.get("sin_match_ns", 0) + counts.get("sin_match_sho", 0)),
        "resurtido_count": int(len(resurtido)),
    }).execute()

    run_id = run_resp.data[0]["id"]

    # Resultados en lotes de 500
    records = [
        {
            "run_id":          run_id,
            "sku":             str(r["sku"]),
            "nombre":          str(r.get("nombre") or ""),
            "subtipo":         str(r.get("subtipo") or ""),
            "ns_qty":          float(r["ns_guayabal"]),
            "sho_qty":         float(r["sho_cedi"]),
            "ns_principal":    float(r["ns_principal"]),
            "ns_distribuidores": float(r["ns_distribuidores"]),
            "status":          str(r["status"]),
            "diff":            float(r["diff"]),
        }
        for _, r in results.iterrows()
    ]
    for i in range(0, len(records), 500):
        client.table("results").insert(records[i:i+500]).execute()

    # Resurtido en lotes de 500
    if len(resurtido) > 0:
        res_records = [
            {
                "run_id":          run_id,
                "sku":             str(r["sku"]),
                "nombre":          str(r.get("nombre") or ""),
                "qty_guayabal":    float(r["ns_guayabal"]),
                "qty_principal":   float(r["ns_principal"]),
                "qty_distribuidores": float(r["ns_distribuidores"]),
                "qty_sugerida":    float(r["qty_sugerida"]),
                "fuente":          str(r["fuente"]),
            }
            for _, r in resurtido.iterrows()
        ]
        for i in range(0, len(res_records), 500):
            client.table("resurtido_lines").insert(res_records[i:i+500]).execute()

    return run_id


def get_runs(limit: int = 30) -> list:
    client = get_client()
    if client is None:
        return []
    return (
        client.table("runs")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
    )


def get_results(run_id: str, status_filter: str = None) -> list:
    client = get_client()
    if client is None:
        return []
    q = client.table("results").select("*").eq("run_id", run_id)
    if status_filter:
        q = q.eq("status", status_filter)
    return q.limit(5000).execute().data


def get_resurtido_lines(run_id: str) -> list:
    client = get_client()
    if client is None:
        return []
    return (
        client.table("resurtido_lines")
        .select("*")
        .eq("run_id", run_id)
        .execute()
        .data
    )
