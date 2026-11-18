"""Guion: ¿Qué pasaría si vivieras 100 días en Marte?"""
from storykit import SUIT, F, Story

st = Story()
sc = st.sc
MARS_G = 1250 / 1920
LEO = {"x": 0.5, "y": MARS_G + 0.02, "scale": 1.2, **SUIT}

sc("m01", "hook", "Te vas a vivir cien días a Marte. Primer problema: llegar.", {
    "background": {"type": "space"},
    "character": {"action": "float", "expression": "excited", "x": 0.5, "y": 0.6, "scale": 1.15,
                  "expressions": [["w8", "worried"]], **SUIT},
    "props": [{"type": "planet", "x": 0.5, "y": 0.98, "r": 420, "enter": "rise", "layer": "back"}],
    "overlays": [{"type": "title", "lines": ["¿100 DÍAS", "EN MARTE?"], "y": 300, "size": 130}],
    "camera": {"move": "punch"}},
   sfx=[{"name": "float", "at": 0.1}, {"name": "boing", "at_word": 8, "gain_db": -4}],
   transition="cut", emphasis=["marte"])

sc("m02", "setup", "Con los cohetes actuales, el viaje dura unos siete meses.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "earth", "x": 0.2, "y": 0.8, "r": 110, "enter": "none"},
              {"type": "planet", "x": 0.82, "y": 0.42, "r": 90, "enter": "none"},
              {"type": "dotted_path", "x": 0.25, "y": 0.75, "dx": 560, "dy": -560, "enter": "fade"},
              {"type": "rocket", "x": 0.5, "y": 0.58, "rot": 0.8, "scale": 0.55, "enter": "slide_left",
               "enter_dur": 1.0, "loop": "bob"}],
    "overlays": [{"type": "counter", "from": 0, "to": 7, "suffix": " MESES", "at_word": 8, "over": 0.6, "y": 330,
                  "sub": "DE VIAJE"}],
    "camera": {"move": "push_in"}},
   claims=[F("Un viaje a Marte con la tecnología actual dura unos 7 meses", "NASA")],
   sfx=[{"name": "whoosh", "at": 0.2}, {"name": "ding", "at_word": 8}], emphasis=["siete", "meses"])

sc("m03", "setup", "Aterrizas, y la báscula te da una alegría: pesas menos de la mitad.", {
    "background": {"type": "mars"},
    "character": {**LEO, "action": "idle", "expression": "happy", "expressions": [["w8", "excited"]],
                  "enter": "drop"},
    "props": [{"type": "scale", "x": 0.5, "y": MARS_G + 0.035, "from": 60, "to": 23, "at_word": 8, "over": 0.8,
               "enter": "none", "layer": "front"}],
    "overlays": [{"type": "fact", "text": "En Marte la gravedad es solo el 38 % de la de la Tierra", "at_word": 8}],
    "camera": {"move": "push_in", "focus": [0.5, 0.6], "impacts": [0.55]}},
   claims=[F("La gravedad en Marte es un 38 % de la terrestre", "NASA Mars Fact Sheet")],
   sfx=[{"name": "boom", "at": 0.5, "gain_db": -6}, {"name": "ding", "at_word": 8}], emphasis=["mitad"])

sc("m04", "development", "Saltas como un canguro… pero ni se te ocurra quitarte el casco.", {
    "background": {"type": "mars"},
    "character": {**LEO, "action": "celebrate", "expression": "laugh", "actions": [["w5", "shock"]],
                  "expressions": [["w5", "worried"]]},
    "overlays": [{"type": "label", "text": "¡NO TE QUITES EL CASCO!", "x": 540, "y": 330, "size": 64, "at_word": 5}],
    "camera": {"move": "static"}},
   sfx=[{"name": "boing", "at": 0.1}, {"name": "boing", "at": 0.8}, {"name": "pop", "at_word": 5}],
   transition="slide", emphasis=["canguro", "casco"])

sc("m05", "development", "El aire es casi todo dióxido de carbono y apenas tiene presión.", {
    "background": {"type": "mars"},
    "character": {**LEO, "action": "look_up", "expression": "worried"},
    "overlays": [{"type": "fact", "text": "Atmósfera: 95 % CO2 y menos del 1 % de la presión de la Tierra", "at": 0.3}],
    "camera": {"move": "push_in", "focus": [0.5, 0.45]}},
   claims=[F("La atmósfera de Marte es ~95 % CO2 y su presión es menos del 1 % de la terrestre", "NASA")],
   emphasis=["dióxido", "carbono"])

