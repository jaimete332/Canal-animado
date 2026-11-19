"""Guion: ¿Qué pasaría si estuvieras 1 hora en el agua helada del Titanic?

Escalada por minutos (0 → 1 → 10 → 30 → 60). Tono respetuoso: fue una tragedia real con más de 1.500 víctimas.
"""
from storykit import F, Story

st = Story()
sc = st.sc
SEA = {"type": "ice_sea", "level": 1050}


def sea(y=1600, **kw):
    return {"type": "sea_front", "abs": True, "x": 0, "y": y, "layer": "front", "enter": "none", **kw}


def leo(frost=0.0, **kw):
    d = {"x": 0.5, "y": 0.99, "scale": 1.25, "action": "swim", "extras": {"frost": frost}}
    d.update(kw)
    return d


def lbl(txt, bg="#2B6BE8", **kw):
    return {"type": "label", "text": txt, "x": 400, "y": 300, "size": 72, "bg": bg, **kw}


def clock(txt, p0, p1, **kw):
    return {"type": "timer", "text": txt, "x": 870, "y": 300, "p0": p0, "p1": p1, "over": 1.5, **kw}


sc("t01", "hook", "El Titanic se está hundiendo y caes al agua helada. Aguanta una hora.", {
    "background": SEA,
    "character": leo(0.1, expression="scared", actions=[["w8", "shock"]]),
    "props": [{"type": "liner", "x": 0.55, "y": 0.5, "scale": 0.55, "tilt": 0.32, "sink": 0.15, "enter": "none"},
              sea()],
    "overlays": [{"type": "title", "lines": ["¿1 HORA EN EL", "AGUA DEL TITANIC?"], "y": 250, "size": 104}],
    "camera": {"move": "punch", "impacts": ["w8"]}},
   sfx=[{"name": "splash", "at_word": 8, "gain_db": -8}], transition="cut", emphasis=["helada", "hora"])

sc("t02", "setup", "Abril de mil novecientos doce: el barco chocó con un iceberg, y no hay botes para todos.", {
    "background": SEA,
    "character": {"visible": False},
    "props": [{"type": "iceberg", "x": 0.75, "y": 0.55, "scale": 0.7, "under": False, "enter": "none"},
              {"type": "liner", "x": 0.4, "y": 0.53, "scale": 0.62, "enter": "slide_left", "smoke": True}],
    "overlays": [{"type": "label", "text": "14-15 DE ABRIL · 1912", "x": 540, "y": 300, "size": 70, "bg": "#E8392F"}],
    "camera": {"move": "push_in"}},
   claims=[F("El Titanic chocó con un iceberg la noche del 14 de abril de 1912 y se hundió a las 2:20 del día 15",
             "Encyclopaedia Britannica")],
   sfx=[{"name": "crack", "at_word": 7, "gain_db": -4}], transition="whip", emphasis=["iceberg"])

sc("t03", "setup", "En los botes caben mil ciento setenta y ocho personas. A bordo van unas dos mil doscientas.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#5C8FE6"},
    "character": {"visible": False},
    "props": [{"type": "lifeboat", "x": 0.3, "y": 0.62, "scale": 0.9, "people": 5},
              {"type": "lifeboat", "x": 0.72, "y": 0.78, "scale": 0.9, "people": 6, "at_word": 2}],
    "overlays": [{"type": "counter", "from": 0, "to": 1178, "suffix": " PLAZAS", "at_word": 4, "over": 0.8, "y": 330,
                  "size": 110},
                 {"type": "counter", "from": 0, "to": 2200, "prefix": "≈", "suffix": " A BORDO", "at_word": 13,
                  "over": 0.7, "y": 520, "size": 110, "color": "#FF6B5C"}],
    "camera": {"move": "static"}},
   claims=[F("Los 20 botes del Titanic tenían capacidad para 1.178 personas; a bordo viajaban unas 2.200",
             "Encyclopaedia Britannica")],
   sfx=[{"name": "tick", "at_word": 4}, {"name": "hit", "at_word": 13, "gain_db": -6}], emphasis=["dos"])

