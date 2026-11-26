"""Guion: ¿Qué pasa si comes 10 zanahorias al día durante un mes?  (formato A: «comer X cada día», presente)

Escalada: semana 1 → betacaroteno → 4 mg por zanahoria → umbral 20-50 mg/día → semana 3: piel anaranjada (carotenemia)
→ no es ictericia ni vitamina A → se revierte. Piel de Leo teñida con extras["tint"].
Voz: ElevenLabs «Mario» (ver scripts/voz_elevenlabs.py).
"""
from storykit import F, Story

st = Story()
sc = st.sc
ROOM = {"type": "living_room"}
SUN = {"type": "burst", "c1": "#FF8A1F", "c2": "#FFB45C"}


def leo(tint=0.0, **kw):
    d = {"x": 0.5, "y": 0.8, "scale": 1.4, "action": "idle", "expression": "happy", "extras": {"tint": tint}}
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


def carrots(n, x=0.74, y=0.74, scale=0.85, **kw):
    return {"type": "carrot", "x": x, "y": y, "n": n, "scale": scale, **kw}


sc("z01", "hook", "Empiezas a comer diez zanahorias al día. Durante un mes.", {
    "background": ROOM,
    "character": leo(0.0, x=0.34, expression="excited"),
    "props": [carrots(6, x=0.74, y=0.74, scale=0.85, enter="pop")],
    "overlays": [{"type": "title", "lines": ["¿10 ZANAHORIAS", "AL DÍA?"], "y": 250, "size": 108}],
    "camera": {"move": "punch", "impacts": [0.3]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -7}, {"name": "pop", "at": 0.3, "gain_db": -6}],
   transition="cut", emphasis=["diez", "zanahorias"])

sc("z02", "setup", "Primera semana: no notas nada. Las zanahorias son sanas, ¿no?", {
    "background": ROOM,
    "character": leo(0.0, x=0.36, expression="smug", action="talk"),
    "props": [carrots(3, x=0.76, y=0.74, scale=0.8)],
    "overlays": [lbl("SEMANA 1", "#2B6BE8", 0)],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "tick", "at_word": 0}], transition="whip", emphasis=["nada"])

sc("z03", "setup", "Son naranjas por el betacaroteno, un pigmento natural.", {
    "background": SUN,
    "character": {"visible": False},
    "props": [carrots(1, x=0.5, y=0.78, scale=1.6, enter="pop")],
    "overlays": [{"type": "fact", "text": "El betacaroteno es el pigmento naranja de las zanahorias", "at_word": 4, "y": 300}],
    "camera": {"move": "static"}},
   claims=[F("El betacaroteno es el pigmento que da el color naranja a las zanahorias", "Cleveland Clinic")],
   sfx=[{"name": "pop", "at_word": 4}], transition="slide", emphasis=["betacaroteno"])

sc("z04", "development", "Una zanahoria mediana tiene unos cuatro miligramos.", {
    "background": SUN,
    "character": {"visible": False},
    "props": [carrots(1, x=0.5, y=0.8, scale=1.4)],
    "overlays": [counter(4, " mg", 5, sub="DE BETACAROTENO POR ZANAHORIA MEDIANA", y=330, size=170)],
    "camera": {"move": "push_in"}},
   claims=[F("Una zanahoria mediana tiene unos 4 mg de betacaroteno", "Cleveland Clinic")],
   sfx=[{"name": "ding", "at_word": 5}], transition="whip", emphasis=["cuatro"])

sc("z05", "development", "Diez al día son unos cuarenta miligramos. Ahí empieza el problema.", {
    "background": SUN,
    "character": {"visible": False},
    "props": [carrots(6, x=0.5, y=0.82, scale=1.1)],
    "overlays": [counter(40, " mg/día", 4, sub="UMBRAL: 20-50 mg AL DÍA DURANTE SEMANAS", y=330, size=150)],
    "camera": {"move": "punch", "impacts": ["w4"]}},
   claims=[F("Unos 20-50 mg de betacaroteno al día durante semanas (≈ 10 zanahorias diarias) pueden causar carotenemia",
             "Cleveland Clinic")],
   sfx=[{"name": "hit", "at_word": 4, "gain_db": -6}], transition="flash", emphasis=["cuarenta", "problema"])

