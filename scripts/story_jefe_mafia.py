"""Guion: ¿Qué pasaría si te convirtieras en el jefe de la mafia?"""
from storykit import F, Story

st = Story()
sc = st.sc
BOSS = {"outfit": "mobster", "helmet": "fedora"}
GOON = {"type": "npc", "outfit": "mobster", "hat": "fedora", "enter": "pop"}
CAPONE = {"type": "npc", "outfit": "mobster", "hat": "fedora", "mustache": True, "hair": "#2A1E18",
          "hat_color": "#D8D2C4", "skin": "#E0A97E"}

sc("a01", "hook", "Eres el jefe de la mafia. Enhorabuena: tu vida es un infierno.", {
    "background": {"type": "office"},
    "character": {"action": "smug", "expression": "smug", "x": 0.5, "y": 0.72, "scale": 1.25,
                  "actions": [["w6", "shock"]], "expressions": [["w6", "worried"]], **BOSS},
    "props": [{"type": "money", "x": 0.78, "y": 0.69, "scale": 0.8, "enter": "none", "layer": "front"}],
    "overlays": [{"type": "title", "lines": ["¿JEFE DE", "LA MAFIA?"], "y": 280, "size": 130}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   sfx=[{"name": "hit", "at_word": 6, "gain_db": -4}], transition="cut", emphasis=["mafia", "infierno"])

sc("a02", "setup", "Primera regla: no te fíes de nadie. Ni siquiera de tu mano derecha.", {
    "background": {"type": "city_night"},
    "character": {"action": "think", "expression": "worried", "x": 0.5, "y": 0.78, "scale": 1.15, **BOSS},
    "props": [{**GOON, "x": 0.17, "y": 0.79, "size": 1.05, "facing": 1, "expression": "neutral"},
              {**GOON, "x": 0.84, "y": 0.79, "size": 1.05, "facing": -1, "expression": "smug", "hat_color": "#4A4652",
               "at_word": 7, "mustache": True}],
    "overlays": [{"type": "label", "text": "REGLA Nº 1", "x": 540, "y": 330, "size": 70}],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "pop", "at_word": 7}], emphasis=["nadie"])

sc("a03", "setup", "Los teléfonos pueden estar pinchados, así que nada de llamadas.", {
    "background": {"type": "office"},
    "character": {"action": "shock", "expression": "shock", "x": 0.33, "y": 0.72, "scale": 1.15, **BOSS},
    "props": [{"type": "phone", "x": 0.72, "y": 0.66, "scale": 1.3, "bug": True, "at_word": 0, "layer": "front"}],
    "overlays": [{"type": "label", "text": "¡PINCHADO!", "x": 760, "y": 900, "size": 64, "at_word": 4}],
    "camera": {"move": "push_in", "focus": [0.6, 0.6]}},
   claims=[F("La policía usa escuchas telefónicas para investigar a la mafia", "Polizia di Stato; DIA (Italia)")],
   sfx=[{"name": "ding", "at_word": 4}], transition="slide", emphasis=["pinchados"])

sc("a04", "development", "El capo Bernardo Provenzano se comunicaba con notas escritas a máquina: los pizzini.", {
    "background": {"type": "countryside", "farm_x": 760},
    "character": {"action": "think", "expression": "neutral", "x": 0.3, "y": 0.8, "scale": 1.0, **BOSS},
    "props": [{"type": "typewriter", "x": 0.66, "y": 0.8, "scale": 0.9, "enter": "drop", "layer": "front"},
              {"type": "note", "x": 0.6, "y": 0.42, "at_word": 7, "tilt": -0.2},
              {"type": "note", "x": 0.82, "y": 0.5, "at_word": 9, "tilt": 0.15},
              {"type": "note", "x": 0.7, "y": 0.28, "at_word": 12, "tilt": -0.05}],
    "overlays": [{"type": "label", "text": "«PIZZINI»", "x": 540, "y": 300, "size": 76, "at_word": 11}],
    "camera": {"move": "push_in"}},
   claims=[F("Bernardo Provenzano se comunicaba mediante pequeñas notas mecanografiadas llamadas «pizzini»", "BBC News (2006); Wikipedia «Bernardo Provenzano»")],
   sfx=[{"name": "tick", "at_word": 7}, {"name": "tick", "at_word": 9}, {"name": "pop", "at_word": 12}],
   emphasis=["provenzano", "pizzini"])

sc("a05", "development", "Así logró esconderse de la policía durante cuarenta y tres años.", {
    "background": {"type": "countryside", "farm_x": 760},
    "character": {"visible": False},
    "props": [{"type": "wanted", "x": 0.5, "y": 0.6, "scale": 1.0, "enter": "drop", "sub": "43 AÑOS"}],
    "overlays": [{"type": "counter", "from": 0, "to": 43, "suffix": " AÑOS", "at_word": 7, "over": 0.7, "y": 300,
                  "sub": "ESCONDIDO"}],
    "camera": {"move": "pull_out", "zoom_from": 1.2}},
   claims=[F("Provenzano estuvo prófugo de 1963 a 2006 (43 años)", "BBC News (2006)")],
   sfx=[{"name": "whoosh", "at": 0.1}, {"name": "ding", "at_word": 7}], transition="zoom", emphasis=["cuarenta", "tres"])

sc("a06", "development", "Lo encontraron en dos mil seis, escondido en una granja cerca de Corleone, su pueblo.", {
    "background": {"type": "countryside", "farm_x": 540, "farm_y": 1200},
    "character": {"visible": False},
    "props": [{"type": "police_car", "x": 0.5, "y": 0.8, "scale": 0.85, "at_word": 1, "enter": "slide_right",
               "enter_dur": 0.6, "layer": "front"}],
    "overlays": [{"type": "label", "text": "CORLEONE (SICILIA) · 2006", "x": 540, "y": 330, "size": 60, "at_word": 9}],
    "camera": {"move": "push_in", "focus": [0.5, 0.6]}},
   claims=[F("Provenzano fue detenido en abril de 2006 en una granja cerca de Corleone", "BBC News (11/04/2006)")],
   sfx=[{"name": "whoosh", "at_word": 1}, {"name": "ding", "at_word": 9}], emphasis=["granja", "corleone"])

sc("a07", "development", "Vivía a base de requesón y achicoria. Muy glamuroso todo.", {
    "background": {"type": "countryside", "farm_x": 820, "farm_y": 1150},
    "character": {"action": "shrug", "expression": "smug", "x": 0.5, "y": 0.76, "scale": 1.2, **BOSS},
    "props": [{"type": "plant", "x": 0.2, "y": 0.66, "at_word": 4, "health": 0.9},
              {"type": "rock", "x": 0.82, "y": 0.66, "at_word": 4, "color": "#FFF8E6", "scale": 1.6}],
    "camera": {"move": "static"}},
   claims=[F("En su escondite comía de forma muy sencilla (requesón, achicoria…)", "Prensa italiana y BBC (2006)", "estimate")],
   sfx=[{"name": "pop", "at_word": 4}, {"name": "boing", "at_word": 7}], transition="slide", emphasis=["glamuroso"])

sc("a08", "development", "Y el dinero tampoco es fácil: si no puedes explicar de dónde sale, te pillan.", {
    "background": {"type": "office"},
    "character": {"action": "sweat", "expression": "worried", "x": 0.35, "y": 0.72, "scale": 1.15, "sweat": 1, **BOSS},
    "props": [{"type": "money", "x": 0.75, "y": 0.69, "scale": 1.0, "enter": "none", "layer": "front"},
              {"type": "handcuffs", "x": 0.7, "y": 0.4, "at_word": 13, "enter": "drop"}],
    "camera": {"move": "push_in", "impacts": ["w13"]}},
   sfx=[{"name": "boom", "at_word": 13, "gain_db": -6}], emphasis=["dinero", "pillan"])

sc("a09", "development", "Que se lo digan a Al Capone, el gánster más famoso de Chicago.", {
    "background": {"type": "city_night", "rain": True},
    "character": {"visible": False},
    "props": [{**CAPONE, "x": 0.5, "y": 0.78, "size": 1.3, "expression": "smug", "action": "smug", "enter": "pop"}],
    "overlays": [{"type": "label", "text": "AL CAPONE · CHICAGO", "x": 540, "y": 330, "size": 66, "at_word": 5}],
    "camera": {"move": "push_in"}},
   claims=[F("Al Capone fue el gánster más conocido de Chicago en los años 20", "FBI (Famous Cases: Al Capone)")],
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -6}, {"name": "ding", "at_word": 5}], transition="flash",
   emphasis=["capone"])

