"""Guion: ¿Qué pasaría si subieras al Everest sin oxígeno?

Escalada por altitud (5.364 → 7.000 → 8.000 → 8.849 m) con contador de metros en pantalla.
"""
from storykit import F, Story

st = Story()
sc = st.sc


def mt(alt, **kw):
    return {"type": "mountain", "alt": alt, **kw}


def leo(**kw):
    d = {"x": 0.5, "y": 0.76, "scale": 1.25, "outfit": "climber", "helmet": "beanie", "action": "walk"}
    d.update(kw)
    return d


def metros(a, b, **kw):
    return {"type": "counter", "from": a, "to": b, "suffix": " m", "over": 1.0, "y": 300, "size": 130, **kw}


def lbl(txt, bg="#E8392F", **kw):
    return {"type": "label", "text": txt, "x": 540, "y": 470, "size": 68, "bg": bg, **kw}


SRC_NHS = "NHS, 'Altitude sickness'"
SRC_WEST = "John B. West, 'Barometric pressures on Mt. Everest', J. Appl. Physiol. (1999)"

sc("v01", "hook", "Subes al Everest sin bombona de oxígeno. Cada metro, el aire es más fino.", {
    "background": mt(0.2),
    "character": leo(expression="determined", actions=[["w9", "sweat"]], expressions=[["w9", "worried"]]),
    "props": [{"type": "oxygen", "x": 0.82, "y": 0.8, "scale": 0.6, "level": 1.0, "until_word": 6},
              {"type": "prayer_flags", "x": 0.5, "y": 0.42, "enter": "none"}],
    "overlays": [{"type": "title", "lines": ["¿EVEREST", "SIN OXÍGENO?"], "y": 250, "size": 120}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   sfx=[{"name": "whoosh", "at_word": 6}, {"name": "hit", "at_word": 6, "gain_db": -6}], transition="cut",
   emphasis=["oxígeno", "fino"])

sc("v02", "setup", "Campo base, a cinco mil trescientos metros: ya respiras la mitad de oxígeno.", {
    "background": mt(0.1),
    "character": leo(x=0.42, action="idle", expression="tired"),
    "props": [{"type": "tent", "x": 0.2, "y": 0.84, "scale": 0.8}, {"type": "tent", "x": 0.82, "y": 0.76,
                                                                     "scale": 0.7, "color": "#2B6BE8"}],
    "overlays": [metros(0, 5364, sub="CAMPO BASE"),
                 lbl("½ DE OXÍGENO", "#2B6BE8", at_word=9)],
    "camera": {"move": "push_in"}},
   claims=[F("El campo base sur del Everest está a unos 5.364 m; allí la presión del aire es aproximadamente la mitad que a nivel del mar",
             SRC_WEST)],
   sfx=[{"name": "ding", "at_word": 9}], emphasis=["mitad"])

sc("v03", "setup", "Te duele la cabeza, no duermes y el corazón va a mil: mal de altura.", {
    "background": mt(0.1),
    "character": leo(x=0.5, action="sweat", expression="dizzy"),
    "props": [{"type": "heart", "x": 0.78, "y": 0.45, "scale": 0.6, "bpm": 130, "at_word": 7}],
    "overlays": [{"type": "fact", "text": "Dolor de cabeza, insomnio, náuseas y mareo son síntomas del mal de altura",
                  "at_word": 10, "y": 250}],
    "camera": {"move": "push_in", "shake": 0.1}},
   claims=[F("Los síntomas del mal agudo de montaña incluyen dolor de cabeza, náuseas, mareo e insomnio", SRC_NHS)],
   sfx=[{"name": "tick", "at_word": 7}], transition="whip", emphasis=["cabeza"])

sc("v04", "setup", "Por eso nadie sube del tirón: pasas semanas subiendo y bajando para aclimatarte.", {
    "background": mt(0.3),
    "character": leo(action="walk", expression="tired", path=[[0, 0.25, 0.79], [2.0, 0.7, 0.73], [4.0, 0.3, 0.78]]),
    "props": [{"type": "calendar", "x": 0.8, "y": 0.35, "scale": 0.7, "at_word": 6}],
    "camera": {"move": "static"}},
   claims=[F("Las expediciones al Everest dedican varias semanas a la aclimatación con rotaciones entre campos",
             "Himalayan Database; Everest expedition practice")],
   emphasis=["semanas"])

sc("v05", "development", "Tu cuerpo responde: fabrica más glóbulos rojos para cargar más oxígeno.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "props": [{"type": "heart", "x": 0.5, "y": 0.6, "scale": 1.3, "bpm": 90, "enter": "pop"}],
    "overlays": [{"type": "counter", "from": 100, "to": 140, "suffix": " %", "at_word": 4, "over": 1.2, "y": 320,
                  "size": 120, "sub": "GLÓBULOS ROJOS (APROX.)"}],
    "camera": {"move": "push_in"}},
   claims=[F("Con la aclimatación aumenta la producción de glóbulos rojos (eritropoyetina)", SRC_NHS + "; " + SRC_WEST,
             "estimate")],
   sfx=[{"name": "sparkle", "at_word": 4}], transition="zoom", emphasis=["glóbulos"])

sc("v06", "development", "Siete mil metros: cada paso te cuesta varias respiraciones.", {
    "background": mt(0.55),
    "character": leo(expression="tired", action="walk", extras={"frost": 0.2}),
    "overlays": [metros(5364, 7000)],
    "camera": {"move": "push_in", "shake": 0.15}},
   sfx=[{"name": "whoosh", "at": 0.3, "gain_db": -6}], transition="whip", emphasis=["paso"])

sc("v07", "development", "Ocho mil metros: entras en la zona de la muerte.", {
    "background": mt(0.8),
    "character": leo(expression="scared", action="sweat", extras={"frost": 0.4}),
    "props": [{"type": "skull", "x": 0.82, "y": 0.42, "scale": 0.7, "at_word": 4, "loop": "wobble"}],
    "overlays": [metros(7000, 8000), lbl("ZONA DE LA MUERTE", at_word=4)],
    "camera": {"move": "punch", "impacts": ["w4"]}},
   claims=[F("Por encima de unos 8.000 m se habla de 'zona de la muerte': el cuerpo no puede aclimatarse", SRC_WEST)],
   sfx=[{"name": "boom", "at_word": 4, "gain_db": -8}], emphasis=["muerte"])

sc("v08", "development", "Aquí arriba, cada bocanada trae solo un tercio del oxígeno que abajo.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#5C8FE6"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.62, "scale": 1.2, "hold": 0.3, "breathe": True}],
    "overlays": [{"type": "label", "text": "⅓ DE OXÍGENO", "x": 540, "y": 330, "size": 90, "bg": "#E8392F",
                  "at_word": 6}],
    "camera": {"move": "static"}},
   claims=[F("En la cima del Everest la presión atmosférica es aproximadamente un tercio de la del nivel del mar",
             SRC_WEST)],
   sfx=[{"name": "ding", "at_word": 6}], transition="slide", emphasis=["tercio"])

