"""Guion CORTO (25-35 s): ¿Qué pasa si aguantas un estornudo?  (formato B: micro-accidente del cuerpo, presente)

Un único dato: tapar nariz y boca para aguantar un estornudo puede romper la garganta (caso publicado en BMJ Case
Reports, 2018: hombre británico de 34 años). Experimento de duración: 9 escenas, ~90 palabras.
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, Story

st = Story()
sc = st.sc
ROOM = {"type": "living_room"}
SUN = {"type": "burst", "c1": "#E8392F", "c2": "#FF8A6B"}


def leo(**kw):
    d = {"x": 0.5, "y": 0.8, "scale": 1.45, "action": "idle", "expression": "worried"}
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


sc("e01", "hook", "Vas a estornudar y decides aguantarlo.", {
    "background": ROOM,
    "character": leo(expression="scared", extras={"swell": 0.15}),
    "props": [],
    "overlays": [{"type": "title", "lines": ["¿AGUANTAR UN", "ESTORNUDO?"], "y": 250, "size": 108}],
    "camera": {"move": "punch", "impacts": [0.3]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "pop", "at": 0.3, "gain_db": -6}],
   transition="cut", emphasis=["estornudar", "aguantarlo"])

sc("e02", "setup", "Te tapas la nariz y cierras la boca. Mala idea.", {
    "background": ROOM,
    "character": leo(expression="shock", extras={"swell": 0.5}, action="shock"),
    "props": [],
    "overlays": [lbl("NARIZ Y BOCA TAPADAS", "#E8392F", 2)],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "hit", "at_word": 9, "gain_db": -6}], transition="whip", emphasis=["Mala", "idea"])

sc("e03", "development", "El aire no tiene salida y la presión se dispara dentro de tu cabeza.", {
    "background": SUN,
    "character": leo(expression="dizzy", extras={"swell": 1.0}, y=0.82, scale=1.55),
    "props": [{"type": "pressure", "x": 0.5, "y": 0.55, "r": 360, "n": 8}],
    "overlays": [{"type": "fact", "text": "Bloquear nariz y boca para parar un estornudo es una maniobra peligrosa", "at_word": 8, "y": 300}],
    "camera": {"move": "push_in", "shake": 0.12}},
   claims=[F("Los autores del caso publicado advierten de que parar un estornudo tapando nariz y boca es una maniobra peligrosa",
             "BMJ Case Reports (2018); NPR")],
   sfx=[{"name": "riser", "at": 0.1, "gain_db": -8}], transition="flash", emphasis=["presión", "cabeza"])

sc("e04", "climax", "En dos mil dieciocho, un británico de treinta y cuatro años lo hizo.", {
    "background": {"type": "color", "color": "#1F2433"},
    "character": {"visible": False},
    "props": [{"type": "newspaper", "x": 0.5, "y": 0.72, "scale": 1.1, "paper": "BMJ CASE REPORTS",
               "headline": "TAPÓ NARIZ Y BOCA\nPARA NO ESTORNUDAR", "year": "2018", "enter": "pop"}],
    "overlays": [lbl("HOMBRE DE 34 AÑOS · 2018", "#1B1B3A", 4, y=300)],
    "camera": {"move": "push_in"}},
   claims=[F("En enero de 2018 BMJ Case Reports publicó el caso de un hombre británico de 34 años que se rompió la garganta al aguantar un estornudo",
             "BMJ Case Reports; NPR; ScienceDaily")],
   sfx=[{"name": "ding", "at_word": 4}], transition="slide", emphasis=["dieciocho", "treinta"])

sc("e05", "climax", "Se le desgarró la garganta.", {
    "background": SUN,
    "character": leo(expression="shock", extras={"swell": 0.6}, action="shock", scale=1.6, y=0.84),
    "props": [{"type": "pow", "x": 0.5, "y": 0.62, "scale": 1.0, "at_word": 3}],
    "overlays": [{"type": "fact", "text": "Desgarro en la parte posterior de la garganta", "at_word": 3, "y": 300}],
    "camera": {"move": "punch", "impacts": ["w3"]}},
   claims=[F("El paciente sufrió una rotura de la parte posterior de la faringe", "BMJ Case Reports (2018); NPR")],
   sfx=[{"name": "boom", "at_word": 3, "gain_db": -5}], transition="flash", emphasis=["desgarró"])

sc("e06", "climax", "El aire se coló bajo la piel del cuello, y le crujía al tocarlo.", {
    "background": ROOM,
    "character": leo(expression="scared", extras={"swell": 0.7}, y=0.82, scale=1.5),
    "props": [{"type": "bubbles", "x": 0.5, "y": 0.62, "at_word": 6}],
    "overlays": [{"type": "fact", "text": "Burbujas de aire bajo la piel del cuello: se oían crujidos al palparlo", "at_word": 6, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("Hubo enfisema subcutáneo extenso en el cuello y crepitación palpable del cuello al tórax", "BMJ Case Reports (2018); CBS News")],
   sfx=[{"name": "sizzle", "at_word": 6, "gain_db": -8}], transition="whip", emphasis=["crujía", "cuello"])

sc("e07", "ending", "Pasó días en el hospital, alimentado por sonda.", {
    "background": ROOM,
    "character": leo(expression="tired", action="idle", y=0.84),
    "props": [{"type": "heart", "x": 0.8, "y": 0.5, "scale": 0.5, "bpm": 90}],
    "overlays": [lbl("HOSPITAL", "#2B6BE8", 3), {"type": "fact", "text": "Sonda para alimentarlo y antibióticos intravenosos", "at_word": 6, "y": 560}],
    "camera": {"move": "static"}},
   claims=[F("Fue alimentado por sonda y tratado con antibióticos intravenosos hasta que bajó la inflamación (unos 7 días)",
             "BMJ Case Reports (2018); NPR")],
   sfx=[{"name": "tick", "at_word": 3}], transition="slide", emphasis=["hospital", "sonda"])

sc("e08", "ending", "Se recuperó, pero los médicos avisaron: nunca aguantes un estornudo.", {
    "background": SUN,
    "character": leo(expression="determined", action="point_up", extras={"swell": 0.0}),
    "props": [],
    "overlays": [lbl("NUNCA LO AGUANTES", "#E8392F", 7)],
    "camera": {"move": "push_in"}},
   claims=[F("Se recuperó por completo y se le aconsejó no taparse nariz y boca al estornudar", "BMJ Case Reports (2018); NPR")],
   sfx=[{"name": "hit", "at_word": 7, "gain_db": -6}], transition="zoom", emphasis=["nunca", "estornudo"])

sc("e09", "ending", "¿Tú lo aguantas alguna vez? Te leo en comentarios.", {
    "background": ROOM,
    "character": leo(expression="excited", action="talk", y=0.55, scale=1.3, actions=[["w5", "point_down"]]),
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="zoom", pause=0.3)

DESC = """Vas a estornudar y lo aguantas: te tapas la nariz y cierras la boca. ¿Qué puede pasar? 🤧

