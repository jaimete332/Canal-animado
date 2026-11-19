"""Guion: ¿Qué le pasaría a tu cuerpo 1 minuto sin casco en el espacio?

Escalada por segundos (0 → 5 → 10 → 15 → 60 → 90) con cronómetro en pantalla.
"""
from storykit import F, Story

st = Story()
sc = st.sc
EARTH = {"type": "space", "earth": {"x": 760, "y": 1650, "r": 520}}


def leo(**kw):
    d = {"x": 0.5, "y": 0.72, "scale": 1.25, "outfit": "suit", "action": "float"}
    d.update(kw)
    return d


def clock(sec, p0, p1, **kw):
    return {"type": "timer", "text": f"0:{sec:02d}" if sec < 60 else f"{sec // 60}:{sec % 60:02d}", "x": 870,
            "y": 300, "p0": p0, "p1": p1, "over": 1.5, **kw}


def lbl(txt, bg="#E8392F", **kw):
    return {"type": "label", "text": txt, "x": 400, "y": 300, "size": 72, "bg": bg, **kw}


sc("e01", "hook", "Estás en el espacio y te quitas el casco. Tienes un minuto.", {
    "background": EARTH,
    "character": leo(expression="smug", actions=[["w7", "shock"]], expressions=[["w7", "shock"]]),
    "props": [{"type": "helmet", "x": 0.78, "y": 0.4, "scale": 0.7, "at_word": 6, "enter": "pop", "loop": "spin",
               "spin": 0.6}],
    "overlays": [{"type": "title", "lines": ["¿1 MINUTO", "SIN CASCO?"], "y": 260, "size": 120}],
    "camera": {"move": "punch", "impacts": ["w7"]}},
   sfx=[{"name": "whoosh", "at_word": 6}, {"name": "hit", "at_word": 9, "gain_db": -6}], transition="cut",
   emphasis=["casco", "minuto"])

sc("e02", "setup", "Segundo cero: suelta el aire. Si lo aguantas, tus pulmones pueden romperse.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.6, "scale": 1.3, "hold": 1.0, "breathe": False, "enter": "pop",
               "loop": "shake", "at_word": 0}],
    "overlays": [lbl("SEGUNDO 0"), clock(0, 0, 0),
                 {"type": "fact", "label": "OJO", "text": "Aguantar la respiración al perder la presión puede dañar los pulmones",
                  "at_word": 5, "y": 470}],
    "camera": {"move": "push_in", "shake": 0.15}},
   claims=[F("Aguantar la respiración durante una descompresión rápida puede dañar gravemente los pulmones",
             "NASA, Bioastronautics Data Book (SP-3006)")],
   sfx=[{"name": "crack", "at_word": 9, "gain_db": -6}], emphasis=["suelta", "pulmones"])

sc("e03", "setup", "Ahí fuera no hay presión: el aire de tu pecho se expande de golpe.", {
    "background": EARTH,
    "character": leo(expression="surprised", extras={"swell": 0.3}),
    "props": [{"type": "bubbles", "x": 0.5, "y": 0.42, "at_word": 7}],
    "overlays": [{"type": "counter", "from": 101, "to": 0, "suffix": " kPa", "at_word": 2, "over": 1.0, "y": 300,
                  "size": 120, "sub": "PRESIÓN A TU ALREDEDOR"}],
    "camera": {"move": "pull_out"}},
   claims=[F("En el espacio la presión es prácticamente nula, frente a unos 101 kPa a nivel del mar", "NASA")],
   sfx=[{"name": "whoosh", "at_word": 9}], transition="whip", emphasis=["golpe"])

sc("e04", "development", "Segundo cinco: la saliva de tu lengua empieza a burbujear, como si hirviera.", {
    "background": EARTH,
    "character": leo(x=0.45, scale=1.5, y=0.82, expression="shock", extras={"swell": 0.4}),
    "props": [{"type": "bubbles", "x": 0.47, "y": 0.42, "at_word": 6}],
    "overlays": [lbl("SEGUNDO 5", "#FF8A00"), clock(5, 0, 5 / 60)],
    "camera": {"move": "push_in", "zoom_to": 1.35, "focus": [0.47, 0.42]}},
   claims=[F("Con presión casi nula, la saliva y las lágrimas empiezan a hervir a temperatura corporal",
             "NASA, Bioastronautics Data Book; testimonio de Jim LeBlanc (1966)")],
   sfx=[{"name": "sizzle", "at_word": 6, "gain_db": -6}], emphasis=["burbujear"])

