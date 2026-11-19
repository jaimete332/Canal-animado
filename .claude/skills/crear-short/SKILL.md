---
name: crear-short
description: Crea un YouTube Short animado del canal «Hipotéticos» de principio a fin con la fábrica del repositorio — guion «¿qué pasaría si…?» con datos y fuentes, dirección visual en el DSL del motor, voz, render, control de calidad, miniatura, título, descripción y etiquetas. Úsala cuando el usuario pida uno o varios vídeos nuevos, un anuncio o regenerar una escena.
---

# Crear un Short con la fábrica

## 0 · Antes de escribir
1. Lee la guía del nicho: `data/research/style_guide.json` (la mantiene la skill `investigar-nicho`).
   Si tiene más de 30 días o no existe, propón actualizarla.
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
- 13-17 escenas de 2-4,5 s (8-14 palabras), 150-190 palabras (≈ 45-60 s con la voz Edge al +10 %),
  o lo que indique la guía del nicho.
- Números escritos con palabras en la narración; las cifras con dígitos, en overlays.
- **Cada dato real en `claims` con su fuente**; lo imaginario como `fiction` (overlay «FICCIÓN» o
  «imagina…»); las hipótesis científicas con overlay `fiction` + `label: "HIPÓTESIS"`.
- Sincroniza props, overlays y efectos con `at_word` (índice de palabra de la escena).
- Metadatos: `title` (≤ 60 caracteres, empieza por «¿Qué pasaría si…»), `description` (gancho,
  datos reales, aviso de ficción, fuentes, pregunta, hashtags), `tags`, `pinned_comment`, `thumbnail`
  (escena, líneas de texto, etiqueta).
- Nombres extranjeros difíciles: añádelos a `tts.lexicon` en `config.yaml`.

## 2 · Previsualizar y producir
```bash
python3 scripts/story_<tema>.py                       # exporta el JSON y valida índices de palabra
python -m fabrica still stories/<slug>.json all       # fotogramas de cada escena → output/<slug>/qa/
python -m fabrica make stories/<slug>.json            # voz, música, escenas, subtítulos, render, QA
python -m fabrica regen <slug> s07                    # rehace solo una escena
python3 scripts/publish_sheet.py <slug>               # samples/<slug>/ + PUBLICAR.md
```
Revisa las imágenes (hoja de contactos `output/<slug>/qa/contact_sheet.jpg`) y corrige solapes,
textos cortados, elementos fuera de cuadro y personajes tapados antes de dar el vídeo por bueno.

## 3 · Control de calidad (debe pasar todo)
`output/<slug>/qa/report.md`: formato 1080×1920 H.264/AAC 30 fps, duración, WER de la voz,
silencios < 0,9 s, subtítulos sincronizados, música ≥ 10 dB bajo la voz, −14 LUFS, sin negros ni
congelados, escenas ≤ 5,5 s, gancho ≤ 4 s. Si una escena sale «dudosa» en el WER, reescribe la frase
o añade el término a `tts.lexicon`.

## 4 · Entrega
Copia a `samples/<slug>/`, haz commit y push en la rama de trabajo, y envía al usuario el MP4, la
miniatura y `PUBLICAR.md`. Nada se publica sin `python -m fabrica approve <slug>`.
Indica qué datos conviene verificar si no se pudieron contrastar con fuentes en línea.
