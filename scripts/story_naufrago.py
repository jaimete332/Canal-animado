"""Guion: ¿Qué pasaría si te quedaras atrapado en el mar sin agua 3 días?

Escalada: rodeado de agua → sal del mar → riñones → beber mar deshidrata → ~3 días sin agua → Poon Lim (1942, 133 días).
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, Story

st = Story()
sc = st.sc
SEA = {"type": "ocean", "level": 1000}


def sea(y=1500, **kw):
    return {"type": "sea_front", "abs": True, "x": 0, "y": y, "layer": "front", "enter": "none", **kw}


def leo(**kw):
    d = {"x": 0.5, "y": 0.97, "scale": 1.25, "action": "swim", "expression": "worried"}
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


sc("n01", "hook", "Flotas en mitad del mar, sin una gota de agua.", {
    "background": SEA,
    "character": leo(expression="shock", actions=[["w5", "shock"]]),
    "props": [sea(), {"type": "sun", "x": 0.8, "y": 0.18, "scale": 1.2, "enter": "none"}],
    "overlays": [{"type": "title", "lines": ["¿3 DÍAS SIN", "AGUA EN EL MAR?"], "y": 250, "size": 104}],
    "camera": {"move": "punch", "impacts": [0.3]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "splash", "at": 0.3, "gain_db": -8}],
   transition="cut", emphasis=["mar", "agua"])

sc("n02", "setup", "Estás rodeado de agua, pero no puedes beberla.", {
    "background": SEA,
    "character": leo(expression="worried", action="swim"),
    "props": [sea(), {"type": "water_bottle", "x": 0.78, "y": 0.5, "scale": 0.8, "at_word": 4}],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "pop", "at_word": 4}], transition="whip", emphasis=["beberla"])

sc("n03", "setup", "El mar lleva unos treinta y cinco gramos de sal por litro.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#5C8FE6"},
    "character": {"visible": False},
    "props": [{"type": "water_bottle", "x": 0.5, "y": 0.78, "scale": 1.5, "label": "MAR", "enter": "pop"}],
    "overlays": [counter(35, " g DE SAL", 6, sub="POR CADA LITRO DE AGUA DE MAR", y=330, size=130)],
    "camera": {"move": "static"}},
   claims=[F("El agua de mar tiene una salinidad media de unos 35 g de sal por litro (≈3,5 %)", "NOAA, National Ocean Service")],
   sfx=[{"name": "ding", "at_word": 6}], transition="slide", emphasis=["treinta", "sal"])

sc("n04", "development", "Y tus riñones solo pueden fabricar orina menos salada que el mar.", {
    "background": {"type": "color", "color": "#3A1B2B"},
    "character": {"visible": False},
    "props": [{"type": "brain", "x": 0.5, "y": 0.55, "scale": 1.0, "enter": "pop"}],
    "overlays": [{"type": "fact", "text": "Los riñones humanos no pueden producir orina más salada que el agua de mar", "at_word": 3, "y": 300}],
    "camera": {"move": "push_in"}},
   claims=[F("Los riñones humanos solo producen orina menos salada que el agua de mar", "NOAA, National Ocean Service")],
   sfx=[{"name": "pop", "at_word": 3}], transition="zoom", emphasis=["riñones", "menos"])

sc("n05", "development", "Así que, por cada trago de mar, perderías más agua de la que bebes.", {
    "background": SEA,
    "character": leo(expression="sick", action="swim"),
    "props": [sea(), {"type": "water_bottle", "x": 0.2, "y": 0.62, "scale": 0.7, "label": "MAR", "enter": "none"}],
    "overlays": [lbl("BEBES 1 L", "#2B6BE8", 4, y=300), lbl("PIERDES MÁS", "#E8392F", 10, y=430)],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "hit", "at_word": 10, "gain_db": -6}], transition="whip", emphasis=["más"])

sc("n06", "development", "Beber del mar es peor que no beber nada. Te seca por dentro.", {
    "background": SEA,
    "character": leo(expression="scared", action="swim"),
    "props": [sea(), {"type": "skull", "x": 0.78, "y": 0.45, "scale": 0.8, "at_word": 8}],
    "overlays": [{"type": "fact", "text": "Un náufrago sin agua dulce empeora si bebe agua de mar", "at_word": 0, "y": 560}],
    "camera": {"move": "punch", "impacts": ["w8"]}},
   claims=[F("Para un náufrago sin agua dulce, beber agua de mar es peor que no beber nada", "Mental Floss, médico de medicina de montaña/salvamento; NOAA")],
   sfx=[{"name": "sizzle", "at_word": 8, "gain_db": -7}], transition="flash", emphasis=["peor", "nada"])

sc("n07", "development", "Día uno: sed, dolor de cabeza y la boca pastosa bajo el sol.", {
    "background": SEA,
    "character": leo(expression="hot", action="swim", sweat=1.0),
    "props": [sea(), {"type": "sun", "x": 0.8, "y": 0.18, "scale": 1.3, "enter": "none"},
              {"type": "heatwaves", "x": 0.5, "y": 0.5}],
    "overlays": [lbl("DÍA 1", "#E8392F", 0, y=300)],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "tick", "at_word": 0}], transition="slide", emphasis=["sed"])

sc("n08", "climax", "Sin agua, la mayoría aguanta unos tres días. Con calor, menos.", {
    "background": SEA,
    "character": leo(expression="tired", action="idle", y=0.95),
    "props": [sea()],
    "overlays": [counter(3, " DÍAS", 7, sub="SIN AGUA (ENTRE 3 Y 7 SEGÚN EL CALOR)", y=330, size=170)],
    "camera": {"move": "static"}},
   claims=[F("Una persona suele sobrevivir unos 3 días sin agua (entre 3 y 7 según calor y esfuerzo)", "Live Science; regla de supervivencia de los tres")],
   sfx=[{"name": "ding", "at_word": 7}], transition="whip", emphasis=["tres"])

sc("n09", "climax", "Pero hay un caso real: Poon Lim, un marinero, en mil novecientos cuarenta y dos.", {
    "background": {"type": "night_sky"},
    "character": {"visible": False},
    "props": [{"type": "lifeboat", "x": 0.5, "y": 0.72, "scale": 0.8, "people": 0, "enter": "none"}, sea(color=(0.02, 0.05, 0.14))],
    "overlays": [lbl("POON LIM · 1942", "#1B1B3A", 5, y=300)],
    "camera": {"move": "push_in"}},
   claims=[F("Poon Lim, mayordomo del SS Benlomond, sobrevivió solo en una balsa tras el hundimiento de su barco en noviembre de 1942", "Wikipedia; Guinness World Records")],
   sfx=[{"name": "boom", "at": 0.1, "gain_db": -9}], transition="zoom", emphasis=["Poon", "Lim"])

sc("n10", "climax", "Torpedearon su barco y se quedó solo en una balsa diminuta.", {
    "background": SEA,
    "character": leo(expression="scared", action="idle", y=0.9, scale=1.0),
    "props": [{"type": "lifeboat", "x": 0.5, "y": 0.68, "scale": 0.8, "people": 0, "enter": "none"}, sea()],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "float", "at": 0.1, "gain_db": -9}], transition="slide", emphasis=["solo"])

sc("n11", "climax", "Bebió agua de lluvia que recogía con una lona, y comía pescado y aves.", {
    "background": SEA,
    "character": leo(expression="determined", action="present", y=0.9, scale=1.0),
    "props": [{"type": "lifeboat", "x": 0.5, "y": 0.68, "scale": 0.8, "people": 0, "enter": "none"},
              {"type": "water_bottle", "x": 0.2, "y": 0.45, "scale": 0.6, "label": "LLUVIA", "at_word": 3}, sea()],
    "overlays": [{"type": "fact", "text": "Recogía lluvia con una cubierta de la balsa y pescaba con un anzuelo improvisado", "at_word": 0, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("Poon Lim recogió agua de lluvia en una lona y se alimentó de pescado y aves", "Wikipedia; Guinness World Records")],
   sfx=[{"name": "pop", "at_word": 3}], transition="whip", emphasis=["lluvia", "pescado"])

sc("n12", "climax", "Aguantó ciento treinta y tres días. Es el récord de un náufrago solo en una balsa.", {
    "background": SEA,
    "character": leo(expression="proud", action="celebrate", y=0.9, scale=1.0),
    "props": [{"type": "lifeboat", "x": 0.5, "y": 0.68, "scale": 0.8, "people": 0, "enter": "none"}, sea(),
              {"type": "trophy", "x": 0.8, "y": 0.35, "scale": 0.8, "at_word": 8}],
    "overlays": [counter(133, " DÍAS", 2, sub="LA BALSA DE POON LIM", y=330, size=150)],
    "camera": {"move": "punch", "impacts": ["w2"]}},
   claims=[F("Poon Lim pasó 133 días a la deriva en el Atlántico Sur y fue rescatado por pescadores brasileños en 1943",
             "Wikipedia; Guinness World Records")],
   sfx=[{"name": "hit", "at_word": 2, "gain_db": -5}, {"name": "sparkle", "at_word": 8}], transition="flash", emphasis=["ciento", "treinta"])

sc("n13", "ending", "La clave no era el mar. Era la lluvia.", {
    "background": SEA,
    "character": leo(expression="excited", action="point_up", y=0.92),
    "props": [sea()],
    "overlays": [{"type": "label", "text": "NO BEBAS AGUA DE MAR", "x": 540, "y": 330, "size": 70, "bg": "#E8392F", "at_word": 0}],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "ding", "at_word": 0}], transition="zoom", emphasis=["lluvia"])

sc("n14", "ending", "¿Tú habrías sobrevivido? Te leo en comentarios.", {
    "background": SEA,
    "character": leo(expression="excited", action="talk", y=0.92, actions=[["w4", "point_down"]]),
    "props": [sea()],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 4, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 4}], transition="zoom", pause=0.35)

DESC = """Flotas en mitad del mar, sin agua dulce. ¿Cuánto aguantarías? 🌊

