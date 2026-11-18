"""Guion: ¿Qué pasaría si te tragara una ballena?"""
from storykit import F, Story

st = Story()
sc = st.sc
DIVER = {"helmet": "diving", "outfit": "casual"}

sc("b01", "hook", "Estás buceando tan tranquilo… y una ballena se te traga.", {
    "background": {"type": "underwater", "floor": 1750},
    "character": {"action": "swim", "expression": "happy", "x": 0.45, "y": 0.78, "scale": 1.05,
                  "expressions": [["w5", "scared"]], "actions": [["w5", "shock"]], **DIVER},
    "props": [{"type": "whale", "x": 0.5, "y": 0.45, "scale": 0.85, "mouth_anim": True, "at_word": 4,
               "enter": "slide_right", "enter_dur": 0.5},
              {"type": "bubbles", "x": 0.5, "y": 0.68, "enter": "none", "layer": "front"}],
    "overlays": [{"type": "title", "lines": ["¿Y SI TE TRAGA", "UNA BALLENA?"], "y": 250, "size": 112}],
    "camera": {"move": "punch", "impacts": ["w8"]}},
   sfx=[{"name": "splash", "at": 0.0, "gain_db": -6}, {"name": "whoosh", "at_word": 4}, {"name": "gulp", "at_word": 8}],
   transition="cut", emphasis=["ballena"])

