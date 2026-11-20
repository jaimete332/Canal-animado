# Canal en inglés: **Stickpothetical** (vídeos largos de stickman, 16:9)

Segundo canal de la fábrica, independiente del de Shorts en español:

| | Canal 1 — Hipotéticos | Canal 2 — Stickpothetical |
|---|---|---|
| Idioma | español (España) | inglés (EE. UU.) |
| Formato | Shorts verticales 1080×1920, ~60 s | vídeos largos 1920×1080, **8-12 min**, con capítulos |
| Motor | Leo (`fabrica/visuals/`) | stickman (`fabrica/stick/`) |
| Voz | Edge `es-ES-AlvaroNeural` | Edge `en-US-AndrewNeural` (ritmo pausado, sin mezclar voces) |
| Subtítulos | karaoke quemado en el vídeo | `captions.srt` para subir a YouTube (subtítulos exactos) |
| Configuración | `config.yaml` | `config.yaml` + `channels/stickman_en.yaml` |
| Guiones | `stories/` | `stories_en/` (se escriben con `scripts/storykit_en.py`) |
| Salida | `output/<slug>/` | `output/stickman_en/<slug>/` |
| Carpeta para subir | `PARA_SUBIR/` | `TO_UPLOAD/` (con `PUBLISH.md`) |

## Nombre
* **Stickpothetical**: *stick* + *hypothetical*. Es el hermano en inglés de «Hipotéticos» y deja claro el formato:
  «¿qué pasaría si TÚ vivieras esto?», contado con stickmen. Identificador sugerido: `@Stickpothetical`
  (alternativas: `@StickpotheticalTV`, `@WhatIfStickman`, `@StanTheStickman`).
* **Mascota:** **Stan**, el stickman de la bufanda roja. Sale en todos los vídeos, sea cual sea la época.
* Antes de crearlo, comprueba que el nombre y el identificador están libres en YouTube: desde aquí no he podido.

## Nicho y formato (por qué así)
* Los vídeos «what if» y de supervivencia histórica con stickmen tienen mucha demanda en inglés y encajan
  con lo que ya hace la fábrica (situaciones hipotéticas con datos reales).
* **8-12 minutos**: a partir de 8 min YouTube permite anuncios a mitad del vídeo (*mid-rolls*), y los
  vídeos largos suman mucho tiempo de visualización (la métrica que más pesa en el algoritmo).
* Estructura: gancho fuerte (≤ 30 s) → capítulos con título (marcas de tiempo automáticas en la descripción)
  → recapitulación → pregunta para comentarios. Un medidor de «survival odds» engancha de principio a fin.
* Originalidad (requisito para monetizar): animación, guion, voz y música propios, con un personaje fijo
  y fuentes citadas. No es contenido reciclado.

## Archivos de marca (`assets/branding_en/`)
| Archivo | Tamaño | Dónde se sube |
|---|---|---|
| `profile.png` | 800×800 | YouTube Studio → Personalización → Imagen de marca → Imagen |
| `banner.png` | 2560×1440 | … → Imagen de banner (`banner_preview.png` muestra las zonas seguras) |
| `watermark.png` | 150×150 | … → Marca de agua |

Se regeneran con `python3 scripts/branding_en.py`.

## Descripción del canal (copiar y pegar)
```
What if YOU woke up as a medieval peasant? A Roman soldier? A sailor on a pirate ship?

On Stickpothetical, Stan the stickman lives through history's wildest situations so you don't have to. Every video is a stickman story with real history: what life was actually like, what would have killed you, and whether you'd make it out alive.

📚 The story is a dramatization, but the facts are real and every video lists its sources.
🎬 New stickman what-if every week.
💬 Got a "what if"? Drop it in the comments — the best ones become videos.

Subscribe and let's find out if you'd survive. 🔔
```
* **Frase corta:** `What if history happened to YOU? Stickman stories with real facts.`
* **Palabras clave:** stickman, what if, history, could you survive, animated history, medieval, ancient rome,
  survival, explained, stickman animation

## Ideas para los próximos episodios
1. Could You Survive a Year as a Roman Legionary?
2. What If You Were a Sailor on a Pirate Ship in 1715?
3. Could You Survive the Oregon Trail?
4. What If You Lived in Pompeii in 79 AD?
5. A Year as a Viking Raider: Would You Make It?
6. What If You Worked in a Victorian Factory in 1840?
7. Could You Survive as a Knight in the Hundred Years' War?
8. What If You Were a Gold Rush Miner in 1849?

## Comandos
```bash
python3 scripts/en_story_<tema>.py                                      # exporta el guion a stories_en/
python -m fabrica --channel stickman_en still stories_en/<slug>.json all # fotogramas de previsualización
python -m fabrica --channel stickman_en make  stories_en/<slug>.json     # vídeo completo + QA
python -m fabrica --channel stickman_en regen <slug> s07 s08             # rehace solo esas escenas
python -m fabrica --channel stickman_en deliver <slug>                   # → TO_UPLOAD/<NN>_<slug>/
```
Para publicar por API en el canal inglés hace falta autorizar **ese** canal (el token se guarda aparte, en
`secrets/youtube_token_stickman_en.json`; ver `docs/YOUTUBE.md`).
