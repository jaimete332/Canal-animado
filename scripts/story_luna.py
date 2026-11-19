"""Guion: ¿Qué pasaría si la Luna desapareciera?"""
from storykit import F, Story

st = Story()
sc = st.sc
LEO_PJ = {"outfit": "pajamas", "helmet": "nightcap"}

sc("l01", "hook", "Esta noche miras al cielo… y la Luna ha desaparecido.", {
    "background": {"type": "night_sky", "moon": False},
    "character": {"action": "look_up", "expression": "surprised", "x": 0.5, "y": 0.78, "scale": 1.2,
                  "expressions": [["w6", "shock"]], "actions": [["w6", "shock"]], **LEO_PJ},
    "props": [{"type": "moon", "x": 0.65, "y": 0.22, "r": 130, "until_word": 6, "enter": "none"},
              {"type": "question", "x": 0.65, "y": 0.22, "at_word": 6, "size": 260}],
    "overlays": [{"type": "flash", "at_word": 6, "over": 0.3},
                 {"type": "title", "lines": ["¿Y SI LA LUNA", "DESAPARECIERA?"], "y": 1460, "size": 100}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   claims=[F("Que la Luna desaparezca de golpe es una hipótesis imposible", "Licencia narrativa", "fiction")],
   sfx=[{"name": "pop", "at_word": 6}, {"name": "hit", "at_word": 6, "gain_db": -6}], transition="cut",
   emphasis=["luna"])

sc("l02", "setup", "Primero lo notarías en la playa: las mareas se quedarían en un tercio.", {
    "background": {"type": "beach", "tide": 1.0, "tide_speed": 2.0},
    "character": {"action": "point_down", "expression": "surprised", "x": 0.72, "y": 0.62, "scale": 1.0,
                  "outfit": "casual"},
    "overlays": [{"type": "counter", "from": 100, "to": 33, "suffix": " %", "at_word": 9, "over": 0.8, "y": 330,
                  "sub": "DE MAREA"}],
    "camera": {"move": "push_in"}},
   claims=[F("Sin la Luna solo quedarían las mareas solares, aproximadamente un tercio de las actuales", "NOAA (Tides and Water Levels)", "estimate")],
   sfx=[{"name": "splash", "at": 0.3, "gain_db": -8}, {"name": "ding", "at_word": 9}], emphasis=["tercio"])

sc("l03", "setup", "Porque es la Luna la que más tira del mar. El Sol también, pero menos de la mitad.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "earth", "x": 0.5, "y": 0.55, "r": 170, "enter": "none"},
              {"type": "moon", "x": 0.82, "y": 0.3, "r": 80, "enter": "pop", "until_word": 9},
              {"type": "arrow", "x": 0.68, "y": 0.42, "rot": -0.75, "scale": 0.6, "color": "#5CE1E6", "until_word": 9},
              {"type": "sun", "x": 0.18, "y": 0.22, "scale": 0.6, "at_word": 9},
              {"type": "arrow", "x": 0.32, "y": 0.38, "rot": 0.85, "scale": 0.35, "at_word": 9, "color": "#FFD23F"}],
    "camera": {"move": "push_in"}},
   claims=[F("La fuerza de marea del Sol es algo menos de la mitad (~46 %) que la de la Luna", "NOAA")],
   sfx=[{"name": "whoosh", "at_word": 9}], transition="zoom", emphasis=["mitad"])

sc("l04", "development", "Las noches serían mucho más oscuras. Adiós a la luna llena.", {
    "background": {"type": "night_sky", "moon": False},
    "character": {"action": "sweat", "expression": "scared", "x": 0.5, "y": 0.78, "scale": 1.15, **LEO_PJ},
    "overlays": [{"type": "vignette", "alpha": 0.8}],
    "camera": {"move": "push_in", "zoom_to": 1.15}},
   claims=[F("La luna llena es, con diferencia, la mayor fuente de luz natural de noche", "NASA")],
   transition="circle", emphasis=["oscuras"])

sc("l05", "development", "Y muchos animales se liarían: los corales de la Gran Barrera se reproducen guiándose por la Luna.", {
    "background": {"type": "underwater", "floor": 1800},
    "character": {"visible": False},
    "props": [{"type": "coral", "x": 0.5, "y": 0.86, "spawn": True, "enter": "none", "scale": 1.2}],
    "overlays": [{"type": "fact", "text": "Los corales de la Gran Barrera de Coral desovan en masa según el ciclo lunar",
                  "at_word": 5}],
    "camera": {"move": "pan_up", "amount": 140}},
   claims=[F("El desove masivo de la Gran Barrera de Coral se sincroniza con la luna llena", "Australian Institute of Marine Science")],
   sfx=[{"name": "sparkle", "at_word": 8}], emphasis=["corales"])

