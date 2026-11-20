---
name: crear-video-stickman
description: Crea un vídeo largo (8-12 min, 16:9) en inglés para el canal de stickman «Stickpothetical» — guion «what if / could you survive» con capítulos, datos y fuentes, dirección visual en el DSL del motor stickman, voz en inglés, render, control de calidad, miniatura 1280x720, subtítulos .srt, título, descripción con capítulos y etiquetas. Úsala cuando el usuario pida vídeos en inglés, de stickman, largos o para el segundo canal.
---

# Crear un vídeo largo de stickman (canal inglés)

Todo comando de la fábrica lleva `--channel stickman_en` (perfil `channels/stickman_en.yaml`).
Identidad del canal y nicho: `docs/CANAL_EN.md`. Ejemplo completo de guion: `scripts/en_story_medieval_peasant.py`.

## 1 · Guion (`scripts/en_story_<tema>.py` → `stories_en/<slug>.json`)
Usa `scripts/storykit_en.py` (`Story`, `cast`, `F`, `st.chapter("…")`).
- **Duración:** 1.450-1.900 palabras ≈ 8-12 min con la voz Andrew a +0 % y `pause_scale` 1,7. Nunca menos de 8 min
  (anuncios a mitad de vídeo). 85-130 escenas de 6-25 palabras (máx. 9 s cada una).
- **Gancho (≤ 30 s):** segunda persona («you wake up…»), la situación ya ocurriendo, la promesa del vídeo y un
  giro («of all years, this is the worst one»). Medidor `meter` de «STAN'S SURVIVAL ODDS» que vuelve en cada capítulo.
- **Capítulos:** 6-9, cada uno abierto con `st.chapter("Title")`; títulos cortos y con intriga. Se convierten en
  marcas de tiempo de la descripción y cambian el ambiente musical (`metadata.chapter_moods`).
- **Cierre:** recapitulación (checklist), el giro histórico final, pregunta para comentarios y llamada a suscribirse.
- **Stan** (bufanda roja) es siempre el protagonista; el reparto recurrente está en `PRESETS` de `fabrica/stick/scene.py`
  (peasant, peasant_woman, lord, king, priest, bishop, knight, reeve, doctor, child, modern).
- **Datos:** cada hecho en `claims` con fuente real (libro o institución); estimaciones como `estimate` y con
  lenguaje prudente («historians estimate», «around»). La ficción de Stan como `fiction` y la etiqueta `STAN'S STORY`
  de vez en cuando. Incluye 1-2 bloques de «myth busting»: retienen muy bien.
- Números en la narración: años con cifras (se leen como «thirteen forty-eight»), el resto mejor en palabras.
- Varía el plano cada escena: fondo (`village`, `field`, `interior`, `church`, `town`, `manor`, `castle`, `map`,
  `chalkboard`, `paper`, `solid`, `forest`, `split`), cámara (`push_in`, `pan_*`, `punch`, `zoom_to`, `focus`) y
  overlays de datos (`fact`, `stat`, `bars`, `people`, `checklist`, `counter`, `meter`, `timeline`, `quote`, `label`).
  Sincroniza con `at_word`/`"wN"`; el kit valida los índices al exportar.
- Metadatos: `title` (≤ 60 caracteres, curiosidad + época), `description_intro`, `hashtags` (3), `tags` (15-20),
  `pinned_comment`, `intro_chapter`, `chapter_moods`, `thumbnail` (+ `thumbnail_alts` para el test A/B de YouTube).
  Miniatura: 2 líneas de texto MUY grandes (≤ 4 palabras cada una), Stan grande con emoción clara y un badge.

## 2 · Previsualizar, producir y revisar
```bash
python3 scripts/en_story_<tema>.py
python -m fabrica --channel stickman_en still stories_en/<slug>.json all   # PNG por escena en output/stickman_en/<slug>/qa/
python -m fabrica --channel stickman_en make stories_en/<slug>.json
python -m fabrica --channel stickman_en regen <slug> s07 s08
```
Mira TODAS las escenas (hojas de contactos) y corrige: personajes tapados por edificios, figuras fuera de cuadro,
textos que se solapan (contador de mes vs. timeline, fact vs. title), objetos demasiado pequeños.

## 3 · Control de calidad (`output/stickman_en/<slug>/qa/report.md`)
1920×1080 H.264/AAC 30 fps, duración 7-18 min, WER de la voz en inglés, **una sola voz** (si Edge falla, se reintenta;
nunca se mezcla con otra voz), silencios, música ≥ 10 dB bajo la voz, −14 LUFS, sin negros ni congelados.

## 4 · Entrega
`python -m fabrica --channel stickman_en deliver <slug>` → `TO_UPLOAD/<NN>_<slug>/` (MP4, `thumbnail.png`,
`captions.srt`, `PUBLISH.md`, `texts.txt`). Commit y push en la rama de trabajo y envía al usuario el MP4,
la miniatura y `PUBLISH.md`. Nada se publica sin `approve`.
