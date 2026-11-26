---
name: investigar-nicho
description: Investiga qué funciona en el nicho de YouTube Shorts «¿qué pasaría si…?» Y en el propio canal (los Shorts que mejor han rendido), y actualiza la guía de estilo que usa la fábrica de vídeos. Úsala cuando el usuario pida investigar la competencia, ver qué funciona, decirte qué vídeos han ido mejor, buscar tendencias o ideas, o antes de escribir una tanda nueva de guiones con la skill crear-short.
---

# Investigar el nicho y actualizar la guía de estilo

Objetivo: descubrir **qué funciona** y convertirlo en reglas concretas que apliquen los guiones de `crear-short`.
Se copian **patrones** (estructura del gancho, ritmo, formato de título, tipo de tema, duración), **nunca** guiones,
personajes, marcas, música ni miniaturas de otros creadores.

**Orden de peso de las fuentes** (lo de arriba manda sobre lo de abajo si se contradicen):
1. **Propio, con métricas reales** del canal (`python -m fabrica metrics`).
2. **Propio, declarado por el usuario** («los que mejor han ido son X, Y, Z»).
3. **Medido en la competencia** (YouTube Data API).
4. **Observado** (búsqueda web, lectura de títulos y canales).

Es nuestra audiencia, nuestro personaje y nuestro formato: un Short propio que funciona vale más que diez ajenos.

## Paso 0 · Lo propio primero (siempre, antes de mirar la competencia)

0. **Pide las métricas de YouTube Studio de TODOS los Shorts** (es el dato que más falta): vistas, «me gusta»,
   % visto medio y, sobre todo, **«vistos frente a deslizados»** (Analytics → Contenido → Shorts), que mide si el
   gancho detiene el dedo. `python -m fabrica research --metrics-template` crea la plantilla
   (`data/research/own_metrics.template.csv`); con ella rellena `python -m fabrica research --own --metrics archivo.csv`.
   Con ≥ 10 Shorts con métricas el análisis correlaciona rasgos ↔ métricas (Spearman, |ρ| ≥ 0,6) y elige los
   ganadores solo por el % de «vistos». Esas correlaciones salen como **hipótesis** (se prueban ~70 combinaciones).
1. **Averigua cuáles han ido mejor.** Si no hay métricas, pregúntaselo al usuario (con cifras si las tiene:
   vistas y % visto medio). Regístralos:
   ```bash
   python -m fabrica research --winner caer-de-un-avion jefe-de-la-mafia un-ano-sin-sol \
          --note "declarados por el usuario" [--views 120000 --retention 78]
   ```
   Se guardan en `data/research/own_winners.json`. Con métricas del registro (`python -m fabrica metrics`) los
   ganadores se eligen solos por retención y vistas.
2. **Analiza** (sin API, instantáneo): `python -m fabrica research --own`. Genera `own_channel_<fecha>.md/.json`:
   ganadores frente al resto en rasgos medibles (título, gancho, % de narración con caso real, personas con nombre,
   tarjetas de dato, contadores…) y **arquetipos de premisa** (caída/altura, ser alguien con poder, quitar algo
   universal, situación cotidiana, cuerpo). Los arquetipos alimentan el banco de ideas (hasta +8 puntos).
3. **Lee los guiones ganadores enteros** (`stories/<slug>.json`) y compáralos con los que no ganaron. Lo más
   informativo es un par parecido que rindió distinto (p. ej. «jefe de la mafia» frente a «traicionar a la mafia»):
   ¿qué cambia en la premisa, el gancho, el giro o el cierre? Anota lo que veas en `own_winners.json` →
   `lecciones` (frases imperativas y cortas). Entran en la guía como «(propio, obs.)» y sobreviven a cualquier
   regeneración.
4. **Sé honesto con la n.** Con menos de 5 ganadores el análisis es una **pista, no una prueba**. Un rasgo solo
   genera regla automática si **todos** los ganadores superan la mediana del resto (columna «¿Los 3 por encima?»);
   si ninguno lo cumple, díselo al usuario en vez de inventar una regla. Nunca presentes una correlación de 3
   vídeos como causa.
5. **No filtres nada del canal al exterior.** Los títulos propios, el nombre del canal y los datos del proyecto no se
   mandan a la API de YouTube ni a buscadores. Las consultas del Paso 1 son siempre genéricas del nicho.

## Paso 1 · Recoger datos del nicho (elige la mejor fuente disponible)

**A0. Atípicos de canales pequeños (el paso que da con vídeos «top»).** El top por visualizaciones lo copan canales
gigantes y anuncios; lo replicable son los vídeos que rindieron decenas de veces más que la media de **su propio**
canal pequeño. `python -m fabrica research --outliers` busca por tramos mensuales (6 consultas × 6 tramos ≈ 3.600
unidades de cuota), añade las estadísticas de cada canal (suscriptores, vistas/vídeo), descarta el ruido (videojuegos,
fandom, deportes, política, anuncios) y compara los atípicos (≥ 8× su canal, canal ≤ 300 k vistas/vídeo, ≥ 100 k vistas)
con el conjunto del formato en **forma de la pregunta, duración, tema y emoji**. Genera reglas «Atípicos: …» solo
donde la diferencia es ≥ 10 puntos. Después **abre los vídeos de la tabla** (URLs en el informe) y analiza gancho,
estructura y primer fotograma de los 5-10 mejores: es lo que no ve el análisis automático.