sc("t04", "development", "Minuto cero: el agua está a dos grados bajo cero. Sí, bajo cero: la sal impide que se congele.", {
    "background": SEA,
    "character": leo(0.3, expression="shock"),
    "props": [sea(), {"type": "thermometer", "x": 0.82, "y": 0.5, "scale": 0.9, "level": 0.08}],
    "overlays": [lbl("MINUTO 0"), clock("0'", 0, 0),
                 {"type": "counter", "from": 10, "to": -2, "suffix": " °C", "at_word": 4, "over": 0.8, "y": 520,
                  "size": 160, "color": "#8FD3FF", "sub": "TEMPERATURA DEL MAR"}],
    "camera": {"move": "push_in"}},
   claims=[F("El agua donde se hundió el Titanic estaba a unos -2 °C; el agua salada se congela por debajo de 0 °C",
             "Encyclopedia Titanica; NOAA")],
   sfx=[{"name": "splash", "at": 0.1, "gain_db": -6}], emphasis=["bajo", "cero"])

sc("t05", "development", "Tu cuerpo da un respingo y boqueas sin querer. Es el choque por frío.", {
    "background": SEA,
    "character": leo(0.4, expression="scared", actions=[["w3", "shock"]]),
    "props": [sea(), {"type": "heart", "x": 0.8, "y": 0.45, "scale": 0.5, "bpm": 160, "at_word": 7}],
    "overlays": [{"type": "fact", "text": "Choque por frío: boqueo involuntario y respiración acelerada en el primer minuto",
                  "at_word": 8, "y": 230}],
    "camera": {"move": "punch", "impacts": ["w3"]}},
   claims=[F("Al caer en agua helada, el choque por frío provoca un boqueo involuntario e hiperventilación",
             "Gordon Giesbrecht; National Center for Cold Water Safety")],
   sfx=[{"name": "gulp", "at_word": 6}], transition="slide", emphasis=["respingo", "choque"])

sc("t06", "development", "Ese primer boqueo es muy peligroso: puedes tragar agua.", {
    "background": {"type": "ice_sea", "under": True},
    "character": {"x": 0.5, "y": 0.75, "scale": 1.3, "action": "swim", "expression": "scared", "extras": {"frost": 0.4}},
    "props": [{"type": "bubbles", "x": 0.5, "y": 0.36, "at_word": 6}],
    "overlays": [{"type": "fact", "label": "OJO", "text": "El boqueo bajo el agua es una de las principales causas de ahogamiento",
                  "at_word": 4, "y": 230}],
    "camera": {"move": "push_in", "shake": 0.1}},
   claims=[F("El boqueo del choque por frío puede hacer que se inhale agua y es causa frecuente de ahogamiento",
             "National Center for Cold Water Safety")],
   sfx=[{"name": "gulp", "at_word": 7}], transition="whip", emphasis=["peligroso"])

sc("t07", "development", "Minuto uno: calma. Lo primero es controlar la respiración.", {
    "background": SEA,
    "character": leo(0.45, expression="determined"),
    "props": [sea()],
    "overlays": [lbl("MINUTO 1"), clock("1'", 0, 1 / 60),
                 {"type": "fact", "text": "Regla del experto Gordon Giesbrecht: primero, controlar la respiración",
                  "at_word": 3, "y": 470}],
    "camera": {"move": "static"}},
   claims=[F("Lo primero en agua helada es controlar la respiración durante el choque por frío (regla 1-10-1)",
             "Gordon Giesbrecht, Universidad de Manitoba")],
   sfx=[{"name": "ding", "at_word": 3}], emphasis=["calma"])

