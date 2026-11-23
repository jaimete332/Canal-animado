"""Guion: ¿Qué pasaría si cayeras hacia Júpiter?

Escalada: tamaño → sin suelo → radiación → gravedad → entrada a 47 km/s (sonda Galileo, 1995) → presión y calor → sin fondo.
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, SUIT, Story

st = Story()
sc = st.sc


def leo(**kw):
    d = {"x": 0.5, "y": 0.62, "scale": 1.25, "action": "float", "expression": "wow", **SUIT}
    d.update(kw)
    return d


def counter(to, suffix, at_word, sub=None, frm=0, y=330, size=130, **kw):
    o = {"type": "counter", "from": frm, "to": to, "suffix": suffix, "at_word": at_word, "over": 0.8, "y": y, "size": size, **kw}
    if sub:
        o["sub"] = sub
    return o


def lbl(txt, bg="#E8392F", at_word=None, y=300, size=66):
    o = {"type": "label", "text": txt, "x": 540, "y": y, "size": size, "bg": bg}
    if at_word is not None:
        o["at_word"] = at_word
    return o


APPROACH = {"type": "jupiter", "mode": "approach"}


def clouds(depth, **kw):
    return {"type": "jupiter", "mode": "clouds", "depth": depth, **kw}


sc("j01", "hook", "Una nave te suelta y caes hacia Júpiter.", {
    "background": APPROACH,
    "character": leo(y=0.52, scale=1.1, expression="shock"),
    "props": [],
    "overlays": [{"type": "title", "lines": ["¿CAER HACIA", "JÚPITER?"], "y": 250, "size": 112}],
    "camera": {"move": "punch", "impacts": [0.2]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "boom", "at": 0.3, "gain_db": -8}],
   transition="cut", emphasis=["Júpiter"])

sc("j02", "setup", "Es tan grande que dentro cabrían más de mil Tierras.", {
    "background": {"type": "space"},
    "character": {"visible": False},
    "props": [{"type": "jupiter_ball", "x": 0.5, "y": 0.62, "r": 360, "enter": "pop"},
              {"type": "earth", "x": 0.82, "y": 0.2, "scale": 0.35, "at_word": 6}],
    "overlays": [counter(1300, " TIERRAS", 6, sub="CABRÍAN DENTRO DE JÚPITER", y=330, size=140)],
    "camera": {"move": "static"}},
   claims=[F("El volumen de Júpiter equivale a más de 1.300 Tierras", "NASA, ficha de datos de Júpiter")],
   sfx=[{"name": "ding", "at_word": 6}], transition="whip", emphasis=["mil"])

sc("j03", "setup", "Pero ojo: no tiene suelo. Es una bola enorme de gas.", {
    "background": APPROACH,
    "character": leo(y=0.4, scale=1.0, expression="surprised"),
    "props": [],
    "overlays": [{"type": "fact", "text": "Júpiter es un gigante gaseoso: no tiene una superficie sólida", "at_word": 3, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("Júpiter es un gigante gaseoso sin superficie sólida", "NASA Science, Júpiter")],
   sfx=[{"name": "pop", "at_word": 3}], transition="slide", emphasis=["suelo"])

sc("j04", "development", "Su radiación es tan fuerte que Juno protege su electrónica con titanio.", {
    "background": {"type": "jupiter", "mode": "approach", "rise": 0.4},
    "character": {"visible": False},
    "props": [{"type": "sparks", "x": 0.5, "y": 0.5, "n": 40},
              {"type": "gem", "x": 0.5, "y": 0.52, "scale": 2.0, "color": "#B8BDC9", "at_word": 9}],
    "overlays": [lbl("SONDA JUNO · NASA", "#1B1B3A", 3)],
    "camera": {"move": "push_in"}},
   claims=[F("La sonda Juno de la NASA protege su electrónica de la radiación de Júpiter con una bóveda de titanio", "NASA/JPL, misión Juno")],
   sfx=[{"name": "sparkle", "at_word": 9}], transition="zoom", emphasis=["radiación", "titanio"])

sc("j05", "development", "La gravedad también aprieta: pesarías dos veces y media más que en la Tierra.", {
    "background": APPROACH,
    "character": leo(y=0.52, scale=1.2, expression="tired", action="idle"),
    "props": [{"type": "gravity_arrows", "x": 0.5, "y": 0.5, "scale": 1.0, "at_word": 3}],
    "overlays": [counter(2.5, "×", 8, sub="TU PESO EN JÚPITER", y=330, size=170, decimals=1)],
    "camera": {"move": "push_in"}},
   claims=[F("La gravedad en las nubes altas de Júpiter es unas 2,5 veces la de la Tierra (24,8 m/s²)", "NASA, ficha de datos de Júpiter")],
   sfx=[{"name": "hit", "at_word": 8, "gain_db": -6}], emphasis=["dos"])

sc("j06", "development", "Llegas a las nubes a unos cuarenta y siete kilómetros por segundo.", {
    "background": clouds(0.05, speed=900),
    "character": leo(y=0.55, scale=1.15, expression="scared", action="fall"),
    "props": [{"type": "speedlines", "x": 0.5, "y": 0.5, "scale": 1.0}],
    "overlays": [counter(47, " KM/S", 7, sub="COMO LA SONDA GALILEO", y=330, size=170)],
    "camera": {"move": "punch", "impacts": ["w7"]}},
   claims=[F("La sonda Galileo entró en la atmósfera de Júpiter el 7 de diciembre de 1995 a unos 47 km/s",
             "NASA/JPL, dossier de prensa de la misión Galileo")],
   sfx=[{"name": "whoosh", "at": 0.0, "gain_db": -6}, {"name": "hit", "at_word": 7, "gain_db": -5}],
   transition="flash", emphasis=["cuarenta", "siete"])

sc("j07", "development", "Eso son ciento setenta mil kilómetros por hora.", {
    "background": clouds(0.1, speed=1100),
    "character": leo(y=0.55, scale=1.15, expression="shock", action="fall"),
    "props": [],
    "overlays": [counter(170000, " KM/H", 3, y=330, size=140)],
    "camera": {"move": "static"}},
   sfx=[{"name": "tick", "at_word": 3}], emphasis=["ciento", "setenta"])

sc("j08", "climax", "El aire te frena de golpe, con hasta doscientas treinta veces la gravedad.", {
    "background": clouds(0.2, speed=700),
    "character": leo(y=0.55, scale=1.1, expression="shock", action="squished"),
    "props": [{"type": "probe", "x": 0.5, "y": 0.28, "scale": 0.9, "fire": 1.0, "enter": "none"}],
    "overlays": [counter(230, " G", 10, sub="FRENAZO DE LA SONDA GALILEO", y=480, size=170)],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   claims=[F("La sonda Galileo soportó una deceleración de hasta unas 230 veces la gravedad terrestre en la entrada",
             "NASA/JPL, dossier de prensa de la misión Galileo")],
   sfx=[{"name": "boom", "at_word": 6, "gain_db": -5}], transition="flash", emphasis=["doscientas", "treinta"])

sc("j09", "climax", "Ningún cuerpo humano aguanta eso. Imagina que tu traje sí.", {
    "background": clouds(0.25, speed=500),
    "character": leo(y=0.58, scale=1.2, expression="determined", action="fall"),
    "props": [],
    "overlays": [{"type": "fiction", "text": "Imaginemos un traje capaz de resistirlo todo", "at_word": 6, "y": 560}],
    "camera": {"move": "static"}},
   sfx=[{"name": "ding", "at_word": 6}], transition="slide", emphasis=["Imagina"])

sc("j10", "climax", "Caes entre nubes de amoníaco y vientos de cientos de kilómetros por hora.", {
    "background": clouds(0.35, speed=420, lightning=True),
    "character": leo(y=0.6, scale=1.2, expression="scared", action="fall"),
    "props": [],
    "overlays": [{"type": "fact", "text": "Las nubes altas de Júpiter son de amoníaco; sus vientos superan los cientos de km/h", "at_word": 0, "y": 560}],
    "camera": {"move": "push_in", "shake": 0.12}},
   claims=[F("Las nubes superiores de Júpiter son de hielo de amoníaco y sus vientos alcanzan cientos de kilómetros por hora",
             "NASA Science, Júpiter")],
   sfx=[{"name": "rumble", "at": 0.1, "gain_db": -8}], transition="whip", emphasis=["amoníaco"])

sc("j11", "climax", "Hay tormentas más grandes que la Tierra, como la Gran Mancha Roja.", {
    "background": clouds(0.3, speed=300, spot=True),
    "character": leo(y=0.75, scale=1.05, expression="wow", action="fall"),
    "props": [{"type": "earth", "x": 0.2, "y": 0.2, "scale": 0.28}],
    "overlays": [lbl("GRAN MANCHA ROJA", "#E8392F", 6, y=300)],
    "camera": {"move": "push_in"}},
   claims=[F("La Gran Mancha Roja es una tormenta más ancha que la Tierra que lleva siglos activa", "NASA Science, Gran Mancha Roja")],
   sfx=[{"name": "sparkle", "at_word": 6}], transition="zoom", emphasis=["Roja"])

sc("j12", "climax", "Cuanto más bajas, más aprietan la presión y el calor.", {
    "background": clouds(0.6, speed=350),
    "character": leo(y=0.6, scale=1.2, expression="hot", action="fall", sweat=1.0),
    "props": [{"type": "thermometer", "x": 0.82, "y": 0.5, "scale": 0.9, "level": 0.7, "at_word": 4}],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "riser", "at": 0.1, "gain_db": -9}], transition="slide", emphasis=["presión", "calor"])

sc("j13", "climax", "A unos doscientos kilómetros, la sonda Galileo soportó veintitrés veces la presión terrestre.", {
    "background": clouds(0.8, speed=250),
    "character": {"visible": False},
    "props": [{"type": "probe", "x": 0.5, "y": 0.55, "scale": 1.1, "fire": 0.3, "enter": "none"}],
    "overlays": [lbl("200 KM DE PROFUNDIDAD", "#1B1B3A", 3, y=300), counter(23, "×", 9, sub="LA PRESIÓN DE LA TIERRA", y=480, size=170)],
    "camera": {"move": "push_in"}},
   claims=[F("La sonda Galileo transmitió hasta unos 200 km de profundidad, donde la presión era de unos 23 bar",
             "NASA/JPL, misión Galileo")],
   sfx=[{"name": "ding", "at_word": 9}], transition="flash", emphasis=["veintitrés"])

sc("j14", "climax", "Allí hacía más de ciento cincuenta grados, y dejó de emitir tras cincuenta y ocho minutos.", {
    "background": clouds(0.95, speed=200),
    "character": {"visible": False},
    "props": [{"type": "probe", "x": 0.5, "y": 0.55, "scale": 1.0, "fire": 0.0, "enter": "none", "loop": "shake"},
              {"type": "thermometer", "x": 0.82, "y": 0.45, "scale": 0.9, "level": 0.95}],
    "overlays": [counter(58, " MIN", 12, sub="HASTA QUE SE SILENCIÓ", y=330, size=170)],
    "camera": {"move": "push_in"}},
   claims=[F("La sonda Galileo dejó de transmitir a unos 152 °C tras 58 minutos en la atmósfera de Júpiter",
             "NASA/JPL, misión Galileo")],
   sfx=[{"name": "sizzle", "at_word": 9, "gain_db": -6}, {"name": "tick", "at_word": 12}], transition="whip", emphasis=["cincuenta", "ocho"])

sc("j15", "ending", "Y no hay suelo donde parar: solo gas cada vez más denso y caliente.", {
    "background": clouds(1.0, speed=150),
    "character": {"visible": False},
    "props": [],
    "overlays": [{"type": "fiction", "label": "HIPÓTESIS", "text": "Más abajo el hidrógeno se vuelve líquido y, quizá, metálico", "at_word": 0, "y": 560}],
    "camera": {"move": "pull_out"}},
   sfx=[{"name": "float", "at": 0.1, "gain_db": -9}], transition="circle", emphasis=["suelo"])

sc("j16", "ending", "¿Tú te atreverías a caer hacia Júpiter? Te leo en comentarios.", {
    "background": APPROACH,
    "character": leo(y=0.45, scale=1.2, action="talk", expression="excited", actions=[["w8", "point_down"]]),
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 8, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 8}], transition="zoom", pause=0.35)

DESC = """Una nave te suelta y caes hacia Júpiter, el planeta más grande del sistema solar. ¿Cuánto aguantarías? 🪐

