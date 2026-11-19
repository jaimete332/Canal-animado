"""Guion: ¿Qué pasaría si traicionaras a la mafia?"""
from storykit import F, Story

st = Story()
sc = st.sc
BOSS = {"outfit": "mobster", "helmet": "fedora"}
GOON = {"type": "npc", "outfit": "mobster", "hat": "fedora", "enter": "pop"}
BUSCETTA = {"type": "npc", "outfit": "mobster", "hat": None, "mustache": True, "hair": "#3A3A3A", "skin": "#D9A07A"}
FALCONE = {"type": "npc", "outfit": "judge", "hat": None, "mustache": True, "hair": "#2A2A2A", "skin": "#E8B48A"}
POLICE = {"type": "npc", "outfit": "police", "hat": "police_cap", "enter": "slide_right"}

sc("c01", "hook", "Eres un mafioso y decides contárselo todo a la policía.", {
    "background": {"type": "city_night", "rain": True},
    "character": {"action": "sweat", "expression": "worried", "x": 0.38, "y": 0.78, "scale": 1.2, **BOSS},
    "props": [{**POLICE, "x": 0.8, "y": 0.79, "size": 1.1, "facing": -1, "expression": "neutral", "at_word": 7}],
    "overlays": [{"type": "title", "lines": ["¿Y SI TRAICIONAS", "A LA MAFIA?"], "y": 280, "size": 108}],
    "camera": {"move": "punch"}},
   sfx=[{"name": "hit", "at": 0.0, "gain_db": -6}, {"name": "pop", "at_word": 7}], transition="cut",
   emphasis=["policía"])

