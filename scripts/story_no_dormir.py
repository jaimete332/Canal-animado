"""Guion: ¿Qué pasaría si no durmieras en una semana?"""
from storykit import F, Story

st = Story()
sc = st.sc
PJ = {"outfit": "pajamas", "helmet": "nightcap"}


def leo(**kw):
    d = {"x": 0.32, "y": 0.75, "scale": 1.2, **PJ}
    d.update(kw)
    return d


sc("d01", "hook", "Decides no dormir en toda una semana. Mala idea.", {
    "background": {"type": "bedroom"},
    "character": leo(action="smug", expression="smug", actions=[["w6", "shock"]], expressions=[["w6", "worried"]]),
    "props": [{"type": "smartphone", "x": 0.78, "y": 0.52, "scale": 0.6, "loop": "bob"}],
    "overlays": [{"type": "title", "lines": ["¿UNA SEMANA", "SIN DORMIR?"], "y": 280, "size": 120}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   sfx=[{"name": "hit", "at_word": 6, "gain_db": -6}], transition="cut", emphasis=["semana"])

sc("d02", "setup", "Día uno: a las veinticuatro horas, tu cerebro va como si hubieras bebido de más.", {
    "background": {"type": "bedroom"},
    "character": leo(action="float", expression="dizzy", extras={"eyebags": 0.4}),
    "props": [{"type": "brain", "x": 0.75, "y": 0.45, "scale": 0.7, "at_word": 6, "loop": "wobble"}],
    "overlays": [{"type": "label", "text": "DÍA 1 · 24 H", "x": 540, "y": 300, "size": 70, "bg": "#2B6BE8"},
                 {"type": "fact", "text": "24 horas sin dormir ≈ conducir con una tasa de alcohol de 1 g/l", "at_word": 9,
                  "y": 400}],
    "camera": {"move": "push_in", "tilt": 0.03}},
   claims=[F("Tras 24 h despierto, el rendimiento equivale a una alcoholemia de ~0,1 %", "Dawson y Reid, Nature (1997)")],
   sfx=[{"name": "boing", "at_word": 6, "gain_db": -6}], emphasis=["veinticuatro"])

sc("d03", "setup", "Te cuesta concentrarte, estás de mal humor y tienes un hambre tremenda.", {
    "background": {"type": "bedroom"},
    "character": leo(action="talk", expression="angry", extras={"eyebags": 0.5}, actions=[["w9", "sweat"]],
                     expressions=[["w9", "hot"]]),
    "props": [{"type": "food", "kind": "bread", "x": 0.75, "y": 0.4, "at_word": 9, "scale": 0.9},
              {"type": "food", "kind": "chocolate", "x": 0.85, "y": 0.58, "at_word": 10, "scale": 0.6}],
    "camera": {"move": "static"}},
   claims=[F("Dormir poco altera las hormonas del hambre (grelina y leptina)", "Spiegel et al., Annals of Internal Medicine (2004)")],
   sfx=[{"name": "gulp", "at_word": 10}], transition="slide", emphasis=["hambre"])

sc("d04", "development", "Día dos: llegan los microsueños. Te duermes unos segundos sin darte cuenta.", {
    "background": {"type": "bedroom"},
    "character": leo(action="idle", expression="tired", extras={"eyebags": 0.8}, actions=[["w5", "float"]],
                     expressions=[["w5", "happy_closed"]]),
    "props": [{"type": "zzz", "x": 0.42, "y": 0.42, "at_word": 6}],
    "overlays": [{"type": "label", "text": "DÍA 2", "x": 540, "y": 300, "size": 70, "bg": "#9D7BFF"}],
    "camera": {"move": "push_in", "zoom_to": 1.15, "focus": [0.35, 0.55]}},
   claims=[F("Con privación de sueño aparecen microsueños: episodios de pocos segundos de sueño involuntario", "National Sleep Foundation")],
   sfx=[{"name": "fall", "at_word": 6, "gain_db": -6}], emphasis=["microsueños"])

sc("d05", "development", "Por eso conducir con sueño es tan peligroso.", {
    "background": {"type": "city_night", "sign": False},
    "character": {"visible": False},
    "props": [{"type": "car", "x": 0.5, "y": 0.8, "scale": 0.9, "enter": "slide_left", "loop": "shake"},
              {"type": "zzz", "x": 0.55, "y": 0.68}],
    "overlays": [{"type": "fact", "label": "OJO", "text": "La somnolencia al volante causa muchos accidentes de tráfico",
                  "at": 0.3}],
    "camera": {"move": "push_in"}},
   claims=[F("La somnolencia al volante es una causa importante de accidentes", "DGT; NHTSA")],
   sfx=[{"name": "whoosh", "at": 0.1}], transition="whip", emphasis=["peligroso"])

sc("d06", "development", "Día tres: empiezas a ver cosas que no están ahí.", {
    "background": {"type": "bedroom"},
    "character": leo(action="shock", expression="scared", extras={"eyebags": 1.0}),
    "props": [{"type": "ghost", "x": 0.72, "y": 0.35, "at_word": 4, "seed": 1},
              {"type": "ghost", "x": 0.85, "y": 0.6, "at_word": 6, "color": "#5CE1E6", "seed": 2, "scale": 0.7},
              {"type": "ghost", "x": 0.15, "y": 0.3, "at_word": 8, "color": "#FF9EB5", "seed": 3, "scale": 0.6}],
    "overlays": [{"type": "label", "text": "DÍA 3", "x": 540, "y": 300, "size": 70, "bg": "#E8392F"}],
    "camera": {"move": "push_in", "shake": 0.25, "tilt": 0.05}},
   claims=[F("Tras varios días sin dormir aparecen alucinaciones", "Waters et al., Frontiers in Psychiatry (2018)")],
   sfx=[{"name": "float", "at_word": 4}, {"name": "boing", "at_word": 8, "gain_db": -6}], emphasis=["ahí"])

sc("d07", "development", "Mientras duermes, tu cerebro hace limpieza. Sin dormir, la basura se acumula.", {
    "background": {"type": "burst", "c1": "#5CE1E6", "c2": "#8FF0F5"},
    "character": {"visible": False},
    "props": [{"type": "brain", "x": 0.5, "y": 0.45, "scale": 1.6, "clean": True, "until_word": 6, "enter": "pop"},
              {"type": "brain", "x": 0.5, "y": 0.45, "scale": 1.6, "dirt": 1.0, "at_word": 6, "enter": "none"}],
    "overlays": [{"type": "fact", "text": "El sistema glinfático elimina desechos del cerebro sobre todo durante el sueño",
                  "at_word": 2}],
    "camera": {"move": "push_in"}},
   claims=[F("Durante el sueño el sistema glinfático elimina desechos del cerebro", "Xie et al., Science (2013)")],
   sfx=[{"name": "sparkle", "at": 0.2}, {"name": "gulp", "at_word": 8}], transition="zoom", emphasis=["limpieza", "basura"])

sc("d08", "climax", "El récord lo tiene Randy Gardner: en mil novecientos sesenta y cuatro aguantó once días despierto.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#5A3A20", "x": 0.3, "y": 0.8, "size": 1.2,
               "expression": "tired", "action": "idle", "shirt": "#E8392F", "enter": "pop"},
              {"type": "trophy", "x": 0.72, "y": 0.55, "text": "11", "at_word": 13, "scale": 1.0}],
    "overlays": [{"type": "label", "text": "RANDY GARDNER · 1964", "x": 540, "y": 300, "size": 66, "at_word": 4},
                 {"type": "counter", "from": 0, "to": 11, "suffix": " DÍAS", "at_word": 13, "over": 0.6, "y": 470,
                  "size": 120}],
    "camera": {"move": "push_in"}},
   claims=[F("En 1964 Randy Gardner estuvo unos 11 días (264 h) sin dormir", "Stanford Medicine (William Dement); Guinness")],
   sfx=[{"name": "ding", "at_word": 4}, {"name": "sparkle", "at_word": 13}], transition="flash",
   emphasis=["randy", "once"])