sc("v09", "development", "Tu cuerpo ya no se adapta: se va gastando, hora a hora.", {
    "background": mt(0.85),
    "character": leo(expression="dizzy", action="sweat", extras={"frost": 0.5}),
    "props": [{"type": "oxygen", "x": 0.82, "y": 0.8, "scale": 0.6, "level": 0.1}],
    "camera": {"move": "push_in"}},
   claims=[F("En la zona de la muerte el deterioro físico continúa aunque se esté aclimatado", SRC_WEST)],
   emphasis=["gastando"])

sc("v10", "development", "Puede encharcarse tu pulmón o hincharse tu cerebro, y casi no te das cuenta.", {
    "background": {"type": "burst", "c1": "#9D7BFF", "c2": "#C2B0FF"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.3, "y": 0.6, "scale": 0.9, "hold": 0.8, "at_word": 2},
              {"type": "brain", "x": 0.72, "y": 0.6, "scale": 0.8, "dirt": 0.5, "at_word": 7, "loop": "wobble"}],
    "overlays": [{"type": "fact", "label": "PELIGRO", "text": "Edema pulmonar y cerebral de altura: pueden ser mortales",
                  "at_word": 10, "y": 250}],
    "camera": {"move": "push_in", "shake": 0.1}},
   claims=[F("El edema pulmonar (HAPE) y cerebral (HACE) de altura son complicaciones potencialmente mortales", SRC_NHS)],
   sfx=[{"name": "crack", "at_word": 7, "gain_db": -8}], transition="zoom", emphasis=["pulmón", "cerebro"])

