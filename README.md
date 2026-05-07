# Triangulación de Inventario — CEDI Guayabal

Sistema de cruce de inventario entre **NetSuite**, **Shopify** y módulo de **Resurtido**.

---

## Módulos

| Módulo | Descripción |
|---|---|
| **1. Triangulación** | Cruza NetSuite (OFICINA : GUAYABAL) vs Shopify CEDI. Detecta sobreventas, stock oculto, SKUs sin match. |
| **2. Resurtido** | Identifica SKUs con CEDI vacío pero stock en Bodega Principal o Distribuidores. Genera orden de traslado en Excel. |

---

## Archivos requeridos

| Archivo | Sistema | Cómo exportarlo |
|---|---|---|
| `InventarioDisponible*.xls` | NetSuite | Reportes → Inventario Disponible por Ubicación - Digital |
| `Export_*.xlsx` | Shopify | Admin → Inventario → Exportar inventario |

---

## Instalación

```bash
# 1. Clonar / descomprimir el proyecto
cd inventory_tri

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de Supabase

# 5. Crear tablas en Supabase
# Ve a https://app.supabase.com → SQL Editor → pega supabase_schema.sql → Run

# 6. Correr la app
streamlit run app.py
```

---

## Configurar Supabase (opcional pero recomendado)

1. Crea cuenta en [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto
3. Ve a **Settings → API** y copia:
   - `Project URL` → `SUPABASE_URL` en `.env`
   - `anon public` key → `SUPABASE_KEY` en `.env`
4. Ve a **SQL Editor**, pega el contenido de `supabase_schema.sql` y ejecuta

> Si no configuras Supabase, la app funciona en modo sin historial. Los resultados de cada sesión se pierden al cerrar el navegador.

---

## Despliegue en Streamlit Community Cloud (gratis)

1. Sube el proyecto a GitHub (sin el `.env`)
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. En **Advanced settings → Secrets**, agrega:
   ```toml
   SUPABASE_URL = "https://tu-proyecto.supabase.co"
   SUPABASE_KEY = "tu-anon-key"
   ```
5. Deploy ✅

---

## Lógica de cruce SKU

El campo `Artículo` de NetSuite puede tener dos formatos:
- Sin colon: `106041124070134` → se usa directamente
- Con colon: `10604112407:106041124070134` → se usa la parte **después** del colon

Shopify usa el campo `Variant SKU`, que corresponde a la parte derecha del colon en NetSuite.

---

## Estados de triangulación

| Estado | Significado | Acción sugerida |
|---|---|---|
| ✅ OK | NS = Shopify | Ninguna |
| ⚠️ Stock oculto | NS > Shopify | Actualizar inventario en Shopify |
| 🔴 Sobreventa | Shopify > NS | Ajustar Shopify urgente |
| ❓ Sin match NS | Solo en Shopify | Dar de alta en NetSuite o revisar SKU |
| 📦 Sin publicar | En NS no en Shopify | Publicar en Shopify |

---

## Estructura del proyecto

```
inventory_tri/
├── app.py                  # Home — resumen del último run
├── pages/
│   ├── 1_Upload.py         # Sube archivos y ejecuta triangulación
│   ├── 2_Resultados.py     # Visualiza discrepancias con filtros
│   ├── 3_Historial.py      # Historial de runs y tendencias
│   └── 4_Resurtido.py      # Genera orden de resurtido
├── utils/
│   ├── parser.py           # Lee NetSuite (SpreadsheetML) y Shopify
│   ├── triangulate.py      # Lógica de cruce y clasificación
│   ├── db.py               # Cliente Supabase
│   └── export.py           # Genera Excel de salida
├── supabase_schema.sql     # Script de creación de tablas
├── .env.example            # Plantilla de variables de entorno
├── requirements.txt
└── README.md
```
