# Panel «Cola de publicación» (dos pestañas: Hipotéticos · Shorts ES y Stickpothetical · vídeos largos EN)

Artefacto: https://claude.ai/artifact/5bSfNZRkaBZDPC6LaHV1W8

* `index.html` — la página. `videos.json` — los datos (se generan con `build_videos_json.py` desde `PARA_SUBIR/`).
* Vídeos y miniaturas viven en el almacén de archivos del artefacto (máx. 20 MiB por archivo; si un vídeo
  pasa de ese tamaño se recomprime a ~18 MiB en dos pasadas, SSIM ≈ 0,997). Sus URL están en `assets.json`.
* Las marcas de «subido» se guardan en la base de datos del artefacto, colección `estado/<slug>`
  (`{subido: true, fecha}`), y Claude las puede leer para archivar lo publicado con `python -m fabrica published`.

Para añadir un vídeo: `python -m fabrica deliver <slug>`, añadir su fecha a `CALENDARIO`, subir vídeo y miniatura
como assets del artefacto, apuntar sus URL en `assets.json`, `python3 panel/build_videos_json.py panel/assets.json`
y volver a publicar `panel/index.html` con `videos.json`.

## Pestaña Stickpothetical (canal inglés)
* Datos: `videos_en.json`, generado con `python3 panel/build_videos_en_json.py panel/assets_en.json` desde `TO_UPLOAD/`
  (fechas en `CALENDARIO` de ese script, hora de España). Marcas de «subido» en la colección `estado_en/<slug>`.
* Los vídeos largos pasan de 20 MiB: se suben troceados (`split -b 18M -d -a 1 <slug>.mp4 <slug>.part_` y renombrar a
  `.mp4`) y el panel junta los trozos al descargar (el archivo es idéntico al original). Para verlo en el panel se
  sube además una versión ligera 960×540 (`preview`). Las URL van en `assets_en.json`.
* Los subtítulos se descargan como `<slug>_captions.srt.txt` (el panel no puede guardar `.srt`): quitar «.txt» antes de
  subirlos a YouTube. También están en `TO_UPLOAD/<NN>_<slug>/captions.srt`.
