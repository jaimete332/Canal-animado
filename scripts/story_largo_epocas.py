"""Vídeo largo (16:9): ¿Cuánto durarías en cada época de la historia?

Nicho elegido con scripts/research_largo.py (data/research/largo_2026-11-22.md): los vídeos largos en español de
«¿cuánto sobrevivirías en otra época?» tienen decenas de miles de visualizaciones al día. Se copia el patrón
(viaje + medidor de supervivencia + datos reales), no el contenido: épocas históricas, datos y guion propios.
"""
from storykit import F, Story

st = Story()
_sc = st.sc
LEO = {"x": 0.3, "y": 0.93, "scale": 0.85}
OUTFIT = {"intro": "casual", "egipto": "linen", "roma": "toga", "vikingos": "peasant", "peste": "peasant",
          "mexica": "linen", "elcano": "sailor", "piratas": "sailor", "londres": "victorian", "panama": "linen"}
BG = {
    "tunel": {"type": "time_tunnel", "window": 960},
    "egipto": {"type": "egypt", "progress": 0.6}, "egipto_obra": {"type": "egypt", "progress": 0.35},
    "roma": {"type": "rome"}, "roma_fuego": {"type": "rome", "fire": 0.9},
    "peste": {"type": "village", "mode": "plague"}, "aldea": {"type": "village"},
    "barco": {"type": "ship_deck"}, "barco_noche": {"type": "ship_deck", "night": True}, "mar": {"type": "ocean"},
    "londres": {"type": "london", "smog": 0.55}, "londres_humo": {"type": "london", "smog": 0.9},
    "hoy": {"type": "backyard"},
    "fiordo": {"type": "fjord"}, "teno": {"type": "tenochtitlan", "window": 1080},
    "teno_ancho": {"type": "tenochtitlan", "window": 960},
    "canal": {"type": "jungle_canal", "rain": 0.3}, "canal_lluvia": {"type": "jungle_canal", "rain": 0.9},
}
era = "intro"


def burst(c1="#FFD23F", c2="#FFB300"):
    return {"type": "burst", "c1": c1, "c2": c2, "window": 960}


def leo(**kw):
    d = {**LEO, "outfit": OUTFIT[era]}
    d.update(kw)
    return d


def fact(text, at_word=1, label=None):
    o = {"type": "fact", "text": text, "at_word": at_word, "y": 60}
    if label:
        o["label"] = label
    return o


def label(text, bg="#E8392F", at_word=None):
    o = {"type": "label", "text": text, "x": 960, "y": 80, "size": 64, "bg": bg}
    if at_word is not None:
        o["at_word"] = at_word
    return o


def meter(value, text, at_word=0):
    return {"type": "survival_meter", "x": 0.5, "y": 0.42, "scale": 1.15, "value": value, "label": text,
            "at_word": at_word, "enter": "pop"}


def S(sid, beat, narration, bg, char=None, props=(), ov=(), cam=None, claims=(), sfx=(), tr="whip", emph=(),
      pause=0.08):
    vis = {"background": dict(BG[bg]) if isinstance(bg, str) else bg,
           "character": char if char is not None else {"visible": False},
           "props": list(props), "overlays": list(ov), "camera": cam or {"move": "push_in", "zoom_to": 1.08}}
    _sc(sid, beat, narration, vis, claims=claims, sfx=sfx, transition=tr, emphasis=list(emph), pause=pause)


# ================================================================== INTRO
S("i01", "hook", "Esta noche, una máquina del tiempo te lanza al pasado.", "tunel",
  leo(x=0.5, y=0.75, action="float", expression="shock"),
  ov=[{"type": "title", "lines": ["¿CUÁNTO DURARÍAS", "EN CADA ÉPOCA?"], "y": 150, "size": 96}],
  cam={"move": "punch", "impacts": [0.2]}, sfx=[{"name": "riser", "at": 0.0, "gain_db": -6}], tr="cut",
  emph=["pasado"])
S("i02", "setup", "Sin móvil, sin vacunas y sin billete de vuelta.", "tunel",
  leo(x=0.5, y=0.75, action="float", expression="worried"),
  props=[{"type": "smartphone", "x": 0.25, "y": 0.4, "scale": 0.8, "crossed": True, "cross_at": 0.5, "loop": "bob"},
         {"type": "question", "x": 0.76, "y": 0.38, "at_word": 4}],
  sfx=[{"name": "pop", "at_word": 4}])
S("i03", "setup", "Vas a visitar nueve épocas de la historia, y en cada una la pregunta será la misma: ¿cuánto durarías?",
  burst("#5CE1E6", "#8FF0F5"), leo(x=0.22, action="present", expression="excited"),
  props=[{"type": "calendar", "x": 0.68, "y": 0.5, "scale": 1.1, "loop": "bob", "from": 2026, "to": -2560, "over": 4.0}],
  emph=["ocho", "durarías"])
S("i04", "setup", "Para saberlo usaremos este medidor: desde unas pocas horas… hasta toda una vida.",
  burst(), props=[meter(0.98, "¿CUÁNTO DURARÍAS?")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.2}], emph=["horas", "vida"])
S("i04b", "setup", "Las reglas: llegas solo, con ropa de la época, y sabiendo lo mismo que la gente de ese tiempo. Ni más ni menos.",
  "aldea", leo(x=0.3, action="present", expression="determined", outfit="peasant"),
  props=[{"type": "note", "x": 0.7, "y": 0.45, "scale": 1.0, "loop": "wobble", "at_word": 1}], tr="slide",
  emph=["reglas"])
S("i05", "setup", "Nada de magia: todo lo que vas a ver sale de arqueólogos, historiadores y médicos.", "aldea",
  leo(x=0.5, action="talk", expression="determined"),
  ov=[{"type": "label", "text": "DATOS REALES · FUENTES EN LA DESCRIPCIÓN", "x": 960, "y": 80, "size": 54,
       "bg": "#22B573"}], tr="slide")
S("i05b", "setup", "Nueve paradas, miles de años y una sola misión: volver vivo para contarlo.", "tunel",
  leo(x=0.5, y=0.75, action="float", expression="determined"),
  ov=[{"type": "counter", "from": 0, "to": 9, "suffix": " ÉPOCAS", "at_word": 0, "over": 0.6, "y": 150, "size": 120}],
  emph=["vivo"])
S("i06", "setup", "Y al final te diré cuál es la época más peligrosa de todas. Agárrate: primera parada.", "tunel",
  leo(x=0.5, y=0.75, action="float", expression="excited"), sfx=[{"name": "whoosh", "at_word": 13}], tr="zoom")