sc("a10", "climax", "Nunca lograron condenarlo por sus crímenes… pero sí por no pagar impuestos.", {
    "background": {"type": "courtroom", "judge": {"expression": "angry"}},
    "character": {"visible": False},
    "props": [{**CAPONE, "x": 0.5, "y": 0.92, "size": 1.0, "expression": "shock", "action": "shock", "at_word": 6,
               "enter": "rise"},
              {"type": "gavel", "x": 0.74, "y": 0.4, "scale": 0.6, "at_word": 6}],
    "overlays": [{"type": "fact", "text": "1931: condenado por evasión de impuestos", "at_word": 7}],
    "camera": {"move": "push_in", "impacts": ["w10"]}},
   claims=[F("En 1931 Al Capone fue condenado por evasión fiscal", "FBI (Famous Cases: Al Capone)")],
   sfx=[{"name": "hit", "at_word": 10, "gain_db": -3}], emphasis=["impuestos"])

sc("a11", "climax", "Le cayeron once años y acabó en Alcatraz.", {
    "background": {"type": "prison"},
    "character": {"visible": False},
    "props": [{**CAPONE, "outfit": "prisoner", "hat": None, "x": 0.45, "y": 0.78, "size": 1.2, "expression": "tired",
               "action": "sweat", "enter": "none"},
              {"type": "bars", "x": 0.5, "y": 0.5, "enter": "drop", "layer": "front", "at": 0.2}],
    "overlays": [{"type": "counter", "from": 0, "to": 11, "suffix": " AÑOS", "at_word": 2, "over": 0.5, "y": 260,
                  "sub": "DE CONDENA"},
                 {"type": "label", "text": "ALCATRAZ", "x": 540, "y": 1100, "size": 64, "at_word": 7}],
    "camera": {"move": "static", "impacts": [0.6]}},
   claims=[F("Capone fue condenado a 11 años y en 1934 lo trasladaron a Alcatraz", "FBI; Federal Bureau of Prisons")],
   sfx=[{"name": "boom", "at": 0.55, "gain_db": -4}, {"name": "ding", "at_word": 2}], transition="circle",
   emphasis=["once", "alcatraz"])

