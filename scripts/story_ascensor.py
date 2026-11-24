"""Guion: ¿Qué pasaría si te quedaras encerrado en un ascensor sin comida 3 semanas?

Escalada: pánico → no cae (Otis 1854) → no te quedas sin aire → semanas sin comida sí, sin agua no → Nicholas White (1999) → Mihavecz (1979).
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, Story

st = Story()
sc = st.sc
OFFICE = {"type": "office"}


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


def lift(alarm=False, display="--", **kw):
    return {"type": "elevator", "x": 0.5, "y": 0.9, "scale": 1.2, "alarm": alarm, "display": display, "enter": "none", **kw}


sc("a01", "hook", "Te quedas encerrado en un ascensor. Nadie te oye.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="shock", action="shock", y=0.82, scale=1.1),
    "props": [lift(alarm=True, display="!")],
    "overlays": [{"type": "title", "lines": ["¿3 SEMANAS EN", "UN ASCENSOR?"], "y": 250, "size": 104}],
    "camera": {"move": "punch", "impacts": [0.3]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "hit", "at": 0.3, "gain_db": -6}],
   transition="cut", emphasis=["ascensor", "Nadie"])

sc("a02", "setup", "Primero, tranquilo: el ascensor no se va a caer.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="worried", y=0.82, scale=1.1, action="talk"),
    "props": [lift(display="12")],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "pop", "at": 0.1}], transition="whip", emphasis=["caer"])

sc("a03", "setup", "Desde mil ochocientos cincuenta y cuatro, los frenos de seguridad de Otis lo impiden.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": {"visible": False},
    "props": [{"type": "newspaper", "x": 0.5, "y": 0.74, "scale": 1.1, "paper": "NEW YORK", "headline": "FRENO DE SEGURIDAD\nDE ELISHA OTIS", "year": "1854", "enter": "pop"}],
    "overlays": [lbl("OTIS · 1854", "#1B1B3A", 3, y=300),
                 {"type": "fact", "text": "Si el cable se rompe, el freno de seguridad agarra los raíles y detiene la cabina", "at_word": 6, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("En 1854 Elisha Otis demostró en Nueva York un freno de seguridad que detiene la cabina si se rompe el cable",
             "Otis; ASME; Encyclopaedia Britannica")],
   sfx=[{"name": "ding", "at_word": 3}], transition="slide", emphasis=["Otis"])

sc("a04", "development", "Tampoco te quedas sin aire: las cabinas no son herméticas.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="surprised", y=0.82, scale=1.1, action="idle"),
    "props": [lift(display="12")],
    "overlays": [{"type": "fact", "text": "En un ascensor atascado no te quedas sin oxígeno: entra aire por el hueco y la ventilación", "at_word": 0, "y": 560}],
    "camera": {"move": "static"}},
   claims=[F("Un ascensor atascado no es hermético: no te quedas sin oxígeno", "Stanford University, Cardinal Ready; Case Western Reserve University")],
   sfx=[{"name": "float", "at": 0.1, "gain_db": -9}], transition="zoom", emphasis=["aire"])

sc("a05", "development", "Con agua, el cuerpo aguanta semanas sin comer.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="think", y=0.82, scale=1.1, action="think"),
    "props": [{"type": "water_bottle", "x": 0.8, "y": 0.5, "scale": 0.8, "at_word": 1}],
    "overlays": [counter(3, " SEMANAS", 5, sub="SIN COMIDA, SI TIENES AGUA", y=330, size=140)],
    "camera": {"move": "push_in"}},
   claims=[F("Con agua, una persona puede sobrevivir semanas sin comer", "Live Science; MedicineNet")],
   sfx=[{"name": "ding", "at_word": 5}], transition="whip", emphasis=["agua", "semanas"])

sc("a06", "development", "Pero en un ascensor no hay agua. Y sin ella, aguantas unos tres días.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="tired", y=0.82, scale=1.1, action="idle"),
    "props": [lift(display="12")],
    "overlays": [counter(3, " DÍAS", 10, sub="SIN AGUA", y=330, size=170, color="#FF6B5C")],
    "camera": {"move": "push_in"}},
   claims=[F("Sin agua, una persona suele aguantar unos 3 días (entre 3 y 7 según las condiciones)", "Live Science")],
   sfx=[{"name": "hit", "at_word": 10, "gain_db": -6}], transition="flash", emphasis=["sin", "tres"])

sc("a07", "climax", "En mil novecientos noventa y nueve, Nicholas White se quedó atrapado en Nueva York.", {
    "background": OFFICE,
    "character": {"visible": False},
    "props": [lift(alarm=True, display="--", x=0.5, y=0.95, scale=1.0)],
    "overlays": [lbl("NICHOLAS WHITE · 1999", "#1B1B3A", 3, y=300)],
    "camera": {"move": "push_in"}},
   claims=[F("En octubre de 1999 Nicholas White, de la revista Business Week, quedó atrapado en un ascensor del edificio McGraw-Hill de Nueva York",
             "ABC News; CBS News; The New Yorker")],
   sfx=[{"name": "boom", "at": 0.1, "gain_db": -9}], transition="slide", emphasis=["Nicholas", "White"])

sc("a08", "climax", "Estuvo cuarenta y una horas sin comida ni agua y salió casi delirando de sed.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="sick", y=0.82, scale=1.1, action="idle"),
    "props": [lift(display="39", alarm=True)],
    "overlays": [counter(41, " HORAS", 2, sub="ATRAPADO SIN COMIDA NI AGUA", y=330, size=160)],
    "camera": {"move": "punch", "impacts": ["w2"]}},
   claims=[F("Nicholas White pasó unas 41 horas en el ascensor, sin comida ni agua, hasta que lo vio un guardia por las cámaras",
             "ABC News; CBS News")],
   sfx=[{"name": "hit", "at_word": 2, "gain_db": -5}], transition="whip", emphasis=["cuarenta", "una"])

sc("a09", "climax", "Y el récord es de Andreas Mihavecz:", {
    "background": {"type": "prison"},
    "character": leo(expression="tired", y=0.82, scale=1.1, action="idle"),
    "props": [],
    "overlays": [lbl("ANDREAS MIHAVECZ", "#1B1B3A", 5, y=300)],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="slide", emphasis=["récord", "Mihavecz"])

sc("a09b", "climax", "dieciocho días olvidado en un calabozo austriaco, en mil novecientos setenta y nueve.", {
    "background": {"type": "prison"},
    "character": leo(expression="sick", y=0.82, scale=1.1, action="idle"),
    "props": [],
    "overlays": [lbl("AUSTRIA · 1979", "#1B1B3A", 7, y=300),
                 counter(18, " DÍAS", 0, sub="SIN COMIDA NI AGUA (SEGÚN GUINNESS)", y=480, size=150)],
    "camera": {"move": "push_in"}},
   claims=[F("En 1979 Andreas Mihavecz, de 18 años, pasó 18 días olvidado en un calabozo policial austriaco; Guinness lo recoge como récord de supervivencia sin comida ni agua",
             "Wikipedia; Guinness World Records; Reuters (1979)")],
   sfx=[{"name": "ding", "at_word": 0}], transition="slide", emphasis=["dieciocho", "calabozo"])

sc("a10", "climax", "Según cuentan, sobrevivió lamiendo la condensación de las paredes, y perdió veinticuatro kilos.", {
    "background": {"type": "prison"},
    "character": leo(expression="sick", y=0.82, scale=1.1, action="idle"),
    "props": [{"type": "water_pump", "x": 0.82, "y": 0.5, "scale": 0.6, "at_word": 6}],
    "overlays": [counter(24, " KG", 9, sub="QUE PERDIÓ", y=330, size=160)],
    "camera": {"move": "push_in"}},
   claims=[F("Mihavecz habría sobrevivido lamiendo la condensación de las paredes y perdió unos 24 kg", "Wikipedia; prensa de 1979")],
   sfx=[{"name": "tick", "at_word": 9}], transition="whip", emphasis=["condensación", "veinticuatro"])

sc("a11", "ending", "Así que tres semanas sin comida son posibles; sin agua, no. Lo que mata es la sed.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="determined", y=0.8, scale=1.1, action="talk"),
    "props": [{"type": "water_bottle", "x": 0.8, "y": 0.5, "scale": 0.8, "at_word": 11}],
    "overlays": [lbl("LO QUE MATA ES LA SED", "#E8392F", 13, y=300)],
    "camera": {"move": "static"}},
   sfx=[{"name": "hit", "at_word": 13, "gain_db": -6}], transition="zoom", emphasis=["sed"])

sc("a12", "ending", "Si te pasa, pulsa la alarma y ahorra fuerzas. Alguien te oirá.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="smug", y=0.82, scale=1.1, action="point_up"),
    "props": [lift(alarm=True, display="12")],
    "overlays": [],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "ding", "at": 0.2}], transition="whip", emphasis=["alarma"])

sc("a13", "ending", "¿Qué harías tú encerrado ahí? Te leo en comentarios.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": leo(expression="excited", y=0.55, scale=1.2, action="talk", actions=[["w5", "point_down"]]),
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Te quedas encerrado en un ascensor y nadie te oye. ¿Podrías aguantar tres semanas? 🛗

Leo repasa qué pasa de verdad: el ascensor no cae, no te quedas sin aire… pero la sed te limita a unos días. Con dos casos reales.

🧪 DATOS REALES DEL VÍDEO
• En 1854 Elisha Otis demostró en Nueva York un freno de seguridad que detiene la cabina si se rompe el cable.
• Un ascensor atascado no es hermético: no te quedas sin oxígeno.
• Con agua, una persona puede sobrevivir semanas sin comer; sin agua, unos 3 días (entre 3 y 7 según las condiciones).
• Octubre de 1999: Nicholas White pasó unas 41 horas atrapado en un ascensor de Nueva York, sin comida ni agua.
• 1979: Andreas Mihavecz pasó 18 días olvidado en un calabozo austriaco; Guinness lo recoge como récord sin comida ni agua. Perdió unos 24 kg.

📚 Fuentes: Otis y ASME (historia del freno de seguridad); Stanford Cardinal Ready y Case Western (aire en ascensores); Live Science; ABC News y CBS News (Nicholas White); Wikipedia, Guinness World Records y Reuters 1979 (Mihavecz).

💬 ¿Qué harías tú? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #ascensor #supervivencia #curiosidades #shorts"""

st.save("ascensor-sin-comida-3-semanas", "¿Qué pasaría si te quedaras encerrado en un ascensor sin comida 3 semanas?",
        "¿Qué pasaría si te quedaras encerrado en un ascensor sin comida 3 semanas?", "supervivencia",
        "¿Qué harías si te quedaras encerrado en un ascensor?", {
            "title": "¿Qué pasaría si te quedaras encerrado en un ascensor sin comida 3 semanas? 🛗",
            "hashtags": ["#quepasariasi", "#ascensor", "#supervivencia", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "atrapado en un ascensor", "sin comida 3 semanas", "nicholas white", "andreas mihavecz",
                     "supervivencia", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Qué harías tú encerrado en un ascensor? 🛗👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "a01", "t": 1.6, "lines": ["¿3 SEMANAS EN", "UN ASCENSOR?"],
                          "badge": "SIN COMIDA NI AGUA", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 0, "h_scale": 0.9},
        }, mood="tense")
