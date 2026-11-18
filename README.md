# Fábrica de YouTube Shorts animados — «¿Y si...?»

Sistema que produce **Shorts animados 2D en español de España** del tipo *«¿Qué pasaría si…?»* con un solo comando:
idea → guion → revisión de datos → voz → música y efectos → animación → subtítulos → render → control de calidad → metadatos.

```bash
python -m fabrica make stories/centro-de-la-tierra.json   # vídeo desde un guion
python -m fabrica auto                                     # todo automático (requiere API key de LLM)
```

Resultado en `output/<slug>/final.mp4` (1080×1920, H.264 + AAC, 30 fps, ~60 s) con `metadata.json`
(título, descripción, hashtags, comentario fijado), `thumbnail.png` e informe `qa/report.md`.

---

## 1. Arquitectura

```
                 ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  ideas/bank ──▶ │ script/writer│──▶│ factcheck    │──▶│ tts/narrator │── voz + tiempos por palabra
 (puntuación,    │  (LLM + DSL  │   │ (reglas+LLM) │   │ Kokoro/Piper/│
  anti-duplicado)│   visual)    │   └──────────────┘   │ Edge/11Labs… │
                 └──────────────┘                      └──────┬───────┘
                                                              ▼
 ┌─────────────────────────┐   ┌───────────────────────┐   ┌────────────────┐
 │ visuals/ (Cairo)        │   │ audio/                │   │ edit/subtitles │
 │  personaje con rig+IK,  │   │  música procedural,   │   │  ASS karaoke   │
 │  fondos, props, cámara, │   │  SFX sintetizados,    │   │  (libass)      │
 │  overlays, transiciones │   │  ducking, -14 LUFS    │   └───────┬────────┘
 │  → 1 MP4 por escena     │   └──────────┬────────────┘           │
 └───────────┬─────────────┘              │                        │
             └─────────────── ffmpeg (concat + subtítulos + audio) ┘
                                          ▼
                        qa/checks (Whisper local, formato, silencios, loudness,
                        congelados, dinamismo) → publish/ (metadatos, miniatura,
                        YouTube con aprobación) → analytics/ (métricas → guiones)
```

### Decisiones técnicas (y por qué)

| Necesidad | Elegido | Alternativas evaluadas | Motivo |
|---|---|---|---|
| Animación | **Motor vectorial propio en Cairo** (personaje con huesos, IK, lip-sync, expresiones; fondos y props animados) | Vídeo generativo (Runway, Kling, Veo), imágenes IA + Ken Burns, After Effects/Remotion | Coherencia total del personaje entre vídeos, movimiento real (no imágenes fijas), coste 0, regeneración por escena, sin deformaciones. El vídeo generativo cuesta 0,3-1 $/clip y no mantiene al personaje. |
| Fondos IA (opcional) | Interfaz `images.provider` (OpenAI / Gemini / FLUX vía Replicate) | Midjourney (sin API oficial) | Se usa solo cuando aporta valor; el movimiento lo sigue poniendo el motor. |
| Voz | **Piper es_ES «sharvard» local** (hablante nativo de España, inferencia directa con onnxruntime) + Kokoro-82M de respaldo | Edge TTS (gratis, muy buena, requiere red), ElevenLabs (la mejor, ~0,18 $/1k car.), OpenAI TTS, Google Chirp3-HD | Gratis, sin GPU, acento peninsular auténtico. Muestras comparativas en `samples/voces/`. Cambiar a ElevenLabs/Edge/Kokoro = una línea en `config.yaml`. |
| Sincronía | Síntesis por cláusula + tiempos por sílaba (o tiempos nativos del proveedor) | Alineado forzado con Whisper | Sin silencios muertos, pausas controladas, subtítulos exactos. |
| Música/SFX | **Sintetizados por código** (100 % originales) | Pixabay / Biblioteca de YouTube | Cero riesgo de Content ID. Puedes añadir pistas con licencia en `assets/music/`. |
| Subtítulos | ASS + libass (ffmpeg) | Dibujar en Cairo | Karaoke palabra a palabra, pop-in, contorno, rápido. |
| Guion | LLM (Claude / GPT / Gemini) con el **catálogo del motor** en el prompt | — | El LLM escribe narración *y* dirección visual en un JSON validado. |
| QA | Whisper small (sherpa-onnx, local) + ffmpeg | — | Inteligibilidad por escena y detección de errores sin coste. |