sc("d09", "climax", "Tenía diecisiete años y lo hizo para una feria de ciencias.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#5A3A20", "x": 0.5, "y": 0.82, "size": 1.35,
               "expression": "happy", "action": "present", "shirt": "#E8392F", "enter": "none"},
              {"type": "sign", "x": 0.72, "y": 0.38, "text": "FERIA DE\nCIENCIAS", "w": 380, "size": 52, "at_word": 7, "scale": 1.5}],
    "camera": {"move": "static"}},
   claims=[F("Gardner tenía 17 años y lo hizo para una feria de ciencias de su instituto", "Stanford Medicine")],
   sfx=[{"name": "pop", "at_word": 7}], emphasis=["diecisiete"])

sc("d10", "climax", "Al final le costaba hablar, olvidaba cosas y veía cosas raras.", {
    "background": {"type": "bedroom", "night": True},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#5A3A20", "x": 0.4, "y": 0.8, "size": 1.25,
               "expression": "dizzy", "action": "float", "shirt": "#E8392F", "enter": "none"},
              {"type": "ghost", "x": 0.8, "y": 0.4, "at_word": 8, "seed": 4}],
    "camera": {"move": "push_in", "tilt": 0.04}},
   claims=[F("Al final del experimento tenía problemas de habla, memoria y alucinaciones", "Stanford Medicine; Smithsonian")],
   transition="slide", emphasis=["raras"])