sc("m06", "development", "Sin traje, perderías el conocimiento en cuestión de segundos.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"action": "float", "expression": "dizzy", "x": 0.5, "y": 0.62, "scale": 1.25, "enter": "pop"},
    "props": [{"type": "question", "char": "!", "x": 0.78, "y": 0.28, "color": "#FFD23F", "loop": "wobble"}],
    "overlays": [{"type": "timer", "text": "15 s", "x": 230, "y": 380, "at_word": 6, "over": 1.2}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("Expuesto a una presión casi nula, una persona pierde el conocimiento en unos 15 segundos", "NASA")],
   sfx=[{"name": "gulp", "at": 0.2}, {"name": "clock", "at_word": 6, "gain_db": -6}], transition="flash",
   emphasis=["segundos"])

sc("m07", "development", "Fuera hace una media de sesenta grados bajo cero.", {
    "background": {"type": "mars"},
    "character": {**LEO, "x": 0.42, "action": "squished", "expression": "scared"},
    "props": [{"type": "thermometer", "x": 0.82, "y": 0.42, "level": 0.12, "text": "-60 °C", "text_color": "#5CE1E6",
               "at_word": 4}],
    "camera": {"move": "push_in", "shake": 0.25}},
   claims=[F("La temperatura media de Marte ronda los -60 °C", "NASA")],
   sfx=[{"name": "pop", "at_word": 4}], emphasis=["sesenta", "cero"])

sc("m08", "development", "Así que montas tu base e intentas cultivar patatas, como en las películas.", {
    "background": {"type": "mars"},
    "character": {**LEO, "x": 0.3, "y": 0.73, "scale": 1.05, "action": "present", "expression": "excited"},
    "props": [{"type": "habitat", "x": 0.55, "y": 0.58, "scale": 0.9, "enter": "drop"},
              {"type": "plant", "x": 0.62, "y": 0.75, "at_word": 6, "health": 1.0, "layer": "front"},
              {"type": "plant", "x": 0.82, "y": 0.77, "at_word": 7, "health": 1.0, "layer": "front"}],
    "camera": {"move": "pull_out", "zoom_from": 1.15}},
   claims=[F("Cultivar en Marte es un guiño a la película «The Martian» (ficción)", "Licencia narrativa", "fiction")],
   sfx=[{"name": "boom", "at": 0.4, "gain_db": -8}, {"name": "pop", "at_word": 6}, {"name": "pop", "at_word": 7}],
   emphasis=["patatas"])

sc("m09", "development", "Problema: el suelo marciano tiene percloratos, unas sales tóxicas.", {
    "background": {"type": "mars"},
    "character": {**LEO, "x": 0.3, "y": 0.73, "scale": 1.05, "action": "shock", "expression": "shock"},
    "props": [{"type": "habitat", "x": 0.55, "y": 0.58, "scale": 0.9, "enter": "none"},
              {"type": "plant", "x": 0.62, "y": 0.75, "health": 0.2, "warning": True, "layer": "front", "at_word": 4},
              {"type": "plant", "x": 0.82, "y": 0.77, "health": 0.2, "layer": "front", "enter": "none"}],
    "overlays": [{"type": "fact", "text": "La sonda Phoenix descubrió percloratos en el suelo de Marte (2008)", "at_word": 4}],
    "camera": {"move": "punch"}},
   claims=[F("El suelo marciano contiene percloratos, sales tóxicas para las personas", "NASA (sonda Phoenix, 2008)")],
   sfx=[{"name": "crack", "at_word": 4}], transition="slide", emphasis=["percloratos", "tóxicas"])