sc("l06", "development", "Y nunca más habría eclipses totales de Sol, esos que convierten el día en noche durante unos minutos.", {
    "background": {"type": "night_sky", "moon": False},
    "character": {"visible": False},
    "props": [{"type": "eclipse", "x": 0.5, "y": 0.42, "r": 220, "enter": "pop", "crossed": True, "cross_at": 1.0,
               "cross_r": 260}],
    "camera": {"move": "push_in"}},
   claims=[F("Los eclipses totales de Sol ocurren porque la Luna tapa el disco solar", "NASA")],
   sfx=[{"name": "crack", "at": 1.0}], transition="flash", emphasis=["eclipses"])

sc("l07", "development", "Pero lo más grave llegaría a lo largo de millones de años.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "clock", "x": 0.5, "y": 0.5, "speed": 30, "scale": 1.5},
              {"type": "earth", "x": 0.5, "y": 0.82, "r": 90, "enter": "none"}],
    "overlays": [{"type": "label", "text": "MILLONES DE AÑOS", "x": 540, "y": 330, "size": 74, "at_word": 6,
                  "bg": "#9D7BFF"}],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "clock", "at": 0.1, "gain_db": -4}, {"name": "riser", "at": 1.2, "gain_db": -6}],
   emphasis=["millones"])

sc("l08", "climax", "La Luna estabiliza el eje de la Tierra, como el peso que equilibra una peonza.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "earth", "x": 0.5, "y": 0.4, "r": 170, "axis": 23, "wobble": 2, "enter": "none"},
              {"type": "moon", "x": 0.82, "y": 0.22, "r": 60, "enter": "none"},
              {"type": "top", "x": 0.5, "y": 0.8, "scale": 0.9, "wobble": 0.05, "at_word": 10}],
    "overlays": [{"type": "label", "text": "EJE: 23,5°", "x": 540, "y": 1160, "size": 60, "at_word": 4, "bg": "#2B6BE8"}],
    "camera": {"move": "push_in"}},
   claims=[F("La Luna estabiliza la inclinación del eje terrestre (~23,5°)", "Laskar et al., Nature (1993); NASA")],
   sfx=[{"name": "pop", "at_word": 10}], transition="slide", emphasis=["eje", "peonza"])

sc("l09", "climax", "Sin ella, según algunos estudios, el eje podría tambalearse y descontrolar las estaciones.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "earth", "x": 0.5, "y": 0.4, "r": 170, "axis": 23, "wobble": 30, "enter": "none"},
              {"type": "top", "x": 0.5, "y": 0.8, "scale": 0.9, "wobble": 1.0, "enter": "none"}],
    "overlays": [{"type": "fiction", "label": "HIPÓTESIS", "text": "Estudios como el de Laskar (1993) apuntan a cambios caóticos del eje",
                  "at_word": 2}],
    "camera": {"move": "static", "shake": 0.3}},
   claims=[F("Sin la Luna la inclinación del eje podría variar de forma caótica (debate abierto)", "Laskar et al., Nature (1993)", "estimate")],
   sfx=[{"name": "rumble", "at": 0.2, "gain_db": -6}], emphasis=["tambalearse", "estaciones"])

sc("l10", "climax", "Imagina inviernos y veranos extremos que cambian de una era a otra.", {
    "background": {"type": "burst", "c1": "#5CE1E6", "c2": "#FF9F1C"},
    "character": {"action": "squished", "expression": "scared", "x": 0.5, "y": 0.72, "scale": 1.25, "outfit": "casual",
                  "sweat": 1},
    "props": [{"type": "thermometer", "x": 0.18, "y": 0.42, "level": 0.1, "text": "-50 °C", "text_color": "#5CE1E6"},
              {"type": "thermometer", "x": 0.82, "y": 0.42, "level": 0.95, "text": "+50 °C", "at_word": 3}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "boing", "at_word": 3}], transition="flash", emphasis=["extremos"])

