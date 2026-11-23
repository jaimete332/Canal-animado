"""Guion: ¿Qué pasaría si no vieras la luz del sol en 1 año?

Escalada: día 1 → reloj interno (Siffre) → ánimo → vitamina D → Polo Sur → lux de la luz artificial → lámparas.
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, Story

st = Story()
sc = st.sc


def leo(**kw):
    d = {"x": 0.5, "y": 0.78, "scale": 1.3, "action": "idle", "expression": "worried"}
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


sc("s01", "hook", "Imagina un año entero sin ver la luz del sol.", {
    "background": {"type": "backyard"},
    "character": leo(expression="shock", action="shock"),
    "props": [{"type": "sun", "x": 0.72, "y": 0.2, "scale": 1.3, "crossed": True, "cross_at": 1.6, "enter": "none"}],
    "overlays": [{"type": "title", "lines": ["¿1 AÑO SIN", "LUZ DEL SOL?"], "y": 250, "size": 110}],
    "camera": {"move": "punch", "impacts": [1.6]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "hit", "at": 1.6, "gain_db": -5}],
   transition="cut", emphasis=["año", "sol"])

sc("s02", "setup", "Día uno: no pasa nada. Pero tu cuerpo ya está contando.", {
    "background": {"type": "bedroom", "night": False},
    "character": leo(expression="neutral", x=0.4),
    "props": [{"type": "calendar", "x": 0.76, "y": 0.35, "scale": 1.0, "loop": "bob", "from": 1, "to": 365, "over": 3.5}],
    "overlays": [lbl("DÍA 1", "#2B6BE8", 0)],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "tick", "at_word": 6}], emphasis=["contando"])

sc("s03", "development", "Tu cerebro tiene un reloj interno que se pone en hora con la luz.", {
    "background": {"type": "burst", "c1": "#5CE1E6", "c2": "#8FF0F5"},
    "character": {"visible": False},
    "props": [{"type": "brain", "x": 0.5, "y": 0.52, "scale": 1.5, "enter": "pop"},
              {"type": "clock", "x": 0.78, "y": 0.3, "scale": 0.8, "speed": 8, "at_word": 4}],
    "overlays": [{"type": "fact", "text": "Reloj circadiano: la luz de la mañana lo pone en hora cada día", "at_word": 3, "y": 620}],
    "camera": {"move": "push_in"}},
   claims=[F("El reloj circadiano humano se sincroniza cada día con el ciclo de luz y oscuridad", "NIGMS (NIH), «Circadian Rhythms»")],
   sfx=[{"name": "pop", "at_word": 4}], transition="zoom", emphasis=["reloj", "luz"])

sc("s04", "development", "Sin luz, ese reloj se descontrola y tu sueño se desplaza.", {
    "background": {"type": "bedroom", "night": True},
    "character": leo(expression="tired", x=0.3, action="idle"),
    "props": [{"type": "clock", "x": 0.7, "y": 0.35, "scale": 1.0, "speed": 30},
              {"type": "zzz", "x": 0.45, "y": 0.55, "scale": 0.8}],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "clock", "at": 0.1, "gain_db": -10}], transition="slide", emphasis=["descontrola"])

sc("s05", "development", "En mil novecientos setenta y dos, Michel Siffre vivió seis meses bajo tierra.", {
    "background": {"type": "cave"},
    "character": leo(expression="tired", x=0.45, y=0.8),
    "props": [],
    "overlays": [lbl("MICHEL SIFFRE · 1972", "#E8392F", 6), counter(205, " DÍAS", 10, sub="EN UNA CUEVA DE TEXAS", y=480, size=130)],
    "camera": {"move": "push_in"}},
   claims=[F("En 1972 el geólogo Michel Siffre pasó unos 205 días en la cueva Midnight Cave (Texas) sin luz natural ni relojes",
             "Michel Siffre; Wikipedia/prensa científica")],
   sfx=[{"name": "ding", "at_word": 10}], transition="whip", emphasis=["Siffre"])

sc("s06", "development", "Sin sol ni relojes, su ciclo de sueño se alargó más de veinticuatro horas.", {
    "background": {"type": "cave"},
    "character": leo(expression="surprised", x=0.45, y=0.8),
    "props": [{"type": "clock", "x": 0.78, "y": 0.3, "scale": 0.9, "speed": -4}],
    "overlays": [{"type": "fact", "text": "Su reloj interno se alargó hasta unas 24,5 horas. Hoy se estima que dura de media 24,2", "at_word": 4, "y": 620}],
    "camera": {"move": "push_in", "zoom_to": 1.12}},
   claims=[F("Sin pistas de tiempo, el ciclo de Siffre se alargó hasta unas 24,5 horas; estudios posteriores (Czeisler, 1999) sitúan el periodo medio en 24,18 h",
             "Czeisler et al., Science (1999); Michel Siffre")],
   sfx=[{"name": "tick", "at_word": 10}], emphasis=["veinticuatro"])

sc("s07", "development", "Semana tres: estás cansado y de mal humor, porque la luz regula el ánimo.", {
    "background": {"type": "bedroom", "night": True},
    "character": leo(expression="tired", x=0.45, action="idle", extras={"eyebags": 0.5}),
    "props": [{"type": "heart", "x": 0.78, "y": 0.4, "scale": 0.7, "bpm": 55, "at_word": 6}],
    "overlays": [lbl("SEMANA 3", "#2B6BE8", 0),
                 {"type": "fact", "text": "La falta de luz se asocia con depresión estacional y mal sueño", "at_word": 8, "y": 620}],
    "camera": {"move": "push_in"}},
   claims=[F("La reducción de la luz natural se asocia con el trastorno afectivo estacional y alteraciones del sueño", "NIMH (EE. UU.); Mayo Clinic")],
   sfx=[{"name": "fall", "at_word": 8, "gain_db": -10}], transition="slide", emphasis=["ánimo"])

sc("s08", "development", "Mes dos: tu piel apenas fabrica vitamina D, la que fortalece tus huesos.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "bone", "x": 0.5, "y": 0.52, "scale": 1.6, "enter": "pop"}],
    "overlays": [lbl("MES 2", "#2B6BE8", 0), {"type": "fact", "text": "La piel fabrica la vitamina D con los rayos UVB del sol", "at_word": 4, "y": 620}],
    "camera": {"move": "push_in"}},
   claims=[F("La piel produce vitamina D al recibir rayos UVB del sol, y esta vitamina es clave para absorber calcio y fortalecer los huesos",
             "NIH, Office of Dietary Supplements")],
   sfx=[{"name": "pop", "at_word": 4}], transition="zoom", emphasis=["vitamina", "huesos"])

sc("s09", "development", "Sin ella, a la larga los huesos se debilitan y duelen.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "props": [{"type": "bone", "x": 0.5, "y": 0.52, "scale": 1.6, "enter": "none", "rot": 0.3, "loop": "shake"}],
    "overlays": [{"type": "fact", "text": "La carencia prolongada de vitamina D puede causar osteomalacia: huesos blandos y dolor", "at_word": 4, "y": 620}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   claims=[F("La carencia prolongada de vitamina D en adultos puede provocar osteomalacia (huesos blandos y dolorosos)", "NIH, Office of Dietary Supplements")],
   sfx=[{"name": "crack", "at_word": 6, "gain_db": -5}], transition="whip", emphasis=["debilitan"])

sc("s10", "climax", "En el Polo Sur el sol se esconde en marzo y no vuelve hasta septiembre.", {
    "background": {"type": "polar", "aurora": 0.0, "sun": True},
    "character": leo(expression="surprised", x=0.3, y=0.86, extras={"frost": 0.4}),
    "props": [],
    "overlays": [lbl("POLO SUR", "#2B6BE8", 0), counter(6, " MESES", 8, sub="SIN SOL", y=480, size=150)],
    "camera": {"move": "push_in"}},
   claims=[F("En la estación del Polo Sur el sol se pone en torno al equinoccio de marzo y no sale hasta el de septiembre: unos seis meses de noche",
             "NOAA")],
   sfx=[{"name": "whoosh", "at_word": 3}], transition="flash", emphasis=["marzo", "septiembre"])

sc("s11", "climax", "Seis meses de noche: allí cuesta dormir y el ánimo se resiente.", {
    "background": {"type": "polar", "aurora": 1.0, "lit": True},
    "character": leo(expression="tired", x=0.3, y=0.86, extras={"frost": 0.6, "eyebags": 0.5}),
    "props": [],
    "overlays": [{"type": "fact", "text": "Quienes pasan el invierno en bases antárticas suelen notar peor sueño y ánimo más bajo", "at_word": 4, "y": 620}],
    "camera": {"move": "push_in"}},
   claims=[F("Las personas que invernan en estaciones antárticas suelen sufrir alteraciones del sueño y del estado de ánimo",
             "Palinkas, estudios sobre invernantes en la Antártida")],
   sfx=[{"name": "float", "at": 0.2, "gain_db": -10}], transition="slide", emphasis=["noche"])

sc("s12", "climax", "Una oficina da quinientos lux de luz. Un día de sol, cien mil.", {
    "background": {"type": "office"},
    "character": {"visible": False},
    "props": [{"type": "lamp", "x": 0.28, "y": 0.62, "scale": 1.0}],
    "overlays": [counter(500, " LUX", 3, sub="UNA OFICINA", y=300, size=140),
                 counter(100000, " LUX", 9, sub="UN DÍA DE SOL", y=720, size=140, color="#FFD23F")],
    "camera": {"move": "static"}},
   claims=[F("La luz recomendada en una oficina ronda los 500 lux; el sol directo puede alcanzar unos 100.000 lux",
             "Norma EN 12464-1; Encyclopaedia Britannica")],
   sfx=[{"name": "tick", "at_word": 3}, {"name": "hit", "at_word": 9, "gain_db": -6}], transition="zoom", emphasis=["quinientos", "cien"])

sc("s13", "climax", "Por eso las lámparas contra la depresión de invierno dan diez mil lux.", {
    "background": {"type": "bedroom", "night": False},
    "character": leo(expression="happy", x=0.3),
    "props": [{"type": "lamp", "x": 0.7, "y": 0.6, "scale": 1.3, "at_word": 3}],
    "overlays": [counter(10000, " LUX", 8, sub="LÁMPARA DE LUZ BRILLANTE", y=300, size=140)],
    "camera": {"move": "push_in"}},
   claims=[F("Las lámparas de fototerapia para la depresión estacional suelen emitir unos 10.000 lux", "Mayo Clinic")],
   sfx=[{"name": "sparkle", "at_word": 3}, {"name": "ding", "at_word": 8}], transition="flash", emphasis=["diez"])

sc("s14", "ending", "Con lámparas y suplementos lo llevarías mejor, pero nada se parece al sol.", {
    "background": {"type": "backyard"},
    "character": leo(expression="happy", action="present", x=0.35),
    "props": [{"type": "sun", "x": 0.75, "y": 0.22, "scale": 1.2, "enter": "pop", "at_word": 11}],
    "overlays": [],
    "camera": {"move": "pull_out"}},
   sfx=[{"name": "sparkle", "at_word": 11}], transition="whip", emphasis=["sol"])

sc("s15", "ending", "¿Tú aguantarías un año sin sol? Te leo en comentarios.", {
    "background": {"type": "backyard"},
    "character": {"x": 0.5, "y": 0.8, "scale": 1.3, "action": "talk", "expression": "excited", "actions": [["w6", "point_down"]]},
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 6, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 6}], transition="zoom", pause=0.35)

DESC = """¿Qué le pasaría a tu cuerpo si pasaras un año entero sin ver la luz del sol? 🌑

