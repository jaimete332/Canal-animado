---
name: investigar-nicho
description: Investiga el nicho de YouTube Shorts «¿qué pasaría si…?» (los vídeos y canales que mejor funcionan, sus ganchos, títulos, duración, temas y miniaturas) y actualiza la guía de estilo que usa la fábrica de vídeos. Úsala cuando el usuario pida investigar la competencia, ver qué funciona, buscar tendencias o ideas, o antes de escribir una tanda nueva de guiones con la skill crear-short.
---

# Investigar el nicho y actualizar la guía de estilo

Objetivo: descubrir **qué funciona en el nicho** y convertirlo en reglas concretas que apliquen los
guiones de `crear-short`. Se copian **patrones** (estructura del gancho, ritmo, formato de título, tipo
de tema, duración), **nunca** guiones, personajes, marcas, música ni miniaturas de otros creadores.

## Paso 1 · Recoger datos (elige la mejor fuente disponible)

**A. YouTube Data API (preferida, datos reales).** Necesita una clave gratuita de Google Cloud
(YouTube Data API v3) en `YOUTUBE_API_KEY` (`.env`) o guardada como secreto de red para
`www.googleapis.com` con el header `X-Goog-Api-Key`.
```bash
python -m fabrica research                       # consultas por defecto del nicho (es + en), últimos 12 meses
python -m fabrica research --queries "qué pasaría si" "y si fueras" --months 6 --per-query 50
```
Coste: unas 100 unidades de cuota por consulta (la cuota diaria gratuita es de 10.000).

**B. Sin clave: búsqueda web.** Usa WebSearch (modo `extended`) y WebFetch para localizar vídeos y
canales del nicho (p. ej. «qué pasaría si shorts», «what if animated shorts», canales de referencia en
`data/research/style_guide.json` → `references`). Por cada vídeo con datos fiables, añade una entrada a
`data/research/manual_<fecha>.json`:
```json
{"videos": [{"title": "...", "channel": "...", "views": 30000000, "published": "2025-06-01",
             "duration_s": 35, "url": "https://youtube.com/shorts/...", "hook": "primera frase si se conoce",
             "thumbnail_text": "", "notes": "fuente de la cifra", "source": "web"}]}
```
y analízalo con `python -m fabrica research --from-file data/research/manual_<fecha>.json`.
Reglas: no inventes cifras (si no hay dato, deja `null`) y anota la fuente en `notes`. No descargues
vídeos ni extraigas subtítulos o audio de otros creadores.

**C. Métricas propias.** Si el canal ya publica: `python -m fabrica metrics` y `python -m fabrica insights`.
Lo que funciona en el propio canal pesa más que lo de la competencia.

## Paso 2 · Analizar

`python -m fabrica research` genera en `data/research/`:
- `report_<fecha>.md`: top de vídeos por visualizaciones/día, patrones de título (top frente al resto),
  temas con más tirón, palabras frecuentes, canales dominantes.
- `style_guide.json`: reglas accionables (`rules`), temas preferidos (`preferred_topics`) y ejemplos.

Revisa el informe y **completa la guía a mano** con lo que el análisis automático no ve: estructura
de los ganchos, ritmo de montaje, uso de humor, tipo de miniatura, finales en bucle, etc. Añádelo a
`rules` con frases imperativas y cortas.

## Paso 3 · Aplicar a la fábrica (alineación con `crear-short`)

La guía se aplica sola:
- `fabrica/script/writer.py` añade `rules` al prompt del guionista.
- `fabrica/ideas/bank.py` da más puntuación a las ideas de `preferred_topics` (`python -m fabrica ideas`).

Cuando escribas guiones a mano con `crear-short`, **lee `data/research/style_guide.json` antes** y
cumple sus reglas (duración, gancho, título, temas).

## Paso 4 · Informar al usuario

Resume en pocas líneas: qué fuentes usaste (y si los datos son reales o estimados), los 3-5 patrones
más claros, los temas recomendados, qué cambiarías en los próximos vídeos y las ideas concretas
propuestas (`python -m fabrica ideas`). Incluye los enlaces a las fuentes consultadas.

## Ética y límites
- Inspiración en patrones, no copia: ni textos, ni personajes, ni miniaturas, ni música ajenos.
- No uses datos personales de otros creadores ni automatices el scraping de YouTube contra sus términos.
- Distingue en la guía lo **medido** (API/métricas) de lo **observado** (búsqueda web).