sc("c02", "setup", "En Italia te llamarían pentito: arrepentido.", {
    "background": {"type": "burst", "c1": "#2BAE66", "c2": "#F4F4F4"},
    "character": {"action": "shrug", "expression": "worried", "x": 0.5, "y": 0.68, "scale": 1.3, "enter": "pop",
                  **BOSS},
    "overlays": [{"type": "label", "text": "«PENTITO» = ARREPENTIDO", "x": 540, "y": 330, "size": 62, "at_word": 4,
                  "bg": "#E8392F"}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("En Italia se llama «pentito» al mafioso que colabora con la justicia", "Treccani; Wikipedia «Pentito»")],
   sfx=[{"name": "ding", "at_word": 4}], transition="flash", emphasis=["pentito"])

sc("c03", "setup", "Y romperías la omertà, la ley del silencio, la regla más sagrada de la mafia.", {
    "background": {"type": "city_night"},
    "character": {"action": "shock", "expression": "scared", "x": 0.5, "y": 0.8, "scale": 1.1, **BOSS},
    "props": [{**GOON, "x": 0.15, "y": 0.79, "size": 1.05, "facing": 1, "expression": "angry", "at_word": 4},
              {**GOON, "x": 0.85, "y": 0.79, "size": 1.05, "facing": -1, "expression": "angry", "hat_color": "#4A4652",
               "mustache": True, "at_word": 5},
              {"type": "speech", "x": 0.5, "y": 0.38, "text": "¡SHHH! OMERTÀ", "size": 70, "at_word": 3, "tail": 0}],
    "camera": {"move": "push_in"}},
   claims=[F("La omertà es el código de silencio de la mafia siciliana", "Encyclopaedia Britannica")],
   sfx=[{"name": "pop", "at_word": 3}, {"name": "riser", "at_word": 8, "gain_db": -6}], emphasis=["omertà", "silencio"])

sc("c04", "development", "El más famoso fue Tommaso Buscetta.", {
    "background": {"type": "office", "desk": False},
    "character": {"visible": False},
    "props": [{**BUSCETTA, "x": 0.5, "y": 0.8, "size": 1.35, "expression": "neutral", "action": "think",
               "enter": "pop"}],
    "overlays": [{"type": "label", "text": "TOMMASO BUSCETTA", "x": 540, "y": 330, "size": 70, "at_word": 4}],
    "camera": {"move": "push_in"}},
   claims=[F("Tommaso Buscetta fue el primer gran «pentito» de la Cosa Nostra", "Encyclopaedia Britannica")],
   sfx=[{"name": "ding", "at_word": 4}], transition="slide", emphasis=["buscetta"])

sc("c05", "development", "En mil novecientos ochenta y cuatro, se lo contó todo al juez Giovanni Falcone.", {
    "background": {"type": "office"},
    "character": {"visible": False},
    "props": [{**BUSCETTA, "x": 0.25, "y": 0.72, "size": 1.05, "expression": "worried", "action": "talk", "facing": 1,
               "enter": "none"},
              {**FALCONE, "x": 0.76, "y": 0.72, "size": 1.05, "expression": "determined", "action": "think",
               "facing": -1, "at_word": 10, "enter": "pop"},
              {"type": "typewriter", "x": 0.5, "y": 0.73, "scale": 0.7, "layer": "front", "enter": "none"}],
    "overlays": [{"type": "label", "text": "JUEZ GIOVANNI FALCONE", "x": 540, "y": 330, "size": 62, "at_word": 10},
                 {"type": "counter", "from": 1950, "to": 1984, "y": 520, "size": 110, "over": 0.8, "plain": True}],
    "camera": {"move": "push_in"}},
   claims=[F("En 1984 Buscetta empezó a colaborar con el juez Giovanni Falcone", "Encyclopaedia Britannica")],
   sfx=[{"name": "tick", "at_word": 8}, {"name": "ding", "at_word": 10}], emphasis=["falcone"])

sc("c06", "development", "Gracias a él se celebró el Maxiproceso de Palermo, con cuatrocientos setenta y cinco acusados.", {
    "background": {"type": "courtroom", "label": "MAXIPROCESO", "cages": True, "judge": {"expression": "determined"}},
    "character": {"visible": False},
    "overlays": [{"type": "counter", "from": 0, "to": 475, "at_word": 10, "over": 0.8, "y": 300, "sub": "ACUSADOS"}],
    "camera": {"move": "pull_out", "zoom_from": 1.25}},
   claims=[F("El Maxiproceso de Palermo (1986-1987) juzgó a 475 acusados", "Encyclopaedia Britannica; Wikipedia «Maxiprocesso di Palermo»")],
   sfx=[{"name": "boom", "at": 0.1, "gain_db": -8}, {"name": "ding", "at_word": 10}], transition="zoom",
   emphasis=["maxiproceso", "cuatrocientos"])

sc("c07", "development", "Construyeron un tribunal blindado, a prueba de bombas, solo para ese juicio.", {
    "background": {"type": "city_night", "sign": False},
    "character": {"visible": False},
    "props": [{"type": "bunker", "x": 0.5, "y": 0.6, "scale": 1.1, "enter": "drop"}],
    "overlays": [{"type": "label", "text": "EL «AULA BÚNKER»", "x": 540, "y": 330, "size": 70, "at_word": 3}],
    "camera": {"move": "punch", "impacts": [0.6]}},
   claims=[F("Para el juicio se construyó una sala blindada, el «aula bunker», junto a la cárcel de Ucciardone", "Wikipedia «Maxiprocesso di Palermo»")],
   sfx=[{"name": "boom", "at": 0.55, "gain_db": -4}], emphasis=["blindado"])

sc("c08", "development", "Más de trescientos acusados fueron condenados.", {
    "background": {"type": "courtroom", "label": "MAXIPROCESO", "cages": True, "judge": {"expression": "angry"}},
    "character": {"visible": False},
    "props": [{"type": "gavel", "x": 0.74, "y": 0.4, "scale": 0.6, "enter": "none"}],
    "overlays": [{"type": "counter", "from": 0, "to": 300, "prefix": "+", "at_word": 2, "over": 0.6, "y": 300,
                  "sub": "CONDENADOS"}],
    "camera": {"move": "push_in", "impacts": ["w5"]}},
   claims=[F("Más de 300 acusados del Maxiproceso fueron condenados", "Encyclopaedia Britannica")],
   sfx=[{"name": "hit", "at_word": 5, "gain_db": -3}], transition="flash", emphasis=["condenados"])

sc("c09", "climax", "Pero traicionar a la mafia tiene un precio: tendrías que desaparecer.", {
    "background": {"type": "city_night", "rain": True},
    "character": {"action": "look_up", "expression": "scared", "x": 0.5, "y": 0.8, "scale": 1.15,
                  "actions": [["w8", "shock"]], **BOSS},
    "props": [{"type": "npc", "outfit": "mobster", "hat": "fedora", "x": 0.88, "y": 0.79, "size": 1.1,
               "facing": -1, "expression": "angry", "at_word": 4, "enter": "slide_right", "hat_color": "#151318"}],
    "overlays": [{"type": "vignette", "alpha": 0.65}],
    "camera": {"move": "push_in", "zoom_to": 1.15}},
   sfx=[{"name": "rumble", "at": 0.0, "gain_db": -6}, {"name": "hit", "at_word": 10, "gain_db": -6}],
   emphasis=["precio", "desaparecer"])

sc("c10", "climax", "Nueva identidad, otra ciudad y escolta las veinticuatro horas.", {
    "background": {"type": "city_night"},
    "character": {"action": "smug", "expression": "smug", "x": 0.5, "y": 0.79, "scale": 1.15, "outfit": "casual",
                  "helmet": "fedora", "extras": {"mustache": True, "hat_color": (0.55, 0.42, 0.3)}},
    "props": [{**POLICE, "x": 0.16, "y": 0.8, "size": 1.05, "facing": 1, "at_word": 5},
              {**POLICE, "x": 0.84, "y": 0.8, "size": 1.05, "facing": -1, "at_word": 5, "mustache": True}],
    "overlays": [{"type": "label", "text": "NUEVA IDENTIDAD", "x": 540, "y": 330, "size": 70, "at_word": 0},
                 {"type": "timer", "text": "24 h", "x": 850, "y": 560, "at_word": 7, "over": 1.0}],
    "camera": {"move": "static"}},
   claims=[F("Italia protege a los colaboradores de la justicia con nuevas identidades y escolta (ley de 1991)", "Ministero dell'Interno (Italia)")],
   sfx=[{"name": "sparkle", "at": 0.1}, {"name": "pop", "at_word": 5}], transition="slide", emphasis=["identidad"])

sc("c11", "climax", "Buscetta pasó sus últimos años lejos de Italia, protegido y con otro nombre.", {
    "background": {"type": "ocean"},
    "character": {"visible": False},
    "props": [{"type": "plane", "x": 0.55, "y": 0.3, "scale": 1.1, "enter": "slide_left", "enter_dur": 1.5, "loop": "bob"}],
    "camera": {"move": "pan_left", "amount": 120}},
   claims=[F("Buscetta vivió bajo protección en Estados Unidos hasta su muerte en el año 2000", "Encyclopaedia Britannica")],
   sfx=[{"name": "whoosh", "at": 0.2}], transition="zoom", emphasis=["nombre"])

sc("c12", "climax", "La mafia se vengó: en mil novecientos noventa y dos asesinó a los jueces Falcone y Borsellino.", {
    "background": {"type": "color", "color": "#1E2236"},
    "character": {"visible": False},
    "props": [{"type": "flowers", "x": 0.5, "y": 0.72, "scale": 1.6, "enter": "rise"}],
    "overlays": [{"type": "label", "text": "1992", "x": 540, "y": 330, "size": 90, "at_word": 4, "bg": "#2B2D6E"},
                 {"type": "fact", "label": "EN SU MEMORIA", "text": "Giovanni Falcone y Paolo Borsellino, jueces antimafia",
                  "at_word": 13, "y": 520}],
    "camera": {"move": "push_in", "zoom_to": 1.06}},
   claims=[F("En 1992 la mafia asesinó a los jueces Giovanni Falcone y Paolo Borsellino", "Encyclopaedia Britannica")],
   transition="circle", emphasis=["falcone", "borsellino"])

sc("c13", "ending", "El Estado respondió con todo y, al año siguiente, detuvo al jefe de jefes, Totò Riina.", {
    "background": {"type": "city_night"},
    "character": {"visible": False},
    "props": [{"type": "police_car", "x": 0.5, "y": 0.82, "scale": 0.9, "enter": "slide_left", "enter_dur": 0.6,
               "layer": "front"},
              {"type": "handcuffs", "x": 0.5, "y": 0.5, "at_word": 9, "enter": "drop", "scale": 1.3}],
    "overlays": [{"type": "label", "text": "1993 · TOTÒ RIINA, DETENIDO", "x": 540, "y": 330, "size": 60, "at_word": 9}],
    "camera": {"move": "punch", "impacts": ["w9"]}},
   claims=[F("Totò Riina, jefe de la Cosa Nostra, fue detenido en enero de 1993", "Encyclopaedia Britannica")],
   sfx=[{"name": "whoosh", "at": 0.1}, {"name": "hit", "at_word": 9, "gain_db": -4}], emphasis=["riina"])

sc("c14", "ending", "Hoy, el aeropuerto de Palermo lleva el nombre de Falcone y Borsellino.", {
    "background": {"type": "ocean", "level": 1150},
    "character": {"visible": False},
    "props": [{"type": "plane", "x": 0.5, "y": 0.26, "scale": 0.9, "enter": "none", "loop": "bob"},
              {"type": "sign", "x": 0.5, "y": 0.62, "text": "AEROPUERTO\nFALCONE-BORSELLINO", "w": 760, "size": 58,
               "at_word": 2, "enter": "drop"}],
    "camera": {"move": "push_in"}},
   claims=[F("El aeropuerto de Palermo se llama Falcone-Borsellino en su honor", "Aeroporto di Palermo (GESAP)")],
   sfx=[{"name": "sparkle", "at_word": 9}], transition="flash", emphasis=["falcone", "borsellino"])

sc("c15", "ending", "¿Tú hablarías? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"action": "talk", "expression": "excited", "x": 0.5, "y": 0.64, "scale": 1.35, "enter": "pop",
                  "actions": [["w2", "point_down"]], **BOSS},
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 2,
                  "arrow": "down", "bg": "#2B6BE8"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 2}], transition="zoom", pause=0.35)