sc("t08", "development", "Minuto diez: la sangre abandona tus manos y tus piernas para proteger el corazón.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#5C8FE6"},
    "character": {"visible": False},
    "props": [{"type": "heart", "x": 0.5, "y": 0.6, "scale": 1.4, "bpm": 90, "cold": 0.2, "enter": "pop"}],
    "overlays": [lbl("MINUTO 10", "#9D7BFF"), clock("10'", 1 / 60, 10 / 60),
                 {"type": "fact", "text": "Con frío, los vasos de la piel se cierran y la sangre se concentra en los órganos",
                  "at_word": 4, "y": 470}],
    "camera": {"move": "push_in"}},
   claims=[F("Con el frío los vasos de la piel y las extremidades se contraen (vasoconstricción) para conservar el calor del tronco",
             "Gordon Giesbrecht; manuales de medicina del frío")],
   sfx=[{"name": "whoosh", "at_word": 4}], transition="zoom", emphasis=["corazón"])

sc("t09", "development", "Tus dedos ya no responden. Nadar se vuelve casi imposible.", {
    "background": SEA,
    "character": leo(0.7, expression="tired", action="idle"),
    "props": [sea()],
    "overlays": [{"type": "fact", "text": "Incapacitación por frío: en unos 10 minutos los músculos de brazos y piernas fallan",
                  "at_word": 2, "y": 470}],
    "camera": {"move": "push_in", "zoom_to": 1.2}},
   claims=[F("En unos 10 minutos de agua helada los músculos de las extremidades pierden fuerza (incapacitación por frío)",
             "Gordon Giesbrecht")],
   sfx=[{"name": "fall", "at_word": 6, "gain_db": -8}], emphasis=["dedos", "imposible"])

sc("t10", "climax", "Minuto treinta: empieza la hipotermia de verdad. Tu temperatura cae y te entra sueño.", {
    "background": SEA,
    "character": leo(0.9, expression="tired", action="idle", expressions=[["w11", "happy_closed"]]),
    "props": [sea(), {"type": "thermometer", "x": 0.82, "y": 0.5, "scale": 0.9, "level": 0.25}],
    "overlays": [lbl("MINUTO 30", "#E8392F"), clock("30'", 10 / 60, 0.5),
                 {"type": "fact", "text": "La hipotermia tarda al menos media hora en desarrollarse", "at_word": 4,
                  "y": 470}],
    "camera": {"move": "push_in", "tilt": 0.04}},
   claims=[F("La hipotermia tarda al menos unos 30 minutos en desarrollarse; causa confusión y somnolencia",
             "Gordon Giesbrecht; Universidad de Manitoba")],
   sfx=[{"name": "riser", "at": 0.2, "gain_db": -8}], transition="flash", emphasis=["hipotermia", "sueño"])

sc("t11", "climax", "Aquella noche, la mayoría de las personas en el agua no aguantó ni media hora.", {
    "background": SEA,
    "character": {"visible": False},
    "props": [{"type": "lifeboat", "x": 0.5, "y": 0.55, "scale": 0.7, "people": 6, "enter": "fade"}],
    "overlays": [{"type": "fact", "label": "EN MEMORIA", "text": "Murieron más de 1.500 personas; la mayoría de las que cayeron al agua, en 15-30 minutos",
                  "at_word": 3, "y": 230}],
    "camera": {"move": "pull_out"}},
   claims=[F("La mayoría de quienes cayeron al agua murieron en 15-30 minutos; en total murieron más de 1.500 personas",
             "Encyclopaedia Britannica; Encyclopedia Titanica")],
   transition="circle", emphasis=["media"])

sc("t12", "climax", "Minuto sesenta: si sigues ahí, es casi un milagro.", {
    "background": SEA,
    "character": leo(1.0, expression="dizzy", action="idle"),
    "props": [sea()],
    "overlays": [lbl("MINUTO 60", "#E8392F"), clock("60'", 0.5, 1.0)],
    "camera": {"move": "push_in", "zoom_to": 1.25, "focus": [0.5, 0.62]}},
   sfx=[{"name": "tick", "at": 0.2}], transition="whip", emphasis=["milagro"])

