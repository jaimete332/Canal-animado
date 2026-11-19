"""Guion: ¿Qué pasaría si te despertaras en la Edad Media?"""
from storykit import F, Story

st = Story()
sc = st.sc
PEASANT = {"outfit": "peasant", "helmet": "straw_hat"}
KNIGHT = {"type": "npc", "outfit": "knight", "hat": "knight"}


def leo(**kw):
    d = {"x": 0.35, "y": 0.8, "scale": 1.2, **PEASANT}
    d.update(kw)
    return d


sc("e01", "hook", "Te despiertas y estás en la Edad Media. Y no, no hay wifi.", {
    "background": {"type": "village"},
    "character": leo(action="shock", expression="surprised", x=0.5, outfit="casual", helmet=None,
                     expressions=[["w8", "worried"]]),
    "props": [{"type": "wifi", "x": 0.78, "y": 0.22, "at_word": 8, "crossed": True, "cross_at": 0.3, "cross_r": 130,
               "scale": 0.8}],
    "overlays": [{"type": "title", "lines": ["¿Y SI VIVIERAS EN", "LA EDAD MEDIA?"], "y": 280, "size": 104}],
    "camera": {"move": "punch", "impacts": ["w9"]}},
   claims=[F("Despertar en otra época es una situación imaginaria", "Licencia narrativa", "fiction")],
   sfx=[{"name": "hit", "at": 0.0, "gain_db": -6}, {"name": "crack", "at_word": 9}], transition="cut",
   emphasis=["edad", "media"])

sc("e02", "setup", "Para empezar: ni patatas, ni tomates, ni chocolate.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"visible": False},
    "props": [{"type": "food", "kind": "potato", "x": 0.22, "y": 0.45, "at_word": 3, "crossed": True},
              {"type": "food", "kind": "tomato", "x": 0.5, "y": 0.45, "at_word": 5, "crossed": True},
              {"type": "food", "kind": "chocolate", "x": 0.78, "y": 0.45, "at_word": 7, "crossed": True}],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "pop", "at_word": 3}, {"name": "pop", "at_word": 5}, {"name": "pop", "at_word": 7}],
   transition="flash", emphasis=["patatas", "tomates", "chocolate"])

sc("e02b", "setup", "Todo eso llegó de América después de mil cuatrocientos noventa y dos.", {
    "background": {"type": "ocean", "level": 1100},
    "character": {"visible": False},
    "props": [{"type": "sign", "x": 0.5, "y": 0.62, "text": "DE AMÉRICA\nDESDE 1492", "w": 520, "size": 58,
               "scale": 1.5, "enter": "drop"},
              {"type": "food", "kind": "potato", "x": 0.2, "y": 0.25, "scale": 0.6, "loop": "bob"},
              {"type": "food", "kind": "tomato", "x": 0.5, "y": 0.2, "scale": 0.6, "loop": "bob"},
              {"type": "food", "kind": "chocolate", "x": 0.8, "y": 0.25, "scale": 0.5, "loop": "bob"}],
    "camera": {"move": "push_in"}},
   claims=[F("La patata, el tomate y el cacao llegaron a Europa desde América tras 1492", "Encyclopaedia Britannica")],
   sfx=[{"name": "boom", "at": 0.5, "gain_db": -8}, {"name": "ding", "at_word": 6}], transition="slide",
   emphasis=["américa"])

sc("e03", "setup", "Lo más probable es que fueras campesino, como la inmensa mayoría de la gente.", {
    "background": {"type": "village"},
    "character": leo(action="look_up", expression="worried", enter="pop"),
    "props": [{"type": "npc", "outfit": "peasant", "hat": "straw_hat", "x": 0.68, "y": 0.8, "size": 1.0,
               "expression": "neutral", "hair": "#4A3520", "at_word": 9},
              {"type": "npc", "outfit": "peasant", "hat": None, "x": 0.88, "y": 0.82, "size": 0.9,
               "expression": "happy", "hair": "#C9A24A", "at_word": 11}],
    "camera": {"move": "push_in"}},
   claims=[F("La gran mayoría de la población medieval era campesina", "Encyclopaedia Britannica")],
   sfx=[{"name": "pop", "at_word": 9}, {"name": "pop", "at_word": 11}], emphasis=["campesino"])

sc("e04", "setup", "Trabajarías la tierra de sol a sol, y parte de la cosecha sería para tu señor.", {
    "background": {"type": "village"},
    "character": leo(action="dig", expression="tired", x=0.38, sweat=0.8),
    "props": [{"type": "food", "kind": "bread", "x": 0.75, "y": 0.62, "at_word": 9, "scale": 0.8, "enter": "pop"},
              {"type": "arrow", "x": 0.72, "y": 0.5, "rot": -1.2, "scale": 0.45, "at_word": 12}],
    "overlays": [{"type": "label", "text": "PARA EL SEÑOR", "x": 760, "y": 400, "size": 56, "at_word": 12}],
    "camera": {"move": "static"}},
   claims=[F("Los campesinos debían entregar parte de la cosecha o trabajo al señor feudal", "Encyclopaedia Britannica")],
   sfx=[{"name": "dig", "at": 0.3}, {"name": "dig", "at": 0.9}, {"name": "dig", "at": 1.5}, {"name": "ding", "at_word": 12}],
   transition="slide", emphasis=["señor"])

