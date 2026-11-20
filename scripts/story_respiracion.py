"""Guion: ¿Qué pasaría si aguantaras la respiración 10 minutos?

Escalada por minutos (0:30 → 1 → 2 → 3 → 5 → 10) con cronómetro. Mensaje de seguridad: nunca apnea solo en el agua.
"""
from storykit import F, Story

st = Story()
sc = st.sc
POOL = {"type": "underwater", "deep": 0.05, "floor": 1650}


def leo(**kw):
    d = {"x": 0.5, "y": 0.62, "scale": 1.3, "action": "float", "expression": "determined"}
    d.update(kw)
    return d


def clock(txt, p0, p1, **kw):
    return {"type": "timer", "text": txt, "x": 870, "y": 300, "p0": p0, "p1": p1, "over": 1.5, **kw}


def lbl(txt, bg="#2B6BE8", **kw):
    return {"type": "label", "text": txt, "x": 400, "y": 300, "size": 72, "bg": bg, **kw}


SRC_PARKES = "M. J. Parkes, 'Breath-holding and its breakpoint', Experimental Physiology (2006)"
SRC_REFLEX = "Godek & Freeman, 'Physiology, Diving Reflex', StatPearls (NCBI)"
SRC_DAN = "Divers Alert Network (DAN), 'Shallow water blackout'"

sc("r01", "hook", "Coges aire, metes la cabeza en el agua y aguantas. Objetivo: diez minutos.", {
    "background": POOL,
    "character": leo(expression="smug", actions=[["w8", "shock"]], expressions=[["w8", "surprised"]]),
    "props": [{"type": "bubbles", "x": 0.52, "y": 0.4, "until_word": 6}],
    "overlays": [{"type": "title", "lines": ["¿10 MINUTOS", "SIN RESPIRAR?"], "y": 250, "size": 115},
                 clock("10:00", 0, 0, at_word=10)],
    "camera": {"move": "punch", "impacts": ["w10"]}},
   sfx=[{"name": "splash", "at": 0.2, "gain_db": -8}, {"name": "hit", "at_word": 10, "gain_db": -6}],
   transition="cut", emphasis=["diez"])

sc("r02", "setup", "Segundo treinta: todo va bien. Tienes oxígeno de sobra en la sangre.", {
    "background": POOL,
    "character": leo(expression="happy"),
    "overlays": [lbl("0:30"), clock("0:30", 0, 0.05)],
    "camera": {"move": "push_in"}},
   claims=[F("Tras 30 segundos de apnea la saturación de oxígeno apenas ha bajado", SRC_PARKES)],
   emphasis=["sobra"])

sc("r03", "setup", "Pero te entran unas ganas enormes de respirar. No es falta de oxígeno: es el dióxido de carbono.", {
    "background": {"type": "burst", "c1": "#2B6BE8", "c2": "#5C8FE6"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.62, "scale": 1.2, "hold": 1.0, "breathe": False, "loop": "shake"}],
    "overlays": [{"type": "label", "text": "¡SUBE EL CO2!", "x": 540, "y": 330, "size": 110, "bg": "#E8392F", "at_word": 13}],
    "camera": {"move": "push_in", "shake": 0.1}},
   claims=[F("La necesidad de respirar se debe sobre todo a la acumulación de CO2, no a la falta de oxígeno", SRC_PARKES)],
   sfx=[{"name": "ding", "at_word": 13}], transition="whip", emphasis=["dióxido"])

sc("r04", "setup", "Minuto uno: aquí la mayoría de la gente ya se rinde.", {
    "background": POOL,
    "character": leo(expression="worried", action="sweat"),
    "overlays": [lbl("1:00", "#FF8A00"), clock("1:00", 0.05, 0.1),
                 {"type": "fact", "text": "La mayoría de personas sin entrenar aguanta entre 30 y 90 segundos",
                  "at_word": 5, "y": 470}],
    "camera": {"move": "push_in"}},
   claims=[F("La mayoría de adultos sin entrenamiento aguanta la respiración entre 30 y 90 segundos",
             "Cleveland Clinic", "estimate")],
   sfx=[{"name": "tick", "at": 0.2}], emphasis=["rinde"])

sc("r05", "development", "Tu diafragma empieza a dar espasmos: intenta respirar sin tu permiso.", {
    "background": POOL,
    "character": leo(expression="shock", action="sweat", extras={"swell": 0.2}),
    "camera": {"move": "static", "shake": 0.35}},
   claims=[F("Durante la apnea aparecen contracciones involuntarias del diafragma", SRC_PARKES)],
   sfx=[{"name": "boing", "at": 0.6, "gain_db": -10}, {"name": "boing", "at": 1.4, "gain_db": -10}],
   transition="whip", emphasis=["espasmos"])