sc("a12", "climax", "Por cierto, su tarjeta de visita decía que vendía muebles usados.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"action": "celebrate", "expression": "laugh", "x": 0.5, "y": 0.82,
                  "scale": 1.05, **BOSS},
    "props": [{"type": "card", "x": 0.5, "y": 0.33, "at_word": 3, "enter": "drop",
               "lines": ["ALPHONSE CAPONE", "Muebles usados"]}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("La tarjeta de visita de Capone lo presentaba como vendedor de muebles de segunda mano", "The Mob Museum (Las Vegas)")],
   sfx=[{"name": "boing", "at_word": 8}], transition="flash", emphasis=["muebles"])

sc("a13", "ending", "Casi todos los grandes capos acaban igual: entre rejas… o algo peor.", {
    "background": {"type": "prison"},
    "character": {"action": "sweat", "expression": "worried", "x": 0.5, "y": 0.78, "scale": 1.2,
                  "outfit": "prisoner"},
    "props": [{"type": "bars", "x": 0.5, "y": 0.5, "at_word": 7, "enter": "drop", "layer": "front"}],
    "camera": {"move": "push_in", "impacts": ["w8"]}},
   claims=[F("Riina, Provenzano, Capone y Messina Denaro, entre otros, acabaron detenidos", "Hemerotecas (BBC, El País)", "estimate")],
   sfx=[{"name": "boom", "at_word": 8, "gain_db": -4}], emphasis=["rejas"])

sc("a14", "ending", "¿Seguirías queriendo ser el jefe? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"action": "talk", "expression": "excited", "x": 0.5, "y": 0.64, "scale": 1.35, "enter": "pop",
                  "actions": [["w5", "point_down"]], **BOSS},
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5,
                  "arrow": "down", "bg": "#2B6BE8"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 5}], transition="zoom", pause=0.35)

DESC = """Te despiertas siendo el jefe de la mafia… y tu vida se convierte en un infierno. 🕴️🎩

Leo descubre la cara menos glamurosa de ser un capo: no fiarte de nadie, no poder usar el teléfono, vivir escondido durante décadas… y acabar cayendo por algo tan aburrido como los impuestos.

🧪 HISTORIA REAL DEL VÍDEO
• Bernardo Provenzano, jefe de la Cosa Nostra siciliana, se comunicaba con notitas escritas a máquina llamadas «pizzini» para evitar las escuchas.
• Estuvo prófugo 43 años (1963-2006) y lo detuvieron en una granja cerca de Corleone, su pueblo.
• Al Capone, el gánster más famoso de Chicago, nunca fue condenado por sus crímenes violentos… sino por evasión de impuestos en 1931.
• Le cayeron 11 años de condena y pasó parte de ella en Alcatraz.
• Su tarjeta de visita decía que se dedicaba a vender muebles usados.

⚠️ Leo es un personaje de ficción. Este vídeo es divulgación histórica: el crimen organizado destroza vidas y casi siempre acaba igual, en la cárcel o algo peor.

📚 Fuentes: FBI (Famous Cases: Al Capone), Federal Bureau of Prisons, The Mob Museum, BBC News (2006), Polizia di Stato.

💬 ¿Seguirías queriendo ser el jefe? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #mafia #historia #curiosidades #shorts"""

st.save("jefe-de-la-mafia", "¿Qué pasaría si te convirtieras en el jefe de la mafia?",
        "¿Qué pasaría si te convirtieras en el jefe de la mafia?", "historia",
        "¿Seguirías queriendo ser el jefe?", {
            "title": "¿Qué pasaría si fueras el jefe de la mafia? 🎩",
            "hashtags": ["#quepasariasi", "#mafia", "#historia", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "jefe de la mafia", "mafia", "al capone", "provenzano", "cosa nostra",
                     "alcatraz", "historia", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Seguirías queriendo ser el jefe sabiendo cómo acabó Capone? 🎩👇",
            "description": DESC,
            "thumbnail": {"scene": "a01", "t": 0.3, "lines": ["¿Y SI FUERAS", "EL JEFE DE", "LA MAFIA?"],
                          "badge": "HISTORIA REAL", "badge_pos": [540, 1620], "y": 260,
                          "character": {"action": "smug", "expression": "smug", "y": 0.8, "scale": 1.4},
                          "crop_y": 0.62, "h_shift": 900, "h_scale": 0.85},
        }, mood="mystery")
