# Diseño para retención y crecimiento

No se prometen visualizaciones: el sistema maximiza las probabilidades con decisiones medibles.

**En cada guion**
* Gancho ≤ 3 s, sin presentación; el título-pregunta aparece en pantalla en el primer fotograma
  con golpe sonoro y zoom (QA: `gancho rápido`).
* Escenas de 2-4,5 s (media ~3 s), cambio de plano o de acción constante (QA: `ritmo de escenas`, `dinamismo`).
* Curiosidad progresiva: cada escena abre un problema nuevo (profundidad creciente, medidor siempre visible).
* «Desmontar mitos» (sello ¡MITO!) y comparativas (núcleo vs Sol) = momentos compartibles.
* Final con giro + pregunta abierta → comentarios; el comentario fijado repite la pregunta.
* Ficción señalizada (tarjeta FICCIÓN) y datos con tarjeta DATO REAL y fuentes en la descripción → confianza.

**Entre vídeos**
* Registro SQLite (`data/registry.sqlite`) con todas las ideas: `ideas` descarta duplicados (similitud ≥ 0,6).
* Ranking de ideas por heurística (peligro, escala, visual, ciencia, novedad) + bonus de categorías con mejor
  retención real cuando hay métricas.
* `insights` resume qué ganchos, duraciones y categorías retienen más; el generador de guiones recibe esas
  pautas en su prompt.
* Mascota y paleta fijas (Leo + sudadera con «?») → identidad reconocible.

**Siguientes experimentos recomendados** (A/B entre vídeos): duración 45 vs 60 s; gancho-pregunta vs
gancho-afirmación; voz Kokoro vs ElevenLabs; con/sin título en pantalla en el primer segundo.