sc("v11", "climax", "Y por fin: ocho mil ochocientos cuarenta y nueve metros. La cima.", {
    "background": mt(1.0, summit=True),
    "character": leo(y=0.74, action="celebrate", expression="excited", extras={"frost": 0.5}),
    "props": [{"type": "prayer_flags", "x": 0.5, "y": 0.6, "w": 700, "scale": 0.8}],
    "overlays": [metros(8000, 8849, sub="CIMA DEL EVEREST", at_word=4)],
    "camera": {"move": "zoom_burst"}},
   claims=[F("La altura oficial del Everest es de 8.848,86 m (medición de China y Nepal, 2020)",
             "Gobiernos de Nepal y China, 2020")],
   sfx=[{"name": "riser", "at": 0}, {"name": "ding", "at_word": 4}], transition="flash", emphasis=["cima"])

sc("v12", "climax", "¿Imposible? No: en mil novecientos setenta y ocho, Messner y Habeler lo lograron sin oxígeno.", {
    "background": mt(1.0, summit=True),
    "character": leo(y=0.74, action="present", expression="wow"),
    "overlays": [{"type": "label", "text": "8 DE MAYO DE 1978", "x": 540, "y": 330, "size": 72, "bg": "#22B573",
                  "at_word": 2}],
    "camera": {"move": "static"}},
   claims=[F("Reinhold Messner y Peter Habeler hicieron la primera ascensión al Everest sin oxígeno embotellado el 8 de mayo de 1978",
             "Encyclopaedia Britannica")],
   sfx=[{"name": "sparkle", "at_word": 2}], emphasis=["Messner"])

sc("v13", "climax", "Aun así, solo un pequeño porcentaje de quienes hacen cumbre lo consigue sin bombona.", {
    "background": {"type": "burst", "c1": "#FF8A00", "c2": "#FFB24D"},
    "character": {"visible": False},
    "props": [{"type": "oxygen", "x": 0.3, "y": 0.75, "scale": 0.9, "level": 1.0},
              {"type": "oxygen", "x": 0.5, "y": 0.75, "scale": 0.9, "level": 1.0},
              {"type": "oxygen", "x": 0.7, "y": 0.75, "scale": 0.9, "level": 1.0}],
    "overlays": [{"type": "label", "text": "MENOS DEL 5 %", "x": 540, "y": 330, "size": 90, "bg": "#E8392F",
                  "at_word": 4}],
    "camera": {"move": "push_in"}},
   claims=[F("Solo una pequeña parte (en torno al 3-5 %) de las ascensiones al Everest se han hecho sin oxígeno embotellado",
             "Himalayan Database", "estimate")],
   emphasis=["porcentaje"])

sc("v14", "climax", "Y lo peor viene después: la mayoría de muertes en la zona alta ocurren al bajar.", {
    "background": mt(0.85),
    "character": leo(action="walk_back", expression="dizzy", extras={"frost": 0.6}, path=[[0, 0.7, 0.72],
                                                                                           [4, 0.3, 0.79]]),
    "overlays": [{"type": "fact", "text": "Un estudio de 1921-2006 halló que la mayoría de muertes cerca de la cima ocurrieron durante el descenso",
                  "at_word": 9, "y": 250}],
    "camera": {"move": "pan_down", "amount": 160}},
   claims=[F("La mayoría de muertes de escaladores en la zona alta del Everest ocurren durante el descenso",
             "Firth et al., 'Mortality on Mount Everest, 1921-2006', BMJ (2008)")],
   sfx=[{"name": "fall", "at_word": 9, "gain_db": -8}], transition="whip", emphasis=["bajar"])