sc("z06", "development", "Tu cuerpo no lo gasta todo, y el sobrante se acumula en la piel.", {
    "background": ROOM,
    "character": leo(0.25, expression="worried", action="think"),
    "props": [],
    "overlays": [{"type": "fact", "text": "El exceso de betacaroteno se deposita en la capa externa de la piel", "at_word": 8, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("El exceso de betacaroteno se acumula en la capa más externa de la piel (estrato córneo)", "DermNet; Wikipedia (carotenemia)")],
   sfx=[{"name": "pop", "at_word": 8}], transition="slide", emphasis=["acumula", "piel"])

sc("z07", "development", "Semana tres: tu piel empieza a ponerse amarillenta, casi naranja.", {
    "background": ROOM,
    "character": leo(1.0, expression="shock", action="shock"),
    "props": [],
    "overlays": [lbl("SEMANA 3", "#E8392F", 0)],
    "camera": {"move": "punch", "impacts": ["w5"]}},
   sfx=[{"name": "hit", "at_word": 5, "gain_db": -6}], transition="flash", emphasis=["naranja"])

sc("z08", "climax", "Se nota primero en la nariz, las palmas y las plantas de los pies.", {
    "background": ROOM,
    "character": leo(1.0, expression="wow", action="present"),
    "props": [],
    "overlays": [lbl("NARIZ · PALMAS · PLANTAS", "#1B1B3A", 5),
                 {"type": "fact", "text": "Primero amarillea la nariz, los pliegues de la nariz, las palmas y las plantas", "at_word": 0, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("La carotenodermia se ve primero en la nariz, los pliegues nasolabiales, las palmas y las plantas, antes de extenderse",
             "DermNet; Wikipedia (carotenosis)")],
   sfx=[{"name": "ding", "at_word": 5}], transition="whip", emphasis=["palmas", "plantas"])

sc("z09", "climax", "Se llama carotenemia y no es peligrosa.", {
    "background": SUN,
    "character": leo(0.9, expression="happy", action="talk", scale=1.25, y=0.78),
    "props": [],
    "overlays": [lbl("CAROTENEMIA", "#FF8A1F", 2), {"type": "fact", "text": "Es inofensiva y no requiere tratamiento", "at_word": 4, "y": 560}],
    "camera": {"move": "static"}},
   claims=[F("La carotenemia es inofensiva y no requiere tratamiento", "Cleveland Clinic; Wikipedia")],
   sfx=[{"name": "ding", "at_word": 2}], transition="slide", emphasis=["carotenemia", "peligrosa"])

sc("z10", "climax", "No es ictericia: el blanco de tus ojos sigue blanco.", {
    "background": ROOM,
    "character": leo(0.9, expression="wow", action="point_up"),
    "props": [],
    "overlays": [{"type": "fact", "text": "En la carotenemia el blanco de los ojos NO se vuelve amarillo; en la ictericia, sí", "at_word": 4, "y": 560}],
    "camera": {"move": "push_in"}},
   claims=[F("En la carotenemia la esclerótica (blanco del ojo) se respeta, lo que la distingue de la ictericia",
             "Cleveland Clinic; DermNet; Wikipedia")],
   sfx=[{"name": "pop", "at_word": 4}], transition="whip", emphasis=["ojos", "blanco"])

sc("z11", "climax", "Y tampoco es intoxicación por vitamina A: el betacaroteno no la causa.", {
    "background": SUN,
    "character": {"visible": False},
    "props": [carrots(2, x=0.5, y=0.8, scale=1.3)],
    "overlays": [{"type": "fact", "text": "El exceso de betacaroteno NO produce toxicidad por vitamina A", "at_word": 0, "y": 300}],
    "camera": {"move": "push_in"}},
   claims=[F("El exceso de betacaroteno no provoca toxicidad por vitamina A", "Cleveland Clinic")],
   sfx=[{"name": "ding", "at_word": 6}], transition="zoom", emphasis=["vitamina"])

sc("z12", "ending", "En cuanto lo dejas, tu piel recupera su color en semanas o meses.", {
    "background": ROOM,
    "character": leo(0.35, expression="happy", action="talk"),
    "props": [],
    "overlays": [lbl("SEMANAS O MESES", "#2B6BE8", 8)],
    "camera": {"move": "push_in"}},
   claims=[F("El color de la piel vuelve a la normalidad al reducir el betacaroteno, en semanas o meses", "Cleveland Clinic; DermNet")],
   sfx=[{"name": "tick", "at_word": 7}], transition="whip", emphasis=["semanas", "meses"])

sc("z13", "ending", "Ojo: pasa igual con los suplementos de betacaroteno.", {
    "background": ROOM,
    "character": leo(0.5, expression="worried", action="point_down"),
    "props": [],
    "overlays": [{"type": "fact", "text": "Los suplementos de betacaroteno también pueden causarla", "at_word": 4, "y": 560}],
    "camera": {"move": "static"}},
   claims=[F("Los suplementos de betacaroteno también pueden causar carotenemia", "Cleveland Clinic")],
   sfx=[{"name": "pop", "at_word": 4}], transition="slide", emphasis=["suplementos"])

sc("z14", "ending", "Así que sí, puedes ponerte naranja. Pero tendrías que insistir mucho.", {
    "background": SUN,
    "character": leo(1.0, expression="smug", action="celebrate", scale=1.3, y=0.78),
    "props": [carrots(4, x=0.76, y=0.8, scale=0.8)],
    "overlays": [],
    "camera": {"move": "punch", "impacts": ["w4"]}},
   sfx=[{"name": "hit", "at_word": 4, "gain_db": -6}], transition="zoom", emphasis=["naranja", "insistir"])

sc("z15", "ending", "¿Tú aguantarías un mes de zanahorias? Te leo en comentarios.", {
    "background": SUN,
    "character": leo(1.0, expression="excited", action="talk", y=0.55, scale=1.3, actions=[["w7", "point_down"]]),
    "props": [],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 7, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 7}], transition="zoom", pause=0.35)

DESC = """Comes diez zanahorias al día durante un mes. ¿Te vuelves naranja de verdad? 🥕

Leo se convierte en el conejillo de indias: qué pasa con tu piel, por qué ocurre y cuándo se va.

🧪 DATOS REALES DEL VÍDEO
• Una zanahoria mediana tiene unos 4 mg de betacaroteno, el pigmento que las pone naranjas.
• Unos 20-50 mg de betacaroteno al día durante semanas (≈ 10 zanahorias diarias) pueden causar carotenemia.
• La carotenemia amarillea la piel, sobre todo en la nariz, los pliegues de la nariz, las palmas y las plantas de los pies.
• Es inofensiva: no es toxicidad por vitamina A y el blanco de los ojos no cambia (en la ictericia, sí).
• Se revierte al reducir el betacaroteno, en semanas o meses. También la causan los suplementos.

⚠️ Esto no es un consejo médico: si notas la piel o los ojos amarillos, consulta a un médico para descartar otras causas.

📚 Fuentes: Cleveland Clinic («¿Pueden las zanahorias ponerte la piel naranja?» y «Carotenemia»); DermNet NZ (carotenoderma); Wikipedia (carotenemia y carotenosis).

💬 ¿Aguantarías un mes de zanahorias? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasa si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasasi #zanahoria #cuerpohumano #curiosidades #shorts"""

st.save("diez-zanahorias-al-dia", "¿Qué pasa si comes 10 zanahorias al día durante un mes?",
        "¿Qué pasa si comes 10 zanahorias al día durante un mes?", "cuerpo",
        "¿Te volverías naranja comiendo zanahorias?", {
            "title": "¿Qué pasa si comes 10 zanahorias al día durante un mes? 🥕😳",
            "hashtags": ["#quepasasi", "#zanahoria", "#cuerpohumano", "#curiosidades", "#shorts"],
            "tags": ["qué pasa si", "comer zanahorias todos los días", "carotenemia", "piel naranja", "betacaroteno",
                     "cuerpo humano", "curiosidades", "ciencia", "animación", "hipotéticos"],
            "pinned_comment": "¿Aguantarías un mes de zanahorias? 🥕👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "z07", "t": 1.6, "lines": ["¿10 ZANAHORIAS", "AL DÍA?"],
                          "badge": "¡PIEL NARANJA!", "badge_pos": [540, 1640], "y": 260,
                          "crop_y": 0.5, "h_shift": 0, "h_scale": 0.9},
        }, mood="funny")