**A. YouTube Data API (preferida, datos reales).** Necesita una clave gratuita de Google Cloud (YouTube Data API v3)
en `YOUTUBE_API_KEY` (`.env`) o guardada como secreto de red para `www.googleapis.com` con el header `X-Goog-Api-Key`.
```bash
python -m fabrica research                       # consultas por defecto del nicho (es + en), últimos 12 meses
python -m fabrica research --queries "qué pasaría si" "y si fueras" --months 6 --per-query 50
```
Coste: unas 100 unidades de cuota por consulta (cuota diaria gratuita: 10.000). La clave solo viaja en la cabecera.

**B. Sin clave: búsqueda web.** WebSearch (modo `extended`) y WebFetch para localizar vídeos y canales del nicho.
Por cada vídeo con datos fiables, añade una entrada a `data/research/manual_<fecha>.json`:
```json
{"videos": [{"title": "...", "channel": "...", "views": 30000000, "published": "2025-06-01",
             "duration_s": 35, "url": "https://youtube.com/shorts/...", "hook": "primera frase si se conoce",
             "thumbnail_text": "", "notes": "fuente de la cifra", "source": "web"}]}
```
y analízalo con `python -m fabrica research --from-file data/research/manual_<fecha>.json`.
No inventes cifras (si no hay dato, `null`) y anota la fuente en `notes`. No descargues vídeos ni extraigas
subtítulos o audio de otros creadores.

## Paso 2 · Analizar

`python -m fabrica research` genera en `data/research/`: `report_<fecha>.md` (top por visualizaciones/día, patrones
de título top frente al resto, temas, palabras, canales), `analysis_<fecha>.json`, `videos_<fecha>.json` y actualiza
`style_guide.json`.

- La guía **se fusiona, no se sobrescribe**: se conservan las reglas manuales y «(propio…)», `topic_notes`,
  `references`, `own_channel`, etc. Antes de escribir, la anterior se copia a `style_guide.prev.json`.
- `preferred_topics_locked: true` fija los temas preferidos curados a mano; ponlo a `false` si quieres que la
  investigación los recalcule.
- Al terminar refresca solo el análisis propio si ya hay ganadores.
- Completa a mano lo que el análisis no ve (estructura de ganchos, ritmo, humor, finales en bucle, miniatura): frases
  imperativas y cortas en `rules`, marcadas **(medido)**, **(obs.)** o **(propio…)** según su origen.

## Paso 3 · Aplicar a la fábrica

- `script/writer.py` añade `rules` al prompt del guionista; `ideas/bank.py` suma bonus por `preferred_topics`
  y por **arquetipos propios**. Revisa `python -m fabrica ideas`.
- Al escribir guiones a mano con `crear-short`, **lee `data/research/style_guide.json` antes** (reglas
  «(propio…)» incluidas) y cumple sus reglas.
- **Explotar y explorar:** 2 de cada 3 Shorts siguen la fórmula ganadora; 1 de cada 3 prueba algo distinto
  (otro arquetipo, otro tipo de gancho) para no quedarse ciego a lo que podría rendir más.
- Si propones ideas nuevas, que cada una lleve ya su **caso real con nombre y año** a verificar con fuentes.
- Con el canal en 1.500-2.500 visitas por Short, **la duración no es la palanca** (medido: los atípicos duran igual que
  el resto, mediana 58 s frente a 51 s). Lo que cambia es la premisa y los primeros 2 segundos: prueba formatos, no
  longitudes.

## Paso 4 · Cerrar el ciclo (validar)

Cuando haya cifras de los Shorts publicados después de aplicar la guía:
1. Pídelas al usuario o descárgalas (`python -m fabrica metrics`) y vuelve a lanzar `research --own`.
2. Si un Short nuevo supera a los ganadores, añádelo (`--winner`); si la fórmula **no** se confirma, quita o
   reescribe la lección en `own_winners.json`. Una regla que no se valida con datos propios se retira.
3. Anota en el informe qué se probó (la parte «explorar») y con qué resultado.

## Paso 5 · Informar al usuario

En pocas líneas: qué fuentes usaste y **cuánto pesa cada una** (propio con métricas / propio declarado / medido /
observado), los patrones más claros del canal propio con la n y su nivel de confianza, 3-5 patrones del nicho, los
temas recomendados, qué cambiarías en los próximos vídeos, las ideas propuestas (`python -m fabrica ideas`) y qué
dato falta para afinar (normalmente: vistas y % visto de los ganadores). Incluye los enlaces a las fuentes.

## Ética y límites
- Inspiración en patrones, no copia: ni textos, ni personajes, ni miniaturas, ni música ajenos.
- No uses datos personales de otros creadores ni automatices el scraping de YouTube contra sus términos.
- Distingue en la guía lo **propio**, lo **medido** (API/métricas) y lo **observado**; no mezcles sus niveles de certeza.
