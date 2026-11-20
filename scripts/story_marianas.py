"""Guion: ¿Qué pasaría si bajaras 11.000 metros a la Fosa de las Marianas?

Escalada por profundidad (10 → 40 → 332 → 1.000 → 3.800 → 8.336 → 10.935 m) con contador en pantalla.
"""
from storykit import F, Story

st = Story()
sc = st.sc


def deep(d, **kw):
    """Fondo según la profundidad (0..1 de oscuridad)."""
    return {"type": "underwater", "deep": d, "floor": 2400, **kw}


ABYSS = {"type": "trench_deep", "floor": 2400}


def sub(**kw):
    return {"type": "bathyscaphe", "x": 0.42, "y": 0.5, "scale": 0.9, "enter": "none", **kw}


def metros(a, b, **kw):
    return {"type": "counter", "from": a, "to": b, "prefix": "-", "suffix": " m", "over": 1.0, "y": 300,
            "size": 130, **kw}


def lbl(txt, bg="#2B6BE8", **kw):
    return {"type": "label", "text": txt, "x": 540, "y": 470, "size": 66, "bg": bg, **kw}


def leo(**kw):
    d = {"x": 0.5, "y": 0.72, "scale": 1.2, "action": "swim", "helmet": "diving"}
    d.update(kw)
    return d


SRC_NOAA = "NOAA Ocean Exploration, 'How deep is the ocean?' / 'Challenger Deep'"

sc("m01", "hook", "Te metes en el mar y empiezas a bajar. Destino: el punto más profundo del planeta.", {
    "background": deep(0.0),
    "character": leo(expression="excited", actions=[["w7", "shock"]], expressions=[["w7", "surprised"]]),
    "overlays": [{"type": "title", "lines": ["¿11.000 METROS", "BAJO EL MAR?"], "y": 250, "size": 110}],
    "camera": {"move": "punch", "impacts": ["w7"]}},
   sfx=[{"name": "splash", "at": 0.1, "gain_db": -6}, {"name": "hit", "at_word": 7, "gain_db": -6}], transition="cut",
   emphasis=["profundo"])

sc("m02", "setup", "Diez metros: la presión ya es el doble que en la superficie. Te duelen los oídos.", {
    "background": deep(0.05),
    "character": leo(expression="worried", action="sweat"),
    "props": [{"type": "pressure", "x": 0.8, "y": 0.45, "scale": 0.6, "at_word": 3}],
    "overlays": [metros(0, 10), lbl("PRESIÓN ×2", at_word=6)],
    "camera": {"move": "push_in"}},
   claims=[F("Cada 10 m de agua de mar añaden aproximadamente 1 atmósfera de presión", SRC_NOAA)],
   sfx=[{"name": "ding", "at_word": 6}], emphasis=["doble"])

sc("m03", "setup", "Cuarenta metros: el límite del buceo recreativo. Más abajo, el aire normal se vuelve peligroso.", {
    "background": deep(0.2),
    "character": leo(expression="scared", action="swim"),
    "props": [{"type": "bubbles", "x": 0.52, "y": 0.4}],
    "overlays": [metros(10, 40), lbl("LÍMITE RECREATIVO", "#E8392F", at_word=3)],
    "camera": {"move": "pan_down", "amount": 150}},
   claims=[F("El límite habitual del buceo recreativo es de 40 m (PADI); más abajo aumentan los riesgos de narcosis y toxicidad",
             "PADI; DAN (Divers Alert Network)")],
   sfx=[{"name": "whoosh", "at": 0.3, "gain_db": -8}], transition="whip", emphasis=["límite"])

sc("m04", "setup", "Trescientos treinta y dos metros: el récord humano con botella. Desde aquí, solo en submarino.", {
    "background": deep(0.45),
    "character": {"visible": False},
    "character": {"visible": False},
    "props": [sub(at_word=10, enter="drop")],
    "overlays": [metros(40, 332), lbl("RÉCORD DE BUCEO", "#22B573", at_word=7)],
    "camera": {"move": "push_in"}},
   claims=[F("El récord de inmersión con botella es de 332,35 m (Ahmed Gabr, 2014)", "Guinness World Records")],
   sfx=[{"name": "ding", "at_word": 7}, {"name": "boing", "at_word": 10, "gain_db": -8}], emphasis=["récord"])

sc("m05", "development", "Mil metros: la luz del sol desaparece del todo. Oscuridad total, para siempre.", {
    "background": deep(0.95, surface=False),
    "character": {"visible": False},
    "props": [sub()],
    "overlays": [metros(332, 1000), lbl("ZONA SIN LUZ", "#19162B", at_word=7)],
    "camera": {"move": "push_in"}},
   claims=[F("Por debajo de unos 1.000 m no llega luz solar (zona afótica)", SRC_NOAA)],
   sfx=[{"name": "rumble", "at": 0.2, "gain_db": -10}], transition="circle", emphasis=["oscuridad"])