## 2. Instalación

```bash
./scripts/setup.sh          # apt/brew + venv + pip + modelos (~850 MB)
python -m fabrica doctor    # verifica todo
```

Manual: `pip install -r requirements.txt` y descarga de modelos según `scripts/setup.sh`.
Fuentes (OFL/Apache) incluidas en `assets/fonts/`.

## 3. Uso

| Comando | Qué hace |
|---|---|
| `python -m fabrica auto [--idea "..."]` | Elige idea (o usa la tuya), escribe el guion y produce el vídeo |
| `python -m fabrica make <guion.json>` | Produce desde un guion (reanudable: reutiliza voz y escenas ya hechas) |
| `python -m fabrica still <guion.json> s07 [t]` | PNG de previsualización de una escena (o `all`) |
| `python -m fabrica regen <slug> s07 s08` | Rehace solo esas escenas y vuelve a montar |
| `python -m fabrica ideas` | Ranking de ideas sin repetir |
| `python -m fabrica list` | Registro de vídeos (estado, duración, coste, ID de YouTube) |
| `python -m fabrica approve <slug>` → `upload <slug>` | Aprobación manual + subida (privado) |
| `python -m fabrica metrics` / `insights` | Métricas de YouTube → pautas para guiones futuros |

Para **editar una escena**: cambia `output/<slug>/script.json` (o el guion original) y ejecuta `regen`.

## 4. El guion (DSL visual)

Cada escena del JSON lleva narración, datos con fuente y dirección visual:

```json
{"id": "s05", "beat": "development",
 "narration": "A cuatro kilómetros pasas la mina más profunda del mundo.",
 "claims": [{"text": "Mponeng supera los 4 km", "kind": "fact", "source": "AngloGold Ashanti"}],
 "visual": {
   "background": {"type": "strata", "depth_from": 0.5, "depth_to": 4, "scroll": 650},
   "character": {"action": "drill", "expression": "excited", "outfit": "suit", "helmet": "dome", "x": 0.5, "y": 0.56},
   "props": [{"type": "sign", "text": "MINA\nMPONENG", "x": 0.84, "y": 0.5, "at_word": 4, "enter": "drop"}],
   "overlays": [{"type": "depth", "from": 0.5, "to": 4}],
   "camera": {"move": "push_in", "shake": 0.35}},
 "sfx": [{"name": "drill", "at": 0}], "transition": "whip"}
```

`at_word` sincroniza cualquier elemento con la palabra N de la narración.
Catálogo completo: `python -c "from fabrica.script.writer import catalog; print(catalog())"`.

## 5. Calidad, costes y seguridad

* QA automático en cada render (`output/<slug>/qa/report.md` + hoja de contactos).
* `costs.json` por vídeo y límite `budget.max_usd_per_video`. Con la configuración por defecto: **0 $ por vídeo**
  (con Claude para guiones ≈ 0,05-0,10 $; con ElevenLabs ≈ +0,20 $).
* Claves solo en `.env` (ignorado por git). Reintentos con backoff en todas las APIs y cadena de respaldo de voz.
* **Nada se publica sin tu aprobación**: `approve` firma el hash del MP4; si cambia, hay que volver a aprobar.

Más detalle: [`docs/API_KEYS.md`](docs/API_KEYS.md), [`docs/YOUTUBE.md`](docs/YOUTUBE.md), [`docs/CRECIMIENTO.md`](docs/CRECIMIENTO.md).
