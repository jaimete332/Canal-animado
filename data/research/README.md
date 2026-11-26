# Investigación del nicho

* `style_guide.json` — guía de estilo vigente (la leen el guionista y el banco de ideas). Se fusiona, no se sobrescribe:
  `style_guide.prev.json` guarda la versión anterior; `preferred_topics_locked` fija los temas curados a mano.
* `report_<fecha>.md` — informes de cada investigación del nicho (`python -m fabrica research`).
* `videos_<fecha>.json` / `analysis_<fecha>.json` — datos crudos y análisis de la competencia.
* `own_winners.json` — **los Shorts que mejor han funcionado en nuestro canal** (los declara el usuario o salen de las
  métricas) y las `lecciones` cualitativas que se han aprendido de ellos.
* `own_channel_<fecha>.md/.json` — ganadores frente al resto en rasgos medibles y arquetipos de premisa
  (`python -m fabrica research --own`).

Peso de las fuentes: propio con métricas > propio declarado > medido en la competencia (API) > observado (web).
Con pocos ganadores (n < 5) el análisis propio es una pista, no una prueba; ver la skill `investigar-nicho`.