sc("e05", "development", "No es calor: sin presión, el agua hierve a la temperatura de tu cuerpo.", {
    "background": {"type": "burst", "c1": "#5CE1E6", "c2": "#8FF0F5"},
    "character": {"visible": False},
    "props": [{"type": "thermometer", "x": 0.3, "y": 0.62, "scale": 1.5, "level": 0.45},
              {"type": "bubbles", "x": 0.68, "y": 0.6, "at_word": 6}],
    "overlays": [{"type": "fact", "text": "Por encima de unos 19 km de altura, el agua hierve a 37 °C (límite de Armstrong)",
                  "at_word": 5, "y": 230},
                 {"type": "label", "text": "37 °C", "x": 700, "y": 1080, "size": 110, "bg": "#2B6BE8", "at_word": 11}],
    "camera": {"move": "push_in"}},
   claims=[F("A partir de unos 19 km de altura (límite de Armstrong) el agua hierve a la temperatura del cuerpo",
             "NASA; Federal Aviation Administration")],
   sfx=[{"name": "sizzle", "at_word": 6, "gain_db": -8}, {"name": "ding", "at_word": 11}], transition="zoom",
   emphasis=["calor", "cuerpo"])

sc("e06", "development", "Pero tu sangre no hierve: tus venas la mantienen a presión.", {
    "background": {"type": "burst", "c1": "#22B573", "c2": "#6EE7A8"},
    "character": {"visible": False},
    "props": [{"type": "heart", "x": 0.5, "y": 0.6, "scale": 1.4, "bpm": 110, "enter": "pop"}],
    "overlays": [{"type": "myth", "text": "TE HIERVE LA SANGRE", "stamp": "¡FALSO!", "y": 330, "stamp_at": 1.0}],
    "camera": {"move": "static"}},
   claims=[F("La sangre no llega a hervir porque la presión del sistema circulatorio la mantiene líquida",
             "NASA, Bioastronautics Data Book (SP-3006)")],
   sfx=[{"name": "hit", "at": 1.0, "gain_db": -6}], transition="slide", emphasis=["sangre"])

sc("e07", "development", "Segundo diez: tu piel se hincha, pero no explotas como en las películas.", {
    "background": EARTH,
    "character": leo(expression="dizzy", extras={"swell": 1.0}, scale_keys=[[0, 1.25], ["w5", 1.4]]),
    "overlays": [lbl("SEGUNDO 10", "#9D7BFF"), clock(10, 5 / 60, 10 / 60),
                 {"type": "fact", "text": "El cuerpo puede hincharse mucho (ebullismo), pero la piel resiste: no se revienta",
                  "at_word": 6, "y": 470}],
    "camera": {"move": "push_in"}},
   claims=[F("El ebullismo puede hinchar el cuerpo hasta casi el doble, pero los tejidos son lo bastante elásticos para no romperse",
             "NASA, Bioastronautics Data Book (SP-3006)")],
   sfx=[{"name": "boing", "at_word": 5, "gain_db": -6}], emphasis=["hincha", "explotas"])

sc("e08", "development", "Tampoco te congelas al momento: en el vacío, el calor se escapa muy despacio.", {
    "background": EARTH,
    "character": leo(x=0.35, expression="surprised", extras={"swell": 0.8}),
    "props": [{"type": "thermometer", "x": 0.78, "y": 0.55, "scale": 1.1, "level": 0.6}],
    "overlays": [{"type": "myth", "text": "TE CONGELAS AL INSTANTE", "stamp": "¡FALSO!", "y": 330, "stamp_at": 1.2}],
    "camera": {"move": "static"}},
   claims=[F("En el vacío no hay aire que robe el calor; el cuerpo se enfría lentamente, sobre todo por radiación",
             "NASA")],
   sfx=[{"name": "hit", "at": 1.2, "gain_db": -6}], transition="whip", emphasis=["congelas"])

sc("e09", "climax", "Segundo quince: el cerebro se queda sin oxígeno y te desmayas.", {
    "background": EARTH,
    "character": leo(expression="dizzy", extras={"swell": 0.9}, actions=[["w8", "fall"]],
                     expressions=[["w8", "happy_closed"]]),
    "props": [{"type": "brain", "x": 0.78, "y": 0.42, "scale": 0.6, "dirt": 0.6, "at_word": 3, "loop": "wobble"}],
    "overlays": [lbl("SEGUNDO 15", "#E8392F"), clock(15, 10 / 60, 15 / 60),
                 {"type": "fact", "text": "Consciencia útil sin presión: unos 10-15 segundos", "at_word": 4, "y": 470}],
    "camera": {"move": "push_in", "tilt": 0.06}},
   claims=[F("Con exposición al vacío se pierde la consciencia en unos 10-15 segundos", "NASA, Bioastronautics Data Book (SP-3006)")],
   sfx=[{"name": "fall", "at_word": 8, "gain_db": -6}], transition="flash", emphasis=["desmayas"])