Un caso real publicado en una revista médica enseña por qué no deberías hacerlo.

🧪 DATOS REALES DEL VÍDEO
• En enero de 2018, BMJ Case Reports publicó el caso de un hombre británico de 34 años que se rompió la parte posterior de la garganta al aguantar un estornudo tapándose nariz y boca.
• El aire se coló bajo la piel del cuello (enfisema subcutáneo) y se notaban crujidos al palpar.
• Estuvo hospitalizado con sonda de alimentación y antibióticos intravenosos; se recuperó por completo.
• Los autores advierten de que bloquear nariz y boca para parar un estornudo es una maniobra peligrosa.

⚠️ Es un caso excepcional y esto no es un consejo médico: ante cualquier dolor o hinchazón en el cuello tras estornudar, consulta a un médico.

📚 Fuentes: BMJ Case Reports (enero de 2018); NPR; ScienceDaily; CBS News.

💬 ¿Aguantas los estornudos? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasa si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasasi #estornudo #cuerpohumano #curiosidades #shorts"""

st.save("aguantar-un-estornudo", "¿Qué pasa si aguantas un estornudo?",
        "¿Qué pasa si aguantas un estornudo?", "cuerpo",
        "¿Aguantas los estornudos?", {
            "title": "¿Qué pasa si aguantas un estornudo? 🤧😱",
            "hashtags": ["#quepasasi", "#estornudo", "#cuerpohumano", "#curiosidades", "#shorts"],
            "tags": ["qué pasa si", "aguantar un estornudo", "estornudo", "garganta rota", "bmj case reports",
                     "cuerpo humano", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Aguantas los estornudos? 🤧👇",
            "description": DESC,
            "target_seconds": [22, 38],
            "thumbnail": {"scene": "e03", "t": 1.4, "lines": ["¿AGUANTAR UN", "ESTORNUDO?"],
                          "badge": "NUNCA LO HAGAS", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 0, "h_scale": 0.9},
        }, mood="tense")
