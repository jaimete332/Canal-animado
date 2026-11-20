# Panel «Cola de publicación»

Artefacto: https://claude.ai/artifact/5bSfNZRkaBZDPC6LaHV1W8

* `index.html` — la página. `videos.json` — los datos (se generan con `build_videos_json.py` desde `PARA_SUBIR/`).
* Vídeos y miniaturas viven en el almacén de archivos del artefacto (máx. 20 MiB por archivo; si un vídeo
  pasa de ese tamaño se recomprime a ~18 MiB en dos pasadas, SSIM ≈ 0,997). Sus URL están en `assets.json`.
* Las marcas de «subido» se guardan en la base de datos del artefacto, colección `estado/<slug>`
  (`{subido: true, fecha}`), y Claude las puede leer para archivar lo publicado con `python -m fabrica published`.

Para añadir un vídeo: `python -m fabrica deliver <slug>`, añadir su fecha a `CALENDARIO`, subir vídeo y miniatura
como assets del artefacto, apuntar sus URL en `assets.json`, `python3 panel/build_videos_json.py panel/assets.json`
y volver a publicar `panel/index.html` con `videos.json`.