sc("e10", "climax", "Le pasó de verdad a Jim LeBlanc en mil novecientos sesenta y seis, en una cámara de vacío de la NASA.", {
    "background": {"type": "office"},
    "character": {"visible": False},
    "props": [{"type": "vacuum_chamber", "x": 0.5, "y": 0.58, "scale": 1.15, "gauge": 0.05, "enter": "pop"}],
    "overlays": [{"type": "label", "text": "JIM LEBLANC · NASA · 1966", "x": 540, "y": 300, "size": 64, "at_word": 4,
                  "bg": "#2B6BE8"}],
    "camera": {"move": "push_in"}},
   claims=[F("El 14 de diciembre de 1966, el traje del técnico de la NASA Jim LeBlanc perdió presión dentro de una cámara de vacío en Houston",
             "NASA; Guinness World Records")],
   sfx=[{"name": "ding", "at_word": 4}], transition="zoom", emphasis=["verdad"])

sc("e11", "climax", "Su traje perdió el aire. Lo último que recordó fue la saliva burbujeando.", {
    "background": {"type": "office"},
    "character": {"visible": False},
    "props": [{"type": "vacuum_chamber", "x": 0.5, "y": 0.58, "scale": 1.15, "gauge": 0.0, "enter": "none",
               "loop": "shake"},
              {"type": "bubbles", "x": 0.5, "y": 0.42, "at_word": 9}],
    "overlays": [{"type": "fact", "text": "Contó que notó la saliva burbujear en la lengua justo antes de desmayarse",
                  "at_word": 5, "y": 230}],
    "camera": {"move": "push_in", "zoom_to": 1.25, "focus": [0.5, 0.45], "shake": 0.1}},
   claims=[F("LeBlanc recordó notar la saliva burbujear en la lengua antes de perder el conocimiento a los ~14 s",
             "NASA (entrevista a Jim LeBlanc)")],
   sfx=[{"name": "sizzle", "at_word": 9, "gain_db": -6}], emphasis=["saliva"])

sc("e12", "climax", "Le devolvieron el aire en menos de un minuto y medio, y despertó sin secuelas.", {
    "background": {"type": "burst", "c1": "#22B573", "c2": "#6EE7A8"},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "suit", "hat": "dome", "x": 0.5, "y": 0.86, "size": 1.3,
               "expression": "happy", "action": "celebrate", "shirt": "#FFFFFF", "enter": "pop"}],
    "overlays": [{"type": "counter", "from": 0, "to": 87, "suffix": " s", "at_word": 4, "over": 0.8, "y": 330,
                  "size": 130, "sub": "HASTA RECUPERAR LA PRESIÓN"}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("La cámara se represurizó en unos 87 segundos y LeBlanc se recuperó sin daños duraderos",
             "Guinness World Records; NASA")],
   sfx=[{"name": "sparkle", "at_word": 12}], transition="flash", emphasis=["despertó"])

sc("e13", "climax", "Segundo sesenta: tu corazón aún late, aunque cada vez más despacio.", {
    "background": EARTH,
    "character": leo(y=0.68, action="float", expression="happy_closed", extras={"swell": 1.0}),
    "props": [{"type": "heart", "x": 0.8, "y": 0.4, "scale": 0.55, "bpm": 35, "cold": 0.3}],
    "overlays": [lbl("SEGUNDO 60", "#E8392F"), clock(60, 15 / 60, 1.0)],
    "camera": {"move": "push_in"}},
   claims=[F("En experimentos con perros, el corazón seguía latiendo, muy despacio, tras 90 segundos de vacío",
             "NASA, Bioastronautics Data Book (SP-3006)")],
   sfx=[{"name": "tick", "at": 0.2}], transition="whip", emphasis=["late"])

sc("e14", "ending", "En experimentos con animales, casi todos se recuperaban si volvía la presión antes del minuto y medio.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "overlays": [{"type": "counter", "from": 0, "to": 90, "suffix": " s", "at_word": 13, "over": 0.8, "y": 700,
                  "size": 170, "sub": "EL LÍMITE PARA RECUPERARSE"},
                 {"type": "fact", "text": "Con menos de 90 s de vacío, los animales solían recuperarse por completo",
                  "at_word": 3, "y": 230}],
    "props": [{"type": "clock", "x": 0.5, "y": 0.57, "scale": 0.85, "at_word": 10}],
    "camera": {"move": "push_in"}},
   claims=[F("Los datos con animales indican recuperación completa con exposiciones al vacío de menos de 90 segundos; más allá de 2 minutos las muertes eran frecuentes",
             "NASA, Bioastronautics Data Book (SP-3006)")],
   sfx=[{"name": "ding", "at_word": 13}], emphasis=["minuto", "medio"])