sc("e05", "development", "Pero desmontemos un mito: no todo el mundo moría a los treinta.", {
    "background": {"type": "village"},
    "character": leo(action="present", expression="smug", x=0.3),
    "overlays": [{"type": "myth", "text": "MORÍAN A LOS 30", "y": 400, "stamp_at": 1.6}],
    "camera": {"move": "punch", "impacts": [1.75]}},
   sfx=[{"name": "hit", "at": 1.75, "gain_db": -3}], emphasis=["mito"])

sc("e06", "development", "La media era baja porque morían muchos niños. Quien llegaba a adulto podía pasar de los cincuenta.", {
    "background": {"type": "village"},
    "character": {"visible": False},
    "props": [{"type": "npc", "outfit": "peasant", "hat": None, "x": 0.5, "y": 0.82, "size": 1.3, "hair": "#DDDDDD",
               "mustache": True, "expression": "happy", "action": "idle", "at_word": 9}],
    "overlays": [{"type": "fact", "text": "La esperanza de vida al nacer era baja por la altísima mortalidad infantil",
                  "at_word": 1},
                 {"type": "counter", "from": 30, "to": 60, "suffix": " AÑOS", "at_word": 13, "over": 0.8, "y": 560,
                  "size": 110}],
    "camera": {"move": "push_in"}},
   claims=[F("La baja esperanza de vida medieval se debía sobre todo a la mortalidad infantil; muchos adultos superaban los 50", "Encyclopaedia Britannica; Our World in Data")],
   sfx=[{"name": "pop", "at_word": 9}, {"name": "ding", "at_word": 13}], transition="zoom", emphasis=["niños", "cincuenta"])

sc("e07", "development", "Otro mito: la gente sí se lavaba. En muchas ciudades había baños públicos.", {
    "background": {"type": "village"},
    "character": leo(action="celebrate", expression="laugh", x=0.25, scale=0.9, y=0.88),
    "props": [{"type": "bathhouse", "x": 0.58, "y": 0.6, "scale": 0.9, "at_word": 7, "enter": "drop"}],
    "overlays": [{"type": "myth", "text": "NO SE BAÑABAN", "y": 350, "stamp_at": 0.8}],
    "camera": {"move": "push_in"}},
   claims=[F("En muchas ciudades medievales existían baños públicos", "Encyclopaedia Britannica; Smithsonian")],
   sfx=[{"name": "splash", "at_word": 7, "gain_db": -6}], transition="slide", emphasis=["lavaba"])

sc("e08", "development", "¿Y los caballeros? No necesitaban grúas para subirse al caballo.", {
    "background": {"type": "village"},
    "character": {"visible": False},
    "props": [{**KNIGHT, "x": 0.35, "y": 0.82, "size": 1.3, "expression": "smug", "action": "smug", "enter": "pop"},
              {"type": "crane", "x": 0.75, "y": 0.55, "scale": 0.7, "at_word": 5, "crossed": True, "cross_at": 0.6}],
    "camera": {"move": "push_in"}},
   claims=[F("La idea de que los caballeros se subían al caballo con grúas es un mito", "Royal Armouries (Leeds)")],
   sfx=[{"name": "crack", "at_word": 6}], emphasis=["grúas"])

sc("e09", "development", "Sus armaduras pesaban unos veinticinco kilos y con ellas podían correr y saltar.", {
    "background": {"type": "village"},
    "character": {"visible": False},
    "props": [{**KNIGHT, "x": 0.5, "y": 0.8, "size": 1.25, "expression": "excited", "action": "celebrate",
               "enter": "none"}],
    "overlays": [{"type": "counter", "from": 0, "to": 25, "prefix": "≈", "suffix": " KG", "at_word": 4, "over": 0.6,
                  "y": 330, "sub": "DE ARMADURA"}],
    "camera": {"move": "static"}},
   claims=[F("Una armadura completa pesaba en torno a 15-25 kg y permitía moverse con agilidad", "Royal Armouries (Leeds)")],
   sfx=[{"name": "boing", "at": 0.4}, {"name": "boing", "at": 1.1}], transition="whip", emphasis=["veinticinco"])