sc("t13", "climax", "Y hubo un milagro: Charles Joughin, el jefe de panaderos del barco.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#4A3020", "x": 0.4, "y": 0.86, "size": 1.3,
               "expression": "happy", "action": "present", "shirt": "#FFFFFF", "mustache": True, "enter": "pop"},
              {"type": "food", "kind": "bread", "x": 0.78, "y": 0.55, "scale": 1.2, "at_word": 8}],
    "overlays": [{"type": "label", "text": "CHARLES JOUGHIN · PANADERO JEFE", "x": 540, "y": 300, "size": 62,
                  "at_word": 4, "bg": "#E8392F"}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("Charles Joughin era el jefe de panaderos del Titanic y sobrevivió al hundimiento", "Encyclopedia Titanica")],
   sfx=[{"name": "sparkle", "at_word": 3}, {"name": "pop", "at_word": 8}], transition="flash", emphasis=["milagro"])

sc("t14", "climax", "Contó que pasó unas dos horas en el agua, casi sin sentir el frío, hasta llegar a un bote volcado.", {
    "background": SEA,
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#4A3020", "x": 0.45, "y": 0.98, "size": 1.15,
               "expression": "determined", "action": "swim", "shirt": "#FFFFFF", "mustache": True, "enter": "none"},
              {"type": "lifeboat", "x": 0.78, "y": 0.66, "scale": 0.8, "people": 0, "rot": 3.0, "at_word": 15},
              sea(1610)],
    "overlays": [{"type": "fact", "label": "SU TESTIMONIO", "text": "Dijo haber estado unas 2 horas en el agua; los historiadores dudan de los tiempos",
                  "at_word": 3, "y": 230}],
    "camera": {"move": "pan_right", "amount": 140}},
   claims=[F("Joughin declaró que estuvo unas dos horas en el agua, que apenas sintió el frío y que llegó al bote plegable B volcado; los historiadores dudan de la precisión de sus tiempos",
             "Comisión británica de investigación (1912); Encyclopedia Titanica")],
   sfx=[{"name": "splash", "at_word": 15, "gain_db": -6}], emphasis=["dos", "horas"])

sc("t15", "ending", "Había bebido licor, pero ojo: los expertos dicen que el alcohol no protege del frío.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "overlays": [{"type": "myth", "text": "EL ALCOHOL TE CALIENTA", "stamp": "¡FALSO!", "y": 420, "stamp_at": 1.6,
                  "at_word": 4}],
    "props": [{"type": "thermometer", "x": 0.5, "y": 0.72, "scale": 1.2, "level": 0.2, "at_word": 4}],
    "camera": {"move": "push_in"}},
   claims=[F("Joughin admitió haber tomado licor; según expertos en hipotermia, el alcohol no protege del agua helada",
             "Comisión británica de investigación (1912); Gordon Giesbrecht; McGill Office for Science and Society")],
   sfx=[{"name": "hit", "at_word": 9, "gain_db": -6}], transition="slide", emphasis=["alcohol"])

sc("t16", "ending", "El Carpathia llegó hacia las cuatro de la madrugada y rescató a unas setecientas personas.", {
    "background": SEA,
    "character": {"visible": False},
    "props": [{"type": "liner", "x": 0.5, "y": 0.52, "scale": 0.6, "funnels": 1, "funnel_color": "#E8392F",
               "enter": "slide_right", "smoke": True},
              {"type": "lifeboat", "x": 0.25, "y": 0.62, "scale": 0.6, "people": 5, "at_word": 4},
              {"type": "lifeboat", "x": 0.75, "y": 0.66, "scale": 0.6, "people": 4, "at_word": 6}],
    "overlays": [{"type": "counter", "from": 0, "to": 705, "prefix": "≈", "suffix": " RESCATADOS", "at_word": 11,
                  "over": 0.8, "y": 330, "size": 120, "sub": "CARPATHIA · 4:10"}],
    "camera": {"move": "pull_out"}},
   claims=[F("El Carpathia llegó al primer bote hacia las 4:10 y rescató a unos 705 supervivientes", "Encyclopaedia Britannica")],
   sfx=[{"name": "ding", "at_word": 11}], transition="zoom", emphasis=["setecientas"])

