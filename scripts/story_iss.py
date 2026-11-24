"""Guion: ¿Qué pasaría si cayeras del espacio a la Tierra desde 400 km?

Escalada: sueltas la ISS → no caes (gravedad ~90 %, caída libre) → 28.000 km/h → el aire te baja despacio → reentrada → caso real Florida 2024.
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, SUIT, Story

st = Story()
sc = st.sc


def leo(**kw):
    d = {"x": 0.5, "y": 0.55, "scale": 1.2, "action": "float", "expression": "wow", **SUIT}
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


ORBIT = {"type": "space", "earth": {"x": 540, "y": 1750, "r": 700}}
FALL = {"type": "sky_fall", "alt": 0.9, "speed": 900}

sc("i01", "hook", "Te sueltas de la estación espacial. ¿Caes a la Tierra?", {
    "background": ORBIT,
    "character": leo(expression="shock", action="shock"),
    "props": [],
    "overlays": [{"type": "title", "lines": ["¿CAER DESDE", "400 KM?"], "y": 250, "size": 112}],
    "camera": {"move": "punch", "impacts": [0.3]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "boom", "at": 0.3, "gain_db": -8}],
   transition="cut", emphasis=["estación", "caes"])

sc("i02", "setup", "La estación orbita a unos cuatrocientos kilómetros de altura.", {
    "background": ORBIT,
    "character": {"visible": False},
    "props": [{"type": "rocket", "x": 0.5, "y": 0.45, "scale": 0.8, "enter": "pop"}],
    "overlays": [counter(400, " KM", 5, sub="ALTURA DE LA ISS", y=330, size=170)],
    "camera": {"move": "static"}},
   claims=[F("La Estación Espacial Internacional orbita a unos 400 km de altura", "NASA, ISS Facts and Figures")],
   sfx=[{"name": "ding", "at_word": 5}], transition="whip", emphasis=["cuatrocientos"])

sc("i03", "setup", "Ahí arriba la gravedad sigue siendo casi un noventa por ciento de la del suelo.", {
    "background": ORBIT,
    "character": leo(expression="surprised", y=0.5),
    "props": [{"type": "gravity_arrows", "x": 0.5, "y": 0.7, "scale": 0.9, "at_word": 4}],
    "overlays": [counter(90, " %", 10, sub="GRAVEDAD EN LA ISS", y=330, size=170)],
    "camera": {"move": "push_in"}},
   claims=[F("A la altura de la ISS la gravedad terrestre es aproximadamente el 90 % de la de la superficie", "NASA, «¿Qué es la microgravedad?»")],
   sfx=[{"name": "ding", "at_word": 10}], transition="slide", emphasis=["noventa"])

sc("i04", "development", "Entonces, ¿por qué flotan los astronautas? Porque están en caída libre.", {
    "background": ORBIT,
    "character": leo(expression="think", action="float", y=0.5),
    "props": [],
    "overlays": [{"type": "fact", "text": "Los astronautas flotan porque la estación y ellos caen alrededor de la Tierra a la vez", "at_word": 5, "y": 1350}],
    "camera": {"move": "static"}},
   claims=[F("Los astronautas flotan porque están en caída libre continua alrededor de la Tierra, no porque no haya gravedad", "NASA")],
   sfx=[{"name": "float", "at_word": 5, "gain_db": -9}], transition="whip", emphasis=["flotan", "libre"])

sc("i05", "development", "No caen porque van de lado a unos veintiocho mil kilómetros por hora.", {
    "background": ORBIT,
    "character": leo(expression="wow", action="float", y=0.5),
    "props": [{"type": "speedlines", "x": 0.5, "y": 0.5, "scale": 1.0}],
    "overlays": [counter(28000, " KM/H", 9, sub="VELOCIDAD ORBITAL", y=330, size=140)],
    "camera": {"move": "punch", "impacts": ["w9"]}},
   claims=[F("La ISS viaja a unos 28.000 km/h (unos 7,7 km/s), tan rápido que al caer siempre «falla» la Tierra", "NASA, ISS Facts and Figures")],
   sfx=[{"name": "whoosh", "at": 0.0, "gain_db": -6}, {"name": "hit", "at_word": 9, "gain_db": -5}], transition="flash", emphasis=["veintiocho", "mil"])

sc("i06", "development", "Si te sueltas, sigues dando vueltas junto a ella. No caes.", {
    "background": ORBIT,
    "character": leo(expression="surprised", action="float", y=0.52),
    "props": [{"type": "rocket", "x": 0.82, "y": 0.28, "scale": 0.5, "enter": "none"}],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "pop", "at_word": 8}], transition="slide", emphasis=["No", "caes"])

sc("i07", "development", "Para bajar tendrías que frenar casi toda esa velocidad, y no hay nada que te frene.", {
    "background": ORBIT,
    "character": leo(expression="worried", action="float", y=0.52),
    "props": [{"type": "question", "x": 0.8, "y": 0.4, "scale": 0.8, "at_word": 12}],
    "overlays": [],
    "camera": {"move": "static"}},
   sfx=[{"name": "tick", "at_word": 12}], transition="whip", emphasis=["frenar"])

sc("i08", "climax", "Solo el aire finísimo te irá bajando, poco a poco. Meses, según el Sol.", {
    "background": ORBIT,
    "character": leo(expression="tired", action="float", y=0.5),
    "props": [{"type": "calendar", "x": 0.82, "y": 0.4, "scale": 0.8, "at_word": 8}],
    "overlays": [{"type": "fact", "text": "Un satélite pequeño soltado desde la ISS tardó 144 días en caer; otros duran cerca de un año", "at_word": 0, "y": 1350}],
    "camera": {"move": "push_in"}},
   claims=[F("Un CubeSat con freno aerodinámico soltado desde la ISS reentró tras 144 días; los satélites sin propulsión suelen durar cerca de un año según la actividad solar",
             "Spaceflight101; Scientific American")],
   sfx=[{"name": "tick", "at_word": 8}], transition="slide", emphasis=["Meses"])

sc("i09", "climax", "Y tu traje se quedaría sin oxígeno mucho antes. Imaginemos que no.", {
    "background": ORBIT,
    "character": leo(expression="scared", action="float", y=0.5),
    "props": [],
    "overlays": [{"type": "fiction", "text": "Imaginemos un traje que te mantiene vivo todo ese tiempo", "at_word": 8, "y": 1350}],
    "camera": {"move": "static"}},
   sfx=[{"name": "ding", "at_word": 8}], transition="whip", emphasis=["oxígeno"])

sc("i10", "climax", "Llegas por fin a la atmósfera a casi ocho kilómetros por segundo.", {
    "background": FALL,
    "character": leo(expression="shock", action="fall", y=0.55),
    "props": [{"type": "speedlines", "x": 0.5, "y": 0.5, "scale": 1.0}],
    "overlays": [counter(7.7, " KM/S", 8, sub="VELOCIDAD DE ENTRADA", y=330, size=150, decimals=1)],
    "camera": {"move": "punch", "impacts": ["w8"]}},
   claims=[F("La velocidad orbital a esa altura es de unos 7,7 km/s", "NASA, ISS Facts and Figures")],
   sfx=[{"name": "whoosh", "at": 0.0, "gain_db": -6}, {"name": "hit", "at_word": 8, "gain_db": -5}], transition="flash", emphasis=["ocho"])

sc("i11", "climax", "El aire se comprime delante de ti y se pone al rojo vivo.", {
    "background": FALL,
    "character": leo(expression="hot", action="fall", y=0.55, sweat=1.0),
    "props": [{"type": "sparks", "x": 0.5, "y": 0.5, "n": 60}, {"type": "heatwaves", "x": 0.5, "y": 0.5},
              {"type": "thermometer", "x": 0.82, "y": 0.5, "scale": 0.9, "level": 0.95, "at_word": 6}],
    "overlays": [lbl("MÁS DE 1.000 °C", "#E8392F", 6, y=300)],
    "camera": {"move": "push_in", "shake": 0.14}},
   claims=[F("En la reentrada, el aire comprimido delante del objeto alcanza miles de grados; no es solo rozamiento", "NASA, reentrada atmosférica")],
   sfx=[{"name": "sizzle", "at_word": 6, "gain_db": -6}], transition="whip", emphasis=["comprime", "rojo"])

sc("i12", "climax", "No sería rozamiento: sería la compresión del aire. Y tú no resistirías.", {
    "background": FALL,
    "character": leo(expression="shock", action="squished", y=0.55),
    "props": [{"type": "burst", "x": 0.5, "y": 0.5, "scale": 1.0}],
    "overlays": [],
    "camera": {"move": "punch", "impacts": ["w10"]}},
   sfx=[{"name": "boom", "at_word": 10, "gain_db": -5}], transition="flash", emphasis=["compresión"])

sc("i13", "ending", "Real: en dos mil veinticuatro, una pieza de una paleta de baterías de la ISS atravesó una casa en Florida.", {
    "background": {"type": "backyard"},
    "character": {"visible": False},
    "props": [{"type": "debris", "x": 0.5, "y": 0.6}, {"type": "pow", "x": 0.5, "y": 0.35, "scale": 1.1, "at_word": 10}],
    "overlays": [lbl("FLORIDA · MARZO 2024", "#1B1B3A", 2, y=300),
                 {"type": "fact", "text": "Un trozo de metal de basura espacial de la ISS atravesó una vivienda de Naples, Florida", "at_word": 10, "y": 560}],
    "camera": {"move": "punch", "impacts": ["w10"]}},
   claims=[F("Una paleta de baterías soltada por la ISS reentró el 8 de marzo de 2024 y un fragmento atravesó una casa en Naples, Florida",
             "NASA; Astronomy.com")],
   sfx=[{"name": "boom", "at_word": 10, "gain_db": -6}], transition="slide", emphasis=["Florida"])

sc("i14", "ending", "Así que no caerías en picado: arderías despacio. ¿Qué harías tú? Te leo en comentarios.", {
    "background": ORBIT,
    "character": leo(expression="excited", action="talk", y=0.5, actions=[["w11", "point_down"]]),
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 11, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 11}], transition="zoom", pause=0.35)

DESC = """Te sueltas de la Estación Espacial Internacional, a 400 km de la Tierra. ¿Caerías de golpe? 🛰️