# ================================================================== 1 · EGIPTO
era = "egipto"
S("e01", "development", "Abres los ojos y el calor te golpea. Estás en Giza, Egipto, hacia el año dos mil quinientos sesenta antes de Cristo.",
  "egipto", leo(action="shock", expression="hot", sweat=0.6),
  ov=[label("1 · EGIPTO · ≈2560 a. C.", "#E8A33A")], cam={"move": "pull_out"},
  sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", emph=["Giza"])
S("e02", "development", "Delante de ti, miles de personas levantan la Gran Pirámide, la tumba del faraón Keops.",
  "egipto_obra", leo(x=0.2, action="point_up", expression="wow"),
  props=[{"type": "stone_block", "x": 0.68, "y": 0.9, "scale": 0.8}],
  claims=[F("La Gran Pirámide de Giza se construyó como tumba del faraón Keops (Jufu), hacia 2560 a. C.", "Encyclopaedia Britannica")],
  cam={"move": "pan_right", "amount": 160})
S("e03", "development", "Y antes de que lo pienses: no, no la construían esclavos.", "egipto",
  leo(action="talk", expression="smug"),
  ov=[{"type": "myth", "text": "LA HICIERON ESCLAVOS", "stamp": "¡FALSO!", "y": 160, "stamp_at": 1.2}],
  sfx=[{"name": "hit", "at": 1.2, "gain_db": -6}], emph=["esclavos"])
S("e04", "development", "Junto a la pirámide se encontraron las tumbas de los obreros. Y a un esclavo jamás le habrían dado un sitio tan cerca del faraón.",
  "egipto", leo(x=0.22, action="present", expression="determined"),
  ov=[fact("Tumbas de los constructores halladas junto a las pirámides de Giza (desde 1990)", 4)],
  claims=[F("Las tumbas de los trabajadores, junto a las pirámides, indican que no eran esclavos", "Zahi Hawass, Consejo Supremo de Antigüedades de Egipto (2010)")],
  tr="slide")
S("e05", "development", "Eran trabajadores organizados en cuadrillas que se turnaban durante meses, y comían a cuenta del Estado.",
  "egipto", leo(x=0.3, action="walk", expression="happy"),
  props=[{"type": "npc", "outfit": "linen", "hair": "#2A1A10", "skin": "#B9825A", "x": 0.62, "y": 0.93, "size": 0.8,
          "action": "walk", "shirt": "#F2EAD6"},
         {"type": "npc", "outfit": "linen", "hair": "#1A1210", "skin": "#A8704A", "x": 0.78, "y": 0.93, "size": 0.8,
          "action": "walk", "shirt": "#F2EAD6", "seed": 2}],
  claims=[F("Trabajaban por turnos de unos tres meses y recibían raciones del Estado", "Zahi Hawass (2010); Mark Lehner, AERA")])
S("e05b", "development", "¿Cuántos eran? Según quién haga la cuenta, entre diez mil y veinte mil personas trabajando a la vez.",
  "egipto_obra", leo(x=0.2, action="think", expression="wow"),
  ov=[{"type": "counter", "from": 0, "to": 20000, "prefix": "10.000-", "suffix": " OBREROS", "at_word": 8, "over": 0.8,
       "y": 160, "size": 100, "sub": "ESTIMACIONES DE LOS ARQUEÓLOGOS"}],
  claims=[F("Las estimaciones de la mano de obra simultánea en Giza van de unos 10.000 (Lehner) a 20.000 o más (Hawass)", "Mark Lehner, AERA; Zahi Hawass")],
  emph=["veinte"])
S("e06", "development", "Lo sabemos, en parte, por el diario de un inspector llamado Merer: los papiros escritos más antiguos que conocemos.",
  burst("#E8A33A", "#F6C46A"),
  props=[{"type": "note", "x": 0.5, "y": 0.55, "scale": 1.4, "loop": "wobble"}],
  ov=[fact("Diario de Merer: anota cómo su equipo transportaba piedra de Tura a la Gran Pirámide", 4)],
  claims=[F("Los papiros de Merer (Wadi al-Jarf) son el diario de un inspector que llevaba piedra caliza de Tura a la Gran Pirámide", "Pierre Tallet (2017)")],
  tr="zoom", emph=["Merer"])
S("e07", "development", "Cuenta, con la calma de un parte de trabajo, cómo su equipo llevaba bloques de piedra por el Nilo.",
  "egipto", props=[{"type": "stone_block", "x": 0.5, "y": 0.86, "scale": 0.9, "enter": "slide_left"}],
  cam={"move": "pan_left", "amount": 140})
S("e08", "development", "Tu primer trabajo: arrastrar un bloque de unas dos toneladas sobre un trineo de madera.",
  "egipto_obra", leo(x=0.78, action="walk", facing=-1.0, expression="determined", sweat=0.8),
  props=[{"type": "stone_block", "x": 0.42, "y": 0.92, "scale": 0.9}],
  ov=[{"type": "counter", "from": 0, "to": 2, "suffix": " TONELADAS", "at_word": 9, "over": 0.7, "y": 160, "size": 110}],
  claims=[F("Los bloques de la Gran Pirámide pesan de media unas 2-2,5 toneladas", "Encyclopaedia Britannica")],
  emph=["toneladas"])
S("e09", "development", "Truco egipcio: mojar la arena delante del trineo. Con la humedad justa, hace falta la mitad de fuerza.",
  burst("#5CE1E6", "#8FF0F5"),
  props=[{"type": "stone_block", "x": 0.5, "y": 0.62, "scale": 1.1}, {"type": "splash", "x": 0.3, "y": 0.66, "at_word": 2,
         "color": "#5CE1E6"}],
  ov=[fact("Física (2014): con la humedad adecuada, la arena reduce a la mitad la fuerza para arrastrar un trineo", 5)],
  claims=[F("Mojar la arena con la cantidad justa de agua reduce a la mitad la fuerza necesaria para arrastrar un trineo", "Fall et al., Physical Review Letters (2014), Universidad de Ámsterdam")],
  sfx=[{"name": "splash", "at_word": 2}], tr="zoom", emph=["mitad"])
S("e10", "development", "Hay pinturas egipcias que muestran justo eso: un hombre echando agua delante de una estatua gigante.",
  "egipto", leo(x=0.3, action="point_up", expression="surprised"),
  props=[{"type": "splash", "x": 0.62, "y": 0.8, "color": "#5CE1E6", "at_word": 6}],
  claims=[F("En la tumba de Djehutihotep, una pintura muestra a un hombre vertiendo agua delante del trineo de una estatua colosal", "Fall et al. (2014)")])
S("e11", "development", "¿La comida? Pan y cerveza a diario, repartidos desde enormes silos reales. Y, según los arqueólogos, carne con frecuencia.",
  burst("#E8A33A", "#F6C46A"),
  props=[{"type": "food", "kind": "bread", "x": 0.3, "y": 0.55, "scale": 1.3},
         {"type": "amphora", "x": 0.55, "y": 0.55, "scale": 0.7, "label": "CERVEZA", "at_word": 3},
         {"type": "meat", "x": 0.78, "y": 0.55, "scale": 1.2, "at_word": 14}],
  claims=[F("Silos reales repartían grano para pan y cerveza; los obreros comían carne con regularidad", "AERA (Mark Lehner); Zahi Hawass (2010)")],
  sfx=[{"name": "pop", "at_word": 3}, {"name": "pop", "at_word": 14}], tr="slide", emph=["cerveza"])
S("e12", "development", "Era una cerveza espesa y floja: más alimento que bebida de fiesta.", "egipto",
  leo(action="celebrate", expression="laugh"),
  props=[{"type": "amphora", "x": 0.6, "y": 0.75, "scale": 0.5, "label": "CERVEZA"}])
S("e12b", "development", "La jornada empieza con la luz del sol. Las herramientas son de cobre y de piedra: nada de hierro todavía.",
  "egipto_obra", leo(action="dig", expression="determined"),
  claims=[F("En el Reino Antiguo se trabajaba con herramientas de cobre, piedra y madera; el hierro no se generalizó en Egipto hasta mucho después", "Encyclopaedia Britannica")],
  emph=["cobre"])
S("e12c", "development", "Y viven en una auténtica ciudad de trabajadores, con panaderías y cervecerías a escala industrial, junto a la obra.",
  "egipto", leo(x=0.3, action="walk", expression="happy"),
  props=[{"type": "food", "kind": "bread", "x": 0.66, "y": 0.6, "scale": 1.0, "at_word": 9},
         {"type": "amphora", "x": 0.82, "y": 0.72, "scale": 0.45, "label": "CERVEZA", "at_word": 11}],
  claims=[F("Mark Lehner excavó junto a Giza la «ciudad perdida de los constructores de pirámides», con panaderías y almacenes", "AERA (Ancient Egypt Research Associates); Harvard Magazine")],
  tr="slide", emph=["ciudad"])
S("e13", "climax", "El peligro no son los látigos: es el trabajo. Los esqueletos tienen artritis y la espalda destrozada.",
  "egipto_obra", leo(action="sweat", expression="tired", sweat=1.0),
  props=[{"type": "bone", "x": 0.72, "y": 0.55, "scale": 1.0, "loop": "wobble", "at_word": 8}],
  claims=[F("Los esqueletos de los constructores muestran artritis y lesiones en la columna por el trabajo duro", "Adel Okasha, excavación de Giza (2010)")],
  cam={"move": "push_in", "shake": 0.1}, emph=["trabajo", "espalda"])
S("e14", "climax", "Pero aquí viene la sorpresa: muchas fracturas se habían curado bien alineadas, como si alguien las hubiera entablillado.",
  burst("#22B573", "#6EE7A8"),
  props=[{"type": "bone", "x": 0.5, "y": 0.6, "scale": 1.8, "enter": "pop"}],
  ov=[fact("Las fracturas de los obreros soldaron bien alineadas: se las entablillaban", 6)],
  claims=[F("La mayoría de las fracturas soldaron con buena alineación, lo que indica que se entablillaban", "Excavación de las tumbas de Giza (Okasha, 2010)")],
  sfx=[{"name": "sparkle", "at_word": 6}], tr="flash", emph=["sorpresa"])
S("e14b", "climax", "Siglos después, el papiro quirúrgico Edwin Smith ya explicaba cómo inmovilizar fracturas con tablillas.",
  burst("#E8A33A", "#F6C46A"), props=[{"type": "note", "x": 0.5, "y": 0.55, "scale": 1.4, "loop": "wobble"}],
  claims=[F("El papiro Edwin Smith (h. 1600 a. C., copia de un texto más antiguo) describe el tratamiento de fracturas con tablillas", "Encyclopaedia Britannica; Biblioteca de la Academia de Medicina de Nueva York")],
  tr="slide", emph=["Edwin", "Smith"])
S("e15", "climax", "Es decir: había médicos cuidando de los obreros de las pirámides.", "egipto",
  leo(action="celebrate", expression="happy"),
  props=[{"type": "npc", "outfit": "linen", "hair": "#1A1210", "skin": "#A8704A", "x": 0.65, "y": 0.93, "size": 0.85,
          "action": "present", "shirt": "#FFFFFF", "expression": "happy"}])
S("e15b", "climax", "¿Cuánto se tardó? El historiador griego Heródoto, dos mil años después, habló de unos veinte años de obra.",
  "egipto", leo(x=0.3, action="think", expression="surprised"),
  props=[],
  ov=[{"type": "counter", "from": 0, "to": 20, "prefix": "≈", "suffix": " AÑOS DE OBRA", "at_word": 15, "over": 0.6, "y": 175,
       "size": 100}],
  claims=[F("Heródoto atribuyó unos 20 años a la construcción de la Gran Pirámide", "Heródoto, Historias II, 124")],
  emph=["veinte"])
S("e16", "ending", "Veredicto egipcio: si no te aplasta un bloque, podrías aguantar años. Eso sí, con la espalda hecha polvo.",
  burst(), props=[meter(0.76, "EGIPTO · ≈2560 a. C.")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["años"])

# ================================================================== 2 · ROMA
era = "roma"
S("r01", "development", "Segunda parada: Roma, año sesenta y cuatro después de Cristo. La ciudad más grande del mundo conocido.",
  "roma", leo(action="look_up", expression="wow"),
  ov=[label("2 · ROMA · 64 d. C.", "#C9543A")], cam={"move": "pan_up", "amount": 160},
  sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", emph=["Roma"])
S("r02", "development", "Unos historiadores calculan que vivían en ella cerca de un millón de personas; otros, la mitad. Aun así, una barbaridad.",
  "roma", leo(x=0.22, action="shrug", expression="surprised"),
  ov=[{"type": "counter", "from": 0, "to": 1000000, "suffix": " HABITANTES", "prefix": "≈", "at_word": 8, "over": 0.9,
       "y": 160, "size": 96, "sub": "SEGÚN OTROS CÁLCULOS, UNOS 450.000"}],
  claims=[F("Las estimaciones de población de Roma en el siglo I van de unos 450.000 a cerca de un millón", "Glenn Storey, Antiquity (1997); estimaciones clásicas")],
  emph=["millón"])
S("r03", "development", "La mayoría vive en ínsulas: bloques de pisos de cuatro, cinco, seis plantas… y alguno más.",
  "roma", leo(x=0.15, action="point_up", expression="wow"), cam={"move": "pan_up", "amount": 200},
  claims=[F("La mayoría de los romanos vivía en ínsulas, bloques de 4 a 6 plantas, algunos de más", "Catálogos Regionarios (s. IV); historiografía sobre la vivienda romana")])
S("r04", "development", "Sin agua corriente en casa, y pagando un alquiler carísimo. Cuanto más alto, más pobre el inquilino.",
  "roma", leo(action="talk", expression="angry"),
  props=[{"type": "money", "x": 0.7, "y": 0.6, "scale": 1.0, "at_word": 7, "loop": "bob"}],
  claims=[F("Las ínsulas no tenían agua corriente en los pisos; los pisos altos eran los más baratos y precarios", "Juvenal, Sátiras III; historiografía")],
  tr="slide")
S("r04b", "development", "El agua la traían los acueductos: Roma llegó a tener once, algunos con decenas de kilómetros de recorrido.",
  {"type": "rome", "window": 900}, leo(x=0.25, action="point_up", expression="wow"),
  ov=[{"type": "counter", "from": 0, "to": 11, "suffix": " ACUEDUCTOS", "at_word": 7, "over": 0.6, "y": 160, "size": 110}],
  claims=[F("Roma llegó a tener once acueductos principales; Frontino describe los nueve de su época (s. I)", "Frontino, De aquaeductu; historiografía")],
  cam={"move": "pan_up", "amount": 140}, emph=["once"])
S("r04c", "development", "¿Y para comer? Como casi nadie tenía cocina, había bares de comida caliente para llevar en cada esquina: los termopolios.",
  "roma", leo(x=0.3, action="celebrate", expression="happy"),
  props=[{"type": "food", "kind": "bread", "x": 0.62, "y": 0.62, "scale": 1.0, "at_word": 10},
         {"type": "amphora", "x": 0.78, "y": 0.72, "scale": 0.45, "label": "VINO", "at_word": 12}],
  claims=[F("Los termopolios vendían comida y bebida caliente; muchos romanos no cocinaban en casa por riesgo de incendio y falta de espacio", "Arqueología de Pompeya (termopolio de la Regio V, 2020)")],
  tr="slide", emph=["termopolios"])
S("r05", "development", "Con estructuras de madera, braseros y lámparas de aceite, un edificio así ardía con facilidad. Y a veces, directamente, se derrumbaba.",
  "roma_fuego", leo(x=0.22, action="shock", expression="scared"), cam={"move": "push_in", "shake": 0.15},
  claims=[F("Los incendios por braseros y lámparas y los derrumbes de ínsulas eran frecuentes", "Juvenal, Sátiras III; Estrabón")],
  sfx=[{"name": "rumble", "at": 0.2, "gain_db": -8}], emph=["ardía", "derrumbaba"])
S("r06", "development", "Por eso Roma tenía bomberos, los vigiles, con cubos, ganchos y hasta bombas de agua.",
  "roma", leo(action="present", expression="excited"),
  props=[{"type": "npc", "outfit": "police", "hair": "#3A2A20", "x": 0.66, "y": 0.93, "size": 0.85, "action": "walk",
          "shirt": "#C9543A", "hat": "hardhat", "hat_color": "#B0B0B0"}],
  claims=[F("Augusto creó los vigiles, cuerpo de bomberos y guardia nocturna, equipados con cubos, ganchos y bombas", "Suetonio; Digesto")])
S("r07", "climax", "Y aquí está tu mala suerte: en julio del año sesenta y cuatro, un incendio arrasa Roma durante días.",
  "roma_fuego", leo(x=0.2, action="shock", expression="shock"), cam={"move": "punch", "impacts": [1.0], "shake": 0.25},
  ov=[label("JULIO DEL 64 · EL GRAN INCENDIO")],
  claims=[F("El gran incendio de Roma comenzó en julio del año 64 y duró varios días", "Tácito, Anales XV")],
  sfx=[{"name": "boom", "at": 1.0, "gain_db": -6}], tr="flash", emph=["incendio"])
S("r08", "climax", "Según el historiador Tácito, de los catorce barrios de Roma, tres quedaron destruidos por completo y siete muy dañados.",
  burst("#E8392F", "#FF6B5C"),
  ov=[{"type": "counter", "from": 0, "to": 3, "suffix": " DE 14 BARRIOS", "at_word": 11, "over": 0.6, "y": 300,
       "size": 120, "sub": "DESTRUIDOS POR COMPLETO · OTROS 7, MUY DAÑADOS"}],
  props=[{"type": "sparks", "x": 0.5, "y": 0.75, "scale": 1.4}],
  claims=[F("De los 14 distritos de Roma, 3 quedaron arrasados y 7 gravemente dañados", "Tácito, Anales XV, 40")],
  cam={"move": "static"}, emph=["catorce", "tres"])
S("r08b", "development", "Y si sobrevives al fuego, prepárate para no dormir: los carros de mercancías solo podían circular por la ciudad de noche.",
  {"type": "rome", "window": 1020}, leo(x=0.3, action="idle", expression="tired"),
  props=[{"type": "cart", "x": 0.68, "y": 0.9, "scale": 0.9, "enter": "slide_right"}, {"type": "zzz", "x": 0.35, "y": 0.45,
         "crossed": True, "cross_at": 1.0}],
  claims=[F("Una ley de época de César prohibía los carros de carga en Roma durante el día; el poeta Juvenal se quejaba del ruido nocturno", "Lex Iulia Municipalis (45 a. C.); Juvenal, Sátiras III")],
  sfx=[{"name": "rumble", "at": 0.4, "gain_db": -10}], tr="slide", emph=["noche"])
S("r08c", "development", "Lo bueno: por una moneda pequeñísima podías pasar la tarde en las termas, con agua caliente, sauna y hasta biblioteca.",
  {"type": "rome", "window": 1020}, leo(x=0.3, action="celebrate", expression="happy"),
  props=[{"type": "bathhouse", "x": 0.7, "y": 0.86, "scale": 0.9}, {"type": "coin", "x": 0.55, "y": 0.45, "scale": 0.6, "at_word": 4}],
  claims=[F("La entrada a las termas públicas costaba muy poco (un cuadrante) y las grandes termas imperiales incluían bibliotecas", "Encyclopaedia Britannica; historiografía")],
  tr="slide", emph=["termas"])
S("r09", "development", "Vamos a lo cotidiano. ¿Necesitas ir al baño? Letrinas públicas: en fila, sin paredes, charlando con el de al lado.",
  "roma", leo(action="shrug", expression="laugh"),
  props=[{"type": "bathhouse", "x": 0.7, "y": 0.86, "scale": 0.9}],
  claims=[F("Las letrinas públicas romanas eran bancos corridos compartidos, sin separaciones", "Arqueología de Ostia y Pompeya")],
  tr="slide", emph=["letrinas"])
S("r10", "development", "¿Y la orina? No se tiraba: se vendía a las lavanderías, que la usaban para limpiar la ropa.",
  burst("#FFD23F", "#FFE48A"),
  props=[{"type": "amphora", "x": 0.4, "y": 0.6, "scale": 0.9, "color": "#E8C25A"},
         {"type": "money", "x": 0.68, "y": 0.6, "scale": 1.0, "at_word": 6}],
  claims=[F("La orina de las letrinas se vendía a lavanderías (fullonicae) por su amoniaco", "Suetonio, Vespasiano 23; arqueología de Pompeya")],
  sfx=[{"name": "ding", "at_word": 6}], emph=["orina"])
S("r11", "development", "Tanto negocio movía, que el emperador Vespasiano le puso un impuesto.", "roma",
  leo(x=0.22, action="talk", expression="surprised"),
  props=[{"type": "npc", "outfit": "toga", "hair": "#6A6A6A", "x": 0.68, "y": 0.93, "size": 0.9, "action": "smug",
          "shirt": "#7A2A6A", "expression": "smug"}],
  claims=[F("Vespasiano estableció un impuesto sobre la orina recogida en las letrinas", "Suetonio, Vida de Vespasiano 23")])
S("r12", "development", "Cuando su hijo se quejó, le acercó una moneda a la nariz y le preguntó si olía mal.",
  burst("#E6B830", "#FFE48A"),
  props=[{"type": "coin", "x": 0.5, "y": 0.55, "scale": 1.6, "text": "$"}],
  tr="zoom", emph=["olía"])
S("r12b", "development", "Según el historiador Suetonio, de ahí viene la famosa frase: el dinero no huele.",
  burst("#7A2A6A", "#A64A92"),
  props=[{"type": "coin", "x": 0.5, "y": 0.62, "scale": 1.2, "text": "$", "spinning": False}],
  ov=[{"type": "label", "text": "«PECUNIA NON OLET»", "x": 960, "y": 160, "size": 80, "bg": "#E6B830", "color": "#19162B",
       "at_word": 7}],
  claims=[F("Suetonio cuenta que Vespasiano acercó a Tito una moneda del impuesto y le preguntó si olía; de ahí «pecunia non olet»", "Suetonio, Vespasiano 23")],
  tr="zoom", emph=["huele"])
S("r12c", "development", "¿Y los gladiadores? En las películas mueren en cada combate. En realidad eran caros de entrenar, y muchos combates acababan sin muertos.",
  {"type": "rome", "window": 1020}, leo(x=0.3, action="shrug", expression="smug"),
  ov=[{"type": "myth", "text": "SIEMPRE A MUERTE", "stamp": "¡FALSO!", "y": 120, "stamp_at": 2.4}],
  claims=[F("Los gladiadores eran costosos de formar y una parte importante de los combates terminaba sin la muerte de ninguno", "Georges Ville; Encyclopaedia Britannica")],
  sfx=[{"name": "hit", "at": 2.4, "gain_db": -6}], emph=["películas"])
S("r12d", "development", "Si te pones enfermo, los médicos romanos operaban cataratas y usaban pinzas y bisturís, como se ha visto en Pompeya.",
  burst("#5CE1E6", "#8FF0F5"), props=[{"type": "magnifier", "x": 0.5, "y": 0.55, "scale": 1.0, "view": "ice"}],
  claims=[F("En Pompeya se han hallado instrumentos quirúrgicos (bisturís, pinzas, espéculos); los médicos romanos practicaban operaciones de cataratas", "Museo Arqueológico Nacional de Nápoles; Celso, De medicina")],
  tr="zoom", emph=["Pompeya"])
S("r13", "climax", "¿Y cuánto vivía un romano? La esperanza de vida al nacer rondaba los veinticinco años…", "roma",
  leo(action="shock", expression="worried"),
  ov=[{"type": "counter", "from": 0, "to": 25, "suffix": " AÑOS", "at_word": 11, "over": 0.6, "y": 160, "size": 120,
       "sub": "ESPERANZA DE VIDA AL NACER"}],
  claims=[F("La esperanza de vida al nacer en el Imperio romano se estima en unos 25 años", "Tablas de vida modelo (Frier; Scheidel)")],
  emph=["veinticinco"])
S("r14", "climax", "Pero ojo, es una trampa estadística: morían muchísimos bebés. Si pasabas la infancia, lo normal era llegar a los cincuenta o más.",
  burst("#22B573", "#6EE7A8"),
  ov=[{"type": "myth", "text": "A LOS 25 YA ERAS VIEJO", "stamp": "¡FALSO!", "y": 160, "stamp_at": 1.6}],
  props=[{"type": "npc", "outfit": "toga", "hair": "#C8C8C8", "x": 0.5, "y": 0.93, "size": 0.95, "action": "wave",
          "shirt": "#FFFFFF", "expression": "happy", "mustache": True}],
  claims=[F("Descontando la mortalidad infantil, la esperanza de vida de los adultos romanos llegaba a los 50-60 años", "Scheidel, demografía romana")],
  sfx=[{"name": "hit", "at": 1.6, "gain_db": -6}], tr="slide", emph=["trampa", "cincuenta"])
S("r15", "ending", "Veredicto romano: con dinero y lejos de los pisos altos, décadas. Pobre y en un sexto piso de madera… ojo con el fuego.",
  burst(), props=[meter(0.68, "ROMA · 64 d. C.")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["décadas", "fuego"])

S("r16", "ending", "Hasta aquí, vas sobreviviendo bastante bien. Pero lo más peligroso del viaje todavía está por llegar.", "tunel",
  leo(x=0.5, y=0.75, action="float", expression="worried", outfit="casual"), sfx=[{"name": "riser", "at": 0.5, "gain_db": -8}],
  tr="flash", emph=["peligroso"])

# ================================================================== 3 · VIKINGOS
era = "vikingos"
S("v01", "development", "Tercera parada: Escandinavia, hacia el año novecientos. Estás en una aldea vikinga, junto a un fiordo.", "fiordo",
  leo(action="look_up", expression="wow"), ov=[label("3 · ESCANDINAVIA · ≈900", "#3F6E96")],
  props=[{"type": "longship", "x": 0.72, "y": 0.6, "scale": 0.55}], sfx=[{"name": "whoosh", "at": 0.0}], tr="flash",
  cam={"move": "pull_out"}, emph=["vikinga"])
S("v01b", "development", "Sus vecinos los temían por algo: en el año setecientos noventa y tres asaltaron el monasterio de Lindisfarne, en Inglaterra.",
  "mar", props=[{"type": "longship", "x": 0.5, "y": 0.55, "scale": 0.9, "enter": "slide_left"}],
  ov=[label("LINDISFARNE · 793", "#E8392F", at_word=10)],
  claims=[F("El ataque al monasterio de Lindisfarne en 793 se considera el inicio de la era vikinga en Inglaterra", "Crónica anglosajona; Encyclopaedia Britannica")],
  emph=["Lindisfarne"])
S("v02", "development", "Primera decepción: nadie lleva cascos con cuernos. Eso salió del vestuario de una ópera de Wagner, en mil ochocientos setenta y seis.",
  burst("#9D7BFF", "#C4B0FF"), props=[{"type": "horned_helmet", "x": 0.5, "y": 0.62, "scale": 1.4}],
  ov=[{"type": "myth", "text": "CASCOS CON CUERNOS", "stamp": "¡FALSO!", "y": 120, "stamp_at": 1.8}],
  claims=[F("Los cascos vikingos con cuernos se popularizaron con el vestuario de Carl Emil Doepler para El anillo del nibelungo de Wagner (Bayreuth, 1876); los cascos vikingos conocidos no tienen cuernos", "Museo Nacional de Dinamarca; History.com")],
  sfx=[{"name": "hit", "at": 1.8, "gain_db": -6}], tr="zoom", emph=["cuernos"])
S("v03", "development", "El único casco vikingo casi completo que se conoce, el de Gjermundbu, es redondo, de hierro y con protección para los ojos.",
  "fiordo", leo(x=0.3, action="present", expression="smug", helmet="knight"),
  claims=[F("El casco de Gjermundbu (Noruega, siglo X) es el único casco vikingo casi completo hallado: redondo, de hierro, con protección ocular", "Museo de Historia Cultural de Oslo")],
  emph=["Gjermundbu"])
S("v04", "development", "Segunda sorpresa: eran bastante limpios. Los arqueólogos encuentran peines de hueso y asta por todas partes.",
  burst("#5CE1E6", "#8FF0F5"), props=[{"type": "comb", "x": 0.5, "y": 0.55, "scale": 1.5, "loop": "wobble"}],
  claims=[F("Los peines de hueso y asta son de los objetos más frecuentes en yacimientos vikingos", "Universidad de York; Smithsonian Magazine")],
  tr="slide", emph=["peines"])
S("v05", "development", "Y en islandés, el sábado se sigue llamando laugardagur: literalmente, el día de lavarse.",
  "fiordo", leo(action="celebrate", expression="laugh"),
  ov=[{"type": "label", "text": "LAUGARDAGUR = DÍA DE LAVARSE", "x": 960, "y": 120, "size": 64, "bg": "#2B6BE8", "at_word": 7}],
  claims=[F("El sábado en islandés es laugardagur, «día de lavarse»", "Diccionarios de nórdico antiguo e islandés")],
  emph=["lavarse"])
S("v06", "development", "Lo de los peines no era solo coquetería: también servían para quitarse los piojos, que estaban por todas partes.",
  "fiordo", leo(action="sweat", expression="angry"),
  props=[{"type": "comb", "x": 0.7, "y": 0.5, "scale": 0.7, "loop": "wobble"}],
  claims=[F("Los peines servían también para combatir los piojos, omnipresentes en la época", "Museo Nacional de Dinamarca")])
S("v07", "development", "¿Te apuntas a una expedición? Un barco largo navegaba a unos cinco o diez nudos, y con buen viento, bastante más.",
  "mar", props=[{"type": "longship", "x": 0.5, "y": 0.55, "scale": 1.0, "enter": "slide_left"}],
  ov=[{"type": "counter", "from": 0, "to": 10, "prefix": "5-", "suffix": " NUDOS", "at_word": 12, "over": 0.6, "y": 175,
       "size": 100, "sub": "VELOCIDAD MEDIA DE UN BARCO LARGO (RÉPLICAS)"}],
  claims=[F("Las réplicas de barcos vikingos navegan de media a 5-10 nudos y pueden superar los 13 nudos con buen viento", "Museo de Barcos Vikingos de Roskilde (réplicas de Skuldelev)")],
  emph=["nudos"])
S("v07b", "development", "Con esos barcos llegaron muy lejos: a Bagdad por los ríos de Rusia, y a América cinco siglos antes que Colón.",
  "mar", props=[{"type": "longship", "x": 0.5, "y": 0.55, "scale": 0.8}, {"type": "dotted_path", "x": 0.5, "y": 0.35, "at_word": 8}],
  claims=[F("Los vikingos comerciaron hasta el califato abasí por las rutas fluviales rusas y se asentaron hacia el año 1000 en L'Anse aux Meadows (Terranova)", "UNESCO (L'Anse aux Meadows); Encyclopaedia Britannica")],
  emph=["América"])
S("v08", "climax", "Pero cuidado: en las incursiones se moría mucho. Y los esqueletos muestran que pocos vikingos pasaban de los cincuenta años.",
  burst("#E8392F", "#FF6B5C"), props=[{"type": "bone", "x": 0.5, "y": 0.6, "scale": 1.5}],
  ov=[{"type": "counter", "from": 0, "to": 50, "suffix": " AÑOS", "at_word": 18, "over": 0.6, "y": 175, "size": 110,
       "sub": "POCOS LLEGABAN MÁS ALLÁ"}],
  claims=[F("Los vikingos rara vez superaban los 35-40 años y pocos pasaban de los 50", "Museo Nacional de Dinamarca")],
  emph=["cincuenta"])
S("v09", "climax", "Sus cráneos cuentan más: sinusitis, infecciones de oído y caries. Una vida dura, sin médicos de verdad.",
  "fiordo", leo(action="idle", expression="tired"),
  claims=[F("Un estudio con TAC de cráneos vikingos de Varnhem (Suecia) halló sinusitis, infecciones de oído, caries y artrosis", "Discover Magazine (estudio de cráneos de Varnhem)")],
  cam={"move": "push_in", "zoom_to": 1.25, "focus": [0.3, 0.6]}, emph=["caries"])
S("v10", "ending", "Veredicto vikingo: como granjero en tu aldea, años. Si te subes al barco de las incursiones… lanza una moneda.",
  burst(), props=[meter(0.6, "ESCANDINAVIA · ≈900")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["años", "moneda"])

# ================================================================== 4 · PESTE NEGRA
era = "peste"
S("p01", "development", "Cuarta parada, y esta es dura: el año mil trescientos cuarenta y ocho.", "tunel",
  leo(x=0.5, y=0.75, action="float", expression="scared"), sfx=[{"name": "whoosh", "at": 0.0}], tr="flash",
  emph=["dura"])
S("p02", "development", "Llegas a un pueblo de Europa justo cuando llega la peste negra.", "peste",
  leo(action="look_up", expression="worried"), ov=[label("4 · EUROPA · 1348", "#4A4458")],
  cam={"move": "pull_out"}, emph=["peste"])
S("p03", "development", "Entre mil trescientos cuarenta y siete y mil trescientos cincuenta y uno, mató a entre un tercio y la mitad de los europeos.",
  burst("#4A4458", "#6E6680"),
  ov=[{"type": "counter", "from": 0, "to": 50, "prefix": "30-", "suffix": " %", "at_word": 18, "over": 0.8, "y": 300,
       "size": 150, "sub": "DE LA POBLACIÓN DE EUROPA (ESTIMACIONES)"}],
  props=[{"type": "rat", "x": 0.5, "y": 0.8, "scale": 1.4, "enter": "slide_right"}],
  claims=[F("La peste negra (1347-1351) mató a entre un tercio y la mitad de la población europea, con grandes diferencias regionales", "Estimaciones historiográficas; Izdebski et al., Nature Ecology & Evolution (2022)")],
  cam={"move": "static"}, emph=["mitad"])
S("p04", "development", "Durante siglos se discutió qué la causaba. En dos mil once, el ADN de víctimas de un cementerio de Londres lo confirmó.",
  burst("#5CE1E6", "#8FF0F5"),
  props=[{"type": "skull", "x": 0.35, "y": 0.58, "scale": 1.3}, {"type": "magnifier", "x": 0.66, "y": 0.55,
         "scale": 0.8, "view": "bubbles", "at_word": 11}],
  claims=[F("El ADN antiguo de víctimas del cementerio de East Smithfield (Londres) permitió reconstruir el genoma de la bacteria", "Bos et al., Nature (2011)")],
  tr="zoom")
S("p05", "development", "La culpable era una bacteria, Yersinia pestis, que transmitían sobre todo las pulgas de las ratas.",
  "peste", leo(x=0.22, action="shock", expression="scared"),
  props=[{"type": "rat", "x": 0.62, "y": 0.9, "scale": 1.0, "enter": "slide_right"}],
  ov=[fact("Yersinia pestis: bacteria de la peste, transmitida sobre todo por pulgas de roedores", 4)],
  claims=[F("La peste la causa Yersinia pestis, que se transmite sobre todo por picaduras de pulgas infectadas", "OMS, nota descriptiva sobre la peste")],
  emph=["pulgas"])
S("p06", "development", "Si te pica una pulga infectada, en pocos días aparecen los bubones: ganglios hinchados y muy dolorosos.",
  "peste", leo(action="sweat", expression="hot", sweat=0.8),
  claims=[F("Tras 1-7 días de incubación aparecen fiebre y bubones (ganglios inflamados y dolorosos)", "OMS, nota descriptiva sobre la peste")],
  cam={"move": "push_in", "zoom_to": 1.25, "focus": [0.3, 0.6]}, emph=["bubones"])
S("p07", "climax", "Sin antibióticos, la peste bubónica mata a entre el treinta y el sesenta por ciento de los enfermos.",
  burst("#E8392F", "#FF6B5C"),
  ov=[{"type": "counter", "from": 0, "to": 60, "prefix": "30-", "suffix": " %", "at_word": 8, "over": 0.7, "y": 300,
       "size": 150, "sub": "MORTALIDAD SIN TRATAMIENTO (OMS)"}],
  props=[{"type": "thermometer", "x": 0.5, "y": 0.8, "scale": 1.0, "level": 0.9}],
  claims=[F("La peste bubónica sin tratar tiene una letalidad del 30 % al 60 %", "OMS, nota descriptiva sobre la peste")],
  cam={"move": "static"}, emph=["sesenta"])
S("p08", "climax", "Y si pasa a los pulmones y se contagia al toser, sin tratamiento es casi siempre mortal.", "peste",
  leo(action="shock", expression="shock"),
  claims=[F("La peste neumónica, sin tratamiento, es siempre mortal", "OMS, nota descriptiva sobre la peste")],
  cam={"move": "punch", "impacts": [0.4]}, emph=["mortal"])
S("p08b", "development", "Y llega rapidísimo: en solo unos años recorrió Europa entera, de los puertos del Mediterráneo hasta Escandinavia.",
  burst("#4A4458", "#6E6680"), props=[{"type": "dotted_path", "x": 0.5, "y": 0.5}, {"type": "rat", "x": 0.3, "y": 0.75, "loop": "bob"}],
  claims=[F("La peste negra llegó a Europa por los puertos del Mediterráneo en 1347 y alcanzó Escandinavia y Rusia hacia 1349-1351", "Encyclopaedia Britannica")],
  tr="slide")
S("p09", "development", "Los médicos de la época no tenían ni idea. En París culparon a una conjunción de planetas y al aire corrupto.",
  "aldea", props=[{"type": "planet", "x": 0.3, "y": 0.3, "scale": 0.9, "loop": "spin"},
                  {"type": "planet", "x": 0.7, "y": 0.25, "scale": 0.7, "loop": "spin", "color": "#E8A33A"},
                  {"type": "npc", "outfit": "judge", "hair": "#7A7A7A", "x": 0.5, "y": 0.93, "size": 0.9,
                   "action": "think", "expression": "worried"}],
  claims=[F("En 1348 la Facultad de Medicina de París atribuyó la peste a una conjunción de Saturno, Júpiter y Marte y a la corrupción del aire", "Informe de la Facultad de Medicina de París (1348)")],
  tr="slide")
S("p10", "development", "Por cierto, un mito: la famosa máscara de pájaro del médico de la peste aún no existía. Apareció unos trescientos años después.",
  burst("#9D7BFF", "#C4B0FF"),
  ov=[{"type": "myth", "text": "MÁSCARA DE PÁJARO EN 1348", "stamp": "¡FALSO!", "y": 160, "stamp_at": 2.0}],
  props=[{"type": "calendar", "x": 0.5, "y": 0.62, "scale": 1.0, "at_word": 15, "from": 1348, "to": 1619, "over": 1.5}],
  claims=[F("El traje con máscara de pico del médico de la peste se atribuye al siglo XVII (Charles de Lorme, h. 1619)", "Historiografía médica")],
  sfx=[{"name": "hit", "at": 2.0, "gain_db": -6}], emph=["mito"])
S("p10b", "development", "Lo que sí funcionó fue aislar a los recién llegados: en mil trescientos setenta y siete, Ragusa les hizo esperar treinta días.",
  "aldea", leo(x=0.22, action="walk", expression="worried"),
  props=[{"type": "calendar", "x": 0.68, "y": 0.5, "scale": 1.0, "at_word": 17, "from": 1377, "to": 1377}],
  ov=[label("RAGUSA (DUBROVNIK) · 1377", "#2B6BE8")],
  claims=[F("En 1377 Ragusa (Dubrovnik) impuso un aislamiento de 30 días a quienes llegaban de zonas con peste", "Historiografía de la salud pública; Encyclopaedia Britannica")],
  tr="slide", emph=["treinta"])
S("p10c", "development", "Después se amplió a cuarenta días. En italiano, quaranta giorni. De ahí viene nuestra palabra: cuarentena.",
  burst("#5CE1E6", "#8FF0F5"),
  ov=[{"type": "counter", "from": 0, "to": 40, "suffix": " DÍAS", "at_word": 4, "over": 0.6, "y": 220, "size": 150,
       "sub": "QUARANTA GIORNI → CUARENTENA"}],
  claims=[F("La palabra cuarentena procede del italiano quaranta giorni, el aislamiento de 40 días", "RAE; historiografía")],
  cam={"move": "static"}, tr="zoom", emph=["cuarentena"])
S("p11", "development", "Otro mito: que en la Edad Media nadie bebía agua, solo cerveza. Bebían agua… y también mucha cerveza floja.",
  "aldea", leo(action="laugh", expression="laugh"),
  props=[{"type": "amphora", "x": 0.62, "y": 0.8, "scale": 0.5, "color": "#8A6A4A", "label": "CERVEZA"},
         {"type": "splash", "x": 0.78, "y": 0.8, "color": "#5CE1E6", "at_word": 12}],
  ov=[{"type": "myth", "text": "SOLO BEBÍAN CERVEZA", "stamp": "¡FALSO!", "y": 160, "stamp_at": 1.8}],
  claims=[F("Los medievales sí bebían agua; la cerveza era un alimento más, de baja graduación", "Jim Chevallier, «The Great Medieval Water Myth»; historiografía")],
  sfx=[{"name": "hit", "at": 1.8, "gain_db": -6}], tr="slide")
S("p12", "development", "Tu mejor estrategia sería la de los ricos: huir al campo y alejarte de la ciudad. Es justo lo que cuenta Boccaccio en el Decamerón.",
  "aldea", leo(x=0.2, action="walk", expression="determined"),
  props=[{"type": "cart", "x": 0.6, "y": 0.9, "scale": 0.9, "enter": "slide_right"}],
  claims=[F("En el Decamerón (1348-1353), un grupo de jóvenes huye de Florencia al campo para escapar de la peste", "Giovanni Boccaccio, Decamerón")],
  emph=["huir"])
S("p12b", "development", "Y una consecuencia inesperada: tras la epidemia faltaban tantos trabajadores que, en muchos sitios, subieron los salarios.",
  "aldea", leo(x=0.3, action="celebrate", expression="surprised"),
  props=[{"type": "money", "x": 0.68, "y": 0.6, "scale": 1.0, "at_word": 12}],
  claims=[F("La escasez de mano de obra tras la peste negra elevó los salarios en buena parte de Europa occidental", "Encyclopaedia Britannica; historiografía económica")],
  emph=["salarios"])
S("p13", "ending", "Veredicto medieval: casi lanzar una moneda al aire. Si te contagias, malas noticias; si huyes a tiempo, puedes salir adelante.",
  burst(), props=[meter(0.32, "EUROPA · 1348")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["moneda"])

# ================================================================== 5 · TENOCHTITLAN
era = "mexica"
S("t01", "development", "Quinta parada: noviembre de mil quinientos diecinueve. Llegas a Tenochtitlan, la capital mexica, construida sobre un lago.",
  "teno_ancho", leo(x=0.25, y=0.95, action="look_up", expression="wow"), ov=[label("5 · TENOCHTITLAN · 1519", "#2B6BE8")],
  sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", cam={"move": "pull_out"}, emph=["Tenochtitlan"])
S("t02", "development", "Y te quedas con la boca abierta: es una de las ciudades más grandes del mundo, quizá con doscientas mil personas.",
  "teno", leo(x=0.3, y=0.95, action="shock", expression="wow"),
  ov=[{"type": "counter", "from": 0, "to": 200000, "prefix": "75.000-", "suffix": " HABITANTES", "at_word": 15,
       "over": 0.8, "y": 175, "size": 84, "sub": "ESTIMACIONES PARA 1519"}],
  claims=[F("Las estimaciones de población de Tenochtitlan en 1519 van de unas 75.000-100.000 a 200.000 personas", "Encyclopaedia Britannica; Anuario de Historia Regional y de las Fronteras (2022)")],
  emph=["doscientas"])
S("t03", "development", "Más que Madrid o Sevilla en aquella época. Los soldados españoles escribieron que parecía cosa de encantamiento.",
  "teno_ancho", props=[{"type": "npc", "outfit": "knight", "hair": "#3A2A20", "x": 0.25, "y": 0.95, "size": 0.85,
                        "action": "shock", "expression": "wow", "hat": "knight"}],
  claims=[F("Bernal Díaz del Castillo comparó lo que vio con «las cosas de encantamiento que cuentan en el libro de Amadís»", "Bernal Díaz del Castillo, Historia verdadera de la conquista de la Nueva España")],
  tr="slide", emph=["encantamiento"])
S("t04", "development", "La ciudad se cruza por calzadas y canales, y el agua potable llega desde los manantiales de Chapultepec por un acueducto doble.",
  "teno", leo(x=0.3, y=0.95, action="present", expression="happy"),
  props=[{"type": "splash", "x": 0.7, "y": 0.6, "color": "#5CE1E6", "at_word": 14}],
  claims=[F("Un acueducto doble de más de 4 km llevaba agua dulce de Chapultepec a Tenochtitlan", "Encyclopaedia Britannica; EBSCO Research Starters")],
  emph=["acueducto"])
S("t04b", "development", "Y alrededor, las chinampas: huertos construidos sobre el lago, donde se cultivaban maíz, frijol y flores.",
  "teno", leo(x=0.3, y=0.95, action="point_up", expression="wow"),
  claims=[F("Las chinampas eran parcelas de cultivo construidas sobre el lago, muy productivas", "Encyclopaedia Britannica; UNESCO (Xochimilco)")],
  emph=["chinampas"])
S("t05", "development", "En el mercado de Tlatelolco se juntan decenas de miles de personas al día. Y puedes pagar con granos de cacao.",
  burst("#6A3A20", "#9A6A40"), props=[{"type": "cacao", "x": 0.5, "y": 0.6, "scale": 1.6}],
  ov=[fact("Mercado de Tlatelolco: unas 20.000-25.000 personas al día; el cacao servía como moneda", 4)],
  claims=[F("El mercado de Tlatelolco recibía unas 20.000-25.000 personas diarias (los españoles hablaron de hasta 60.000); los granos de cacao se usaban como unidad de cambio", "Jaffary, Osowski y Porter (Routledge); Encyclopaedia Britannica")],
  tr="zoom", emph=["cacao"])
S("t06", "development", "Comparada con muchas ciudades europeas de la época, Tenochtitlan era limpia: había gente encargada de recoger la basura.",
  "teno", leo(x=0.3, y=0.95, action="celebrate", expression="happy"),
  claims=[F("Las crónicas describen calles limpias y trabajadores dedicados a la limpieza de Tenochtitlan", "Crónicas de la conquista; Encyclopaedia Britannica")])
S("t07", "climax", "Pero has llegado en el peor momento. En mil quinientos veinte, entre la guerra y una enfermedad nueva, todo se derrumba.",
  "teno_ancho", cam={"move": "push_in", "shake": 0.15}, sfx=[{"name": "rumble", "at": 0.5, "gain_db": -8}],
  tr="flash", emph=["peor"])
S("t08", "climax", "La viruela, llegada de Europa, mata a muchísima gente que nunca había estado expuesta a ella. Hasta al gobernante Cuitláhuac.",
  burst("#4A4458", "#6E6680"),
  ov=[fact("Epidemia de viruela de 1520: el tlatoani Cuitláhuac murió en diciembre de ese año", 2)],
  claims=[F("La viruela llegó en 1520 y causó una mortalidad enorme en una población sin inmunidad; Cuitláhuac murió de viruela en diciembre de 1520", "Encyclopaedia Britannica")],
  emph=["viruela"])
S("t09", "ending", "Veredicto mexica: en mil quinientos diecinueve, una ciudad asombrosa. Un año después, uno de los momentos más peligrosos del viaje.",
  burst(), props=[meter(0.42, "TENOCHTITLAN · 1519-1520")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["asombrosa", "peligrosos"])

# ================================================================== 6 · LA PRIMERA VUELTA AL MUNDO
era = "elcano"
NAVE = {"type": "sailing_ship", "x": 0.5, "y": 0.55, "scale": 0.9, "flag": "none"}
S("m01", "development", "Mientras tanto, en España: Sanlúcar de Barrameda, veinte de septiembre de mil quinientos diecinueve. Te enrolas con Magallanes.",
  "barco", leo(action="look_up", expression="excited"), ov=[label("6 · SANLÚCAR · 1519", "#C9543A")],
  sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", cam={"move": "pull_out"}, emph=["Magallanes"])
S("m02", "development", "Cinco naos y unos doscientos cuarenta hombres van a buscar las islas de las Especias navegando hacia el oeste.",
  "mar", props=[dict(NAVE, x=0.3, scale=0.6), dict(NAVE, x=0.55, scale=0.5, seed=1), dict(NAVE, x=0.78, scale=0.45)],
  ov=[{"type": "counter", "from": 0, "to": 239, "prefix": "≈", "suffix": " HOMBRES", "at_word": 4, "over": 0.7, "y": 175,
       "size": 100, "sub": "5 NAOS · ENTRE 239 Y 265 SEGÚN LAS FUENTES"}],
  claims=[F("La expedición zarpó de Sanlúcar el 20 de septiembre de 1519 con cinco naos y unos 239 hombres (las fuentes dan entre 239 y 265)", "Armada Española, Cuadernos del Instituto de Historia y Cultura Naval")],
  emph=["Especias"])
S("m03", "development", "Tras cruzar el estrecho que hoy lleva su nombre, entran en un océano tan tranquilo que lo bautizan Pacífico.",
  "mar", props=[dict(NAVE, enter="slide_left")],
  claims=[F("Magallanes cruzó en 1520 el estrecho que lleva su nombre y llamó «Pacífico» al océano por su calma", "Encyclopaedia Britannica")],
  emph=["Pacífico"])
S("m04", "climax", "Pero nadie imaginaba lo enorme que era: pasan más de tres meses sin pisar tierra y sin comida fresca.",
  "barco_noche", leo(action="idle", expression="worried"),
  ov=[{"type": "counter", "from": 0, "to": 3, "prefix": "+", "suffix": " MESES", "at_word": 11, "over": 0.6, "y": 175,
       "size": 110, "sub": "CRUZANDO EL PACÍFICO SIN TOCAR TIERRA"}],
  claims=[F("La travesía del Pacífico duró más de tres meses sin avituallamiento", "Antonio Pigafetta, Relación del primer viaje alrededor del mundo")],
  emph=["tres"])
S("m05", "climax", "El cronista Antonio Pigafetta lo apuntó todo: comían galleta hecha polvo, llena de gusanos, y cuero ablandado en agua de mar.",
  burst("#C9A060", "#E2C27A"), props=[{"type": "food", "kind": "bread", "x": 0.35, "y": 0.6, "scale": 1.2},
                                       {"type": "worm", "x": 0.42, "y": 0.5, "scale": 0.6, "at_word": 11}],
  claims=[F("Pigafetta cuenta que comían galleta reducida a polvo y agusanada, cuero de las vergas ablandado en el mar y serrín", "Antonio Pigafetta, Relación del primer viaje alrededor del mundo")],
  tr="zoom", emph=["Pigafetta", "cuero"])
S("m06", "climax", "Y una rata se vendía a medio ducado. Aun así, no había para todos.",
  "barco_noche", leo(action="shock", expression="angry"),
  props=[{"type": "rat", "x": 0.62, "y": 0.9, "enter": "slide_right"}, {"type": "coin", "x": 0.75, "y": 0.45, "scale": 0.6, "at_word": 6}],
  claims=[F("Según Pigafetta, las ratas llegaron a venderse a medio ducado cada una", "Antonio Pigafetta, Relación del primer viaje alrededor del mundo")],
  emph=["rata"])
S("m07", "climax", "Y llega el escorbuto: a muchos se les hinchaban tanto las encías que no podían comer.",
  "barco_noche", leo(action="idle", expression="tired"), cam={"move": "push_in", "zoom_to": 1.25, "focus": [0.3, 0.6]},
  claims=[F("Pigafetta describe cómo a muchos les crecían las encías hasta impedirles comer, y murieron", "Antonio Pigafetta, Relación del primer viaje alrededor del mundo")],
  emph=["encías"])
S("m08", "climax", "En abril de mil quinientos veintiuno, Magallanes muere en combate en la isla de Mactán, en las actuales Filipinas.",
  burst("#4A4458", "#6E6680"), ov=[label("MACTÁN · 27 DE ABRIL DE 1521", "#4A4458")],
  claims=[F("Magallanes murió el 27 de abril de 1521 en la batalla de Mactán (Filipinas)", "Encyclopaedia Britannica")],
  emph=["Magallanes"])
S("m09", "development", "Al final, Juan Sebastián Elcano, un marino de Guetaria, toma el mando de la nao Victoria y vuelve por el otro lado del mundo.",
  "barco", props=[{"type": "npc", "outfit": "sailor", "hair": "#3A2A20", "x": 0.35, "y": 0.93, "size": 0.95,
                   "action": "point_up", "expression": "determined", "mustache": True}],
  ov=[label("JUAN SEBASTIÁN ELCANO", "#C9543A", at_word=3)],
  claims=[F("Elcano, natural de Guetaria, regresó al mando de la Victoria por el océano Índico y el cabo de Buena Esperanza", "Encyclopaedia Britannica; Armada Española")],
  emph=["Elcano"])
S("m10", "climax", "El seis de septiembre de mil quinientos veintidós, la Victoria llega a Sanlúcar con solo dieciocho hombres.",
  "mar", props=[dict(NAVE, enter="slide_right")],
  ov=[{"type": "counter", "from": 239, "to": 18, "suffix": " HOMBRES", "at_word": 15, "over": 1.0, "y": 175, "size": 120,
       "sub": "COMPLETARON LA VUELTA EN LA VICTORIA"}],
  claims=[F("El 6 de septiembre de 1522 la Victoria llegó a Sanlúcar con 18 hombres", "Armada Española; National Geographic")],
  sfx=[{"name": "ding", "at_word": 15}], emph=["dieciocho"])
S("m11", "development", "Y un detalle alucinante: al llegar a Cabo Verde descubrieron que en su diario les faltaba un día. Lo habían perdido dando la vuelta al mundo.",
  burst("#5CE1E6", "#8FF0F5"), props=[{"type": "calendar", "x": 0.5, "y": 0.55, "scale": 1.2, "from": 1522, "to": 1522,
                                        "label": "¿MIÉRCOLES?"}, {"type": "question", "x": 0.72, "y": 0.4, "at_word": 15}],
  claims=[F("En Cabo Verde (1522) comprobaron que su cuenta de días iba un día por detrás: lo habían «perdido» al circunnavegar hacia el oeste", "Antonio Pigafetta, Relación del primer viaje alrededor del mundo")],
  tr="zoom", emph=["día"])
S("m12", "ending", "Veredicto de la vuelta al mundo: una hazaña histórica… pero de cada trece que salieron, solo uno la completó en la Victoria.",
  burst(), props=[meter(0.35, "PRIMERA VUELTA AL MUNDO · 1519-1522")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["trece"])

# ================================================================== 7 · PIRATAS
era = "piratas"
S("b01", "development", "Séptima parada: el mar Caribe, hacia mil setecientos veinte, la edad de oro de la piratería.", "mar",
  props=[{"type": "sailing_ship", "x": 0.5, "y": 0.55, "scale": 1.0, "enter": "slide_right"}],
  ov=[label("7 · CARIBE · ≈1720", "#1A1A22")], sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", emph=["piratería"])
S("b01b", "development", "Muchos piratas eran antiguos marineros mercantes, hartos de pagas miserables y castigos brutales a bordo.",
  "barco", leo(action="talk", expression="angry"),
  claims=[F("Gran parte de las tripulaciones piratas procedía de la marina mercante, huyendo de malas pagas y castigos", "Marcus Rediker, Villains of All Nations (2004)")],
  emph=["castigos"])
S("b02", "development", "Te enrolas en un barco pirata. Y te sorprenderá: los piratas tenían normas escritas.", "barco",
  leo(action="shock", expression="surprised"), props=[{"type": "note", "x": 0.68, "y": 0.5, "scale": 1.0, "at_word": 11}],
  claims=[F("Las tripulaciones piratas firmaban «artículos»: normas escritas de reparto y disciplina", "Charles Johnson, Historia general de los piratas (1724)")],
  emph=["normas"])
S("b03", "development", "Las llamaban artículos: cómo repartir el botín, qué estaba prohibido… y hasta un seguro por heridas.",
  burst("#1A1A22", "#3A3A48"), props=[{"type": "note", "x": 0.5, "y": 0.55, "scale": 1.5, "loop": "wobble"}],
  tr="zoom", emph=["seguro"])
S("b04", "development", "Ya en tiempos del bucanero Henry Morgan, el cronista Exquemelin contó que perder el brazo derecho se pagaba con seiscientas piezas de a ocho.",
  burst("#E6B830", "#FFE48A"),
  props=[{"type": "coin", "x": 0.5, "y": 0.5, "scale": 1.5}],
  ov=[{"type": "counter", "from": 0, "to": 600, "suffix": " PIEZAS DE A OCHO", "at_word": 19, "over": 0.8, "y": 160,
       "size": 90, "sub": "POR PERDER EL BRAZO DERECHO"}],
  claims=[F("Según Exquemelin (1678), los bucaneros pagaban 600 piezas de a ocho por perder el brazo derecho", "Alexandre O. Exquemelin, Piratas de América (1678)")],
  emph=["seiscientas"])
S("b05", "development", "Un ojo o un dedo, cien. Era casi una mutua… con espadas.", "barco",
  leo(action="laugh", expression="laugh"), props=[{"type": "coin", "x": 0.7, "y": 0.45, "scale": 0.8}],
  claims=[F("Un ojo o un dedo se compensaban con 100 piezas de a ocho", "Exquemelin (1678)")], tr="slide")
S("b05b", "development", "Y no esperes una carrera larga: Barbanegra, el pirata más famoso, solo estuvo activo un par de años. Murió en combate en mil setecientos dieciocho.",
  "mar", props=[{"type": "sailing_ship", "x": 0.5, "y": 0.55, "scale": 0.9}],
  ov=[label("BARBANEGRA · †1718", "#1A1A22")],
  claims=[F("Barbanegra (Edward Teach) actuó como pirata hacia 1716-1718 y murió en combate en Ocracoke en noviembre de 1718", "Encyclopaedia Britannica")],
  sfx=[{"name": "boom", "at_word": 18, "gain_db": -8}], emph=["Barbanegra"])
S("b06", "climax", "Pero tu mayor enemigo no es la Armada. Es una enfermedad: el escorbuto.", "barco_noche",
  leo(action="shock", expression="scared"), cam={"move": "punch", "impacts": [2.0]},
  sfx=[{"name": "hit", "at": 2.0, "gain_db": -6}], emph=["escorbuto"])
S("b07", "development", "Pasas semanas comiendo galleta seca y carne salada. Sin fruta ni verdura fresca, te falta vitamina C.",
  burst("#C9A060", "#E2C27A"),
  props=[{"type": "food", "kind": "bread", "x": 0.35, "y": 0.55, "scale": 1.2},
         {"type": "meat", "x": 0.65, "y": 0.55, "scale": 1.2},
         {"type": "lemon", "x": 0.5, "y": 0.3, "scale": 0.8, "crossed": True, "cross_at": 1.5, "at_word": 10}],
  claims=[F("El escorbuto lo causa la falta de vitamina C, ausente en la galleta y la carne salada", "Encyclopaedia Britannica; NIH")],
  emph=["vitamina"])
S("b07b", "development", "Y la galleta suele traer premio: gorgojos. Muchos marineros comían a oscuras para no verlos.",
  "barco_noche", leo(action="shock", expression="angry"),
  props=[{"type": "food", "kind": "bread", "x": 0.66, "y": 0.6, "scale": 1.0}],
  claims=[F("La galleta de barco se infestaba a menudo de gorgojos y larvas", "Royal Museums Greenwich")], tr="slide")
S("b08", "development", "Primero llega el cansancio. Luego te sangran las encías, se te aflojan los dientes… y se te reabren heridas viejas.",
  "barco", leo(action="idle", expression="tired"), cam={"move": "push_in", "zoom_to": 1.25, "focus": [0.3, 0.6]},
  claims=[F("Síntomas del escorbuto: cansancio, encías sangrantes, pérdida de dientes y reapertura de heridas cicatrizadas", "NIH; historia de la medicina naval")],
  emph=["encías", "heridas"])
S("b09", "climax", "Según algunas estimaciones, entre mil quinientos y mil ochocientos el escorbuto mató a unos dos millones de marineros. Más que las batallas.",
  burst("#E8392F", "#FF6B5C"),
  ov=[{"type": "counter", "from": 0, "to": 2000000, "prefix": "≈", "suffix": " MARINEROS", "at_word": 14, "over": 0.9,
       "y": 300, "size": 110, "sub": "MUERTOS POR ESCORBUTO, 1500-1800 (ESTIMACIÓN)"}],
  props=[{"type": "lemon", "x": 0.5, "y": 0.72, "scale": 1.3, "crossed": True, "cross_at": 0.8, "cross_r": 130}],
  claims=[F("Se estima que el escorbuto mató a unos 2 millones de marineros entre 1500 y 1800, más que los combates", "Estimaciones historiográficas recogidas por Popular Science y el Royal College of Physicians of Edinburgh")],
  cam={"move": "static"}, emph=["millones"])
S("b10", "development", "La solución llegó en mil setecientos cuarenta y siete. El médico James Lind probó seis remedios con doce marineros enfermos.",
  "barco", props=[{"type": "npc", "outfit": "victorian", "hair": "#E8E0D0", "x": 0.35, "y": 0.93, "size": 0.9,
                   "action": "present", "expression": "determined"}],
  ov=[label("JAMES LIND · 1747", "#2B6BE8")],
  claims=[F("En 1747, a bordo del HMS Salisbury, James Lind dividió a 12 marineros con escorbuto en 6 parejas con remedios distintos", "James Lind, Tratado del escorbuto (1753); James Lind Library")],
  tr="slide", emph=["Lind"])
S("b11", "development", "Solo se curaron los que comieron naranjas y limones. Es uno de los primeros ensayos clínicos controlados de la historia.",
  burst("#FFE13A", "#FFF09A"),
  props=[{"type": "lemon", "x": 0.4, "y": 0.55, "scale": 1.4}, {"type": "orange", "x": 0.62, "y": 0.55,
         "scale": 1.3}],
  ov=[fact("El ensayo de Lind se considera uno de los primeros ensayos clínicos controlados", 10)],
  claims=[F("Solo mejoraron rápidamente los marineros que tomaron cítricos; se considera uno de los primeros ensayos clínicos", "James Lind Library; Royal College of Physicians of Edinburgh")],
  sfx=[{"name": "sparkle", "at": 0.6}], tr="zoom", emph=["limones"])
S("b12", "development", "Aunque la Marina británica tardó casi cincuenta años en dar zumo de limón a sus marineros.", "barco",
  leo(action="shrug", expression="angry"),
  claims=[F("La Marina británica no introdujo raciones de cítricos hasta 1795", "Royal College of Physicians of Edinburgh; USNI")])
S("b12b", "development", "Por eso a los marineros británicos los llamaron «limeys»: por las limas que acabaron llevando a bordo.",
  "barco", leo(action="laugh", expression="laugh"), props=[{"type": "lemon", "x": 0.68, "y": 0.5, "scale": 1.0, "loop": "bob"}],
  claims=[F("El apodo «limey» para los marineros británicos procede de las raciones de cítricos (limas) contra el escorbuto", "Oxford English Dictionary; Royal Museums Greenwich")],
  emph=["limeys"])
S("b13", "ending", "Veredicto pirata: con limones y sin abordajes, meses. Sin fruta, en uno o dos meses el escorbuto te deja fuera de combate.",
  burst(), props=[meter(0.5, "CARIBE · ≈1720")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["meses"])

# ================================================================== 5 · LONDRES
era = "londres"
S("l01", "development", "Octava parada: Londres, mil ochocientos cincuenta y cuatro, la capital del mundo industrial.", "londres",
  leo(action="look_up", expression="dizzy"), ov=[label("8 · LONDRES · 1854", "#5C4E3E")],
  sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", cam={"move": "pull_out"}, emph=["Londres"])
S("l02", "development", "Humo de carbón por todas partes, fábricas sin descanso y calles llenas de barro… y de cosas peores.",
  "londres_humo", leo(x=0.22, action="sweat", expression="angry"), cam={"move": "pan_right", "amount": 160})
S("l03", "development", "Si eres niño, quizá trabajes en una fábrica. Una ley de mil ochocientos treinta y tres lo prohibió a los menores de nueve años.",
  "londres", leo(scale=0.65, action="sweat", expression="tired"),
  ov=[fact("Ley de Fábricas de 1833: prohibido el trabajo textil a menores de 9 años", 5)],
  claims=[F("La Ley de Fábricas de 1833 prohibió emplear a menores de 9 años en fábricas textiles", "Factory Act 1833, Parlamento británico")],
  emph=["nueve"])
S("l04", "development", "Y limitó a nueve horas al día la jornada de los niños de nueve a trece. Antes, podían ser muchas más.",
  burst("#5C4E3E", "#8A7460"), props=[{"type": "clock", "x": 0.5, "y": 0.55, "scale": 1.2}],
  ov=[{"type": "counter", "from": 0, "to": 9, "suffix": " HORAS AL DÍA", "at_word": 3, "over": 0.6, "y": 160, "size": 110,
       "sub": "NIÑOS DE 9 A 13 AÑOS"}],
  claims=[F("La misma ley limitó a 9 horas diarias el trabajo de los niños de 9 a 13 años", "Factory Act 1833")],
  tr="zoom")
S("l05", "development", "La esperanza de vida al nacer en Inglaterra rondaba los cuarenta años, y más de uno de cada cuatro niños moría antes de los cinco.",
  "londres", leo(action="idle", expression="worried"),
  ov=[{"type": "counter", "from": 0, "to": 40, "prefix": "≈", "suffix": " AÑOS", "at_word": 10, "over": 0.6, "y": 160,
       "size": 110, "sub": "ESPERANZA DE VIDA AL NACER (INGLATERRA, 1850)"}],
  claims=[F("En 1850 la esperanza de vida al nacer en Inglaterra y Gales era de unos 40-42 años y más del 25 % de los niños moría antes de los 5", "Estadísticas históricas de Inglaterra y Gales (Office for National Statistics; Cambridge Group)")],
  emph=["cuarenta"])
S("l05b", "development", "Y ojo con lo que comes: a menudo el pan llevaba alumbre para parecer más blanco, y la leche venía aguada.",
  burst("#F2EAD6", "#FFF8E8"), props=[{"type": "food", "kind": "bread", "x": 0.4, "y": 0.55, "scale": 1.3},
                                       {"type": "food", "kind": "water", "x": 0.65, "y": 0.55, "scale": 1.1, "at_word": 17}],
  claims=[F("En la Inglaterra victoriana era habitual adulterar el pan con alumbre y aguar la leche; lo denunció Arthur Hassall en The Lancet (1851-1854)", "English Heritage; The Lancet")],
  tr="slide", emph=["alumbre"])
S("l06", "climax", "Y en agosto llega el gran peligro: el cólera, una diarrea tan brutal que puede matar en cuestión de horas.",
  "londres_humo", leo(action="shock", expression="shock"), cam={"move": "punch", "impacts": [1.4]},
  claims=[F("El cólera provoca una diarrea acuosa grave que puede matar en horas si no se trata", "OMS, nota descriptiva sobre el cólera")],
  sfx=[{"name": "hit", "at": 1.4, "gain_db": -6}], emph=["cólera", "horas"])
S("l07", "climax", "En el barrio del Soho, a pocas calles de distancia, hay más de quinientas muertes en solo diez días.",
  burst("#E8392F", "#FF6B5C"),
  ov=[{"type": "counter", "from": 0, "to": 500, "prefix": "+", "suffix": " MUERTES", "at_word": 11, "over": 0.7, "y": 300,
       "size": 140, "sub": "EN 10 DÍAS · SOHO, 1854"}],
  props=[{"type": "water_pump", "x": 0.5, "y": 0.98, "scale": 0.8, "enter": "rise"}],
  claims=[F("Snow contabilizó más de 500 muertes por cólera en diez días en un radio de unas 250 yardas en Soho", "John Snow, Sobre el modo de transmisión del cólera (1855)")],
  cam={"move": "static"}, emph=["quinientas"])
S("l08", "development", "Casi todos los médicos creen que el cólera se contagia por el aire sucio, el miasma.", "londres_humo",
  props=[{"type": "npc", "outfit": "victorian", "hair": "#4A4A4A", "x": 0.35, "y": 0.93, "size": 0.9, "action": "talk",
          "expression": "smug", "hat": "fedora"}],
  claims=[F("La teoría dominante atribuía el cólera al miasma, el aire viciado", "Historiografía médica")], tr="slide")
S("l09", "development", "Pero un médico, John Snow, no se lo cree. Marca en un mapa cada muerte, casa por casa.",
  "londres", leo(x=0.22, action="think", expression="determined"),
  props=[{"type": "dotted_path", "x": 0.5, "y": 0.6, "at_word": 10}],
  ov=[label("JOHN SNOW", "#2B6BE8", at_word=4)], tr="slide", emph=["Snow"])
S("l09b", "development", "Y ve que casi todas rodean una bomba de agua: la de Broad Street.",
  "londres", leo(x=0.22, action="point_up", expression="wow"),
  props=[{"type": "water_pump", "x": 0.66, "y": 0.97, "scale": 0.9, "at_word": 6}],
  ov=[label("BROAD STREET", "#2B6BE8", at_word=9)],
  claims=[F("John Snow cartografió las muertes y vio que se concentraban alrededor de la bomba de Broad Street", "John Snow (1855); CDC")],
  sfx=[{"name": "ding", "at_word": 9}], emph=["bomba"])
S("l10", "climax", "Convence a las autoridades y quitan la manivela de la bomba. Nadie más puede beber de ella.", "londres",
  props=[{"type": "water_pump", "x": 0.55, "y": 0.97, "scale": 1.0, "handle": False, "enter": "none"}],
  ov=[fact("8 de septiembre de 1854: retiran la manivela de la bomba de Broad Street", 2)],
  claims=[F("El 8 de septiembre de 1854 se retiró la manivela de la bomba de Broad Street", "CDC, MMWR (2004)")],
  cam={"move": "push_in", "zoom_to": 1.2, "focus": [0.55, 0.75]}, sfx=[{"name": "crack", "at_word": 6}],
  emph=["manivela"])
S("l11", "development", "Algunos historiadores creen que la epidemia ya iba a menos. Pero Snow había demostrado algo enorme: el cólera viaja por el agua.",
  burst("#5CE1E6", "#8FF0F5"), props=[{"type": "splash", "x": 0.5, "y": 0.6, "color": "#5CE1E6", "at_word": 18}],
  ov=[fact("El brote ya remitía cuando se quitó la manivela; aun así, Snow probó el contagio por agua", 1)],
  claims=[F("El brote ya estaba remitiendo cuando se retiró la manivela, pero Snow aportó pruebas del contagio por agua", "JSTOR Daily; historiografía de la epidemiología")],
  tr="zoom", emph=["agua"])
S("l11b", "development", "Al año siguiente lo remató: los vecinos que bebían agua sacada del Támesis río abajo, contaminada, morían muchas veces más que los demás.",
  "londres", leo(x=0.25, action="present", expression="determined"),
  props=[{"type": "splash", "x": 0.6, "y": 0.75, "color": "#7A6A3A", "at_word": 9},
         {"type": "splash", "x": 0.78, "y": 0.75, "color": "#5CE1E6", "at_word": 14}],
  claims=[F("Snow comparó a los clientes de dos compañías de aguas: los de Southwark & Vauxhall (agua del Támesis contaminada) tuvieron muchas más muertes que los de Lambeth", "John Snow, Sobre el modo de transmisión del cólera (1855)")],
  emph=["contaminada"])
S("l12", "development", "Cuatro años después llega el Gran Hedor: el Támesis apesta tanto que el Parlamento aprueba la gran red de alcantarillas de Londres.",
  "londres_humo", leo(action="sweat", expression="angry"),
  ov=[label("1858 · EL GRAN HEDOR", "#5C4E3E")],
  claims=[F("Tras el «Gran Hedor» de 1858, el Parlamento aprobó la red de alcantarillado de Joseph Bazalgette", "UK Parliament; historiografía")],
  emph=["Hedor"])
S("l12b", "development", "Aquel verano fue tan caluroso que en el Parlamento colgaron cortinas empapadas en cal para aguantar el olor.",
  "londres_humo", leo(action="laugh", expression="laugh"),
  claims=[F("Durante el Gran Hedor de 1858 se colgaron cortinas empapadas en cloruro de cal en el Parlamento", "UK Parliament (historia del edificio)")])
S("l13", "ending", "Veredicto londinense: si hierves el agua y no te toca la fábrica de niño, años. Si bebes de la bomba equivocada… quizá horas.",
  burst(), props=[meter(0.72, "LONDRES · 1854")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["años", "horas"])

# ================================================================== 8 · PANAMÁ
era = "panama"
S("c01", "development", "Novena y última parada: Panamá, mil ochocientos ochenta y cinco. Los franceses intentan abrir un canal entre dos océanos.",
  "canal", leo(action="look_up", expression="hot", sweat=0.5), ov=[label("9 · PANAMÁ · 1885", "#22B573")],
  sfx=[{"name": "whoosh", "at": 0.0}], tr="flash", cam={"move": "pull_out"}, emph=["Panamá"])
S("c02", "development", "Lo dirige Ferdinand de Lesseps, el mismo que había abierto el canal de Suez. Parece imposible que salga mal.",
  "canal", props=[{"type": "npc", "outfit": "victorian", "hair": "#E8E0D0", "x": 0.35, "y": 0.93, "size": 0.9,
                   "action": "smug", "expression": "smug", "mustache": True, "hat": "fedora"}],
  claims=[F("Ferdinand de Lesseps, constructor del canal de Suez, dirigió el intento francés en Panamá desde 1881", "Encyclopaedia Britannica")],
  emph=["Suez"])
S("c03", "development", "Pero aquí el enemigo no es la roca. Es la lluvia, la selva… y un bicho diminuto.", "canal_lluvia",
  leo(action="sweat", expression="worried", sweat=0.9),
  props=[{"type": "mosquito", "x": 0.68, "y": 0.4, "at_word": 13, "scale": 1.2}],
  sfx=[{"name": "boing", "at_word": 13, "gain_db": -8}], emph=["diminuto"])
S("c04", "climax", "La fiebre amarilla y la malaria matan a miles de trabajadores. En la etapa francesa murieron más de veintidós mil personas.",
  burst("#E8392F", "#FF6B5C"),
  ov=[{"type": "counter", "from": 0, "to": 22000, "prefix": "+", "suffix": " MUERTOS", "at_word": 15, "over": 0.8, "y": 300,
       "size": 130, "sub": "OBRAS FRANCESAS DEL CANAL, 1881-1889"}],
  props=[{"type": "mosquito", "x": 0.5, "y": 0.72, "swarm": 12}],
  claims=[F("Más de 22.000 trabajadores murieron durante el intento francés (1881-1889), muchos de malaria y fiebre amarilla", "Linda Hall Library; Smithsonian Libraries")],
  cam={"move": "static"}, emph=["veintidós"])
S("c04b", "development", "Y lo peor: los médicos no saben cómo se contagia. Muchos creen, otra vez, que es culpa del aire malo.",
  "canal_lluvia", leo(action="shrug", expression="worried"), tr="slide")
S("c05", "development", "En los hospitales ponen las patas de las camas en cuencos de agua para frenar a las hormigas.",
  "canal", props=[{"type": "mosquito_net", "x": 0.6, "y": 0.8, "scale": 0.8}, {"type": "mosquito", "x": 0.4, "y": 0.4, "swarm": 6}],
  claims=[F("En los hospitales franceses se ponían las patas de las camas en recipientes con agua contra las hormigas, lo que creaba criaderos de mosquitos", "Smithsonian Libraries, «Make the Dirt Fly»; historiografía")],
  tr="slide", emph=["agua"])
S("c06", "climax", "Sin saberlo, estaban criando mosquitos justo al lado de los enfermos.", "canal_lluvia",
  props=[{"type": "mosquito", "x": 0.5, "y": 0.45, "swarm": 10}], cam={"move": "push_in", "zoom_to": 1.2},
  emph=["mosquitos"])
S("c07", "development", "Ya en mil ochocientos ochenta y uno, un médico cubano, Carlos Finlay, había propuesto que la fiebre amarilla la transmitía un mosquito.",
  burst("#2B6BE8", "#5C8FE6"),
  props=[{"type": "npc", "outfit": "victorian", "hair": "#2A2A2A", "x": 0.35, "y": 0.93, "size": 0.95, "action": "present",
          "expression": "determined", "mustache": True}, {"type": "mosquito", "x": 0.72, "y": 0.45, "scale": 1.3}],
  ov=[label("CARLOS FINLAY · CUBA · 1881", "#E8392F")],
  claims=[F("En 1881 Carlos J. Finlay propuso que el mosquito transmitía la fiebre amarilla", "Linda Hall Library; Encyclopaedia Britannica")],
  tr="zoom", emph=["Finlay"])
S("c08", "development", "Casi nadie le hizo caso. Hasta que en mil novecientos el equipo de Walter Reed lo confirmó en Cuba.",
  burst("#22B573", "#6EE7A8"), ov=[fact("Walter Reed confirmó en Cuba (1900) la transmisión de la fiebre amarilla por mosquitos", 6)],
  claims=[F("En 1900 la comisión de Walter Reed confirmó en Cuba la hipótesis de Finlay", "Linda Hall Library; Gavi")],
  emph=["Reed"])
S("c09", "development", "Cuando los estadounidenses retomaron la obra, el médico William Gorgas declaró la guerra a los mosquitos: secar charcos, mosquiteras y fumigación.",
  "canal", props=[{"type": "npc", "outfit": "police", "hair": "#C8C8C8", "x": 0.3, "y": 0.93, "size": 0.9, "action": "point_up",
                   "expression": "determined", "mustache": True},
                  {"type": "mosquito_net", "x": 0.72, "y": 0.8, "scale": 0.7, "at_word": 17}],
  claims=[F("Desde 1904, William Gorgas eliminó aguas estancadas, instaló mosquiteras y fumigó para controlar los mosquitos", "Linda Hall Library; EBSCO Research Starters")],
  emph=["Gorgas"])
S("c10", "climax", "A finales de mil novecientos cinco, la fiebre amarilla había desaparecido de la zona del canal.",
  burst("#22B573", "#6EE7A8"), props=[{"type": "mosquito", "x": 0.5, "y": 0.55, "scale": 1.6, "crossed": True, "cross_at": 1.0}],
  claims=[F("A finales de 1905 ya no se registraban muertes por fiebre amarilla en Panamá", "Linda Hall Library")],
  sfx=[{"name": "sparkle", "at": 1.0}], cam={"move": "static"}, emph=["desaparecido"])
S("c11", "ending", "Veredicto panameño: con los franceses, en temporada de lluvias, quizá semanas. Con mosquitero y unos años más tarde, toda una carrera.",
  burst(), props=[meter(0.38, "PANAMÁ · 1885")], cam={"move": "static"},
  sfx=[{"name": "ding", "at": 1.0}], tr="zoom", emph=["semanas"])

# ================================================================== FINAL
era = "intro"
S("f01", "climax", "Hagamos el recuento. La época más peligrosa de las nueve es la peste negra: casi una moneda al aire.",
  burst("#4A4458", "#6E6680"), props=[meter(0.32, "1.º MÁS PELIGROSA: PESTE NEGRA")], cam={"move": "static"},
  tr="flash", emph=["peste"])
S("f02", "climax", "Muy cerca, la vuelta al mundo de Elcano y el canal de Panamá de los franceses. Y después, Tenochtitlan en mil quinientos veinte.",
  burst("#1A1A22", "#3A3A48"), props=[meter(0.35, "2.º VUELTA AL MUNDO · 3.º PANAMÁ 1885")], cam={"move": "static"},
  emph=["Elcano", "Panamá"])
S("f02a", "climax", "En medio quedan el escorbuto pirata, los vikingos de las incursiones y los incendios de Roma.", "fiordo",
  leo(x=0.3, action="shrug", expression="surprised", outfit="casual"),
  props=[{"type": "longship", "x": 0.7, "y": 0.6, "scale": 0.5}])
S("f02b", "climax", "Y las más llevaderas, con dolor de espalda incluido: Egipto y el Londres de John Snow, si hierves el agua.",
  "tunel", leo(x=0.5, y=0.75, action="float", expression="surprised"), emph=["Egipto", "Snow"])
S("f02c", "climax", "Fíjate: en casi todas las épocas, lo que más mataba no eran las guerras, sino bacterias, virus, mosquitos y falta de vitaminas.",
  burst("#5CE1E6", "#8FF0F5"), props=[{"type": "mosquito", "x": 0.3, "y": 0.45, "scale": 1.0}, {"type": "rat", "x": 0.55, "y": 0.6},
                                       {"type": "lemon", "x": 0.75, "y": 0.45, "scale": 0.8}],
  emph=["bacterias", "mosquitos"])
S("f03", "climax", "Pero hay una época que gana a todas por goleada: la tuya.", "hoy",
  leo(x=0.5, action="celebrate", expression="excited", outfit="casual"),
  cam={"move": "zoom_burst"}, sfx=[{"name": "sparkle", "at_word": 9}], tr="flash", emph=["tuya"])
S("f04", "ending", "Hoy la esperanza de vida en el mundo ronda los setenta y tres años: casi el doble que en el Londres de John Snow.",
  burst("#22B573", "#6EE7A8"),
  ov=[{"type": "counter", "from": 0, "to": 73, "suffix": " AÑOS", "at_word": 11, "over": 0.7, "y": 300, "size": 160,
       "sub": "ESPERANZA DE VIDA MUNDIAL (OMS, 2023)"}],
  claims=[F("La esperanza de vida mundial fue de 73,3 años en 2023", "OMS, Estimaciones Mundiales de Salud (2026)")],
  cam={"move": "static"}, emph=["setenta"])
S("f05", "ending", "¿Por qué? Agua limpia, antibióticos, vacunas, mosquiteras y fruta todo el año: justo lo que habría salvado a la gente de este viaje.",
  "hoy", leo(x=0.3, action="present", expression="happy", outfit="casual"),
  props=[{"type": "splash", "x": 0.62, "y": 0.5, "color": "#5CE1E6", "at_word": 4},
         {"type": "lemon", "x": 0.78, "y": 0.42, "scale": 0.7, "at_word": 9}],
  emph=["agua", "antibióticos", "vacunas"])
S("f06", "ending", "Así que la próxima vez que te quejes del wifi, acuérdate de los marineros de James Lind.", "hoy",
  leo(x=0.3, action="laugh", expression="laugh", outfit="casual"),
  props=[{"type": "wifi", "x": 0.7, "y": 0.4, "scale": 1.0}], sfx=[{"name": "boing", "at_word": 8}], tr="slide")
S("f07", "ending", "¿Y tú? ¿A qué época viajarías? Te leo en comentarios, y si quieres más viajes así, suscríbete a Hipotéticos.",
  "hoy", leo(x=0.5, action="talk", expression="excited", outfit="casual", actions=[["w8", "point_down"]]),
  ov=[{"type": "label", "text": "COMENTA ABAJO", "x": 960, "y": 120, "size": 70, "at_word": 6, "arrow": "down"}],
  cam={"move": "zoom_burst"}, sfx=[{"name": "ding", "at_word": 6}], tr="zoom", pause=0.5)

DESC = """Una máquina del tiempo te lanza a nueve épocas de la historia: las pirámides de Egipto, la Roma del gran incendio, una aldea vikinga, la peste negra, Tenochtitlan en 1519, la primera vuelta al mundo con Magallanes y Elcano, un barco pirata del Caribe, el Londres del cólera y el canal de Panamá. ¿Cuánto durarías en cada una? ⏳

Leo lo comprueba con datos reales de arqueólogos, historiadores y médicos, y un medidor que va de «horas» a «toda la vida».

{CAPITULOS}

🧪 ALGUNOS DATOS DEL VÍDEO
• Las pirámides no las levantaron esclavos: los obreros tenían tumbas junto a ellas, raciones del Estado y hasta atención médica (fracturas entablilladas).
• Mojar la arena reduce a la mitad la fuerza necesaria para arrastrar un trineo (Physical Review Letters, 2014).
• Roma pudo rondar el millón de habitantes; en el incendio del año 64 ardieron por completo 3 de sus 14 barrios (Tácito).
• Vespasiano gravó la orina que se vendía a las lavanderías: de ahí «el dinero no huele» (Suetonio).
• Los vikingos no llevaban cascos con cuernos (eso viene de una ópera de Wagner de 1876) y eran bastante limpios: en islandés, el sábado es «laugardagur», el día de lavarse.
• Tenochtitlan pudo tener hasta 200.000 habitantes en 1519, con acueducto de agua dulce y un mercado al que acudían decenas de miles de personas; el cacao servía como moneda.
• De los unos 239 hombres que salieron con Magallanes en 1519, solo 18 completaron la vuelta al mundo con Elcano en la Victoria (1522). En el Pacífico comieron cuero y ratas a medio ducado (Pigafetta).
• La peste negra (1347-1351) mató a entre un tercio y la mitad de los europeos. Sin antibióticos, la bubónica mata al 30-60 % de los enfermos (OMS).
• La máscara de pájaro del médico de la peste es del siglo XVII, no de 1348.
• El escorbuto mató a unos 2 millones de marineros entre 1500 y 1800 (estimación). En 1747 James Lind demostró que los cítricos lo curaban.
• En 1854, John Snow vinculó el cólera de Soho con la bomba de Broad Street.
• En las obras francesas del canal de Panamá (1881-1889) murieron más de 22.000 personas, sobre todo de fiebre amarilla y malaria. El cubano Carlos Finlay propuso en 1881 que la transmitía un mosquito; Walter Reed lo confirmó en 1900 y William Gorgas la erradicó de la zona en 1905.
• Hoy la esperanza de vida mundial es de 73,3 años (OMS, 2023).

⚠️ Los «veredictos» del medidor son una estimación divulgativa para comparar épocas, no un cálculo científico.

📚 Fuentes: Encyclopaedia Britannica; Zahi Hawass y Adel Okasha (Giza, 2010); Mark Lehner/AERA; Pierre Tallet (papiros de Merer, 2017); Fall et al., Physical Review Letters (2014); Tácito, Anales XV; Suetonio, Vida de Vespasiano; Glenn Storey, Antiquity (1997); Walter Scheidel; Bos et al., Nature (2011); OMS (peste, cólera, esperanza de vida); Boccaccio, Decamerón; Museo Nacional de Dinamarca; Universidad de York; Museo de Barcos Vikingos de Roskilde; Bernal Díaz del Castillo; Jaffary, Osowski y Porter; Antonio Pigafetta, Relación del primer viaje alrededor del mundo; Armada Española (Instituto de Historia y Cultura Naval); Exquemelin, Piratas de América (1678); Royal Museums Greenwich; James Lind Library; Royal College of Physicians of Edinburgh; Factory Act 1833; John Snow (1855); CDC; Linda Hall Library; Smithsonian Libraries.

💬 ¿A qué época viajarías tú? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#historia #quepasariasi #egipto #roma #vikingos #tenochtitlan #pestenegra #piratas #documental"""

st.save("cuanto-durarias-en-cada-epoca", "¿Cuánto durarías en cada época de la historia?",
        "¿Cuánto durarías en cada época de la historia?", "historia", "¿A qué época viajarías?", {
            "format": "landscape",
            "title": "¿Cuánto durarías en cada época de la historia? ⏳",
            "hashtags": ["#historia", "#quepasariasi", "#documental"],
            "tags": ["cuánto durarías", "qué pasaría si", "historia", "viaje en el tiempo", "antiguo egipto",
                     "pirámides", "antigua roma", "peste negra", "edad media", "piratas", "escorbuto",
                     "londres victoriano", "cólera", "john snow", "vikingos", "tenochtitlan", "aztecas", "historia animada",
                     "canal de panamá", "fiebre amarilla", "elcano", "magallanes", "vuelta al mundo", "carlos finlay", "hipotéticos"],
            "pinned_comment": "¿A qué época viajarías tú… y cuánto crees que durarías? ⏳👇",
            "description": DESC,
            "target_seconds": [900, 1080],
            "custom_thumbnail": True,
            "chapters": {"i01": "Intro: la máquina del tiempo", "e01": "1 · Egipto, las pirámides (≈2560 a. C.)",
                         "r01": "2 · Roma y el gran incendio (64 d. C.)", "v01": "3 · Los vikingos (≈900)",
                         "p01": "4 · La peste negra (1348)", "t01": "5 · Tenochtitlan (1519)",
                         "m01": "6 · La primera vuelta al mundo (1519-1522)",
                         "b01": "7 · Piratas y escorbuto (≈1720)", "l01": "8 · Londres y el cólera (1854)",
                         "c01": "9 · El canal de Panamá (1885)",
                         "f01": "La época más peligrosa… y la mejor"},
        }, mood="adventure")