sc("v15", "ending", "Y si te dejaran en la cima sin aclimatarte, te desmayarías en pocos minutos.", {
    "background": mt(1.0, summit=True),
    "character": leo(y=0.74, action="fall", expression="happy_closed"),
    "overlays": [{"type": "timer", "text": "2 MIN", "x": 860, "y": 320, "p0": 0, "p1": 1, "over": 2.0,
                  "at_word": 10}],
    "camera": {"move": "push_in", "zoom_to": 1.2}},
   claims=[F("A unos 8.500-9.000 m sin aclimatar ni oxígeno, el tiempo de conciencia útil es de solo 1-3 minutos",
             "FAA, 'Hypoxia: the higher you fly…' (tiempo de conciencia útil)", "estimate")],
   sfx=[{"name": "fall", "at_word": 9, "gain_db": -6}], emphasis=["minutos"])

sc("v16", "ending", "¿Tú subirías al Everest sin oxígeno? Te leo en comentarios.", {
    "background": mt(0.2),
    "character": leo(action="talk", expression="excited", actions=[["w5", "point_down"]], x=0.5),
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5,
                  "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Subes al Everest sin bombona de oxígeno… ¿qué le pasa a tu cuerpo metro a metro? 🏔️

Leo sube desde el campo base hasta la cima y descubre qué hace la falta de oxígeno: mal de altura, aclimatación, la zona de la muerte y por qué lo más peligroso es bajar.

🧪 DATOS REALES DEL VÍDEO
• En el campo base (unos 5.364 m) la presión del aire es más o menos la mitad que a nivel del mar.
• Dolor de cabeza, insomnio, náuseas y mareo: síntomas del mal de altura.
• Las expediciones pasan semanas aclimatándose; el cuerpo fabrica más glóbulos rojos.
• Por encima de unos 8.000 m está la «zona de la muerte»: el cuerpo ya no puede aclimatarse.
• En la cima la presión es aproximadamente un tercio de la del nivel del mar.
• El edema pulmonar y el cerebral de altura pueden ser mortales.
• Altura oficial: 8.848,86 m (medición de 2020).
• Messner y Habeler subieron sin oxígeno embotellado el 8 de mayo de 1978.
• Solo una pequeña parte de las ascensiones se hacen sin oxígeno (estimación).
• La mayoría de muertes en la zona alta ocurren durante el descenso (BMJ, 2008).
• Sin aclimatar, a esa altura perderías el conocimiento en pocos minutos.

📚 Fuentes: J. B. West (J. Appl. Physiol.), NHS, Himalayan Database, Firth et al. (BMJ 2008), Encyclopaedia Britannica, FAA.

💬 ¿Tú subirías al Everest sin oxígeno? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #everest #cuerpohumano #montaña #shorts"""

st.save("everest-sin-oxigeno", "¿Qué pasaría si subieras al Everest sin oxígeno?",
        "¿Qué pasaría si subieras al Everest sin oxígeno?", "cuerpo humano",
        "¿Tú subirías al Everest sin oxígeno?", {
            "title": "¿Qué pasaría si subieras 8.849 m sin oxígeno? 💀",
            "hashtags": ["#quepasariasi", "#everest", "#cuerpohumano", "#montaña", "#shorts"],
            "tags": ["qué pasaría si", "everest", "sin oxígeno", "zona de la muerte", "mal de altura", "messner",
                     "montaña", "alpinismo", "cuerpo humano", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Hasta qué altura crees que llegarías tú? 🏔️👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "v07", "t": 1.5, "lines": ["¿EVEREST", "SIN OXÍGENO?"],
                          "badge": "8.000 m: ZONA DE LA MUERTE", "badge_pos": [540, 1640], "y": 260,
                          "character": {"action": "sweat", "expression": "scared", "x": 0.5, "y": 0.8, "scale": 1.5,
                                        "outfit": "climber", "helmet": "beanie", "extras": {"frost": 0.4}},
                          "crop_y": 0.55, "h_shift": 800, "h_scale": 0.8},
        }, mood="epic")