sc("d11", "ending", "Hoy, Guinness ya no acepta este récord: es demasiado peligroso.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "props": [{"type": "trophy", "x": 0.5, "y": 0.5, "text": "11", "enter": "none", "scale": 1.4, "crossed": True,
               "cross_at": 1.2, "cross_r": 230}],
    "camera": {"move": "punch", "impacts": [1.3]}},
   claims=[F("Guinness dejó de registrar récords de privación de sueño por el riesgo para la salud", "Guinness World Records")],
   sfx=[{"name": "hit", "at": 1.3, "gain_db": -4}], transition="flash", emphasis=["peligroso"])

sc("d12", "ending", "La buena noticia: tras dormir unas catorce horas seguidas, Randy se recuperó.", {
    "background": {"type": "bedroom", "night": False},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "plain", "hair": "#5A3A20", "x": 0.62, "y": 0.68, "size": 1.0,
               "expression": "happy_closed", "action": "float", "shirt": "#E8392F", "enter": "none"},
              {"type": "zzz", "x": 0.72, "y": 0.4}],
    "overlays": [{"type": "counter", "from": 0, "to": 14, "suffix": " HORAS", "at_word": 5, "over": 0.6, "y": 330,
                  "sub": "DURMIENDO"}],
    "camera": {"move": "push_in"}},
   claims=[F("Después del experimento durmió unas 14 horas y se recuperó sin secuelas aparentes", "Stanford Medicine")],
   sfx=[{"name": "sparkle", "at_word": 11}], emphasis=["catorce"])

sc("d13", "ending", "Así que deja el móvil y a dormir. ¿Cuántas horas duermes tú? Te leo en comentarios.", {
    "background": {"type": "bedroom"},
    "character": leo(action="talk", expression="excited", x=0.5, scale=1.3, actions=[["w12", "point_down"]]),
    "props": [{"type": "smartphone", "x": 0.8, "y": 0.45, "scale": 0.6, "crossed": True, "cross_at": 0.6}],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 12, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("Los adultos necesitan dormir al menos 7 horas", "American Academy of Sleep Medicine")],
   sfx=[{"name": "pop", "at": 0.6}, {"name": "ding", "at_word": 12}], transition="zoom", pause=0.35)

DESC = """Decides no dormir en toda una semana… ¿qué le pasaría a tu cuerpo? 😵‍💫

Leo intenta aguantar despierto y descubre, día a día, lo que hace la falta de sueño: microsueños, alucinaciones, un hambre tremenda… y la historia real de Randy Gardner, el chico que estuvo 11 días sin dormir.

🧪 DATOS REALES DEL VÍDEO
• Tras 24 horas despierto, el rendimiento se parece al de alguien con una alcoholemia de 1 g/l (Dawson y Reid, Nature, 1997).
• Dormir poco altera las hormonas del hambre.
• Con privación de sueño aparecen los microsueños: segundos de sueño involuntario. Por eso conducir con sueño es tan peligroso.
• Tras varios días sin dormir pueden aparecer alucinaciones.
• Mientras dormimos, el sistema glinfático limpia de desechos el cerebro (Xie et al., Science, 2013).
• En 1964, Randy Gardner, de 17 años, estuvo unos 11 días sin dormir para una feria de ciencias. Después durmió unas 14 horas y se recuperó.
• Guinness ya no registra este tipo de récords por ser peligrosos.

⚠️ No lo intentes: dormir es imprescindible. Los adultos necesitan al menos 7 horas.

📚 Fuentes: Nature (1997), Annals of Internal Medicine (2004), Science (2013), Frontiers in Psychiatry (2018), Stanford Medicine, Guinness World Records, American Academy of Sleep Medicine, DGT.

💬 ¿Cuántas horas duermes tú? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #sueño #cuerpohumano #curiosidades #shorts"""

st.save("una-semana-sin-dormir", "¿Qué pasaría si no durmieras en una semana?",
        "¿Qué pasaría si no durmieras durante una semana?", "cuerpo", "¿Cuántas horas duermes tú?", {
            "title": "¿Qué pasaría si no durmieras en una semana? 😵‍💫",
            "hashtags": ["#quepasariasi", "#sueño", "#cuerpohumano", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "no dormir", "una semana sin dormir", "privación de sueño", "randy gardner",
                     "cerebro", "salud", "cuerpo humano", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Cuántas horas duermes tú de media? 😴👇",
            "description": DESC,
            "thumbnail": {"scene": "d06", "t": 0.9, "lines": ["¿UNA SEMANA", "SIN DORMIR?"],
                          "badge": "DÍA 3: ALUCINACIONES", "badge_pos": [540, 1640], "y": 260,
                          "character": {"action": "shock", "expression": "shock", "x": 0.4, "y": 0.8, "scale": 1.35,
                                        "extras": {"eyebags": 1.0}},
                          "crop_y": 0.55, "h_shift": 800, "h_scale": 0.8},
        }, mood="funny")