Leo cae hacia Júpiter con una sonda real como guía: la Galileo, que entró en 1995 a 47 km/s y siguió transmitiendo 58 minutos.

🧪 DATOS REALES DEL VÍDEO
• El volumen de Júpiter equivale a más de 1.300 Tierras.
• Es un gigante gaseoso: no tiene superficie sólida.
• La sonda Juno protege su electrónica de la radiación con una bóveda de titanio.
• La gravedad en sus nubes altas es unas 2,5 veces la de la Tierra.
• La sonda Galileo entró en su atmósfera el 7 de diciembre de 1995 a unos 47 km/s (unos 170.000 km/h) y frenó con hasta unas 230 g.
• A unos 200 km de profundidad la presión era de unos 23 bar y la temperatura rondaba los 152 °C; la sonda dejó de transmitir tras 58 minutos.
• La Gran Mancha Roja es una tormenta más ancha que la Tierra.

⚠️ Los tramos con el traje «imposible» y el interior profundo de Júpiter son hipotéticos: ningún humano sobreviviría a la entrada.

📚 Fuentes: NASA Science (Júpiter y Gran Mancha Roja); NASA/JPL, dossier de prensa de la misión Galileo; NASA/JPL, misión Juno.

💬 ¿Te atreverías? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #jupiter #espacio #curiosidades #shorts"""

st.save("caer-hacia-jupiter", "¿Qué pasaría si cayeras hacia Júpiter?",
        "¿Qué pasaría si cayeras hacia Júpiter?", "espacio", "¿Te atreverías a caer hacia Júpiter?", {
            "title": "¿Qué pasaría si cayeras hacia Júpiter? 🪐",
            "hashtags": ["#quepasariasi", "#jupiter", "#espacio", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "caer hacia júpiter", "júpiter", "sonda galileo", "gran mancha roja", "gigante gaseoso",
                     "espacio", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Te atreverías a caer hacia Júpiter? 🪐👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "j01", "t": 1.6, "lines": ["¿CAER HACIA", "JÚPITER?"],
                          "badge": "SIN SUELO", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 800, "h_scale": 0.8},
        }, mood="epic")