sc("r06", "development", "Si el agua está fría, tu corazón se frena solo. Es el reflejo de inmersión, el de las focas.", {
    "background": {"type": "burst", "c1": "#22B573", "c2": "#6EE7A8"},
    "character": {"visible": False},
    "props": [{"type": "heart", "x": 0.5, "y": 0.6, "scale": 1.3, "bpm": 45}],
    "overlays": [{"type": "counter", "from": 80, "to": 50, "suffix": " lpm", "at_word": 7, "over": 1.5, "y": 320,
                  "size": 130, "sub": "PULSO (APROX.)"}],
    "camera": {"move": "push_in"}},
   claims=[F("El reflejo de inmersión de los mamíferos ralentiza el corazón al mojar la cara en agua fría", SRC_REFLEX)],
   transition="zoom", emphasis=["reflejo"])

sc("r07", "development", "Minuto dos: tu bazo se aprieta y suelta glóbulos rojos de reserva.", {
    "background": POOL,
    "character": leo(expression="determined"),
    "props": [{"type": "heart", "x": 0.78, "y": 0.42, "scale": 0.5, "bpm": 50, "at_word": 3}],
    "overlays": [lbl("2:00", "#9D7BFF"), clock("2:00", 0.1, 0.2)],
    "camera": {"move": "push_in"}},
   claims=[F("Durante la apnea el bazo se contrae y libera glóbulos rojos a la sangre",
             "Schagatay et al., 'Splenic contraction during apnea', J. Appl. Physiol.")],
   sfx=[{"name": "sparkle", "at_word": 3}], emphasis=["bazo"])

sc("r08", "development", "Minuto tres: el oxígeno baja en picado y tus labios se ponen morados.", {
    "background": POOL,
    "character": leo(expression="dizzy", extras={"frost": 0.3}),
    "overlays": [lbl("3:00", "#E8392F"), clock("3:00", 0.2, 0.3),
                 {"type": "counter", "from": 98, "to": 70, "suffix": " %", "at_word": 4, "over": 1.5, "y": 520,
                  "size": 110, "color": "#FF6B5C", "sub": "OXÍGENO EN SANGRE"}],
    "camera": {"move": "push_in", "zoom_to": 1.25, "focus": [0.5, 0.45]}},
   claims=[F("Una apnea prolongada reduce la saturación de oxígeno y puede causar cianosis (labios azulados)",
             SRC_PARKES)],
   sfx=[{"name": "tick", "at_word": 4}], emphasis=["morados"])

sc("r09", "climax", "Y aquí está el peligro real: te desmayas sin ningún aviso.", {
    "background": POOL,
    "character": leo(expression="happy_closed", action="fall"),
    "overlays": [{"type": "flash", "at_word": 6, "over": 0.3}, {"type": "vignette", "alpha": 0.7}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   claims=[F("La hipoxia por apnea puede causar pérdida de conocimiento repentina, sin síntomas previos claros",
             SRC_DAN)],
   sfx=[{"name": "fall", "at_word": 6, "gain_db": -6}], transition="flash", emphasis=["desmayas"])

sc("r10", "climax", "En tierra, tu cuerpo volvería a respirar solo. En el agua, así se ahogan muchos apneístas.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.62, "scale": 1.1, "breathe": True}],
    "overlays": [{"type": "fact", "label": "PELIGRO", "text": "Desmayo en aguas poco profundas (shallow water blackout)",
                  "at_word": 9, "y": 250}],
    "camera": {"move": "push_in"}},
   claims=[F("Al perder el conocimiento la respiración se reanuda sola; bajo el agua eso provoca ahogamiento", SRC_DAN)],
   transition="whip", emphasis=["ahogan"])

sc("r11", "climax", "Por eso la regla de oro es clara: nunca practiques apnea solo en el agua.", {
    "background": POOL,
    "character": leo(action="point_up", expression="angry", y=0.68),
    "overlays": [{"type": "label", "text": "NUNCA SOLO", "x": 540, "y": 330, "size": 100, "bg": "#E8392F",
                  "at_word": 8}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("Las organizaciones de buceo recomiendan no practicar nunca la apnea en el agua sin compañía", SRC_DAN)],
   sfx=[{"name": "hit", "at_word": 8, "gain_db": -8}], emphasis=["nunca"])

sc("r12", "climax", "Sin oxígeno, el cerebro empieza a sufrir daños en unos cinco minutos.", {
    "background": {"type": "burst", "c1": "#9D7BFF", "c2": "#C2B0FF"},
    "character": {"visible": False},
    "props": [{"type": "brain", "x": 0.5, "y": 0.6, "scale": 1.1, "dirt": 0.6, "loop": "wobble"}],
    "overlays": [clock("5:00", 0.3, 0.5, x=540, y=330)],
    "camera": {"move": "push_in"}},
   claims=[F("Las neuronas empiezan a morir a los pocos minutos (unos 4-6) sin oxígeno",
             "NINDS (National Institute of Neurological Disorders and Stroke), 'Cerebral hypoxia'", "estimate")],
   sfx=[{"name": "crack", "at": 1.0, "gain_db": -8}], transition="zoom", emphasis=["cerebro"])

sc("r13", "development", "¿Y los diez minutos? Solo los mejores apneístas lo consiguen: el récord supera los once.", {
    "background": POOL,
    "character": leo(action="float", expression="smug", helmet="diving"),
    "props": [{"type": "trophy", "x": 0.8, "y": 0.42, "scale": 0.6, "at_word": 10}],
    "overlays": [clock("11:00+", 0.9, 1.0)],
    "camera": {"move": "push_in"}},
   claims=[F("El récord de apnea estática sin oxígeno puro supera los 11 minutos (AIDA)", "AIDA International")],
   sfx=[{"name": "ding", "at_word": 10}], emphasis=["once"])

sc("r14", "ending", "Respirando oxígeno puro antes, un croata llegó a veinticuatro minutos y medio.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFE58A"},
    "character": {"visible": False},
    "props": [{"type": "trophy", "x": 0.5, "y": 0.62, "scale": 1.1}],
    "overlays": [{"type": "counter", "from": 0, "to": 24.6, "decimals": 1, "suffix": " min", "at_word": 8,
                  "over": 1.2, "y": 320, "size": 140, "sub": "BUDIMIR ŠOBAT, 2021"}],
    "camera": {"move": "push_in"}},
   claims=[F("Budimir Šobat aguantó 24 min 37 s tras respirar oxígeno puro (2021)", "Guinness World Records")],
   sfx=[{"name": "sparkle", "at_word": 8}], transition="slide", emphasis=["veinticuatro"])