sc("e15", "ending", "Por desgracia, en mil novecientos setenta y uno la Soyuz once perdió el aire, y sus tres cosmonautas murieron.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "rocket", "x": 0.5, "y": 0.55, "scale": 0.9, "enter": "fade", "loop": "bob"}],
    "overlays": [{"type": "fact", "label": "EN MEMORIA", "text": "Soyuz 11 (1971): las únicas personas fallecidas en el espacio",
                  "at_word": 7, "y": 230}],
    "camera": {"move": "pull_out"}},
   claims=[F("En 1971 la Soyuz 11 se despresurizó durante el regreso y murieron sus tres cosmonautas: las únicas muertes ocurridas en el espacio",
             "NASA; ESA")],
   transition="circle", emphasis=["Soyuz"])

sc("e16", "ending", "Así que un minuto sin casco no es el final… si alguien te rescata a tiempo.", {
    "background": EARTH,
    "character": leo(action="float", expression="happy", extras={"swell": 0.4}),
    "props": [{"type": "helmet", "x": 0.78, "y": 0.4, "scale": 0.7, "loop": "spin", "spin": 0.6, "enter": "none"},
              {"type": "habitat", "x": 0.22, "y": 0.35, "scale": 0.6, "at_word": 9, "enter": "slide_left"}],
    "overlays": [{"type": "timer", "text": "1:00", "x": 870, "y": 300, "p0": 1.0, "p1": 1.0}],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "sparkle", "at_word": 9}], transition="slide", emphasis=["rescata"])

sc("e17", "ending", "¿Tú saldrías al espacio? Te leo en comentarios.", {
    "background": EARTH,
    "character": leo(action="talk", expression="excited", helmet="dome", scale=1.3, actions=[["w4", "point_down"]]),
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 4, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 4}], transition="zoom", pause=0.35)

DESC = """Estás en el espacio y te quitas el casco… ¿qué le pasaría a tu cuerpo en un minuto? 🧑‍🚀

Leo flota junto a la Tierra sin casco y descubre, segundo a segundo, lo que hace el vacío: la saliva que burbujea, la piel que se hincha… y la historia real de Jim LeBlanc, el técnico de la NASA que lo vivió en 1966.

🧪 DATOS REALES DEL VÍDEO
• Lo primero es soltar el aire: aguantar la respiración en una descompresión puede dañar los pulmones.
• Por encima de unos 19 km (límite de Armstrong), el agua hierve a 37 °C: la saliva y las lágrimas burbujean.
• La sangre no hierve: la presión del sistema circulatorio la mantiene líquida.
• El cuerpo se hincha (ebullismo), pero la piel resiste: no explotas.
• No te congelas al instante: en el vacío el calor se pierde despacio.
• Se pierde la consciencia en unos 10-15 segundos.
• En 1966, el traje de Jim LeBlanc perdió presión en una cámara de vacío de la NASA; tras unos 87 s se recuperó la presión y despertó sin secuelas.
• Con animales, la recuperación era completa con menos de 90 s de vacío.
• En 1971, la Soyuz 11 se despresurizó y murieron sus tres cosmonautas: las únicas muertes ocurridas en el espacio.

📚 Fuentes: NASA (Bioastronautics Data Book, SP-3006), Guinness World Records, ESA, FAA.

💬 ¿Tú saldrías al espacio? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #espacio #cuerpohumano #astronauta #shorts"""

st.save("sin-casco-en-el-espacio", "¿Qué le pasaría a tu cuerpo 1 minuto sin casco en el espacio?",
        "¿Qué le pasaría a tu cuerpo 1 minuto sin casco en el espacio?", "espacio",
        "¿Tú saldrías al espacio?", {
            "title": "¿Qué pasaría si te quitaras el casco en el espacio? 🧑‍🚀",
            "hashtags": ["#quepasariasi", "#espacio", "#cuerpohumano", "#astronauta", "#shorts"],
            "tags": ["qué pasaría si", "espacio", "sin casco", "vacío", "astronauta", "nasa", "jim leblanc",
                     "ebullismo", "cuerpo humano", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Cuántos segundos crees que aguantarías tú? ⏱️👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "e07", "t": 1.8, "lines": ["¿1 MINUTO", "SIN CASCO?"],
                          "badge": "SEGUNDO 10: TE HINCHAS", "badge_pos": [540, 1640], "y": 260,
                          "character": {"action": "float", "expression": "shock", "x": 0.5, "y": 0.78, "scale": 1.45,
                                        "outfit": "suit", "extras": {"swell": 1.0}},
                          "crop_y": 0.55, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
