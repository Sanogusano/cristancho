-- ============================================================
-- Triangulación de Inventario — Schema Supabase
-- Ejecuta este script en el SQL Editor de tu proyecto Supabase
-- ============================================================

-- Tabla: runs
-- Un registro por cada vez que se sube y procesa el par de archivos
CREATE TABLE IF NOT EXISTS runs (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ns_filename      TEXT,
    sho_filename     TEXT,
    total_skus       INTEGER DEFAULT 0,
    ok_count         INTEGER DEFAULT 0,
    ns_mayor_count   INTEGER DEFAULT 0,
    sho_mayor_count  INTEGER DEFAULT 0,
    sin_match_count  INTEGER DEFAULT 0,
    resurtido_count  INTEGER DEFAULT 0
);

-- Tabla: results
-- Una fila por SKU por run — guarda el estado de la triangulación
CREATE TABLE IF NOT EXISTS results (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id              UUID NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    sku                 TEXT NOT NULL,
    nombre              TEXT,
    subtipo             TEXT,
    ns_qty              NUMERIC DEFAULT 0,
    sho_qty             NUMERIC DEFAULT 0,
    ns_principal        NUMERIC DEFAULT 0,
    ns_distribuidores   NUMERIC DEFAULT 0,
    status              TEXT NOT NULL,
    diff                NUMERIC DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_results_run_id ON results(run_id);
CREATE INDEX IF NOT EXISTS idx_results_status  ON results(status);
CREATE INDEX IF NOT EXISTS idx_results_sku     ON results(sku);

-- Tabla: resurtido_lines
-- Líneas de la orden de resurtido generada en cada run
CREATE TABLE IF NOT EXISTS resurtido_lines (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id              UUID NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
    sku                 TEXT NOT NULL,
    nombre              TEXT,
    qty_guayabal        NUMERIC DEFAULT 0,
    qty_principal       NUMERIC DEFAULT 0,
    qty_distribuidores  NUMERIC DEFAULT 0,
    qty_sugerida        NUMERIC DEFAULT 0,
    fuente              TEXT   -- 'PRINCIPAL' | 'DISTRIBUIDORES'
);

CREATE INDEX IF NOT EXISTS idx_resurtido_run_id ON resurtido_lines(run_id);

-- ============================================================
-- Row Level Security (opcional pero recomendado)
-- Descomenta si quieres que solo usuarios autenticados lean datos
-- ============================================================

-- ALTER TABLE runs            ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE results         ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE resurtido_lines ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "Solo autenticados" ON runs
--   FOR ALL USING (auth.role() = 'authenticated');
-- CREATE POLICY "Solo autenticados" ON results
--   FOR ALL USING (auth.role() = 'authenticated');
-- CREATE POLICY "Solo autenticados" ON resurtido_lines
--   FOR ALL USING (auth.role() = 'authenticated');