sc("e10", "climax", "Lo peor llegaría en mil trescientos cuarenta y siete: la peste negra.", {
    "background": {"type": "village", "mode": "plague"},
    "character": leo(action="squished", expression="scared", x=0.5),
    "overlays": [{"type": "label", "text": "1347 · PESTE NEGRA", "x": 540, "y": 330, "size": 70, "at_word": 8,
                  "bg": "#2B2D3A"},
                 {"type": "vignette", "alpha": 0.6}],
    "camera": {"move": "push_in", "shake": 0.2}},
   claims=[F("La peste negra llegó a Europa en 1347", "Encyclopaedia Britannica")],
   sfx=[{"name": "rumble", "at": 0.0, "gain_db": -6}], transition="circle", emphasis=["peste"])

sc("e11", "climax", "Mató a entre un tercio y la mitad de la población de Europa.", {
    "background": {"type": "village", "mode": "plague"},
    "character": {"visible": False},
    "overlays": [{"type": "counter", "from": 0, "to": 50, "suffix": " %", "prefix": "30-", "at_word": 1, "over": 1.0,
                  "y": 600, "sub": "DE LA POBLACIÓN DE EUROPA", "size": 150},
                 {"type": "vignette", "alpha": 0.6}],
    "camera": {"move": "push_in"}},
   claims=[F("La peste negra mató a entre un tercio y la mitad de la población europea (1347-1351)", "Encyclopaedia Britannica")],
   emphasis=["tercio", "mitad"])

sc("e12", "ending", "Así que mejor no te acerques a las ratas… ni a sus pulgas.", {
    "background": {"type": "village", "mode": "plague"},
    "character": leo(action="shock", expression="shock", x=0.3),
    "props": [{"type": "rat", "x": 0.72, "y": 0.86, "fleas": True, "enter": "slide_right", "loop": "shake"}],
    "camera": {"move": "punch"}},
   claims=[F("La peste se transmitía sobre todo por las pulgas de las ratas", "CDC; Encyclopaedia Britannica")],
   sfx=[{"name": "boing", "at_word": 9}], emphasis=["ratas", "pulgas"])

sc("e13", "ending", "¿Sobrevivirías una semana en la Edad Media? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#B5532F", "c2": "#D6A84E"},
    "character": leo(action="talk", expression="excited", x=0.5, y=0.64, scale=1.35, enter="pop",
                     actions=[["w7", "point_down"]]),
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 7, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 7}], transition="zoom", pause=0.35)

DESC = """Te despiertas y estás en la Edad Media… ¿sobrevivirías? 🏰

Leo viaja al pasado y descubre cómo era la vida de verdad: sin patatas ni tomates, trabajando para el señor feudal… y desmonta tres mitos que casi todo el mundo se cree. Hasta que llega la peste negra.

🧪 DATOS REALES DEL VÍDEO
• La patata, el tomate y el cacao no existían en Europa: llegaron de América después de 1492.
• La inmensa mayoría de la población medieval era campesina y entregaba parte de la cosecha o de su trabajo al señor.
• MITO: «todos morían a los 30». La esperanza de vida al nacer era baja por la altísima mortalidad infantil, pero muchos adultos pasaban de los 50.
• MITO: «no se lavaban». En muchas ciudades había baños públicos.
• MITO: «los caballeros necesitaban grúas para subir al caballo». Una armadura pesaba unos 15-25 kg y permitía correr y saltar.
• La peste negra llegó en 1347 y mató a entre un tercio y la mitad de la población de Europa. Se transmitía sobre todo por las pulgas de las ratas.

⚠️ El viaje en el tiempo de Leo es ficción; los datos históricos son reales y aproximados.

📚 Fuentes: Encyclopaedia Britannica, Royal Armouries (Leeds), Our World in Data, Smithsonian, CDC.

💬 ¿Sobrevivirías una semana en la Edad Media? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?» cada semana.

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #edadmedia #historia #curiosidades #shorts"""

st.save("despertar-en-la-edad-media", "¿Qué pasaría si te despertaras en la Edad Media?",
        "¿Qué pasaría si te despertaras en la Edad Media?", "historia", "¿Sobrevivirías una semana en la Edad Media?", {
            "title": "¿Qué pasaría si te despertaras en la Edad Media? 🏰",
            "hashtags": ["#quepasariasi", "#edadmedia", "#historia", "#curiosidades", "#shorts"],
            "tags": ["qué pasaría si", "edad media", "vida en la edad media", "mitos de la edad media", "caballeros",
                     "peste negra", "historia", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Cuántos días aguantarías tú en la Edad Media? 🏰👇",
            "description": DESC,
            "thumbnail": {"scene": "e03", "t": 0.95, "lines": ["¿Y SI VIVIERAS EN", "LA EDAD MEDIA?"],
                          "badge": "3 MITOS FALSOS", "badge_pos": [540, 1660], "y": 260, "size": 120,
                          "character": {"action": "shock", "expression": "shock", "x": 0.35, "y": 0.82, "scale": 1.35},
                          "crop_y": 0.58, "h_shift": 800, "h_scale": 0.8},
        }, mood="adventure")