Spoiler: no. Leo te explica por qué sigues en órbita y qué pasaría meses después, si llegaras a la atmósfera.

🧪 DATOS REALES DEL VÍDEO
• La ISS orbita a unos 400 km de altura y viaja a unos 28.000 km/h (unos 7,7 km/s).
• A esa altura la gravedad es aproximadamente el 90 % de la de la superficie; los astronautas flotan porque están en caída libre continua.
• Un objeto soltado desde la ISS sigue en órbita y desciende lentamente por el rozamiento del aire: un satélite pequeño con freno tardó 144 días y otros duran cerca de un año, según el Sol.
• En la reentrada el aire comprimido delante del objeto alcanza miles de grados.
• El 8 de marzo de 2024 reentró una paleta de baterías soltada desde la ISS y un fragmento atravesó una casa en Naples, Florida.

⚠️ El traje que te mantiene vivo meses es hipotético; la ficción se marca como tal en el vídeo.

📚 Fuentes: NASA (ISS Facts and Figures, microgravedad, reentrada); Spaceflight101; Scientific American; Astronomy.com.

💬 ¿Qué harías tú? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #espacio #iss #curiosidades #shorts"""

st.save("caer-desde-la-iss", "¿Qué pasaría si cayeras del espacio a la Tierra desde 400 km?",
        "¿Qué pasaría si cayeras del espacio a la Tierra desde 400 km?", "espacio",
        "¿Qué harías si cayeras desde la ISS?", {
            "title": "¿Qué pasaría si cayeras del espacio a la Tierra desde 400 km? 🛰️",
            "hashtags": ["#quepasariasi", "#espacio", "#iss", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "caer desde la iss", "caer del espacio", "estación espacial internacional",
                     "reentrada atmosférica", "espacio", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Qué harías tú si cayeras desde la ISS? 🛰️👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "i01", "t": 1.6, "lines": ["¿CAER DESDE", "400 KM?"],
                          "badge": "¿SIGUES EN ÓRBITA?", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 0, "h_scale": 0.9},
        }, mood="epic")