sc("r15", "ending", "Pero la campeona absoluta es una ballena picuda: casi cuatro horas sin respirar.", {
    "background": {"type": "underwater", "deep": 0.5, "floor": 2400},
    "character": {"visible": False},
    "props": [{"type": "whale", "x": 0.5, "y": 0.55, "scale": 0.8, "enter": "slide_right"}],
    "overlays": [{"type": "counter", "from": 0, "to": 222, "suffix": " min", "at_word": 8, "over": 1.2, "y": 320,
                  "size": 140, "sub": "ZIFIO DE CUVIER"}],
    "camera": {"move": "pull_out"}},
   claims=[F("Un zifio de Cuvier permaneció 222 minutos sumergido", "Quick et al., J. Exp. Biol. (2020)")],
   sfx=[{"name": "ding", "at_word": 8}], emphasis=["ballena"])

sc("r16", "ending", "¿Cuánto crees que aguantarías tú? Te leo en comentarios.", {
    "background": POOL,
    "character": leo(action="talk", expression="excited", actions=[["w5", "point_down"]]),
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5,
                  "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Coges aire, metes la cabeza en el agua… ¿qué le pasaría a tu cuerpo si aguantaras 10 minutos sin respirar? 🫁

Leo aguanta minuto a minuto: las ganas de respirar, los espasmos, el reflejo de inmersión, el bazo… y el peligro real, el desmayo sin aviso.

🧪 DATOS REALES DEL VÍDEO
• Las ganas de respirar las provoca sobre todo el CO2 acumulado, no la falta de oxígeno.
• La mayoría de personas sin entrenar aguanta entre 30 y 90 segundos.
• El diafragma da contracciones involuntarias.
• Con la cara en agua fría el corazón se frena (reflejo de inmersión).
• El bazo se contrae y suelta glóbulos rojos de reserva.
• La apnea larga puede causar desmayo sin aviso; bajo el agua eso provoca ahogamiento.
• Sin oxígeno, el cerebro empieza a dañarse en unos minutos.
• Récord de apnea estática (sin oxígeno puro): más de 11 minutos.
• Con oxígeno puro antes: 24 min 37 s (Budimir Šobat, 2021).
• Un zifio de Cuvier aguantó 222 minutos sumergido.

⚠️ Nunca practiques apnea solo ni en el agua sin supervisión.

📚 Fuentes: Parkes (Experimental Physiology, 2006), StatPearls (NCBI), Schagatay et al., DAN, NINDS, Cleveland Clinic, AIDA, Guinness World Records, Quick et al. (J. Exp. Biol., 2020).

💬 ¿Cuánto crees que aguantarías tú? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #cuerpohumano #apnea #curiosidades #shorts"""

st.save("aguantar-la-respiracion", "¿Qué pasaría si aguantaras la respiración 10 minutos?",
        "¿Qué pasaría si aguantaras la respiración 10 minutos?", "cuerpo humano",
        "¿Cuánto crees que aguantarías tú?", {
            "title": "¿Qué pasaría si aguantaras 10 minutos sin respirar? 💀",
            "hashtags": ["#quepasariasi", "#cuerpohumano", "#apnea", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "aguantar la respiración", "apnea", "10 minutos sin respirar", "cuerpo humano",
                     "reflejo de inmersión", "récord", "ballena", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Cuántos segundos aguantas tú? (en seco y sentado, ¡nunca en el agua solo!) ⏱️👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "r08", "t": 1.5, "lines": ["¿10 MINUTOS", "SIN RESPIRAR?"],
                          "badge": "MINUTO 3: LABIOS MORADOS", "badge_pos": [540, 1640], "y": 260,
                          "character": {"action": "float", "expression": "dizzy", "x": 0.5, "y": 0.75, "scale": 1.5,
                                        "extras": {"frost": 0.3}},
                          "crop_y": 0.5, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