sc("m06", "development", "Pero no estás solo: aquí cazan peces con linternas en la cabeza.", {
    "background": ABYSS,
    "character": {"visible": False},
    "props": [sub(light=True), {"type": "anglerfish", "x": 0.72, "y": 0.72, "scale": 0.9, "at_word": 4,
                                "enter": "slide_right"}],
    "camera": {"move": "push_in", "focus": [0.7, 0.7]}},
   claims=[F("Los rapes abisales usan un señuelo bioluminiscente para cazar", SRC_NOAA)],
   sfx=[{"name": "sparkle", "at_word": 4}], emphasis=["linternas"])

sc("m07", "development", "Tres mil ochocientos metros: pasas junto al Titanic, que descansa a esta profundidad.", {
    "background": ABYSS,
    "character": {"visible": False},
    "props": [sub(), {"type": "liner", "x": 0.6, "y": 0.86, "scale": 0.5, "tilt": 0.12, "sink": 0.0,
                      "at_word": 5, "enter": "rise"}],
    "overlays": [metros(1000, 3800)],
    "camera": {"move": "pan_down", "amount": 120}},
   claims=[F("Los restos del Titanic están a unos 3.800 m de profundidad", "NOAA; Woods Hole Oceanographic Institution")],
   transition="whip", emphasis=["Titanic"])

sc("m08", "development", "La presión aquí aplastaría una lata de refresco como si fuera papel.", {
    "background": ABYSS,
    "character": {"visible": False},
    "props": [sub(), {"type": "pressure", "x": 0.75, "y": 0.4, "scale": 0.7, "at_word": 2, "loop": "shake"}],
    "overlays": [{"type": "fact", "text": "A 4.000 m la presión es unas 400 veces la de la superficie",
                  "at_word": 3, "y": 250}],
    "camera": {"move": "push_in", "shake": 0.2}},
   claims=[F("A 4.000 m la presión es de unas 400 atmósferas", SRC_NOAA)],
   sfx=[{"name": "crack", "at_word": 5, "gain_db": -6}], emphasis=["aplastaría"])

sc("m09", "development", "Ocho mil trescientos metros: el pez más profundo jamás filmado. Un pez caracol rosa.", {
    "background": ABYSS,
    "character": {"visible": False},
    "props": [sub(), {"type": "snailfish", "x": 0.72, "y": 0.75, "scale": 1.0, "at_word": 6}],
    "overlays": [metros(3800, 8336), lbl("RÉCORD: 8.336 m", "#FF6B5C", at_word=6)],
    "camera": {"move": "push_in", "focus": [0.7, 0.72]}},
   claims=[F("En 2022 se filmó un pez caracol a 8.336 m, el pez más profundo registrado",
             "University of Western Australia / Tokyo University of Marine Science, 2023")],
   sfx=[{"name": "sparkle", "at_word": 6}], transition="zoom", emphasis=["caracol"])

sc("m10", "climax", "Y por fin, el fondo: casi once mil metros. El abismo Challenger.", {
    "background": {"type": "trench_deep", "floor": 1500},
    "character": {"visible": False},
    "props": [sub(y=0.62)],
    "overlays": [metros(8336, 10935, sub="ABISMO CHALLENGER")],
    "camera": {"move": "zoom_burst"}},
   claims=[F("El abismo Challenger, en la Fosa de las Marianas, tiene unos 10.935 m de profundidad", SRC_NOAA)],
   sfx=[{"name": "riser", "at": 0}, {"name": "boom", "at": 1.0, "gain_db": -8}], transition="flash",
   emphasis=["fondo"])

sc("m11", "climax", "Aquí la presión es más de mil veces la de la superficie. Como un elefante sobre cada dedo.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#5C8FE6"},
    "character": {"visible": False},
    "props": [{"type": "pressure", "x": 0.5, "y": 0.62, "scale": 1.2, "loop": "shake"}],
    "overlays": [{"type": "counter", "from": 1, "to": 1071, "prefix": "×", "at_word": 6, "over": 1.2, "y": 320,
                  "size": 140, "sub": "LA PRESIÓN DE LA SUPERFICIE"}],
    "camera": {"move": "push_in", "shake": 0.25}},
   claims=[F("En el fondo del abismo Challenger la presión supera las 1.000 atmósferas (unos 1.086 bar)", SRC_NOAA)],
   sfx=[{"name": "ding", "at_word": 6}], transition="slide", emphasis=["mil"])