sc("m10", "development", "Día cuarenta: escribes a casa, y el mensaje tarda hasta veintidós minutos en llegar.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "planet", "x": 0.2, "y": 0.82, "r": 120, "enter": "none"},
              {"type": "earth", "x": 0.8, "y": 0.3, "r": 110, "enter": "none"},
              {"type": "message", "x": 0.55, "y": 0.55, "at_word": 2, "enter": "slide_left", "enter_dur": 2.2,
               "loop": "bob", "scale": 0.8}],
    "overlays": [{"type": "label", "text": "DÍA 40", "x": 300, "y": 300, "size": 70, "bg": "#2B6BE8"},
                 {"type": "timer", "text": "22 MIN", "x": 820, "y": 640, "at_word": 10, "over": 1.0}],
    "camera": {"move": "pan_right", "amount": 80}},
   claims=[F("Una señal entre Marte y la Tierra tarda entre 3 y 22 minutos", "NASA")],
   sfx=[{"name": "whoosh", "at_word": 2}, {"name": "ding", "at_word": 10}], transition="zoom",
   emphasis=["veintidós", "minutos"])

sc("m11", "climax", "Día sesenta: una tormenta de polvo envuelve el planeta entero.", {
    "background": {"type": "mars", "mode": "dust"},
    "character": {**LEO, "action": "squished", "expression": "scared"},
    "props": [{"type": "habitat", "x": 0.15, "y": 0.6, "scale": 0.7, "enter": "none", "loop": "shake"}],
    "overlays": [{"type": "label", "text": "DÍA 60", "x": 300, "y": 300, "size": 70, "bg": "#E8392F"}],
    "camera": {"move": "push_in", "shake": 0.6}},
   claims=[F("En Marte hay tormentas de polvo que llegan a cubrir todo el planeta durante semanas", "NASA")],
   sfx=[{"name": "rumble", "at": 0.0}, {"name": "whoosh", "at": 0.6}, {"name": "whoosh", "at": 1.8}],
   emphasis=["tormenta", "polvo"])

sc("m12", "climax", "Una así dejó sin energía al robot Opportunity en dos mil dieciocho.", {
    "background": {"type": "mars", "mode": "dust"},
    "character": {"visible": False},
    "props": [{"type": "rover", "x": 0.5, "y": 0.72, "scale": 1.3, "dust": 0.9, "sleeping": True, "enter": "none"}],
    "overlays": [{"type": "fact", "text": "El rover Opportunity se apagó en la tormenta global de 2018", "at_word": 3}],
    "camera": {"move": "push_in", "focus": [0.5, 0.62], "shake": 0.2}},
   claims=[F("El rover Opportunity perdió la energía durante la tormenta de polvo global de 2018", "NASA JPL")],
   sfx=[{"name": "fall", "at_word": 2, "gain_db": -6}], transition="circle", emphasis=["opportunity"])

sc("m13", "climax", "Cuando se despeja, descubres algo increíble: en Marte, los atardeceres son azules.", {
    "background": {"type": "mars", "mode": "blue_sunset"},
    "character": {**LEO, "y": 0.82, "scale": 1.0, "action": "float", "expression": "wow", "action_params": {}},
    "camera": {"move": "pull_out", "zoom_from": 1.25, "focus": [0.5, 0.45]}},
   claims=[F("En Marte los atardeceres son azulados por cómo el polvo dispersa la luz", "NASA (rover Curiosity)")],
   sfx=[{"name": "sparkle", "at_word": 10}, {"name": "float", "at": 0.0}], transition="flash", emphasis=["azules"])

sc("m14", "ending", "Día cien. Hora de volver a casa… pero no hay vuelo.", {
    "background": {"type": "mars"},
    "character": {**LEO, "x": 0.38, "action": "wave", "expression": "happy", "actions": [["w7", "shock"]],
                  "expressions": [["w7", "shock"]]},
    "props": [{"type": "habitat", "x": 0.72, "y": 0.6, "scale": 0.7, "enter": "none"}],
    "overlays": [{"type": "label", "text": "DÍA 100", "x": 300, "y": 300, "size": 70, "bg": "#2BAE66"}],
    "camera": {"move": "punch", "impacts": ["w8"]}},
   sfx=[{"name": "hit", "at_word": 8, "gain_db": -3}], emphasis=["vuelo"])

sc("m15", "ending", "Marte y la Tierra solo se alinean bien para viajar cada veintiséis meses.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "sun", "x": 0.5, "y": 0.55, "scale": 0.6, "enter": "none"},
              {"type": "earth", "x": 0.25, "y": 0.72, "r": 80, "enter": "none", "loop": "bob"},
              {"type": "planet", "x": 0.8, "y": 0.4, "r": 70, "enter": "none", "loop": "bob"}],
    "overlays": [{"type": "counter", "from": 0, "to": 26, "suffix": " MESES", "at_word": 11, "over": 0.6, "y": 330,
                  "sub": "ENTRE VENTANAS DE LANZAMIENTO"}],
    "camera": {"move": "push_in"}},
   claims=[F("Las ventanas de lanzamiento Tierra-Marte se repiten cada ~26 meses", "NASA")],
   sfx=[{"name": "ding", "at_word": 11}], transition="zoom", emphasis=["veintiséis"])