sc("b02", "setup", "La buena noticia: casi ninguna ballena podría tragarte.", {
    "background": {"type": "burst", "c1": "#2BAE66", "c2": "#46C982"},
    "character": {"action": "celebrate", "expression": "laugh", "x": 0.5, "y": 0.64, "scale": 1.3, "enter": "pop",
                  **DIVER},
    "overlays": [{"type": "label", "text": "¡BUENA NOTICIA!", "x": 540, "y": 320, "size": 76, "bg": "#2B6BE8"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "sparkle", "at": 0.1}], transition="flash", emphasis=["buena"])

sc("b03", "setup", "La ballena azul es el animal más grande que ha existido, pero su garganta es muy estrecha.", {
    "background": {"type": "underwater", "floor": 2400, "deep": 0.2},
    "character": {"action": "swim", "expression": "wow", "x": 0.25, "y": 0.8, "scale": 0.6, **DIVER},
    "props": [{"type": "whale", "x": 0.55, "y": 0.42, "scale": 1.0, "color": "#4C6E9E", "enter": "slide_right",
               "enter_dur": 0.8, "loop": "bob"},
              {"type": "arrow", "x": 0.82, "y": 0.56, "rot": 2.3, "scale": 0.5, "at_word": 13, "color": "#E8392F"}],
    "overlays": [{"type": "label", "text": "BALLENA AZUL · HASTA 30 m", "x": 540, "y": 300, "size": 62, "at_word": 2},
                 {"type": "fact", "text": "Su garganta es demasiado estrecha para tragarse a una persona", "at_word": 11,
                  "y": 230}],
    "camera": {"move": "pull_out", "zoom_from": 1.2}},
   claims=[F("La ballena azul (hasta ~30 m) es el animal más grande conocido, pero su garganta es estrecha", "NOAA Fisheries")],
   sfx=[{"name": "rumble", "at": 0.2, "gain_db": -8}, {"name": "pop", "at_word": 11}], emphasis=["azul", "estrecha"])

sc("b04", "development", "Y la de la jorobada, tampoco. Lo sabemos por experiencia.", {
    "background": {"type": "underwater", "floor": 1750},
    "character": {"action": "think", "expression": "smug", "x": 0.3, "y": 0.8, "scale": 1.0, **DIVER},
    "props": [{"type": "whale", "x": 0.62, "y": 0.38, "scale": 0.8, "enter": "none", "loop": "bob"}],
    "overlays": [{"type": "label", "text": "BALLENA JOROBADA", "x": 600, "y": 300, "size": 64, "bg": "#2B6BE8"}],
    "camera": {"move": "push_in"}},
   claims=[F("La garganta de la ballena jorobada tampoco permite tragar a una persona", "NOAA Fisheries")],
   transition="slide", emphasis=["jorobada"])

sc("b05", "development", "En dos mil veintiuno, una jorobada atrapó a un buceador con la boca.", {
    "background": {"type": "underwater", "floor": 1750},
    "character": {"action": "shock", "expression": "shock", "x": 0.72, "y": 0.6, "scale": 0.85, **DIVER},
    "props": [{"type": "whale", "x": 0.45, "y": 0.5, "scale": 0.95, "mouth": 0.9, "enter": "slide_left",
               "enter_dur": 0.5}],
    "overlays": [{"type": "fact", "label": "PASÓ DE VERDAD", "text": "Michael Packard, Cape Cod (EE. UU.), junio de 2021",
                  "at_word": 5}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   claims=[F("En 2021 una ballena jorobada atrapó en su boca al buceador Michael Packard en Cape Cod", "Cape Cod Times; CBS News (junio 2021)")],
   sfx=[{"name": "gulp", "at_word": 6}, {"name": "hit", "at_word": 6, "gain_db": -6}], emphasis=["buceador"])

sc("b06", "development", "Unos treinta segundos después, lo escupió. Salió con moratones, pero vivo.", {
    "background": {"type": "underwater", "floor": 1750},
    "character": {"action": "fall", "expression": "dizzy", "x": 0.55, "y": 0.5, "scale": 0.9,
                  "path": [[0, 0.5, 0.5], ["w3", 0.5, 0.5], ["w5", 0.72, 0.42]], "actions": [["w6", "celebrate"]],
                  "expressions": [["w6", "laugh"]], **DIVER},
    "props": [{"type": "whale", "x": 0.42, "y": 0.62, "scale": 0.85, "mouth": 0.7, "enter": "none"},
              {"type": "splash", "x": 0.6, "y": 0.42, "at_word": 3, "enter": "none", "color": "#BFEFFF"}],
    "overlays": [{"type": "timer", "text": "30 s", "x": 220, "y": 360, "over": 1.2}],
    "camera": {"move": "static", "impacts": ["w3"]}},
   claims=[F("Packard estuvo unos 30-40 segundos en la boca de la ballena y salió solo con moratones", "Cape Cod Times; CBS News")],
   sfx=[{"name": "clock", "at": 0.0, "gain_db": -6}, {"name": "splash", "at_word": 3}, {"name": "boing", "at_word": 4}],
   transition="zoom", emphasis=["vivo"])

sc("b07", "development", "Pero hay una excepción: el cachalote, que se traga calamares gigantes enteros.", {
    "background": {"type": "underwater", "deep": 0.8, "floor": 2400},
    "character": {"visible": False},
    "props": [{"type": "sperm_whale", "x": 0.52, "y": 0.4, "scale": 0.85, "mouth": 0.6, "enter": "slide_right",
               "enter_dur": 0.6, "loop": "bob"},
              {"type": "squid", "x": 0.55, "y": 0.74, "scale": 0.75, "at_word": 7, "enter": "rise", "loop": "bob"}],
    "overlays": [{"type": "label", "text": "CACHALOTE", "x": 540, "y": 300, "size": 76, "at_word": 4, "bg": "#E8392F"}],
    "camera": {"move": "push_in", "focus": [0.5, 0.5]}},
   claims=[F("El cachalote tiene una garganta lo bastante grande para tragar calamares gigantes enteros", "NOAA Fisheries; Britannica")],
   sfx=[{"name": "riser", "at": 0.1, "gain_db": -6}, {"name": "pop", "at_word": 4}], emphasis=["cachalote"])

sc("b08", "climax", "Si uno te tragara, acabarías en un estómago con varias cámaras.", {
    "background": {"type": "stomach", "squeeze": 0.3},
    "character": {"action": "fall", "expression": "scared", "x": 0.5, "y": 0.72, "scale": 1.1, "enter": "drop",
                  "actions": [["w5", "shock"]], **DIVER},
    "overlays": [{"type": "label", "text": "ESTÓMAGO DEL CACHALOTE", "x": 540, "y": 300, "size": 60, "at_word": 6}],
    "camera": {"move": "punch", "impacts": [0.6]}},
   claims=[F("El cachalote tiene un estómago dividido en varias cámaras", "Britannica; NOAA")],
   sfx=[{"name": "fall", "at": 0.0}, {"name": "splash", "at": 0.55}], transition="circle", emphasis=["estómago"])

sc("b09", "climax", "No hay aire, hace unos treinta y siete grados y huele fatal.", {
    "background": {"type": "stomach", "squeeze": 0.5},
    "character": {"action": "sweat", "expression": "hot", "x": 0.42, "y": 0.75, "scale": 1.1, "sweat": 1, **DIVER},
    "props": [{"type": "thermometer", "x": 0.8, "y": 0.42, "level": 0.6, "text": "37 °C", "at_word": 4},
              {"type": "heatwaves", "x": 0.42, "y": 0.38, "enter": "none"}],
    "camera": {"move": "push_in"}},
   claims=[F("La temperatura corporal de un cachalote ronda los 36-37 °C", "Estudios de termorregulación en cetáceos", "estimate")],
   sfx=[{"name": "gulp", "at_word": 10}], emphasis=["aire", "fatal"])

sc("b10", "climax", "Sus paredes musculosas aprietan para triturar la comida. Y la comida eres tú.", {
    "background": {"type": "stomach", "squeeze": 1.0},
    "character": {"action": "squished", "expression": "scared", "x": 0.5, "y": 0.75, "scale": 1.15, **DIVER},
    "props": [{"type": "pressure", "x": 540, "y": 1100, "abs": True, "r": 470, "n": 6, "enter": "none"}],
    "camera": {"move": "push_in", "shake": 0.4, "impacts": ["w12"]}},
   claims=[F("La primera cámara del estómago del cachalote es muscular y tritura el alimento", "Britannica")],
   sfx=[{"name": "rumble", "at": 0.0, "gain_db": -4}, {"name": "hit", "at_word": 12, "gain_db": -4}],
   emphasis=["tú"])

sc("b11", "climax", "Encima, el cachalote puede bajar a más de mil metros de profundidad.", {
    "background": {"type": "underwater", "deep": 1.0, "floor": 2400, "fish": False},
    "character": {"visible": False},
    "props": [{"type": "sperm_whale", "x": 0.5, "y": 0.5, "scale": 0.8, "rot": 0.55, "enter": "none", "loop": "bob"},
              {"type": "speedlines", "x": 0.5, "y": 0.5, "enter": "none", "dir": -1}],
    "overlays": [{"type": "counter", "from": 0, "to": 1000, "suffix": " m", "at_word": 8, "over": 0.8, "y": 330,
                  "sub": "DE PROFUNDIDAD"}],
    "camera": {"move": "pan_up", "amount": 200}},
   claims=[F("El cachalote se sumerge habitualmente a más de 1.000 m de profundidad", "NOAA Fisheries")],
   sfx=[{"name": "fall", "at": 0.1, "gain_db": -6}, {"name": "ding", "at_word": 8}], transition="whip",
   emphasis=["mil", "metros"])

sc("b12", "climax", "Lo único bueno: en sus intestinos podrías encontrar ámbar gris, que vale una fortuna en perfumería.", {
    "background": {"type": "stomach", "squeeze": 0.2},
    "character": {"action": "present", "expression": "wow", "x": 0.3, "y": 0.75, "scale": 1.05, **DIVER},
    "props": [{"type": "ambergris", "x": 0.68, "y": 0.5, "at_word": 8, "scale": 1.3, "loop": "bob"},
              {"type": "perfume", "x": 0.78, "y": 0.28, "at_word": 13, "loop": "wobble"}],
    "overlays": [{"type": "label", "text": "ÁMBAR GRIS", "x": 540, "y": 300, "size": 70, "at_word": 8, "bg": "#9D7BFF"}],
    "camera": {"move": "push_in"}},
   claims=[F("El ámbar gris se forma en los intestinos del cachalote y se cotiza en perfumería", "Britannica; Natural History Museum (Londres)")],
   sfx=[{"name": "sparkle", "at_word": 8}, {"name": "ding", "at_word": 13}], transition="slide",
   emphasis=["ámbar", "fortuna"])

sc("b13", "ending", "¿Y el marinero que sobrevivió dentro de una ballena en mil ochocientos noventa y uno?", {
    "background": {"type": "burst", "c1": "#C9A66B", "c2": "#D9BC86"},
    "character": {"action": "think", "expression": "neutral", "x": 0.25, "y": 0.86, "scale": 0.9, **DIVER},
    "props": [{"type": "newspaper", "x": 0.58, "y": 0.42, "enter": "drop", "headline": "MARINERO TRAGADO\nPOR UNA BALLENA",
               "paper": "EL DIARIO", "year": "1891"}],
    "camera": {"move": "push_in", "focus": [0.55, 0.42]}},
   claims=[F("Circuló la historia del marinero James Bartley, supuestamente tragado por una ballena en 1891", "Edward B. Davis, «A Whale of a Tale» (1991)")],
   sfx=[{"name": "whoosh", "at": 0.0}], transition="flash")

sc("b14", "ending", "Los historiadores no encontraron ninguna prueba: era un bulo.", {
    "background": {"type": "burst", "c1": "#C9A66B", "c2": "#D9BC86"},
    "character": {"action": "shrug", "expression": "smug", "x": 0.25, "y": 0.86, "scale": 0.9, **DIVER},
    "props": [{"type": "newspaper", "x": 0.58, "y": 0.5, "enter": "none", "headline": "MARINERO TRAGADO\nPOR UNA BALLENA",
               "paper": "EL DIARIO", "year": "1891"}],
    "overlays": [{"type": "myth", "text": "LA HISTORIA DE 1891", "stamp": "¡BULO!", "y": 330, "stamp_at": 1.6}],
    "camera": {"move": "punch", "impacts": [1.75]}},
   claims=[F("No hay pruebas de la historia de James Bartley; los historiadores la consideran un bulo", "Edward B. Davis, «A Whale of a Tale» (1991)")],
   sfx=[{"name": "hit", "at": 1.75, "gain_db": -2}], transition="cut", emphasis=["bulo"])

sc("b15", "ending", "En la vida real, sin aire, no aguantarías más que unos minutos.", {
    "background": {"type": "stomach", "squeeze": 0.6},
    "character": {"action": "float", "expression": "dizzy", "x": 0.5, "y": 0.7, "scale": 1.1, **DIVER},
    "overlays": [{"type": "fiction", "label": "OJO", "text": "Sin aire, una persona solo resiste unos minutos", "y": 240}],
    "camera": {"move": "push_in"}},
   claims=[F("Sin oxígeno, el ser humano pierde la consciencia en minutos", "Fisiología humana básica", "estimate")],
   sfx=[{"name": "gulp", "at": 0.4}], transition="circle", emphasis=["minutos"])

sc("b16", "ending", "¿Te meterías al mar después de esto? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#4B86F0"},
    "character": {"action": "talk", "expression": "excited", "x": 0.5, "y": 0.62, "scale": 1.35, "enter": "pop",
                  "actions": [["w6", "point_down"]], **DIVER},
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 6,
                  "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 6}], transition="zoom", pause=0.35)

DESC = """Estás buceando tan tranquilo… y una ballena se te traga. ¿Podrías sobrevivir? 🐋

Leo descubre por qué casi ninguna ballena podría tragarte, la increíble historia real de un buceador atrapado en la boca de una jorobada, qué hay dentro de un cachalote y qué tesoro carísimo esconde.

🧪 DATOS REALES DEL VÍDEO
• La ballena azul (hasta unos 30 m) es el animal más grande que ha existido, pero su garganta es demasiado estrecha para tragarse a una persona.
• En junio de 2021, una ballena jorobada atrapó en su boca al buceador Michael Packard en Cape Cod (EE. UU.). Unos 30-40 segundos después lo escupió: solo sufrió moratones.
• El cachalote sí tiene una garganta enorme: se traga calamares gigantes enteros.
• Su estómago tiene varias cámaras, y la primera es muscular y tritura el alimento.
• Su cuerpo está a unos 36-37 °C y puede sumergirse a más de 1.000 metros.
• En sus intestinos se forma el ámbar gris, muy valorado en perfumería.
• La famosa historia de James Bartley, el marinero «tragado por una ballena» en 1891, nunca se ha podido demostrar: los historiadores la consideran un bulo.

⚠️ La aventura de Leo es ficción: en la realidad nadie sobreviviría más de unos minutos sin aire. Los datos son reales y aproximados.

📚 Fuentes: NOAA Fisheries, Encyclopaedia Britannica, Natural History Museum de Londres, Cape Cod Times y CBS News (2021), Edward B. Davis, «A Whale of a Tale» (1991).

💬 ¿Te meterías al mar después de esto? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #ballena #oceano #curiosidades #shorts"""

st.save("te-traga-una-ballena", "¿Qué pasaría si te tragara una ballena?",
        "¿Qué pasaría si te tragara una ballena?", "supervivencia", "¿Te meterías al mar después de esto?", {
            "title": "¿Qué pasaría si te tragara una ballena? 🐋",
            "hashtags": ["#quepasariasi", "#ballena", "#oceano", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "tragado por una ballena", "ballena", "cachalote", "ballena jorobada",
                     "ballena azul", "ámbar gris", "michael packard", "océano", "animales", "curiosidades",
                     "animación", "hipotéticos"],
            "pinned_comment": "¿Te meterías al mar después de esto? 🐋👇 (La historia del buceador de 2021 es 100 % real)",
            "description": DESC,
            "thumbnail": {"scene": "b05", "t": 0.75, "lines": ["¿Y SI TE", "TRAGA UNA", "BALLENA?"],
                          "badge": "¡PASÓ DE VERDAD!", "badge_pos": [540, 1560], "y": 230,
                          "character": {"action": "shock", "expression": "shock", "x": 0.66, "y": 0.62, "scale": 1.2},
                          "crop_y": 0.45},
        }, mood="mystery")