sc("m12", "climax", "Hace mucho frío, apenas unos grados, y el suelo es un barro finísimo.", {
    "background": {"type": "trench_deep", "floor": 1500},
    "character": {"visible": False},
    "props": [sub(y=0.62), {"type": "thermometer", "x": 0.82, "y": 0.4, "scale": 0.8, "level": 0.12, "at_word": 3}],
    "camera": {"move": "static"}},
   claims=[F("El agua en el fondo de la fosa está a unos 1-4 °C", SRC_NOAA)],
   emphasis=["frío"])

sc("m13", "ending", "Solo un puñado de personas ha llegado hasta aquí. La primera vez fue en mil novecientos sesenta.", {
    "background": {"type": "trench_deep", "floor": 1500},
    "character": {"visible": False},
    "props": [sub(y=0.62)],
    "overlays": [{"type": "label", "text": "TRIESTE · 23/1/1960", "x": 540, "y": 330, "size": 72, "bg": "#FFD23F",
                  "color": "#19162B", "at_word": 11}],
    "camera": {"move": "pull_out"}},
   claims=[F("Jacques Piccard y Don Walsh llegaron al abismo Challenger en el batiscafo Trieste el 23 de enero de 1960",
             "Encyclopaedia Britannica"),
           F("Desde entonces solo unas pocas decenas de personas han visitado el abismo Challenger", SRC_NOAA,
             "estimate")],
   sfx=[{"name": "sparkle", "at_word": 11}], emphasis=["puñado"])

sc("m14", "ending", "Han subido más personas a la Luna que las que bajaron aquí durante décadas.", {
    "background": {"type": "night_sky", "moon": False},
    "character": {"visible": False},
    "props": [{"type": "moon", "x": 0.5, "y": 0.45, "r": 220}],
    "overlays": [{"type": "label", "text": "12 EN LA LUNA", "x": 540, "y": 1200, "size": 80, "bg": "#9D7BFF",
                  "at_word": 5}],
    "camera": {"move": "push_in"}},
   claims=[F("Doce personas han caminado sobre la Luna; hasta 2019 solo tres habían bajado al abismo Challenger",
             "NASA; NOAA")],
   transition="zoom", emphasis=["Luna"])

sc("m15", "ending", "¿Tú bajarías once mil metros? Te leo en comentarios.", {
    "background": deep(0.0),
    "character": leo(action="talk", expression="excited", actions=[["w5", "point_down"]]),
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5,
                  "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Empiezas a bajar al fondo del mar… ¿qué encontrarías en los 11.000 metros de la Fosa de las Marianas? 🌊

Leo baja metro a metro: el límite del buceo, la zona donde ya no llega la luz, el Titanic, el pez más profundo jamás filmado y el abismo Challenger.

🧪 DATOS REALES DEL VÍDEO
• Cada 10 m de agua añaden más o menos una atmósfera de presión.
• El límite del buceo recreativo es de 40 m.
• Récord de buceo con botella: 332,35 m (Ahmed Gabr, 2014).
• Por debajo de unos 1.000 m no llega la luz del sol.
• El Titanic descansa a unos 3.800 m.
• En 2022 se filmó un pez caracol a 8.336 m: el pez más profundo registrado.
• El abismo Challenger tiene unos 10.935 m; la presión supera las 1.000 atmósferas.
• El agua del fondo está a 1-4 °C.
• Primera bajada: Piccard y Walsh, batiscafo Trieste, 23 de enero de 1960.
• Doce personas han pisado la Luna; hasta 2019 solo tres habían bajado al abismo Challenger.

📚 Fuentes: NOAA Ocean Exploration, Guinness World Records, PADI/DAN, Woods Hole, University of Western Australia, Encyclopaedia Britannica, NASA.

💬 ¿Tú bajarías once mil metros? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #fosadelasmarianas #oceano #curiosidades #shorts"""

st.save("fosa-de-las-marianas", "¿Qué pasaría si bajaras 11.000 metros a la Fosa de las Marianas?",
        "¿Qué pasaría si bajaras 11.000 metros a la Fosa de las Marianas?", "tierra / catástrofes",
        "¿Tú bajarías once mil metros?", {
            "title": "¿Qué pasaría si bajaras 11.000 metros bajo el mar? 🤯",
            "hashtags": ["#quepasariasi", "#fosadelasmarianas", "#oceano", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "fosa de las marianas", "abismo challenger", "océano", "fondo del mar",
                     "presión", "titanic", "pez caracol", "batiscafo", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Hasta qué profundidad llegarías tú? 🌊👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "m06", "t": 1.6, "lines": ["¿11.000 M", "BAJO EL MAR?"],
                          "badge": "AQUÍ NO LLEGA LA LUZ", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