DESC = """Eres un mafioso y decides contárselo todo a la policía. ¿Qué te pasaría? 🤫

Leo rompe la omertà, la ley del silencio de la mafia, y descubre la historia real de Tommaso Buscetta, el arrepentido que ayudó a sentar en el banquillo a cientos de mafiosos… y el precio que pagaron quienes se atrevieron a enfrentarse a la Cosa Nostra.

🧪 HISTORIA REAL DEL VÍDEO
• En Italia, al mafioso que colabora con la justicia se le llama «pentito» (arrepentido).
• La omertà es el código de silencio de la mafia siciliana.
• En 1984, Tommaso Buscetta empezó a colaborar con el juez Giovanni Falcone.
• Su testimonio fue clave en el Maxiproceso de Palermo (1986-1987): 475 acusados y más de 300 condenas.
• Para el juicio se construyó una sala blindada, el «aula búnker».
• Los colaboradores reciben nueva identidad y escolta; Buscetta vivió sus últimos años protegido fuera de Italia.
• En 1992 la mafia asesinó a los jueces Giovanni Falcone y Paolo Borsellino. En 1993 fue detenido Totò Riina, el «jefe de jefes».
• Hoy el aeropuerto de Palermo se llama Falcone-Borsellino en su honor.

⚠️ Leo es un personaje de ficción. Este vídeo es divulgación histórica en memoria de quienes lucharon contra la mafia.

📚 Fuentes: Encyclopaedia Britannica, Ministero dell'Interno (Italia), Aeroporto di Palermo (GESAP), Wikipedia (Maxiprocesso di Palermo).

💬 ¿Tú hablarías? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #mafia #historia #curiosidades #shorts"""

st.save("traicionar-a-la-mafia", "¿Qué pasaría si traicionaras a la mafia?",
        "¿Qué pasaría si traicionaras a la mafia?", "historia", "¿Tú hablarías?", {
            "title": "¿Qué pasaría si traicionaras a la mafia? 🤫",
            "hashtags": ["#quepasariasi", "#mafia", "#historia", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "traicionar a la mafia", "mafia", "pentito", "omertà", "buscetta",
                     "falcone", "borsellino", "maxiproceso", "cosa nostra", "historia", "animación", "hipotéticos"],
            "pinned_comment": "¿Tú hablarías o guardarías silencio? 🤫👇",
            "description": DESC,
            "thumbnail": {"scene": "c03", "t": 0.85, "lines": ["¿Y SI", "TRAICIONAS A", "LA MAFIA?"],
                          "badge": "¡OMERTÀ!", "badge_pos": [540, 1640], "y": 230,
                          "drop_props": ["speech"],
                          "character": {"action": "shock", "expression": "scared", "y": 0.8, "scale": 1.2},
                          "crop_y": 0.62, "h_shift": 760, "h_scale": 0.78},
        }, mood="mystery")