Leo se queda a la deriva y cuenta por qué no puedes beber del mar… y cómo un marinero real sobrevivió 133 días.

🧪 DATOS REALES DEL VÍDEO
• El agua de mar tiene unos 35 gramos de sal por litro.
• Los riñones humanos solo producen orina menos salada que el agua de mar, así que beber mar te deshidrata.
• Una persona suele aguantar unos 3 días sin agua (entre 3 y 7 según el calor y el esfuerzo).
• Poon Lim, mayordomo del SS Benlomond, torpedeado en noviembre de 1942, pasó 133 días en una balsa en el Atlántico Sur. Bebió agua de lluvia y comió pescado y aves.

📚 Fuentes: NOAA National Ocean Service («¿Por qué no podemos beber agua de mar?»); Mental Floss; Live Science (cuánto se sobrevive sin agua); Wikipedia y Guinness World Records (Poon Lim).

💬 ¿Habrías sobrevivido? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #supervivencia #mar #curiosidades #shorts"""

st.save("naufrago-sin-agua", "¿Qué pasaría si te quedaras atrapado en el mar sin agua 3 días?",
        "¿Qué pasaría si te quedaras atrapado en el mar sin agua 3 días?", "supervivencia",
        "¿Habrías sobrevivido en el mar sin agua?", {
            "title": "¿Qué pasaría si te quedaras atrapado en el mar sin agua 3 días? 🌊",
            "hashtags": ["#quepasariasi", "#supervivencia", "#mar", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "náufrago", "beber agua de mar", "sin agua 3 días", "poon lim", "supervivencia en el mar",
                     "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Habrías sobrevivido en el mar sin agua? 🌊👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "n01", "t": 1.6, "lines": ["¿3 DÍAS SIN", "AGUA EN EL MAR?"],
                          "badge": "NO BEBAS DEL MAR", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 0, "h_scale": 0.9},
        }, mood="tense")
