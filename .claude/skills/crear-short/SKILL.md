---
name: crear-short
description: Crea un YouTube Short animado del canal «Hipotéticos» de principio a fin con la fábrica del repositorio — guion «¿qué pasaría si…?» con datos y fuentes, dirección visual en el DSL del motor, voz, render, control de calidad, miniatura, título, descripción y etiquetas. Úsala cuando el usuario pida uno o varios vídeos nuevos, un anuncio o regenerar una escena.
---

# Crear un Short con la fábrica

## 0 · Antes de escribir
1. Lee la guía del nicho: `data/research/style_guide.json` (la mantiene la skill `investigar-nicho`).
   Si tiene más de 30 días o no existe, propón actualizarla. Las reglas marcadas **«(propio…)»** salen de los
   Shorts que mejor han funcionado en ESTE canal y pesan más que las de la competencia: premisa universal, giro a
   un caso real con nombre y año, humor seco, cierre con postura. Sigue la fórmula en 2 de cada 3 Shorts y prueba
   algo distinto en el tercero. Si no hay ganadores registrados, pregunta cuáles han ido mejor
   (`python -m fabrica research --winner <slug> ...`).
   Lee también `estrategia` en esa guía (objetivo y formatos vigentes). Tanda estándar: Short A (comer X cada día)
   + Short B (micro-accidente del cuerpo) de 50-60 s + 1 **Short corto de 25-35 s** (8-9 escenas, 70-95 palabras,
   `target_seconds` [22, 38], un único dato visual con número en pantalla, cierre en bucle).
2. Elige la idea: `python -m fabrica ideas` (puntúa y descarta duplicados del registro `data/registry.sqlite`).
3. Mira el catálogo del motor para saber qué se puede dibujar:
   `python -c "from fabrica.script.writer import catalog; print(catalog())"`.
   Si el tema necesita escenarios u objetos que no existen, créalos en `fabrica/visuals/world*.py`
   (funciones puras de `t`, registradas en `BACKGROUNDS` / `PROPS`) y pruébalos con un render rápido.

## 1 · Guion (`scripts/story_<tema>.py` → `stories/<slug>.json`)
Usa `scripts/storykit.py` (ver `scripts/story_luna.py` como ejemplo). Estructura obligatoria:
- **hook** (≤ 3 s): segunda persona, la situación ya ocurriendo, título-pregunta en pantalla.
- **setup** (3-15 s), **development** (15-40 s), **climax** (40-55 s), **ending**: giro + pregunta
  «… Te leo en comentarios.»
- 13-17 escenas de 2-4,5 s (8-14 palabras), 150-175 palabras (≈ 55-70 s con la voz de ElevenLabs acelerada un 12 %; ajusta `target_seconds` del vídeo a [50, 75]),
  o lo que indique la guía del nicho.
- Números escritos con palabras en la narración; las cifras con dígitos, en overlays.
- **Cada dato real en `claims` con su fuente**; lo imaginario como `fiction` (overlay «FICCIÓN» o
  «imagina…»); las hipótesis científicas con overlay `fiction` + `label: "HIPÓTESIS"`.
- Sincroniza props, overlays y efectos con `at_word` (índice de palabra de la escena).
- Metadatos: `title` (≤ 60 caracteres, empieza por «¿Qué pasaría si…»), `description` (gancho,
  datos reales, aviso de ficción, fuentes, pregunta, hashtags), `tags`, `pinned_comment`, `thumbnail`
  (escena, líneas de texto, etiqueta).
- Nombres extranjeros difíciles: añádelos a `tts.lexicon` en `config.yaml`.

## 2 · Voz: ElevenLabs «Mario» (obligatoria en todos los vídeos nuevos)
Orden del usuario (2026-11-23): todos los vídeos nuevos llevan la voz **Mario** de ElevenLabs
(`tts.eleven_connector` en `config.yaml`: voz `tomkxGQGz4b1kE0EM722`, modelo `eleven_v4`). Edge queda solo como respaldo
de vídeos antiguos. Se genera con el conector de ElevenLabs de Claude, una toma por escena:
1. `python3 scripts/story_<tema>.py` y `python3 scripts/voz_elevenlabs.py list <slug>`: da el texto exacto de cada escena y el
   total de caracteres (1 carácter = 1 crédito).
2. Carga las herramientas con ToolSearch (`mcp__ElevenLabs__account_get_usage`, `creative_generate_speech`,
   `creative_get_flow_run_status`). Con `account_get_usage` comprueba que quedan créditos de sobra. **Si no alcanzan
   (el plan gratuito da 10.000 al mes; un Short gasta ≈ 1.200 y un vídeo largo ≈ 16.000), NO cambies a otra voz sin
   decirlo: avisa al usuario y pregunta.**
3. Una llamada a `creative_generate_speech` por escena: `voice_id` y `model_id` de la config, `generations_count: 1`, y el
   mismo `flow_id` en todas. En el plan gratuito algunas salen con «generaciones ocupadas» (no se cobran): reinténtalas
   de una en una más tarde, nunca repitas una escena que ya arrancó.
4. Consulta con `creative_get_flow_run_status` hasta `all_completed` y descarga cada `content_url` con `curl` a una carpeta
   `<id_escena>.mp3` (el dominio `elevenlabsusercontent.com` debe estar en los hosts permitidos del entorno).
5. `python3 scripts/voz_elevenlabs.py apply <slug> <carpeta>`: acelera los clips y rellena `voice_clip` en la historia.
   `make` alinea las palabras con las pausas reales del audio. Una escena nueva o cambiada se vuelve a generar y a aplicar.

## 3 · Previsualizar y producir
```bash
python3 scripts/story_<tema>.py                       # exporta el JSON y valida índices de palabra
python -m fabrica still stories/<slug>.json all       # fotogramas de cada escena → output/<slug>/qa/
python -m fabrica make stories/<slug>.json            # música, escenas, subtítulos, render, QA (la voz ya está aplicada)
python -m fabrica regen <slug> s07                    # rehace solo una escena
python -m fabrica deliver <slug>                     # PARA_SUBIR/<NN>_<slug>/ (vídeo, miniatura, textos)
```
Revisa las imágenes (hoja de contactos `output/<slug>/qa/contact_sheet.jpg`) y corrige solapes,
textos cortados, elementos fuera de cuadro y personajes tapados antes de dar el vídeo por bueno.

## 4 · Control de calidad (debe pasar todo)
`output/<slug>/qa/report.md`: formato 1080×1920 H.264/AAC 30 fps, duración, WER de la voz,
silencios < 0,9 s, subtítulos sincronizados, música ≥ 10 dB bajo la voz, −14 LUFS, sin negros ni
congelados, escenas ≤ 5,5 s, gancho ≤ 4 s. Si una escena sale «dudosa» en el WER, reescribe la frase
o añade el término a `tts.lexicon`.

## 5 · Entrega
Entrega con `python -m fabrica deliver <slug>` (queda en `PARA_SUBIR/<NN>_<slug>/`; al publicarse, `python -m fabrica published <slug>` lo archiva en `samples/`), haz commit y push en la rama de trabajo, y envía al usuario el MP4, la
miniatura y `PUBLICAR.md`. Nada se publica sin `python -m fabrica approve <slug>`.
Indica qué datos conviene verificar si no se pudieron contrastar con fuentes en línea.