sc("t17", "ending", "¿Y tú, qué harías en ese primer minuto? Te leo en comentarios.", {
    "background": SEA,
    "character": {"x": 0.5, "y": 0.86, "scale": 1.3, "action": "talk", "expression": "excited",
                  "actions": [["w7", "point_down"]]},
    "props": [sea(1480)],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 7, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 7}], transition="zoom", pause=0.35)

DESC = """El Titanic se hunde y caes al agua a -2 °C… ¿qué le pasaría a tu cuerpo si aguantaras una hora? 🧊

Leo cae al Atlántico Norte la noche del 15 de abril de 1912 y descubre, minuto a minuto, lo que hace el agua helada: el choque por frío, la incapacitación, la hipotermia… y la historia real de Charles Joughin, el panadero jefe que dijo haber pasado unas dos horas en el agua.

🧪 DATOS REALES DEL VÍDEO
• Los botes del Titanic tenían plazas para 1.178 personas; a bordo iban unas 2.200.
• El agua estaba a unos -2 °C: el agua salada se congela por debajo de 0 °C.
• Al caer, el choque por frío provoca un boqueo involuntario: el primer minuto es el más peligroso.
• En unos 10 minutos los músculos de brazos y piernas fallan; la hipotermia tarda al menos media hora.
• La mayoría de quienes cayeron al agua murieron en 15-30 minutos. En total murieron más de 1.500 personas.
• Charles Joughin, jefe de panaderos, declaró haber estado unas dos horas en el agua antes de llegar a un bote volcado (los historiadores dudan de sus tiempos). Había tomado licor, pero el alcohol no protege del frío.
• El Carpathia llegó hacia las 4:10 y rescató a unos 705 supervivientes.

🕯️ En memoria de las víctimas del Titanic.
⚠️ Si caes en agua helada: no luches contra el primer boqueo, controla la respiración y sal o pide ayuda cuanto antes.

📚 Fuentes: Encyclopaedia Britannica, Encyclopedia Titanica, Comisión británica de investigación (1912), Gordon Giesbrecht (Universidad de Manitoba), National Center for Cold Water Safety, McGill Office for Science and Society.

💬 ¿Qué harías en ese primer minuto? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #titanic #cuerpohumano #historia #shorts"""

st.save("agua-helada-del-titanic", "¿Qué pasaría si estuvieras 1 hora en el agua helada del Titanic?",
        "¿Qué pasaría si estuvieras 1 hora en el agua helada del Titanic?", "historia",
        "¿Qué harías en ese primer minuto?", {
            "title": "¿Qué pasaría si cayeras al agua del Titanic 1 hora? 🧊",
            "hashtags": ["#quepasariasi", "#titanic", "#cuerpohumano", "#historia", "#shorts"],
            "tags": ["qué pasaría si", "titanic", "agua helada", "hipotermia", "choque por frío", "charles joughin",
                     "1912", "historia", "cuerpo humano", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Qué harías tú en el primer minuto en el agua? 🧊👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "t04", "t": 1.6, "lines": ["¿1 HORA EN EL", "AGUA DEL TITANIC?"],
                          "badge": "EL AGUA: -2 °C", "badge_pos": [540, 1640], "y": 260,
                          "character": {"action": "shock", "expression": "shock", "x": 0.5, "y": 0.9, "scale": 1.45,
                                        "extras": {"frost": 0.6}},
                          "crop_y": 0.55, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