Leo lo cuenta del día 1 al año: tu reloj interno, el ánimo, la vitamina D… con el experimento real de Michel Siffre en una cueva y los seis meses de noche del Polo Sur.

🧪 DATOS REALES DEL VÍDEO
• El reloj circadiano se pone en hora cada día con la luz.
• En 1972, el geólogo Michel Siffre pasó unos 205 días en una cueva de Texas sin luz natural ni relojes; su ciclo de sueño se alargó hasta unas 24,5 horas. Estudios posteriores sitúan el periodo medio humano en 24,2 horas.
• La piel fabrica vitamina D con los rayos UVB del sol; la carencia prolongada puede causar osteomalacia.
• En el Polo Sur el sol se pone en marzo y no vuelve hasta septiembre: unos seis meses de noche.
• Una oficina tiene unos 500 lux; un día de sol, hasta unos 100.000. Las lámparas contra la depresión estacional dan unos 10.000 lux.

⚠️ Si tienes poca exposición a la luz o dudas sobre tu salud, consulta con un profesional sanitario.

📚 Fuentes: NIGMS (NIH); NIMH; NIH Office of Dietary Supplements; NOAA; Czeisler et al., Science (1999); Michel Siffre; Mayo Clinic; norma EN 12464-1; Palinkas.

💬 ¿Aguantarías un año sin sol? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #sol #cuerpohumano #curiosidades #shorts"""

st.save("un-ano-sin-sol", "¿Qué pasaría si no vieras la luz del sol en 1 año?",
        "¿Qué pasaría si no vieras la luz del sol en 1 año?", "ciencia", "¿Aguantarías un año sin sol?", {
            "title": "¿Qué pasaría si no vieras la luz del sol en 1 año? 🌑",
            "hashtags": ["#quepasariasi", "#sol", "#cuerpohumano", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "sin luz del sol", "vitamina d", "ritmo circadiano", "michel siffre", "polo sur",
                     "depresión estacional", "cuerpo humano", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Cuánto aguantarías tú sin ver el sol? 🌑👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "s01", "t": 1.8, "lines": ["¿1 AÑO SIN", "LUZ DEL SOL?"],
                          "badge": "TU CUERPO CAMBIA", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
