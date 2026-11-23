"""Guion: ¿Qué pasaría si cayeras de un avión a 10.000 metros?

Escalada: frío y falta de oxígeno → velocidad terminal → el suelo → el caso real de Vesna Vulović (1972).
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, Story

st = Story()
sc = st.sc
FALL = {"x": 0.5, "y": 0.76, "scale": 1.3, "action": "fall"}


def sky(alt=1.0, **kw):
    return {"type": "sky_fall", "alt": alt, **kw}


def counter(to, suffix, at_word, sub=None, frm=0, y=330, size=130, **kw):
    o = {"type": "counter", "from": frm, "to": to, "suffix": suffix, "at_word": at_word, "over": 0.8, "y": y, "size": size, **kw}
    if sub:
        o["sub"] = sub
    return o


sc("a01", "hook", "Estás a diez mil metros de altura y caes del avión sin paracaídas.", {
    "background": sky(1.0),
    "character": {**FALL, "expression": "scared", "actions": [["w9", "fall"]]},
    "props": [{"type": "plane", "x": 0.72, "y": 0.18, "scale": 0.7, "enter": "slide_right"}],
    "overlays": [{"type": "title", "lines": ["¿CAER DE UN", "AVIÓN A 10.000 M?"], "y": 250, "size": 104}],
    "camera": {"move": "punch", "impacts": ["w9"]}},
   sfx=[{"name": "whoosh", "at": 0.0, "gain_db": -6}, {"name": "fall", "at_word": 8, "gain_db": -8}],
   transition="cut", emphasis=["diez", "paracaídas"])

sc("a02", "setup", "Primer problema: ahí arriba hace cincuenta grados bajo cero.", {
    "background": sky(1.0),
    "character": {**FALL, "expression": "scared", "extras": {"frost": 0.35}},
    "props": [{"type": "thermometer", "x": 0.82, "y": 0.5, "scale": 0.9, "level": 0.05, "at_word": 4}],
    "overlays": [counter(-50, " °C", 5, sub="A 10.000 M DE ALTURA", frm=10, color="#8FD3FF", y=330, size=150)],
    "camera": {"move": "push_in"}},
   claims=[F("A 10.000 m de altitud la temperatura de la atmósfera estándar es de unos -50 °C",
             "Atmósfera estándar internacional (OACI/ISO 2533)")],
   sfx=[{"name": "tick", "at_word": 5}], emphasis=["cincuenta"])

sc("a03", "development", "Y el aire es tan fino que casi no hay oxígeno para respirar.", {
    "background": sky(1.0),
    "character": {**FALL, "expression": "shock", "extras": {"frost": 0.35}},
    "props": [{"type": "lungs", "x": 0.2, "y": 0.28, "scale": 0.5, "at_word": 8}],
    "overlays": [{"type": "fact", "text": "A 10.000 m la presión del aire es solo el 26 % de la del suelo", "at_word": 3, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("A 10.000 m de altitud la presión atmosférica es de unos 26 kPa, el 26 % de la del nivel del mar",
             "Atmósfera estándar internacional (OACI/ISO 2533)")],
   sfx=[{"name": "gulp", "at_word": 9}], transition="whip", emphasis=["fino", "oxígeno"])

sc("a04", "development", "En menos de dos minutos perderías el conocimiento.", {
    "background": sky(0.95),
    "character": {**FALL, "expression": "dizzy", "actions": [["w3", "fall"]], "extras": {"frost": 0.5}},
    "props": [{"type": "clock", "x": 0.2, "y": 0.28, "scale": 0.6, "speed": 20, "at_word": 3}],
    "overlays": [{"type": "fact", "text": "A 10.000 m de altura el tiempo de conciencia útil sin oxígeno es de menos de 2 minutos", "at_word": 0, "y": 560}],
    "camera": {"move": "push_in", "shake": 0.1}},
   claims=[F("A unos 10.000 m (33.000 pies) el tiempo de conciencia útil sin oxígeno suplementario es de menos de 2 minutos",
             "FAA, fisiología de la altitud (tiempo de conciencia útil)")],
   sfx=[{"name": "riser", "at": 0.1, "gain_db": -9}], emphasis=["conocimiento"])

sc("a05", "development", "Pero no caes como una piedra: el aire te frena.", {
    "background": sky(0.85),
    "character": {**FALL, "expression": "wow"},
    "props": [{"type": "speedlines", "x": 0.5, "y": 0.5, "scale": 1.0, "at_word": 6}],
    "overlays": [],
    "camera": {"move": "push_in", "zoom_to": 1.15}},
   sfx=[{"name": "whoosh", "at_word": 6}], transition="slide", emphasis=["frena"])

sc("a06", "development", "Boca abajo y con los brazos abiertos, bajas a unos doscientos kilómetros por hora.", {
    "background": sky(0.7, speed=1.4),
    "character": {**FALL, "expression": "excited", "spin": 0.25},
    "props": [],
    "overlays": [counter(200, " KM/H", 10, sub="VELOCIDAD TERMINAL", y=330, size=160)],
    "camera": {"move": "static"}},
   claims=[F("En caída libre boca abajo la velocidad terminal ronda los 200 km/h (unos 55 m/s)",
             "Federación Aeronáutica Internacional (FAI); Universe Today")],
   sfx=[{"name": "tick", "at_word": 10}, {"name": "hit", "at_word": 10, "gain_db": -6}], transition="zoom", emphasis=["doscientos"])

sc("a07", "climax", "Es la velocidad terminal: ya no aceleras más.", {
    "background": sky(0.55, speed=1.3),
    "character": {**FALL, "expression": "determined", "spin": 0.2},
    "props": [],
    "overlays": [{"type": "fact", "text": "Velocidad terminal: el rozamiento del aire iguala a tu peso y dejas de acelerar", "at_word": 3, "y": 560}],
    "camera": {"move": "static"}},
   claims=[F("La velocidad terminal se alcanza cuando el rozamiento del aire iguala al peso y deja de haber aceleración",
             "Universe Today; física clásica")],
   sfx=[{"name": "ding", "at_word": 3}], emphasis=["terminal"])

sc("a08", "climax", "Chocar contra el suelo a esa velocidad es como estrellar un coche.", {
    "background": sky(0.2, ground=0.55),
    "character": {**FALL, "y": 0.62, "expression": "scared"},
    "props": [{"type": "car", "x": 0.5, "y": 0.9, "scale": 1.2, "enter": "none", "at_word": 8},
              {"type": "pow", "x": 0.72, "y": 0.78, "scale": 0.9, "at_word": 10}],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "hit", "at_word": 10, "gain_db": -4}], transition="flash", emphasis=["coche"])

sc("a09", "climax", "Casi nadie sobrevive a algo así. Casi.", {
    "background": {"type": "burst", "c1": "#1B1B3A", "c2": "#3B3F78"},
    "character": {"visible": False},
    "props": [{"type": "skull", "x": 0.5, "y": 0.45, "scale": 1.4, "enter": "pop"}],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "boom", "at": 0.1, "gain_db": -8}], transition="whip", pause=0.2, emphasis=["Casi"])

sc("a10", "climax", "En mil novecientos setenta y dos, Vesna Vulović cayó más de diez kilómetros.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#5A3A20", "x": 0.5, "y": 0.9, "size": 1.5, "expression": "happy",
               "action": "present", "shirt": "#2B6BE8", "enter": "pop"}],
    "overlays": [{"type": "label", "text": "VESNA VULOVIĆ · 1972", "x": 540, "y": 300, "size": 66, "bg": "#E8392F", "at_word": 6},
                 counter(10160, " M", 12, y=480, size=140)],
    "camera": {"move": "zoom_burst"}},
   claims=[F("El 26 de enero de 1972, la azafata Vesna Vulović sobrevivió a una caída de 10.160 m tras estallar el avión JAT 367",
             "Guinness World Records")],
   sfx=[{"name": "sparkle", "at_word": 8}, {"name": "ding", "at_word": 12}], transition="flash", emphasis=["Vulović"])

sc("a11", "climax", "Era azafata, y su avión estalló en el aire.", {
    "background": sky(1.0),
    "character": {"visible": False},
    "props": [{"type": "plane", "x": 0.5, "y": 0.4, "scale": 1.1, "enter": "none", "rot": 0.1},
              {"type": "pow", "x": 0.55, "y": 0.38, "scale": 1.4, "at_word": 6}],
    "overlays": [{"type": "fact", "text": "Vuelo JAT 367 · 26 de enero de 1972 · 28 personas a bordo", "at_word": 0, "y": 560}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   claims=[F("El vuelo JAT 367 estalló en el aire el 26 de enero de 1972 con 28 personas a bordo; solo sobrevivió Vulović",
             "Guinness World Records")],
   sfx=[{"name": "boom", "at_word": 6, "gain_db": -4}], transition="cut", emphasis=["estalló"])

sc("a12", "climax", "Quedó atrapada en la cola, sujeta por un carrito de comida.", {
    "background": sky(0.9),
    "character": {"visible": False},
    "props": [{"type": "plane_tail", "x": 0.5, "y": 0.5, "scale": 1.2, "enter": "none", "rot": -0.2}],
    "overlays": [{"type": "fact", "text": "Un carrito de comida la mantuvo sujeta dentro de la cola mientras caía", "at_word": 4, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("Vulović quedó atrapada en la sección de cola, sujeta por un carrito de comida", "Guinness World Records")],
   sfx=[{"name": "fall", "at": 0.2, "gain_db": -8}], transition="whip", emphasis=["carrito"])

sc("a13", "climax", "La cola cayó en una ladera nevada llena de árboles, que amortiguó el golpe.", {
    "background": sky(0.0, ground=0.8, snow=True, speed=0.0),
    "character": {"visible": False},
    "props": [{"type": "plane_tail", "x": 0.5, "y": 0.46, "scale": 1.3, "enter": "drop", "rot": -0.15}],
    "overlays": [{"type": "fact", "text": "La cola cayó en una ladera con nieve y árboles, que amortiguó el impacto", "at_word": 0, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("La sección de cola cayó en una ladera nevada y arbolada cerca de Srbská Kamenice (hoy República Checa)",
             "Guinness World Records; investigación checoslovaca")],
   sfx=[{"name": "hit", "at": 0.5, "gain_db": -4}], transition="zoom", emphasis=["amortiguó"])

sc("a14", "ending", "Pasó casi un mes en coma, pero sobrevivió y volvió a caminar.", {
    "background": {"type": "bedroom", "night": False},
    "character": {"visible": False},
    "props": [{"type": "heart", "x": 0.5, "y": 0.5, "scale": 1.2, "bpm": 70, "enter": "pop"}],
    "overlays": [{"type": "fact", "text": "Estuvo en coma varias semanas y años después volvió a caminar", "at_word": 0, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("Vulović pasó semanas en coma con fracturas graves y acabó recuperando la capacidad de caminar",
             "Guinness World Records")],
   sfx=[{"name": "ding", "at_word": 9}], transition="slide", emphasis=["sobrevivió"])

sc("a15", "ending", "Sigue siendo el récord de la caída más alta sin paracaídas.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "trophy", "x": 0.5, "y": 0.55, "scale": 1.4, "enter": "pop"}],
    "overlays": [{"type": "label", "text": "RÉCORD GUINNESS", "x": 540, "y": 300, "size": 74, "bg": "#E8392F", "at_word": 4}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("La caída de Vulović (10.160 m) sigue siendo el récord Guinness de caída más alta sobrevivida sin paracaídas",
             "Guinness World Records")],
   sfx=[{"name": "sparkle", "at_word": 4}], transition="flash", emphasis=["récord"])

sc("a16", "ending", "¿Tú crees que habrías aguantado? Te leo en comentarios.", {
    "background": sky(0.6),
    "character": {"x": 0.5, "y": 0.78, "scale": 1.3, "action": "talk", "expression": "excited", "actions": [["w5", "point_down"]]},
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Estás a 10.000 metros, sin paracaídas, y caes. ¿Qué le pasaría a tu cuerpo… y existe alguien que lo haya vivido? ✈️

Leo cae desde 10 km y descubre el frío extremo, la falta de oxígeno, la velocidad terminal de unos 200 km/h… y la historia real de Vesna Vulović, la azafata que en 1972 sobrevivió a la caída más alta sin paracaídas.

🧪 DATOS REALES DEL VÍDEO
• A 10.000 m la temperatura de la atmósfera estándar es de unos -50 °C y la presión del aire es solo el 26 % de la del suelo.
• Sin oxígeno suplementario, a esa altura el tiempo de conciencia útil es de menos de 2 minutos.
• Boca abajo, la velocidad terminal en caída libre ronda los 200 km/h.
• El 26 de enero de 1972, el avión JAT 367 estalló en el aire. De las 28 personas a bordo, solo sobrevivió la azafata Vesna Vulović, que cayó 10.160 m.
• Quedó atrapada en la cola, sujeta por un carrito de comida, y la sección cayó sobre una ladera nevada con árboles que amortiguó el golpe.
• Estuvo semanas en coma, volvió a caminar y sigue teniendo el récord Guinness de la caída más alta sobrevivida sin paracaídas.

⚠️ Su supervivencia fue excepcional: nadie debería esperar sobrevivir a una caída así.

📚 Fuentes: Guinness World Records; atmósfera estándar internacional (OACI/ISO 2533); FAA, fisiología de la altitud; Federación Aeronáutica Internacional; Universe Today.

💬 ¿Habrías aguantado tú? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #avion #cuerpohumano #curiosidades #shorts"""

st.save("caer-de-un-avion", "¿Qué pasaría si cayeras de un avión a 10.000 metros?",
        "¿Qué pasaría si cayeras de un avión a 10.000 metros?", "ciencia", "¿Habrías aguantado tú?", {
            "title": "¿Qué pasaría si cayeras de un avión a 10.000 metros? ✈️",
            "hashtags": ["#quepasariasi", "#avion", "#cuerpohumano", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "caer de un avión", "velocidad terminal", "vesna vulovic", "caída libre", "10000 metros",
                     "récord guinness", "cuerpo humano", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Crees que habrías aguantado la caída? ✈️👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "a01", "t": 1.6, "lines": ["¿CAER DE UN", "AVIÓN A 10.000 M?"],
                          "badge": "SIN PARACAÍDAS", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