sc("l11", "ending", "Por cierto, la Luna ya se aleja de nosotros casi cuatro centímetros cada año.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "earth", "x": 0.25, "y": 0.6, "r": 120, "enter": "none"},
              {"type": "moon", "x": 0.7, "y": 0.45, "r": 70, "enter": "none", "loop": "bob"},
              {"type": "arrow", "x": 0.85, "y": 0.4, "rot": -0.3, "scale": 0.45, "at_word": 6}],
    "overlays": [{"type": "counter", "from": 0, "to": 3.8, "decimals": 1, "suffix": " cm/año", "at_word": 8, "over": 0.6,
                  "y": 330}],
    "camera": {"move": "pan_right", "amount": 100}},
   claims=[F("La Luna se aleja unos 3,8 cm al año (medido con láser)", "NASA (Lunar Laser Ranging)")],
   sfx=[{"name": "ding", "at_word": 8}], transition="zoom", emphasis=["centímetros"])

sc("l12", "ending", "Así que, en cierto modo, la Luna ya se está despidiendo de nosotros.", {
    "background": {"type": "night_sky", "moon": True},
    "character": {"action": "wave", "expression": "happy", "x": 0.5, "y": 0.78, "scale": 1.15, **LEO_PJ},
    "camera": {"move": "pull_out", "zoom_from": 1.2}},
   sfx=[{"name": "float", "at": 0.0}], transition="circle", emphasis=["despidiendo"])

sc("l13", "ending", "¿Tú la echarías de menos? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#2B2D6E", "c2": "#3D3F8F"},
    "character": {"action": "talk", "expression": "excited", "x": 0.5, "y": 0.64, "scale": 1.35, "enter": "pop",
                  "actions": [["w5", "point_down"]], **LEO_PJ},
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Esta noche miras al cielo… y la Luna ha desaparecido. ¿Qué cambiaría en la Tierra? 🌙

Leo descubre todo lo que hace la Luna por nosotros: las mareas, las noches, los corales, los eclipses… y algo mucho más importante que no se ve.

🧪 DATOS REALES DEL VÍDEO
• La Luna es la principal causante de las mareas; el Sol también las provoca, pero con algo menos de la mitad de fuerza. Sin la Luna, las mareas serían aproximadamente un tercio de las actuales.
• Las noches serían mucho más oscuras: la luna llena es la mayor fuente de luz natural nocturna.
• Los corales de la Gran Barrera de Coral sincronizan su desove masivo con el ciclo lunar.
• Sin Luna no habría eclipses totales de Sol.
• La Luna ayuda a estabilizar la inclinación del eje terrestre (unos 23,5°); según algunos estudios, sin ella podría variar de forma caótica a lo largo de millones de años (es un debate científico abierto).
• La Luna se aleja de la Tierra unos 3,8 cm cada año.

⚠️ Que la Luna desaparezca es imposible: es una situación hipotética. Los datos son reales y aproximados.

📚 Fuentes: NASA, NOAA, Australian Institute of Marine Science, Laskar et al. (Nature, 1993).

💬 ¿Tú la echarías de menos? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #luna #espacio #ciencia #shorts"""

st.save("la-luna-desapareciera", "¿Qué pasaría si la Luna desapareciera?", "¿Qué pasaría si la Luna desapareciera?",
        "espacio", "¿Tú la echarías de menos?", {
            "title": "¿Qué pasaría si la Luna desapareciera? 🌙",
            "hashtags": ["#quepasariasi", "#luna", "#espacio", "#ciencia", "#shorts"],
            "tags": ["qué pasaría si", "luna", "si la luna desapareciera", "mareas", "eclipse", "eje de la tierra",
                     "espacio", "astronomía", "ciencia", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Tú echarías de menos a la Luna? 🌙👇",
            "description": DESC,
            "thumbnail": {"scene": "l01", "t": 0.9, "lines": ["¿Y SI LA LUNA", "DESAPARECIERA?"],
                          "badge": "¡PASARÍA ESTO!", "badge_pos": [540, 1640], "y": 260, "drop_props": ["moon", "question"],
                          "props": [{"type": "moon", "x": 0.5, "y": 0.4, "r": 150, "crossed": True, "cross_at": 0,
                                     "cross_r": 190, "enter": "none"}],
                          "character": {"action": "shock", "expression": "shock", "y": 0.82, "scale": 1.35},
                          "crop_y": 0.55, "h_shift": 860, "h_scale": 0.8},
        }, mood="mystery")