sc("m16", "ending", "Así que tus cien días acaban de convertirse en más de un año.", {
    "background": {"type": "mars"},
    "character": {**LEO, "x": 0.38, "action": "sweat", "expression": "worried", "actions": [["w8", "shrug"]],
                  "expressions": [["w8", "happy"]]},
    "props": [{"type": "calendar", "x": 0.78, "y": 0.42, "from": 100, "to": 500, "over": 2.6, "label": "DÍAS", "at": 0.3}],
    "camera": {"move": "push_in"}},
   claims=[F("Las misiones tripuladas planeadas a Marte prevén ~500 días en la superficie esperando la ventana de regreso",
             "NASA Mars Design Reference Architecture 5.0", "estimate")],
   sfx=[{"name": "clock", "at": 0.3, "gain_db": -6}, {"name": "boing", "at_word": 8}], emphasis=["año"])

sc("m17", "ending", "¿Te quedarías? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"action": "talk", "expression": "excited", "x": 0.5, "y": 0.62, "scale": 1.35, "enter": "pop",
                  "actions": [["w2", "point_down"]], **SUIT},
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 2,
                  "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 2}], transition="zoom", pause=0.35)

DESC = """Te vas a vivir 100 días a Marte… ¿qué podría salir mal? 🚀🔴

Leo viaja siete meses, aterriza, salta como un canguro, intenta cultivar patatas, sobrevive a una tormenta de polvo que cubre todo el planeta… y descubre que volver a casa no es tan fácil.

🧪 DATOS REALES DEL VÍDEO
• Con los cohetes actuales, el viaje a Marte dura unos 7 meses.
• La gravedad de Marte es el 38 % de la terrestre: si pesas 60 kg, allí la báscula marca unos 23.
• Su atmósfera es un 95 % dióxido de carbono y tiene menos del 1 % de la presión de la Tierra.
• Sin traje perderías el conocimiento en unos 15 segundos.
• La temperatura media ronda los 60 °C bajo cero.
• El suelo marciano contiene percloratos, sales tóxicas (descubiertas por la sonda Phoenix en 2008).
• Un mensaje entre Marte y la Tierra tarda entre 3 y 22 minutos.
• Las tormentas de polvo pueden envolver el planeta entero: una apagó el rover Opportunity en 2018.
• Los atardeceres en Marte son azules.
• Las ventanas para viajar entre la Tierra y Marte se abren cada ~26 meses.

⚠️ La aventura de Leo es ficción: hoy nadie puede vivir en Marte. Los datos científicos son reales y aproximados.

📚 Fuentes: NASA (Mars Fact Sheet, misiones Phoenix, Opportunity y Curiosity), NASA JPL, NASA Mars Design Reference Architecture 5.0.

💬 ¿Te quedarías en Marte o volverías corriendo? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #marte #espacio #curiosidades #shorts"""

st.save("100-dias-en-marte", "¿Qué pasaría si vivieras 100 días en Marte?",
        "¿Qué pasaría si vivieras 100 días en Marte?", "espacio", "¿Te quedarías en Marte o volverías corriendo?", {
            "title": "¿Qué pasaría si vivieras 100 días en Marte? 🚀",
            "hashtags": ["#quepasariasi", "#marte", "#espacio", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "vivir en marte", "100 días en marte", "marte", "nasa", "espacio",
                     "astronomía", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Te quedarías en Marte o volverías corriendo a la Tierra? 🚀👇",
            "description": DESC,
            "thumbnail": {"scene": "m08", "t": 0.7, "lines": ["¿Y SI VIVES", "100 DÍAS", "EN MARTE?"],
                          "badge": "-60 °C", "badge_color": "#2B6BE8", "badge_pos": [800, 1420],
                          "character": {"action": "shock", "expression": "shock", "x": 0.33, "y": 0.78, "scale": 1.3},
                          "crop_y": 0.62, "h_shift": 1000, "h_scale": 0.8},
        })
