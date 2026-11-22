"""Vídeo largo (16:9): ¿Qué pasaría si se apagara la electricidad en todo el mundo?

Nicho elegido con data/research/largo_2026-11-22.md y largo2_2026-11-22.md: los «¿qué pasaría si…?» largos en
español tienen una mediana de ~3.700 vistas/día (p75 > 12.000) y un vídeo sobre un mundo sin electricidad supera las
26.000 vistas/día. Se copia el patrón (escalada temporal minuto → año + casos reales), no el contenido: guion,
datos y estructura propios, con el apagón ibérico del 28 de abril de 2025 como ancla.
"""
from storykit import F, Story

st = Story()
_sc = st.sc
LEO = {"x": 0.3, "y": 0.93, "scale": 0.85}
BEARD = 0.0     # la barba crece con el paso del tiempo (gag)
BAGS = 0.0      # ojeras


def nb(kind, **kw):
    return {"type": kind, "native": True, **kw}


def candle_glow(x, y, s=1.0):
    """Posición de la llama de una vela (prop en x, y fraccionales) para el hueco de luz del fondo."""
    return [x * 1920, y * 1080 - 200 * s, 360 * s]


BG = {
    "espacio": {"type": "space"},
    "ciudad": nb("modern_city"), "ciudad_dia": nb("modern_city", day=True),
    "ciudad_off": nb("modern_city", lights=0, stars=1, milky=0.0),
    "ciudad_via": nb("modern_city", lights=0, stars=1, milky=1.0, moon=False),
    "salon": nb("living_room"), "salon_dia": nb("living_room", day=True, tv=0),
    "cocina": nb("kitchen", day=True), "cocina_off": nb("kitchen", day=True, lights=0, blink=True),
    "super": nb("supermarket"), "super_off": nb("supermarket", lights=0, dark=0.35, stock=0.8),
    "super_vacio": nb("supermarket", lights=0, dark=0.35, stock=0.12, sign_text="CERRADO"),
    "hospital": nb("hospital"), "hospital_gen": nb("hospital", lights=0, backup=True),
    "torres": nb("grid_field"), "torres_noche": nb("grid_field", night=True),
    "aurora": nb("grid_field", night=True, aurora=1.0, lights=0),
    "aurora_chispas": nb("grid_field", night=True, aurora=1.0, sparks=True),
    "sol": nb("solar_storm"), "sol_impacto": nb("solar_storm", impact=True, speed=0.7),
    "control_rojo": nb("control_room", state="red", label="RED ELÉCTRICA · SIN TENSIÓN"),
    "control_verde": nb("control_room", state="mixed", restored=[0.0, 1.05, 7.0], label="REPOSICIÓN"),
    "metro": nb("metro", moving=True), "metro_off": nb("metro", lights=0, dark=0.45),
    "gasolinera": nb("gas_station", lights=0, error=True),
    "campo": {"type": "countryside"}, "oficina": {"type": "office"}, "london": {"type": "london", "smog": 0.5},
}


def burst(c1="#FFD23F", c2="#FFB300"):
    return {"type": "burst", "c1": c1, "c2": c2, "window": 960}


def leo(**kw):
    d = {**LEO, "outfit": "casual"}
    ex = {"beard_color": "hair"}
    if BEARD:
        d["beard"] = BEARD
    if BAGS:
        ex["eyebags"] = BAGS
    ex.update(kw.pop("extras", {}))
    d["extras"] = ex
    d.update(kw)
    return d


def fact(text, at_word=1, label=None):
    o = {"type": "fact", "text": text, "at_word": at_word, "y": 60}
    if label:
        o["label"] = label
    return o


def label(text, bg="#E8392F", at_word=None, y=80):
    o = {"type": "label", "text": text, "x": 960, "y": y, "size": 64, "bg": bg}
    if at_word is not None:
        o["at_word"] = at_word
    return o


def chapter(text):
    return {"type": "title", "lines": [text], "y": 120, "size": 110}


def meter(value, at_word=0):
    """Medidor recurrente: cuánto del mundo moderno sigue funcionando."""
    return {"type": "survival_meter", "x": 0.5, "y": 0.42, "scale": 1.15, "value": value,
            "label": "¿CUÁNTO SIGUE FUNCIONANDO?", "ticks": ["NADA", "POCO", "LA MITAD", "CASI TODO", "TODO"],
            "at_word": at_word, "enter": "pop"}


def counter(to, suffix="", sub=None, at_word=0, frm=0, over=0.8, y=300, size=160, plain=False):
    o = {"type": "counter", "from": frm, "to": to, "suffix": suffix, "at_word": at_word, "over": over, "y": y,
         "size": size}
    if sub:
        o["sub"] = sub
    if plain:
        o["plain"] = True
    return o


VIG = {"type": "vignette", "alpha": 0.55}


def S(sid, beat, narration, bg, char=None, props=(), ov=(), cam=None, claims=(), sfx=(), tr="slide", emph=(),
      pause=0.08):
    vis = {"background": dict(BG[bg]) if isinstance(bg, str) else bg,
           "character": char if char is not None else {"visible": False},
           "props": list(props), "overlays": list(ov), "camera": cam or {"move": "push_in", "zoom_to": 1.06}}
    _sc(sid, beat, narration, vis, claims=claims, sfx=sfx, transition=tr, emphasis=list(emph), pause=pause)


SRC_ES = "La Moncloa (declaración del presidente del Gobierno, 28/04/2025)"
SRC_USDA = "USDA FSIS, «Keeping Food Safe During an Emergency»"

# ================================================================== INTRO
S("i01", "hook", "Imagina que ahora mismo, en todo el planeta a la vez, se apagan todas las luces.", "espacio",
  props=[{"type": "earth_night", "x": 0.5, "y": 0.55, "scale": 1.35, "off_at": 2.2, "off_spread": 1.6,
          "enter": "none", "loop": "bob"}],
  ov=[{"type": "title", "lines": ["¿Y SI SE APAGARA", "TODO EL MUNDO?"], "y": 130, "size": 92}],
  cam={"move": "push_in", "zoom_to": 1.12}, sfx=[{"name": "riser", "at": 0.0, "gain_db": -6},
                                                  {"name": "boom", "at_word": 13, "gain_db": -4}],
  tr="cut", emph=["planeta", "luces"])
S("i02", "setup", "Y no vuelven. Ni en un minuto, ni en una hora, ni mañana.", "ciudad_off",
  leo(action="shock", expression="scared"), ov=[VIG], cam={"move": "punch", "impacts": [0.1]},
  sfx=[{"name": "hit", "at_word": 0}], emph=["vuelven"])
S("i03", "setup", "Parece ciencia ficción, pero una parte de esto ya ocurrió hace muy poco, aquí al lado.",
  "ciudad_dia", leo(action="present", expression="determined"),
  ov=[label("28 DE ABRIL DE 2025", at_word=9)], sfx=[{"name": "ding", "at_word": 9}])
S("i04", "setup", "El veintiocho de abril de 2025, a las doce y treinta y tres, España y Portugal se quedaron sin luz.",
  "ciudad_dia", leo(x=0.22, action="shock", expression="shock", actions=[[0, "talk"], ["w14", "shock"]]),
  props=[{"type": "traffic_light", "x": 0.62, "y": 0.97, "scale": 1.0, "state": "green", "off_at": 4.6},
         {"type": "traffic_light", "x": 0.86, "y": 0.97, "scale": 1.0, "state": "red", "off_at": 4.7}],
  ov=[label("12:33", bg="#1B1B3A", at_word=6)],
  claims=[F("El apagón ibérico empezó a las 12:33 del 28 de abril de 2025", SRC_ES)],
  sfx=[{"name": "crack", "at_word": 15}])
S("i05", "setup", "En apenas cinco segundos desaparecieron quince gigavatios: alrededor del sesenta por ciento de lo que consumía España en ese momento.",
  burst("#1B1B3A", "#3B3F78"),
  ov=[counter(60, " %", "DE LA DEMANDA, EN 5 SEGUNDOS", at_word=9, y=380, size=220)],
  claims=[F("Se perdieron 15 GW de generación en unos cinco segundos, cerca del 60 % de la demanda", SRC_ES)],
  cam={"move": "static"}, sfx=[{"name": "hit", "at_word": 9}], emph=["quince", "sesenta"])
S("i05b", "setup", "Y no es el récord. En julio de 2012, en la India, un apagón dejó sin luz a más de seiscientos veinte millones de personas.",
  burst("#FF8A3D", "#FFB36B"),
  ov=[counter(620, " MILLONES", "INDIA · JULIO 2012", at_word=17, y=300, size=150)],
  claims=[F("El apagón de la India del 30-31 de julio de 2012 afectó a más de 620 millones de personas", "Gobierno de la India / prensa internacional")],
  cam={"move": "static"}, sfx=[{"name": "hit", "at_word": 17}], emph=["seiscientos"])
S("i05c", "setup", "Y en 2003, otro dejó a oscuras a unos cincuenta y cinco millones en el noreste de Estados Unidos y Canadá.",
  "ciudad_off", leo(x=0.25, action="present", expression="surprised"),
  ov=[label("2003 · 55 MILLONES", bg="#3B82F6", at_word=1)],
  claims=[F("El apagón del noreste de 2003 afectó a unos 55 millones de personas en EE. UU. y Canadá", "U.S.-Canada Power System Outage Task Force (2004)")])
S("i06", "setup", "Millones de personas pasaron casi un día entero descubriendo cuántas cosas dependen de un enchufe.",
  "cocina_off", leo(action="shrug", expression="worried"),
  props=[{"type": "fridge", "x": 0.8, "y": 0.92, "scale": 0.95, "lights": 0, "enter": "none"}])
S("i07", "setup", "Hoy lo llevamos al extremo: un apagón total, en todo el mundo, que dura minutos, horas, días… y luego años.",
  burst("#5CE1E6", "#8FF0F5"), leo(x=0.25, action="present", expression="excited"),
  props=[{"type": "clock", "x": 0.68, "y": 0.47, "scale": 1.2, "speed": 14, "loop": "bob"}],
  emph=["extremo", "años"])
S("i08", "setup", "Con datos reales: lo que pasó en apagones de verdad y lo que cuentan los ingenieros.",
  "control_rojo", leo(action="point_up", expression="determined"),
  props=[{"type": "magnifier", "x": 0.72, "y": 0.5, "scale": 1.0, "at_word": 3}],
  sfx=[{"name": "pop", "at_word": 3}])
S("i09", "setup", "Vamos a ver cuánto tarda en romperse cada cosa que das por hecha. Empieza la cuenta atrás.",
  burst("#FFD23F", "#FFB300"), leo(x=0.25, action="talk", expression="excited"),
  props=[meter(1.0, at_word=4)], tr="zoom", emph=["romperse"])

# ================================================================== MINUTO 1
S("m01", "development", "Segundo cero. Estás en casa, es mediodía… y de repente la nevera deja de zumbar.",
  nb("kitchen", day=True, off_at=4.4),
  leo(x=0.3, action="idle", expression="happy", expressions=[["w11", "surprised"]]),
  props=[{"type": "fridge", "x": 0.8, "y": 0.92, "scale": 0.95, "enter": "none", "off_at": 4.4}],
  ov=[chapter("SEGUNDO 0")], sfx=[{"name": "whoosh", "at": 0.0}], tr="zoom", emph=["nevera"])
S("m01b", "development", "Si estabas con el ordenador de sobremesa, lo que no hubieras guardado acaba de desaparecer. Primera pérdida del día.",
  "oficina", leo(x=0.3, action="shock", expression="angry", actions=[[0, "talk"], ["w11", "shock"]]),
  sfx=[{"name": "crack", "at_word": 11}], emph=["guardado"])
S("m02", "development", "Lo primero que notas es el silencio: ni la nevera, ni el router, ni el aire acondicionado.",
  "cocina_off", leo(action="look_up", expression="worried"),
  props=[{"type": "wifi", "x": 0.72, "y": 0.4, "scale": 1.0, "crossed": True, "at_word": 10}],
  sfx=[{"name": "pop", "at_word": 10}], emph=["silencio"])
S("m03", "development", "Miras el móvil: la batería va bien, pero el wifi ha desaparecido. Y fuera empieza el lío.",
  "cocina_off", leo(action="talk", expression="surprised"),
  props=[{"type": "smartphone", "x": 0.7, "y": 0.45, "scale": 0.9, "loop": "bob"}])
S("m04", "development", "En la calle, los semáforos se apagan de golpe. Así se dieron cuenta muchos el veintiocho de abril.",
  "ciudad_dia", leo(x=0.2, action="look_up", expression="surprised"),
  props=[{"type": "traffic_light", "x": 0.55, "y": 0.97, "scale": 1.0, "state": "green", "off_at": 1.6},
         {"type": "traffic_light", "x": 0.82, "y": 0.97, "scale": 1.0, "state": "red", "off_at": 1.7}],
  claims=[F("La desconexión de los semáforos fue uno de los primeros síntomas visibles del apagón", "Prensa española, 28/04/2025")],
  sfx=[{"name": "crack", "at_word": 5}])
S("m05", "development", "Cada cruce se convierte en una negociación entre conductores, hasta que llegan los agentes a dirigir el tráfico.",
  "ciudad_dia", leo(x=0.2, action="shrug", expression="worried"),
  props=[{"type": "car", "x": 0.5, "y": 0.86, "scale": 0.8, "enter": "slide_left"},
         {"type": "car", "x": 0.82, "y": 0.9, "scale": 0.8, "flip": -1, "enter": "slide_right"},
         {"type": "traffic_light", "x": 0.66, "y": 0.97, "scale": 0.9, "state": "off", "layer": "back"}],
  sfx=[{"name": "boing", "at_word": 5}])
S("m05b", "development", "Las fábricas se detienen en seco: hornos, cintas y robots se quedan quietos a mitad de tarea.",
  "torres", leo(x=0.22, action="look_up", expression="surprised"),
  props=[{"type": "crane", "x": 0.68, "y": 0.9, "scale": 0.8}])
S("m06", "development", "Arriba, en los edificios, mucha gente se queda encerrada en ascensores, parados entre dos plantas.",
  burst("#3B3F78", "#5A5FA0"), leo(x=0.28, action="sweat", expression="scared", sweat=0.8),
  props=[{"type": "elevator", "x": 0.68, "y": 0.98, "scale": 1.15, "display": "--", "alarm": True}],
  sfx=[{"name": "ding", "at_word": 7}], emph=["encerrada"])
S("m07", "development", "Aquel día, solo en Madrid, los servicios de emergencia hicieron doscientos ochenta y seis rescates en ascensores.",
  burst("#3B3F78", "#5A5FA0"),
  props=[{"type": "elevator", "x": 0.5, "y": 1.0, "scale": 0.9, "display": "--", "enter": "none"}],
  ov=[counter(286, "", "RESCATES EN ASCENSORES · MADRID", at_word=10, y=230, size=180)],
  claims=[F("En Madrid se realizaron 286 rescates en ascensores durante el apagón", "El País, 29/04/2025")],
  cam={"move": "static"}, sfx=[{"name": "hit", "at_word": 10}])
S("m08", "development", "Bajo tierra es peor: el metro se para en mitad del túnel y las luces se apagan.",
  nb("metro", moving=True, off_at=3.2), leo(x=0.5, action="shock", expression="shock", actions=[[0, "talk"], ["w9", "shock"]]),
  sfx=[{"name": "crack", "at_word": 9}], emph=["túnel"])
S("m09", "development", "Las luces de emergencia aguantan un rato con baterías, y toca bajar a las vías y caminar hasta la estación.",
  "metro_off", leo(x=0.3, action="walk", expression="worried"),
  props=[{"type": "flashlight", "x": 0.46, "y": 0.6, "scale": 0.9, "flip": 1}], ov=[VIG])
S("m10", "development", "En España se quedaron parados más de cien trenes y hubo que evacuar a unos treinta y cinco mil pasajeros.",
  burst("#1B1B3A", "#3B3F78"),
  ov=[counter(35000, "", "PASAJEROS EVACUADOS DE TRENES", at_word=13, y=330, size=190)],
  claims=[F("El apagón dejó parados más de un centenar de trenes y obligó a evacuar a unos 35.000 pasajeros",
            "Ministerio de Transportes, recogido por la prensa (29/04/2025)")],
  cam={"move": "static"}, sfx=[{"name": "hit", "at_word": 13}], emph=["cien", "treinta"])
S("m10b", "development", "¿Tienes coche eléctrico? Pues lo que lleve en la batería es todo lo que vas a tener durante mucho tiempo.",
  "ciudad_dia", leo(x=0.22, action="shrug", expression="smug"),
  props=[{"type": "car", "x": 0.6, "y": 0.88, "scale": 0.9}, {"type": "battery", "x": 0.6, "y": 0.42, "scale": 0.7, "level": 0.64, "at_word": 6}],
  sfx=[{"name": "pop", "at_word": 6}])
S("m11", "development", "Mientras tanto, en los hospitales, pasa algo que casi nadie ve.", nb("hospital", off_at=2.6),
  leo(x=0.3, action="think", expression="surprised"), sfx=[{"name": "crack", "at": 2.6}])
S("m12", "development", "Al caer la red arrancan solos los generadores. En muchos países la norma les exige dar corriente en unos diez segundos.",
  "hospital_gen", leo(x=0.3, action="point_up", expression="determined"),
  props=[{"type": "generator", "x": 0.68, "y": 0.92, "scale": 0.8, "fuel": 0.95}],
  ov=[counter(10, " s", "PARA QUE ENTRE EL GENERADOR", at_word=16, y=170, size=120)],
  claims=[F("La norma NFPA 110 exige que la energía de emergencia de los sistemas de seguridad vital entre en 10 segundos",
            "NFPA 99/110 (EE. UU.)")],
  sfx=[{"name": "rumble", "at_word": 4, "gain_db": -6}], emph=["diez"])
S("m13", "development", "Pero el generador no da para todo: se reserva para quirófanos, cuidados intensivos y las máquinas que mantienen a gente con vida.",
  "hospital_gen", leo(x=0.3, action="present", expression="worried"),
  props=[{"type": "heart", "x": 0.6, "y": 0.4, "scale": 0.8, "loop": "pulse", "at_word": 8}])
S("m14", "development", "¿Y los aviones que están volando? Tranquilo: producen su propia electricidad con los motores.",
  "ciudad_dia", leo(x=0.22, action="look_up", expression="surprised", expressions=[["w5", "happy"]]),
  props=[{"type": "plane", "x": 0.66, "y": 0.28, "scale": 0.9, "enter": "slide_right"}],
  sfx=[{"name": "whoosh", "at_word": 1}])
S("m15", "development", "El problema es aterrizar: torres de control, radares y luces de pista tendrían que tirar de generadores de emergencia.",
  "ciudad_dia", leo(x=0.22, action="think", expression="worried"),
  props=[{"type": "plane", "x": 0.66, "y": 0.35, "scale": 0.8, "enter": "none", "rot": 0.15},
         {"type": "generator", "x": 0.82, "y": 0.92, "scale": 0.6, "at_word": 12}])
S("m16", "development", "Balance del primer minuto: el mundo aún funciona a medias, gracias a pilas, baterías y generadores.",
  burst("#22B573", "#6EE7A8"), leo(x=0.2, action="present", expression="determined"),
  props=[meter(0.78, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== HORA 1
S("h01", "development", "Hora uno. Pruebas a llamar a casa… y la llamada no entra.", "cocina_off",
  leo(action="talk", expression="worried", expressions=[["w6", "surprised"]]),
  props=[{"type": "smartphone", "x": 0.66, "y": 0.45, "scale": 0.9, "crossed": True, "cross_at": 0.6}],
  ov=[chapter("HORA 1")], tr="zoom", sfx=[{"name": "whoosh", "at": 0.0}])
S("h02", "development", "Las antenas de telefonía tienen baterías de respaldo, pero suelen durar solo entre dos y cuatro horas.",
  "torres", leo(x=0.2, action="present", expression="worried"),
  props=[{"type": "cell_tower", "x": 0.52, "y": 0.95, "scale": 1.15},
         {"type": "battery", "x": 0.8, "y": 0.4, "scale": 0.9, "level": [1.0, 0.25, 5.0], "label": "BATERÍA DE LA ANTENA"}],
  claims=[F("Las baterías de respaldo de las antenas suelen durar entre 2 y 4 horas", "FCC / informes del sector de telecomunicaciones")],
  emph=["dos", "cuatro"])
S("h03", "development", "Además, millones de personas llaman a la vez para saber si su familia está bien. La red se satura.",
  "torres", leo(x=0.2, action="sweat", expression="scared", sweat=0.5),
  props=[{"type": "cell_tower", "x": 0.55, "y": 0.95, "scale": 1.15, "on": False},
         {"type": "message", "x": 0.78, "y": 0.3, "scale": 0.8, "at_word": 4},
         {"type": "message", "x": 0.84, "y": 0.5, "scale": 0.7, "at_word": 7}],
  sfx=[{"name": "pop", "at_word": 4}, {"name": "pop", "at_word": 7}], emph=["satura"])
S("h04", "development", "Internet aguanta algo más, porque los grandes centros de datos tienen generadores. Pero si tu router no tiene luz, da igual.",
  "cocina_off", leo(action="shrug", expression="smug"),
  props=[{"type": "wifi", "x": 0.72, "y": 0.42, "scale": 1.0, "crossed": True, "at_word": 14}],
  sfx=[{"name": "boing", "at_word": 18}])
S("h04b", "development", "Colegios y oficinas mandan a todo el mundo a casa. Sin metro ni trenes, miles de personas vuelven andando kilómetros.",
  "ciudad_dia", leo(x=0.3, action="walk", expression="tired"),
  props=[{"type": "npc", "x": 0.55, "y": 0.93, "scale": 0.7}, {"type": "npc", "x": 0.7, "y": 0.93, "scale": 0.7, "seed": 5},
         {"type": "npc", "x": 0.85, "y": 0.93, "scale": 0.7, "seed": 6}],
  cam={"move": "pan_right"})
S("h05", "development", "Vas a comprar agua y pan. El datáfono no funciona, el cajero tampoco: solo vale el efectivo.",
  "super_off", leo(x=0.28, action="talk", expression="surprised"),
  props=[{"type": "atm", "x": 0.6, "y": 0.95, "scale": 0.85, "on": False, "at_word": 8},
         {"type": "money", "x": 0.82, "y": 0.7, "scale": 0.8, "at_word": 15}],
  sfx=[{"name": "hit", "at_word": 8}, {"name": "ding", "at_word": 15}], emph=["efectivo"])
S("h06", "development", "El veintiocho de abril pasó justo eso: colas en supermercados y cajeros, y gente sin un euro en el bolsillo.",
  "super_off", leo(x=0.28, action="shrug", expression="worried"),
  props=[{"type": "npc", "x": 0.55, "y": 0.93, "scale": 0.7}, {"type": "npc", "x": 0.68, "y": 0.93, "scale": 0.7, "seed": 2},
         {"type": "npc", "x": 0.81, "y": 0.93, "scale": 0.7, "seed": 3}],
  claims=[F("Durante el apagón se formaron aglomeraciones en supermercados y cajeros", "Prensa (Primicias/EFE, 28/04/2025)")])
S("h07", "development", "Muchas tiendas cerraron: sin luz no hay cajas, ni neveras, ni puertas automáticas. Solo aguantaron las que tenían generador.",
  "super_vacio", leo(x=0.3, action="present", expression="worried"),
  claims=[F("Muchos supermercados cerraron por falta de refrigeración y cobro; otros siguieron abiertos con generadores",
            "Prensa española (El Cronista, Xataka, 28/04/2025)")])
S("h07b", "development", "Lo primero que vuela de las estanterías es el agua embotellada, las pilas, las velas y las linternas.",
  "super_vacio", leo(x=0.3, action="sweat", expression="worried", sweat=0.4),
  props=[{"type": "water_bottle", "x": 0.62, "y": 0.8, "scale": 0.5, "at_word": 9},
         {"type": "candle", "x": 0.76, "y": 0.8, "scale": 0.6, "at_word": 14},
         {"type": "flashlight", "x": 0.86, "y": 0.5, "scale": 0.5, "at_word": 17, "on": False}],
  sfx=[{"name": "pop", "at_word": 9}, {"name": "pop", "at_word": 14}])
S("h08", "development", "Piensas en llenar el depósito del coche, por si acaso. Mala idea.", "gasolinera",
  leo(x=0.2, action="walk", expression="determined", actions=[["w8", "shock"]], expressions=[["w8", "surprised"]]),
  props=[{"type": "car", "x": 0.83, "y": 0.9, "scale": 0.8, "enter": "slide_right"}],
  sfx=[{"name": "boing", "at_word": 9}])
S("h09", "development", "Los surtidores son bombas eléctricas. Sin corriente, la gasolina está ahí abajo… y no hay forma de sacarla.",
  "gasolinera", leo(x=0.2, action="shrug", expression="angry"),
  props=[{"type": "jerrycan", "x": 0.86, "y": 0.92, "scale": 0.7, "at_word": 15}],
  claims=[F("Sin electricidad no funcionan las bombas de combustible ni los sistemas de pago de las gasolineras",
            "Motorpasión / El Debate, 28/04/2025")],
  emph=["eléctricas"])
S("h09b", "development", "Las radios y las teles públicas tienen generadores para seguir emitiendo. El problema es que en tu casa la tele no se enciende.",
  "salon_dia", leo(x=0.62, action="shrug", expression="smug"),
  props=[{"type": "radio", "x": 0.35, "y": 0.82, "scale": 0.6}],
  sfx=[{"name": "boing", "at_word": 19}])
S("h10", "development", "Vuelves a casa. La nevera lleva una hora apagada, y empieza una cuenta atrás que sí importa.",
  "cocina_off", leo(x=0.3, action="think", expression="worried"),
  props=[{"type": "fridge", "x": 0.8, "y": 0.92, "scale": 0.95, "lights": 0, "temp": "6 °C", "enter": "none"}])
S("h11", "development", "Con la puerta cerrada, la comida de la nevera se mantiene segura unas cuatro horas. Cada vez que la abres, pierdes frío.",
  "cocina_off", leo(x=0.3, action="point_up", expression="determined"),
  props=[{"type": "fridge", "x": 0.8, "y": 0.92, "scale": 0.95, "lights": 0, "open": 0.0, "temp": "4 H",
          "temp_color": "#FFD23F", "enter": "none"}],
  claims=[F("Una nevera cerrada mantiene la comida segura unas 4 horas sin electricidad", SRC_USDA)],
  ov=[fact("Nevera cerrada: comida segura ≈ 4 horas sin luz", at_word=7)], emph=["cuatro"])
S("h12", "development", "Un congelador lleno aguanta unas cuarenta y ocho horas. Si está a medias, solo unas veinticuatro.",
  burst("#5CE1E6", "#8FF0F5"), leo(x=0.25, action="present", expression="surprised"),
  ov=[counter(48, " H", "CONGELADOR LLENO", at_word=4, y=260, size=170),
      {"type": "label", "text": "MEDIO LLENO: 24 H", "x": 1250, "y": 720, "size": 64, "bg": "#E8392F", "at_word": 11}],
  claims=[F("Un congelador lleno mantiene la temperatura unas 48 horas; medio lleno, unas 24", SRC_USDA)],
  cam={"move": "static"}, sfx=[{"name": "ding", "at_word": 11}])
S("h13", "development", "Balance de la primera hora: sin cobertura, sin pagos con tarjeta y sin gasolina. Y todavía es de día.",
  burst("#FFD23F", "#FFB300"), leo(x=0.2, action="sweat", expression="worried", sweat=0.4),
  props=[meter(0.6, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== PRIMERA NOCHE
S("n01", "development", "Y llega algo que no has vivido nunca: la primera noche sin luz.", nb("modern_city", off_at=2.8, off_spread=1.4),
  leo(x=0.25, action="look_up", expression="surprised", expressions=[["w8", "scared"]]),
  ov=[chapter("NOCHE 1")], sfx=[{"name": "riser", "at": 1.6, "gain_db": -8}], tr="zoom", emph=["noche"])
S("n02", "development", "Sin farolas, sin ventanas encendidas, sin carteles. La ciudad queda tan oscura como el campo.",
  "ciudad_off", leo(x=0.3, action="sweat", expression="scared", sweat=0.4), ov=[VIG])
S("n03", "development", "Y entonces miras hacia arriba.", "ciudad_via",
  leo(x=0.3, action="look_up", expression="wow"), cam={"move": "pull_out"}, sfx=[{"name": "sparkle", "at_word": 3}])
S("n04", "development", "Ahí está la Vía Láctea. Más de un tercio de la humanidad no puede verla desde casa por la contaminación lumínica.",
  "ciudad_via", leo(x=0.25, action="present", expression="wow"),
  claims=[F("La Vía Láctea está oculta para más de un tercio de la humanidad por la contaminación lumínica",
            "Falchi et al., Science Advances (2016)")],
  emph=["Láctea", "tercio"])
S("n05", "development", "En Europa, el sesenta por ciento de la gente. En Norteamérica, casi el ochenta.", "ciudad_via",
  ov=[counter(60, " %", "DE LOS EUROPEOS NO LA VE", at_word=2, y=280, size=170),
      {"type": "label", "text": "NORTEAMÉRICA: ≈80 %", "x": 960, "y": 720, "size": 66, "bg": "#E8392F", "at_word": 9}],
  claims=[F("El 60 % de los europeos y casi el 80 % de los norteamericanos no pueden ver la Vía Láctea",
            "Falchi et al., Science Advances (2016)")],
  cam={"move": "static"}, sfx=[{"name": "ding", "at_word": 9}])
S("n06", "development", "Esa noche, millones de personas verían por primera vez el cielo que veían sus bisabuelos.", "ciudad_via",
  leo(x=0.3, action="look_up", expression="happy"), cam={"move": "pull_out"})
S("n07", "development", "Pero lo bonito dura poco. Velas encendidas en millones de casas a la vez disparan el riesgo de incendio.",
  nb("living_room", lights=0, dark=0.72, glows=[candle_glow(0.62, 0.8, 1.0), candle_glow(0.8, 0.8, 0.9)]),
  leo(x=0.3, action="sweat", expression="worried", sweat=0.4),
  props=[{"type": "candle", "x": 0.62, "y": 0.8, "scale": 1.0}, {"type": "candle", "x": 0.8, "y": 0.8, "scale": 0.9, "seed": 4}],
  emph=["incendio"])
S("n08", "development", "Y pedir ayuda no es fácil: si las antenas se han quedado sin batería, llamar a emergencias se vuelve casi imposible.",
  "torres_noche", leo(x=0.2, action="talk", expression="scared"),
  props=[{"type": "cell_tower", "x": 0.55, "y": 0.95, "scale": 1.15, "on": False},
         {"type": "battery", "x": 0.82, "y": 0.4, "scale": 0.8, "level": 0.0, "label": "SIN BATERÍA"}],
  ov=[VIG])
S("n09", "development", "Lo que más se agradece esa noche es una linterna y una radio a pilas. Muchos se enteraron así de lo que pasaba en abril.",
  nb("living_room", lights=0, dark=0.7, glows=[[1150, 560, 520]]),
  leo(x=0.3, action="present", expression="happy"),
  props=[{"type": "radio", "x": 0.66, "y": 0.78, "scale": 0.8}, {"type": "flashlight", "x": 0.42, "y": 0.5, "scale": 0.8}],
  sfx=[{"name": "ding", "at_word": 11}], emph=["radio"])
S("n09b", "development", "Sin calefacción ni aire acondicionado, la temperatura de tu casa empieza a parecerse a la de la calle.",
  nb("living_room", lights=0, dark=0.7, glows=[candle_glow(0.7, 0.82, 0.9)]),
  leo(x=0.3, action="sweat", expression="worried", sweat=0.3),
  props=[{"type": "candle", "x": 0.7, "y": 0.82, "scale": 0.9}, {"type": "thermometer", "x": 0.86, "y": 0.6, "scale": 0.8, "level": 0.3}])
S("n09c", "development", "Y un aviso importante: nunca enciendas un generador dentro de casa. Su gas, el monóxido de carbono, no huele y puede matar.",
  nb("living_room", lights=0, dark=0.65, glows=[[1150, 560, 520]]),
  leo(x=0.3, action="point_up", expression="angry"),
  props=[{"type": "generator", "x": 0.68, "y": 0.92, "scale": 0.7, "running": True, "crossed": True, "cross_at": 0.4},
         {"type": "skull", "x": 0.86, "y": 0.4, "scale": 0.6, "at_word": 21}],
  claims=[F("Los generadores nunca deben usarse en interiores por el riesgo de intoxicación por monóxido de carbono", "CDC (EE. UU.)")],
  sfx=[{"name": "hit", "at_word": 21}], emph=["nunca", "monóxido"])
S("n09d", "development", "Y entonces lo notas: el silencio. Sin tráfico, sin aires acondicionados, sin zumbidos. Solo grillos y algún perro.",
  "ciudad_via", leo(x=0.3, action="idle", expression="happy_closed"), cam={"move": "pull_out"})
S("n10", "development", "En los pisos altos, alguien abre el grifo… y no sale nada.",
  nb("kitchen", lights=0, dark=0.6, glows=[candle_glow(0.42, 0.62, 0.7)]),
  leo(x=0.22, action="shock", expression="shock", actions=[[0, "idle"], ["w7", "shock"]]),
  props=[{"type": "tap", "x": 0.68, "y": 0.4, "scale": 1.1, "flow": [1.0, 0.0, 2.2]},
         {"type": "candle", "x": 0.42, "y": 0.62, "scale": 0.7}],
  sfx=[{"name": "gulp", "at_word": 9}])
S("n11", "development", "El agua no sube sola: la empujan bombas eléctricas. Los edificios altos y las depuradoras dependen de ellas.",
  burst("#3B82F6", "#7FB8E6"), leo(x=0.25, action="present", expression="determined"),
  props=[{"type": "pipe", "x": 0.68, "y": 0.5, "scale": 1.0}, {"type": "splash", "x": 0.75, "y": 0.35, "color": "#5CE1E6", "at_word": 5}],
  claims=[F("El bombeo y el tratamiento del agua dependen de la electricidad; los edificios altos necesitan bombas para subirla",
            "EPA (EE. UU.), guía de resiliencia energética para servicios de agua")])
S("n12", "development", "Hay depósitos elevados que dan presión durante un tiempo. Pero cuando se vacían y nadie los rellena, el grifo se seca.",
  burst("#3B82F6", "#7FB8E6"), leo(x=0.25, action="shrug", expression="worried"),
  props=[{"type": "tap", "x": 0.7, "y": 0.42, "scale": 1.1, "flow": [0.8, 0.0, 6.0]}])
S("n13", "development", "Balance de la primera noche: a oscuras, sin agua en muchos pisos… y con un cielo espectacular.",
  burst("#FFD23F", "#FFB300"), leo(x=0.2, action="shrug", expression="tired"),
  props=[meter(0.47, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== DÍA 3
BEARD, BAGS = 0.18, 0.35
S("d01", "development", "Día tres. Te despiertas con barba de un par de días, y la casa empieza a oler raro.", "cocina_off",
  leo(x=0.3, action="sweat", expression="tired", sweat=0.3), ov=[chapter("DÍA 3")], tr="zoom",
  sfx=[{"name": "whoosh", "at": 0.0}], emph=["oler"])
S("d02", "development", "El congelador se ha rendido. Lo que había dentro hay que cocinarlo hoy… o tirarlo.", "cocina_off",
  leo(x=0.3, action="shock", expression="angry"),
  props=[{"type": "fridge", "x": 0.78, "y": 0.92, "scale": 0.95, "lights": 0, "open_at": 0.6, "drip": True,
          "enter": "none"}],
  sfx=[{"name": "splash", "at_word": 4, "gain_db": -6}])
S("d03", "development", "En el supermercado, los estantes se vacían. Sin frío, lo fresco se estropea; y sin luz, no hay forma de cobrar.",
  "super_vacio", leo(x=0.3, action="walk", expression="worried"), ov=[VIG])
S("d04", "development", "Tras el apagón de abril, las tiendas tuvieron que tirar toneladas de fruta, verdura, carne y pescado.",
  "super_vacio", leo(x=0.3, action="shrug", expression="worried"),
  props=[{"type": "food", "x": 0.68, "y": 0.8, "scale": 0.9, "at_word": 8}, {"type": "meat", "x": 0.82, "y": 0.75, "scale": 0.6, "at_word": 12}],
  claims=[F("Tras el apagón, trabajadores de supermercados tiraron toneladas de fruta, verdura, carne y pescado",
            "Prensa española (Vozpópuli, 2025)")])
S("d05", "development", "Y reponer es imposible: los camiones necesitan gasóleo, y los almacenes funcionan con ordenadores y cintas eléctricas.",
  "gasolinera", leo(x=0.2, action="present", expression="worried"),
  props=[{"type": "cart", "x": 0.6, "y": 0.9, "scale": 0.9}, {"type": "jerrycan", "x": 0.84, "y": 0.92, "scale": 0.7, "crossed": True, "cross_at": 0.5}])
S("d06", "development", "Los hospitales siguen en pie con sus generadores. En Estados Unidos, por ejemplo, se les pide prepararse para aguantar noventa y seis horas.",
  "hospital_gen", leo(x=0.3, action="point_up", expression="determined"),
  ov=[counter(96, " H", "DE AUTONOMÍA PLANIFICADA", at_word=18, y=200, size=150)],
  claims=[F("Los hospitales acreditados en EE. UU. deben planificar cómo sostener sus servicios durante 96 horas",
            "The Joint Commission, estándares de gestión de emergencias")],
  emph=["noventa"])
S("d06b", "development", "El problema serio está en las casas: hay personas que dependen de concentradores de oxígeno o de otras máquinas eléctricas para vivir.",
  "salon_dia", leo(x=0.62, action="sweat", expression="worried", sweat=0.5),
  props=[{"type": "battery", "x": 0.3, "y": 0.4, "scale": 0.7, "level": [0.5, 0.1, 6.0]}])
S("d07", "development", "Cuatro días. Después, todo depende de que lleguen camiones de gasóleo… que también lo necesitan para moverse.",
  "hospital_gen", leo(x=0.3, action="sweat", expression="scared", sweat=0.6),
  props=[{"type": "generator", "x": 0.68, "y": 0.92, "scale": 0.8, "fuel": [0.45, 0.05, 6.0]}])
S("d08", "development", "Por cierto: la Unión Europea recomienda que cada hogar pueda arreglárselas solo durante setenta y dos horas.",
  burst("#3B82F6", "#7FB8E6"), leo(x=0.22, action="present", expression="determined"),
  ov=[counter(72, " H", "RECOMENDACIÓN DE LA UE", at_word=14, y=260, size=170)],
  claims=[F("La Estrategia de Preparación de la UE (26/03/2025) recomienda que la población pueda ser autosuficiente al menos 72 horas",
            "Comisión Europea, Estrategia de la Unión de Preparación (2025)")],
  sfx=[{"name": "ding", "at_word": 14}], emph=["setenta"])
S("d09", "development", "Agua, comida en conserva, linterna, radio, algo de efectivo y tus medicinas. Justo lo que ahora echas de menos.",
  burst("#22B573", "#6EE7A8"), leo(x=0.18, action="talk", expression="happy"),
  props=[{"type": "water_bottle", "x": 0.38, "y": 0.62, "scale": 0.6, "at_word": 0},
         {"type": "food_can", "x": 0.52, "y": 0.62, "scale": 0.7, "at_word": 1},
         {"type": "flashlight", "x": 0.62, "y": 0.4, "scale": 0.55, "at_word": 4, "on": False},
         {"type": "radio", "x": 0.8, "y": 0.6, "scale": 0.6, "at_word": 5, "on": False},
         {"type": "money", "x": 0.55, "y": 0.86, "scale": 0.6, "at_word": 8},
         {"type": "heart", "x": 0.8, "y": 0.86, "scale": 0.45, "at_word": 11}],
  sfx=[{"name": "pop", "at_word": 0}, {"name": "pop", "at_word": 4}, {"name": "pop", "at_word": 8}])
S("d09b", "development", "La basura se acumula en las esquinas: los camiones necesitan gasóleo, y las plantas de tratamiento, electricidad.",
  "ciudad_dia", leo(x=0.3, action="sweat", expression="angry", sweat=0.4),
  props=[{"type": "debris", "x": 0.68, "y": 0.85, "scale": 0.9}, {"type": "rat", "x": 0.82, "y": 0.9, "scale": 0.6, "at_word": 6}],
  sfx=[{"name": "pop", "at_word": 6}])
S("d09c", "development", "Policías, bomberos y ambulancias siguen comunicándose por sus propias redes de radio, que también tiran de baterías y generadores.",
  "ciudad_dia", leo(x=0.22, action="present", expression="determined"),
  props=[{"type": "police_car", "x": 0.68, "y": 0.88, "scale": 0.8, "enter": "slide_right"},
         {"type": "radio", "x": 0.7, "y": 0.45, "scale": 0.5, "at_word": 8}])
S("d10", "development", "Sin agua corriente, las cisternas y las depuradoras dejan de funcionar bien. La higiene se convierte en un problema de salud.",
  burst("#8A5A30", "#B07A48"), leo(x=0.3, action="sweat", expression="worried", sweat=0.5),
  props=[{"type": "tap", "x": 0.7, "y": 0.42, "scale": 1.0, "flow": 0}])
S("d11", "development", "Balance del día tres: la nevera perdida, las tiendas vacías y el gasóleo convertido en oro.",
  burst("#FFD23F", "#FFB300"), leo(x=0.2, action="shrug", expression="tired"),
  props=[meter(0.33, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== SEMANA 1
BEARD, BAGS = 0.4, 0.5
S("s01", "development", "Semana uno. A estas alturas, muchos generadores empiezan a quedarse sin combustible.", "hospital_gen",
  leo(x=0.3, action="sweat", expression="tired", sweat=0.4),
  props=[{"type": "generator", "x": 0.68, "y": 0.92, "scale": 0.8, "fuel": [0.12, 0.0, 4.0], "running": True}],
  ov=[chapter("SEMANA 1")], tr="zoom", sfx=[{"name": "whoosh", "at": 0.0}])
S("s02", "development", "Y aparece una pregunta que da miedo: ¿qué pasa con las centrales nucleares?", "control_rojo",
  leo(x=0.3, action="shock", expression="scared"), cam={"move": "punch", "impacts": [0.4]},
  sfx=[{"name": "hit", "at_word": 10}], emph=["nucleares"])
S("s03", "development", "Cuando cae la red, el reactor se detiene automáticamente. Pero el combustible sigue dando calor, y hay que refrigerarlo.",
  burst("#3B82F6", "#7FB8E6"), leo(x=0.25, action="present", expression="determined"),
  props=[{"type": "thermometer", "x": 0.7, "y": 0.62, "scale": 1.1, "level": 0.8, "at_word": 10}],
  claims=[F("Tras la parada, el combustible nuclear sigue generando calor residual y necesita refrigeración",
            "World Nuclear Association")])
S("s04", "development", "Para eso tienen generadores diésel y baterías. En Fukushima, en 2011, el tsunami inundó esos generadores.",
  "control_rojo", leo(x=0.3, action="sweat", expression="scared", sweat=0.6),
  props=[{"type": "generator", "x": 0.7, "y": 0.92, "scale": 0.75, "running": False},
         {"type": "splash", "x": 0.7, "y": 0.75, "color": "#5CE1E6", "at_word": 12}],
  claims=[F("En Fukushima Daiichi (2011) el tsunami inundó los generadores diésel y dejó la central sin corriente",
            "World Nuclear Association; OIEA (2011)")],
  sfx=[{"name": "splash", "at_word": 12}])
S("s05", "development", "Sin refrigeración, tres reactores se fundieron. Desde entonces, las centrales guardan más equipos portátiles para emergencias.",
  "control_rojo", leo(x=0.3, action="present", expression="worried"),
  claims=[F("Los núcleos de tres reactores de Fukushima Daiichi se fundieron; después las centrales de EE. UU. añadieron equipos portátiles de refrigeración",
            "World Nuclear Association; National Research Council (EE. UU.)")])
S("s06", "development", "En el campo, las granjas modernas también sufren: las ordeñadoras son eléctricas, y las vacas hay que ordeñarlas cada día.",
  "campo", leo(x=0.2, action="shrug", expression="worried"),
  props=[{"type": "cow", "x": 0.62, "y": 0.92, "scale": 0.85}], sfx=[{"name": "boing", "at_word": 17}])
S("s07", "development", "Y las naves de pollos dependen de ventiladores. Sin ellos, el calor puede acabar con muchísimos animales en pocas horas.",
  "campo", leo(x=0.2, action="sweat", expression="hot", sweat=0.8),
  props=[{"type": "heatwaves", "x": 0.65, "y": 0.55, "scale": 1.0}])
S("s08", "development", "Las ciudades empiezan a vaciarse. Quien tiene familia en un pueblo, con pozo y huerto, coge lo que puede y se va.",
  "ciudad_dia", leo(x=0.3, action="walk", expression="determined"),
  props=[{"type": "jerrycan", "x": 0.45, "y": 0.92, "scale": 0.45}, {"type": "car", "x": 0.8, "y": 0.9, "scale": 0.8, "enter": "slide_left"}],
  cam={"move": "pan_right"})
S("s09", "development", "Para enterarse de algo, se vuelve a lo de siempre: la radio a pilas, los bandos del ayuntamiento y el boca a boca.",
  "campo", leo(x=0.22, action="talk", expression="happy"),
  props=[{"type": "radio", "x": 0.6, "y": 0.75, "scale": 0.75}, {"type": "newspaper", "x": 0.83, "y": 0.5, "scale": 0.8, "at_word": 12}])
S("s10", "development", "Los diabéticos que usan insulina tienen otra cuenta atrás: muchas insulinas aguantan unos veintiocho días fuera de la nevera.",
  burst("#5CE1E6", "#8FF0F5"), leo(x=0.22, action="point_up", expression="determined"),
  ov=[counter(28, " DÍAS", "INSULINA ENTRE 15 Y 30 °C", at_word=12, y=260, size=160)],
  claims=[F("Muchos viales y plumas de insulina pueden estar hasta 28 días sin refrigerar entre 15 y 30 °C (depende del producto)",
            "FDA, información sobre insulina en emergencias")],
  emph=["veintiocho"])
S("s10b", "development", "Hay que hervir el agua de ríos y pozos para beberla. Pero cocinar sin vitrocerámica significa hacer fuego… y la leña se acaba rápido.",
  "campo", leo(x=0.25, action="present", expression="tired"),
  props=[{"type": "lamp", "x": 0.6, "y": 0.75, "scale": 0.8}, {"type": "splash", "x": 0.78, "y": 0.7, "color": "#5CE1E6", "at_word": 9}],
  sfx=[{"name": "sizzle", "at_word": 15, "gain_db": -6}])
S("s10c", "development", "El vecino con un pequeño panel solar portátil se convierte en la persona más popular del barrio: cargar un móvil vale oro.",
  "campo", leo(x=0.25, action="laugh", expression="laugh"),
  props=[{"type": "smartphone", "x": 0.62, "y": 0.5, "scale": 0.7, "at_word": 19}, {"type": "sun", "x": 0.82, "y": 0.28, "scale": 0.7}],
  sfx=[{"name": "ding", "at_word": 19}])
S("s11", "development", "Las farmacias, sin ordenadores y sin nadie que les traiga más, empiezan a racionar.", "super_vacio",
  leo(x=0.3, action="shrug", expression="worried"), ov=[VIG])
S("s12", "development", "Balance de la primera semana: menos generadores, ciudades medio vacías y un país pegado a la radio.",
  burst("#FFD23F", "#FFB300"), leo(x=0.2, action="sweat", expression="tired", sweat=0.4),
  props=[meter(0.22, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== MES 1
BEARD, BAGS = 0.65, 0.6
S("me01", "development", "Un mes. Tu barba ya es oficial, y la vida se parece cada vez más a la de hace siglo y medio.", "campo",
  leo(x=0.3, action="laugh", expression="laugh"), ov=[chapter("MES 1")], tr="zoom",
  sfx=[{"name": "whoosh", "at": 0.0}, {"name": "boing", "at_word": 5}], emph=["barba"])
S("me02", "development", "Si es invierno, el frío se convierte en el gran peligro: hasta las calderas de gas necesitan electricidad para funcionar.",
  "ciudad_off", leo(x=0.3, action="sweat", expression="worried", extras={"frost": 0.5}),
  props=[{"type": "thermometer", "x": 0.72, "y": 0.62, "scale": 1.1, "level": 0.1}], ov=[VIG])
S("me03", "development", "En febrero de 2021, una ola de frío dejó sin luz a millones de hogares de Texas durante varios días.",
  burst("#5CE1E6", "#8FF0F5"), leo(x=0.25, action="present", expression="scared", extras={"frost": 0.7}),
  ov=[label("TEXAS · FEBRERO 2021", bg="#3B82F6", at_word=2)],
  claims=[F("La tormenta invernal de febrero de 2021 dejó sin electricidad a más de 4,5 millones de hogares y negocios de Texas",
            "FERC/NERC, informe de la tormenta Uri (2021)")])
S("me04", "development", "Murieron doscientas cuarenta y seis personas, según las cifras oficiales. Y aquello duró días, no un mes.",
  burst("#1B1B3A", "#3B3F78"),
  ov=[counter(246, "", "MUERTES OFICIALES EN TEXAS", at_word=1, y=330, size=200)],
  claims=[F("El estado de Texas atribuyó oficialmente 246 muertes a la tormenta invernal de 2021",
            "Texas Department of State Health Services (2021)")],
  cam={"move": "static"}, sfx=[{"name": "hit", "at_word": 1}])
S("me05", "development", "En verano pasa lo contrario: sin aire acondicionado ni ventiladores, las olas de calor golpean sobre todo a los mayores.",
  "ciudad_dia", leo(x=0.3, action="sweat", expression="hot", sweat=1.0),
  props=[{"type": "sun", "x": 0.75, "y": 0.28, "scale": 1.0}, {"type": "heatwaves", "x": 0.6, "y": 0.6, "scale": 1.0}])
S("me06", "development", "Sin neveras, la comida vuelve a guardarse como antes: en sal, en aceite, ahumada o en conserva.",
  "campo", leo(x=0.22, action="present", expression="happy"),
  props=[{"type": "meat", "x": 0.58, "y": 0.6, "scale": 0.7, "at_word": 9},
         {"type": "food_can", "x": 0.78, "y": 0.8, "scale": 0.7, "at_word": 15, "label": "CONSERVA"}])
S("me06b", "development", "Y tu reloj biológico cambia. En un experimento, una semana de acampada sin luz artificial adelantó unas dos horas el reloj interno de los participantes.",
  "campo", leo(x=0.3, action="talk", expression="tired", actions=[["w14", "sweat"]]),
  props=[{"type": "clock", "x": 0.72, "y": 0.4, "scale": 0.9, "speed": -3}],
  claims=[F("Tras una semana de acampada solo con luz natural, el reloj interno de los participantes se adelantó unas 2 horas",
            "Wright et al., Current Biology (2013)")],
  emph=["dos"])
S("me06c", "development", "Te acostarías poco después de anochecer y te despertarías con el sol, como casi todo el mundo antes de la bombilla.",
  "campo", leo(x=0.3, action="idle", expression="happy_closed"),
  props=[{"type": "zzz", "x": 0.42, "y": 0.4, "scale": 0.8}, {"type": "sun", "x": 0.8, "y": 0.3, "scale": 0.8, "at_word": 12}])
S("me06d", "development", "¿Y las placas solares del tejado? Sorpresa: la mayoría se desconectan solas cuando cae la red. Es una protección obligatoria.",
  "ciudad_dia", leo(x=0.25, action="shock", expression="surprised"),
  claims=[F("Las instalaciones de autoconsumo conectadas a la red se desconectan en un apagón por la protección anti-isla del RD 244/2019",
            "Energías Renovables (2025); Real Decreto 244/2019")],
  ov=[label("PROTECCIÓN ANTI-ISLA", bg="#FF8A3D", at_word=18)], sfx=[{"name": "boing", "at_word": 6}])
S("me06e", "development", "Sirve para no electrocutar a los técnicos que reparan los cables. Solo las que tienen un sistema de respaldo pueden seguir dando luz.",
  "ciudad_dia", leo(x=0.25, action="present", expression="determined"),
  props=[{"type": "battery", "x": 0.72, "y": 0.42, "scale": 0.7, "level": 0.9, "label": "SISTEMA DE RESPALDO", "at_word": 16}])
S("me07", "development", "El trabajo cambia por completo. Sin ordenadores ni internet, oficinas enteras dejan de tener sentido.",
  "oficina", leo(x=0.3, action="shrug", expression="tired"),
  props=[{"type": "wifi", "x": 0.72, "y": 0.38, "scale": 0.9, "crossed": True}])
S("me08", "development", "Y tu dinero del banco existe… pero no puedes tocarlo. Vuelve el trueque: gasóleo por comida, pilas por agua.",
  burst("#22B573", "#6EE7A8"), leo(x=0.2, action="smug", expression="smug"),
  props=[{"type": "jerrycan", "x": 0.48, "y": 0.75, "scale": 0.55, "at_word": 13},
         {"type": "arrow", "x": 0.6, "y": 0.62, "scale": 0.7, "at_word": 14},
         {"type": "food_can", "x": 0.72, "y": 0.75, "scale": 0.6, "at_word": 15},
         {"type": "water_bottle", "x": 0.88, "y": 0.75, "scale": 0.5, "at_word": 18}],
  sfx=[{"name": "pop", "at_word": 13}, {"name": "pop", "at_word": 15}], emph=["trueque"])
S("me08b", "development", "La ropa se lava a mano, las noticias llegan con días de retraso y un viaje de cien kilómetros vuelve a ser una aventura.",
  "campo", leo(x=0.3, action="shrug", expression="tired"),
  props=[{"type": "newspaper", "x": 0.7, "y": 0.45, "scale": 0.8, "at_word": 6}, {"type": "cart", "x": 0.82, "y": 0.88, "scale": 0.8, "at_word": 14}])
S("me08c", "development", "Pero también pasa algo bueno: los vecinos se organizan. Cocinas comunitarias, huertos compartidos y turnos para buscar agua.",
  "campo", leo(x=0.3, action="celebrate", expression="happy"),
  props=[{"type": "plant", "x": 0.68, "y": 0.9, "scale": 0.8}, {"type": "plant", "x": 0.8, "y": 0.9, "scale": 0.7}])
S("me09", "development", "Balance del primer mes: frío o calor sin defensas, comida en salazón y una economía de trueque.",
  burst("#FFD23F", "#FFB300"), leo(x=0.2, action="shrug", expression="tired"),
  props=[meter(0.14, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== AÑO 1
BEARD, BAGS = 1.0, 0.4
S("a01", "development", "Un año. Barba de náufrago.", "campo", leo(x=0.4, action="pose", expression="smug"),
  ov=[chapter("AÑO 1")], tr="zoom", sfx=[{"name": "whoosh", "at": 0.0}, {"name": "boing", "at_word": 3}])
S("a02", "development", "Sin electricidad, el mundo vuelve a antes de 1882, cuando Thomas Edison abrió en Nueva York una de las primeras centrales eléctricas.",
  "london", leo(x=0.25, action="present", expression="determined"),
  props=[{"type": "bulb", "x": 0.72, "y": 0.45, "scale": 1.0, "at_word": 11}],
  ov=[label("1882", bg="#1B1B3A", at_word=6)],
  claims=[F("La central de Pearl Street de Edison empezó a dar servicio en Nueva York en septiembre de 1882",
            "Smithsonian / IEEE History Center")],
  sfx=[{"name": "ding", "at_word": 11}])
S("a03", "development", "Pero ahora somos más de ocho mil millones de personas, y casi todo lo que nos mantiene vivos funciona con enchufe.",
  burst("#3B82F6", "#7FB8E6"),
  ov=[counter(8000, " MILLONES", "DE PERSONAS", at_word=4, y=330, size=150)],
  claims=[F("La población mundial superó los 8.000 millones en noviembre de 2022", "Naciones Unidas")],
  cam={"move": "static"}, emph=["ocho"])
S("a04", "development", "Bombear agua limpia, fabricar medicinas, llevar comida del campo a las ciudades… Todo habría que reinventarlo con músculo, vapor y leña.",
  "campo", leo(x=0.3, action="dig", expression="tired", tool={"type": "shovel"}),
  props=[{"type": "water_pump", "x": 0.72, "y": 0.95, "scale": 0.8, "pumping": True}])
S("a04b", "development", "Los hospitales funcionarían como en el siglo diecinueve: sin rayos X, sin máquinas de diálisis y sin neveras para las vacunas.",
  nb("hospital", lights=0, dark=0.5, glows=[candle_glow(0.62, 0.62, 0.8)]),
  leo(x=0.3, action="sweat", expression="worried", sweat=0.4),
  props=[{"type": "candle", "x": 0.62, "y": 0.62, "scale": 0.8}])
S("a04c", "development", "Y el campo produciría mucho menos: sin gasóleo para tractores ni bombas de riego, la comida se volvería muy cara.",
  "campo", leo(x=0.3, action="dig", expression="tired"),
  props=[{"type": "jerrycan", "x": 0.72, "y": 0.9, "scale": 0.5, "crossed": True, "cross_at": 0.3}])
S("a05", "development", "Las ciudades gigantes serían muy difíciles de mantener. Lo más probable es que mucha gente volviera al campo, cerca de ríos y pozos.",
  "ciudad_off", leo(x=0.3, action="walk", expression="worried"), ov=[VIG], cam={"move": "pan_left"})
S("a05b", "development", "¿Quién lo pasaría mejor? Quien sabe cultivar, hacer fuego, conservar comida y arreglar cosas con las manos.",
  "campo", leo(x=0.3, action="smug", expression="smug"),
  props=[{"type": "plant", "x": 0.7, "y": 0.9, "scale": 0.9}])
S("a05c", "development", "Los amish de Estados Unidos, que viven casi sin conectarse a la red eléctrica, apenas notarían la diferencia.",
  "campo", leo(x=0.3, action="laugh", expression="laugh"), props=[{"type": "cart", "x": 0.72, "y": 0.88, "scale": 0.9}],
  claims=[F("Las comunidades amish evitan, por norma general, conectarse a la red eléctrica pública", "Encyclopaedia Britannica")])
S("a06", "development", "Y ojo: para unos setecientos treinta millones de personas, vivir sin electricidad no es un hipotético. Es su día a día.",
  "espacio", props=[{"type": "earth_night", "x": 0.5, "y": 0.55, "scale": 1.2, "lights": 0.55, "enter": "none", "loop": "bob"}],
  ov=[counter(730, " MILLONES", "SIN ELECTRICIDAD HOY (AIE, 2024)", at_word=4, y=150, size=120)],
  claims=[F("Unos 730 millones de personas no tenían acceso a la electricidad en 2024", "Agencia Internacional de la Energía (2025)")],
  cam={"move": "static"}, emph=["setecientos"])
S("a07", "development", "Balance del primer año: un mundo de 1880… con ocho mil millones de personas. Una combinación muy difícil.",
  burst("#FFD23F", "#FFB300"), leo(x=0.2, action="sweat", expression="tired", sweat=0.3),
  props=[meter(0.06, at_word=3)], sfx=[{"name": "ding", "at_word": 3}], tr="zoom")

# ================================================================== ¿PODRÍA PASAR?
BEARD, BAGS = 0.0, 0.0
S("c01", "climax", "Vale. Pero ¿de verdad podría apagarse el mundo entero? Hay un sospechoso principal: el Sol.", "sol",
  ov=[chapter("¿PODRÍA PASAR?")], cam={"move": "push_in", "zoom_to": 1.1},
  sfx=[{"name": "riser", "at": 0.0, "gain_db": -6}, {"name": "boom", "at_word": 13, "gain_db": -6}], tr="flash",
  emph=["Sol"])
S("c02", "climax", "A veces el Sol escupe una nube gigantesca de partículas cargadas: una eyección de masa coronal.", "sol",
  ov=[label("EYECCIÓN DE MASA CORONAL", bg="#FF8A3D", at_word=11, y=1000)],
  claims=[F("Una eyección de masa coronal es una expulsión de plasma y campo magnético desde la corona solar",
            "NOAA Space Weather Prediction Center")])
S("c03", "climax", "Si golpea la Tierra, sacude su campo magnético y hace que corran corrientes por los cables largos de la red eléctrica.",
  "sol_impacto", ov=[label("CORRIENTES INDUCIDAS", bg="#E8392F", at_word=12, y=1000)],
  claims=[F("Las tormentas geomagnéticas inducen corrientes en las líneas largas que pueden dañar transformadores",
            "NOAA SWPC; Departamento de Energía de EE. UU.")],
  sfx=[{"name": "rumble", "at_word": 3, "gain_db": -6}])
S("c04", "climax", "Ya pasó en 1859. Se llama evento Carrington, por el astrónomo que vio el destello en el Sol.",
  "london", leo(x=0.25, action="present", expression="surprised", outfit="victorian"),
  props=[{"type": "telegraph", "x": 0.7, "y": 0.7, "scale": 0.9}], ov=[label("1859", bg="#1B1B3A", at_word=3)],
  claims=[F("El 1 de septiembre de 1859 Richard Carrington observó la fulguración que precedió a la gran tormenta geomagnética",
            "NASA / Royal Astronomical Society")])
S("c05", "climax", "Los telégrafos se volvieron locos: algunos operadores recibieron descargas, y de los aparatos saltaban chispas.",
  "london", leo(x=0.25, action="shock", expression="shock", outfit="victorian", sweat=0.6),
  props=[{"type": "telegraph", "x": 0.68, "y": 0.7, "scale": 1.0, "sparks": True}],
  claims=[F("Durante la tormenta de 1859 fallaron sistemas de telégrafo, hubo operadores que recibieron descargas y chispas en los equipos",
            "NASA Science; registros históricos de 1859")],
  cam={"move": "punch", "impacts": [0.3]}, sfx=[{"name": "crack", "at_word": 8}, {"name": "crack", "at_word": 13}],
  emph=["chispas"])
S("c06", "climax", "Y hubo auroras en lugares donde casi nunca se ven, muy cerca del trópico.", "aurora",
  leo(x=0.3, action="look_up", expression="wow", outfit="victorian"), cam={"move": "pull_out"},
  claims=[F("Las auroras de 1859 se vieron a latitudes muy bajas, cerca del trópico", "NASA Science")],
  sfx=[{"name": "sparkle", "at_word": 2}])
S("c07", "climax", "En 1859 casi nada dependía de la electricidad. Hoy, una tormenta así sería otra historia.", "aurora_chispas",
  leo(x=0.3, action="sweat", expression="worried", sweat=0.5), emph=["otra"])
S("c08", "climax", "Tenemos un aviso más reciente: en marzo de 1989, una tormenta solar tumbó la red eléctrica de Quebec, en Canadá.",
  "torres_noche", leo(x=0.2, action="present", expression="surprised"),
  ov=[label("QUEBEC · 1989", bg="#3B82F6", at_word=8)],
  claims=[F("El 13 de marzo de 1989 una tormenta geomagnética provocó el colapso de la red de Hydro-Québec",
            "NASA; Hydro-Québec")])
S("c09", "climax", "Seis millones de personas se quedaron sin luz en noventa segundos, y tardaron unas nueve horas en recuperarla.",
  burst("#1B1B3A", "#3B3F78"),
  ov=[counter(90, " S", "Y 6 MILLONES A OSCURAS", at_word=8, y=330, size=200)],
  claims=[F("La red de Quebec cayó en unos 90 segundos; 6 millones de personas pasaron unas 9 horas sin electricidad",
            "NASA, «The Day the Sun Brought Darkness» (2009)")],
  cam={"move": "static"}, sfx=[{"name": "hit", "at_word": 8}], emph=["noventa"])
S("c10", "climax", "Y en mayo de 2024, la tormenta más fuerte desde 2003 pintó auroras sobre buena parte de España.", "aurora",
  leo(x=0.3, action="look_up", expression="wow"),
  ov=[label("ESPAÑA · MAYO 2024", bg="#22B573", at_word=2)],
  claims=[F("La tormenta geomagnética G5 del 10-11 de mayo de 2024, la más intensa desde 2003, dejó auroras visibles en gran parte de España",
            "NOAA SWPC; AEMET")],
  sfx=[{"name": "sparkle", "at_word": 11}])
S("c10b", "climax", "Y en julio de 2012 nos libramos por poco: una eyección tan fuerte como la de Carrington cruzó la órbita de la Tierra.",
  "sol", ov=[label("JULIO 2012", bg="#E8392F", at_word=2, y=1000)],
  claims=[F("La eyección del 23 de julio de 2012 habría sido comparable al evento Carrington si hubiera alcanzado la Tierra",
            "NASA Science, «Near Miss: The Solar Superstorm of July 2012» (2014); Baker et al., Space Weather (2013)")])
S("c10c", "climax", "Si hubiera salido del Sol más o menos una semana antes, nos habría dado de lleno.",
  "sol_impacto", leo(x=0.2, action="shock", expression="shock", sweat=0.8),
  cam={"move": "punch", "impacts": [0.6]}, sfx=[{"name": "boom", "at_word": 13, "gain_db": -6}], emph=["semana"])
S("c11", "climax", "Lo que más preocupa a los ingenieros son los grandes transformadores: piezas de cientos de toneladas que se fabrican por encargo.",
  "torres", leo(x=0.2, action="present", expression="worried"),
  props=[{"type": "transformer", "x": 0.66, "y": 0.92, "scale": 1.0, "label": "100-400 TONELADAS"}],
  claims=[F("Los grandes transformadores de potencia pesan entre 100 y 400 toneladas y se fabrican a medida",
            "Departamento de Energía de EE. UU. (2024)")])
S("c12", "climax", "Hoy, conseguir uno nuevo puede llevar de dos a cuatro años. Si se quemaran muchos a la vez, no habría repuestos para todos.",
  "torres", leo(x=0.2, action="sweat", expression="scared", sweat=0.6),
  props=[{"type": "transformer", "x": 0.66, "y": 0.92, "scale": 1.0, "burning": True}],
  ov=[label("ESPERA: 2-4 AÑOS", bg="#E8392F", at_word=5, y=90)],
  claims=[F("En 2024 los plazos de entrega de transformadores rondaban las 120 semanas, y hasta 210 para los grandes",
            "NERC, recogido por la prensa especializada (2024)")],
  sfx=[{"name": "sizzle", "at_word": 15}], emph=["cuatro"])
S("c13", "climax", "¿Y la probabilidad? Los estudios no se ponen de acuerdo: van desde un uno hasta un doce por ciento por década.",
  burst("#5CE1E6", "#8FF0F5"), leo(x=0.22, action="think", expression="surprised"),
  ov=[{"type": "label", "text": "1 % – 12 % POR DÉCADA", "x": 1200, "y": 400, "size": 90, "bg": "#1B1B3A", "at_word": 9}],
  claims=[F("Las estimaciones de una tormenta tipo Carrington van de ~1 % (Moriña et al., 2019) a ~12 % por década (Riley, 2012)",
            "Riley, Space Weather (2012); Moriña et al., Scientific Reports (2019)")],
  sfx=[{"name": "ding", "at_word": 9}])
S("c14", "climax", "La buena noticia: estas nubes tardan uno o varios días en llegar, y hay satélites vigilando el Sol que las ven salir.",
  "sol",
  ov=[label("AVISO: 1-3 DÍAS", bg="#22B573", at_word=7, y=1000)],
  claims=[F("Las eyecciones de masa coronal suelen tardar entre 1 y 3 días en llegar a la Tierra", "NOAA SWPC")])
S("c15", "climax", "Con ese aviso, las eléctricas pueden proteger la red, repartir la carga e incluso desconectar equipos antes del golpe.",
  "control_verde", leo(x=0.3, action="present", expression="happy"))
S("c15b", "climax", "El Sol no es el único sospechoso. En diciembre de 2015, un ciberataque dejó sin luz a unos doscientos veinticinco mil clientes en Ucrania.",
  "control_rojo", leo(x=0.3, action="shock", expression="angry"),
  ov=[label("UCRANIA · 2015", bg="#E8392F", at_word=8)],
  claims=[F("El 23 de diciembre de 2015 un ciberataque contra distribuidoras ucranianas dejó sin luz a unos 225.000 clientes durante horas",
            "CISA (EE. UU.), alerta ICS IR-ALERT-H-16-056-01")],
  sfx=[{"name": "hit", "at_word": 8}])
S("c15c", "climax", "Los operadores tuvieron que ir a las subestaciones y volver a conectarlo todo a mano. Tardaron unas horas, no años.",
  "control_rojo", leo(x=0.3, action="present", expression="determined"))
S("c16", "climax", "Por eso, el escenario realista no es un planeta a oscuras durante años, sino apagones grandes en algunas regiones.",
  "torres", leo(x=0.25, action="smug", expression="happy"), emph=["realista"])

# ================================================================== CÓMO SE VUELVE A ENCENDER
S("r01", "climax", "Y si todo se apaga, ¿cómo se vuelve a encender? No basta con darle a un interruptor.", "control_rojo",
  leo(x=0.3, action="think", expression="surprised"), ov=[chapter("¿CÓMO SE ENCIENDE?")], tr="zoom")
S("r02", "climax", "Muchas centrales necesitan electricidad para arrancar. Es como arrancar un coche que tiene la batería muerta.",
  "control_rojo", leo(x=0.3, action="shrug", expression="smug"),
  props=[{"type": "car", "x": 0.7, "y": 0.86, "scale": 0.8}, {"type": "battery", "x": 0.7, "y": 0.4, "scale": 0.7, "level": 0.02}])
S("r03", "climax", "Por eso se empieza con centrales que pueden arrancar solas, como las hidroeléctricas, y la red se enciende por islas.",
  "torres", leo(x=0.2, action="present", expression="determined"),
  props=[{"type": "dam", "x": 0.68, "y": 0.75, "scale": 0.6}],
  claims=[F("La reposición tras un apagón total empieza por centrales con arranque autónomo, como las hidroeléctricas",
            "Red Eléctrica (REE)")])
S("r03b", "climax", "Y no se puede ir con prisas: toda la red de Europa gira sincronizada a cincuenta hercios, como una orquesta enorme.",
  "control_verde", leo(x=0.3, action="present", expression="determined"),
  ov=[counter(50, " Hz", "LA RED EUROPEA, SINCRONIZADA", at_word=12, y=230, size=150)],
  claims=[F("La red síncrona de Europa continental funciona a una frecuencia de 50 Hz", "ENTSO-E")],
  emph=["cincuenta"])
S("r03c", "climax", "Si conectas demasiados consumidores de golpe, la frecuencia cae y la isla que acabas de encender se vuelve a apagar.",
  "control_rojo", leo(x=0.3, action="shock", expression="shock"), cam={"move": "punch", "impacts": [0.5]},
  sfx=[{"name": "crack", "at_word": 12}])
S("r04", "climax", "En España, el veintiocho de abril, ayudaron las hidroeléctricas, las centrales de gas y la electricidad que llegó desde Francia y Marruecos.",
  "control_verde", leo(x=0.3, action="point_up", expression="happy"),
  claims=[F("La reposición se apoyó en las interconexiones con Francia y Marruecos, ciclos combinados e hidroeléctricas", SRC_ES)])
S("r05", "climax", "A la mañana siguiente, ya estaba recuperada prácticamente toda la demanda. En un apagón mundial, no habría vecinos a los que pedir ayuda.",
  "control_verde", leo(x=0.3, action="celebrate", expression="happy", actions=[["w12", "think"]], expressions=[["w12", "worried"]]),
  claims=[F("Red Eléctrica dio por recuperada la totalidad de la demanda la mañana del 29 de abril de 2025",
            "Red Eléctrica (REE), 29/04/2025")],
  emph=["vecinos"])

# ================================================================== FINAL
S("f01", "ending", "Resumiendo: en un minuto, caos en la calle. En unas horas, sin cobertura ni gasolina.", "ciudad_dia",
  leo(x=0.25, action="present", expression="determined"),
  props=[{"type": "traffic_light", "x": 0.66, "y": 0.97, "scale": 0.9, "state": "off"},
         {"type": "cell_tower", "x": 0.86, "y": 0.97, "scale": 0.8, "on": False, "at_word": 7}],
  tr="flash")
S("f02", "ending", "En unos días, sin comida fresca. Y en un año, un salto atrás de casi siglo y medio.", "super_vacio",
  leo(x=0.25, action="shrug", expression="worried", beard=0.8), ov=[VIG])
S("f03", "ending", "La electricidad es tan invisible que solo nos acordamos de ella cuando se va.",
  nb("living_room", lights=0.0), leo(x=0.6, action="look_up", expression="happy", actions=[["w5", "celebrate"]]),
  props=[{"type": "bulb", "x": 0.5, "y": 0.28, "scale": 0.9, "flicker": True, "at_word": 6}],
  sfx=[{"name": "sparkle", "at_word": 6}], emph=["invisible"])
S("f04", "ending", "Un consejo práctico: ten en casa una linterna, una radio a pilas, agua, comida en lata y algo de efectivo.",
  "salon", leo(x=0.2, action="talk", expression="happy"),
  props=[{"type": "flashlight", "x": 0.42, "y": 0.45, "scale": 0.55, "at_word": 7, "on": False},
         {"type": "radio", "x": 0.6, "y": 0.62, "scale": 0.6, "at_word": 9, "on": False},
         {"type": "water_bottle", "x": 0.74, "y": 0.68, "scale": 0.5, "at_word": 13},
         {"type": "food_can", "x": 0.86, "y": 0.66, "scale": 0.55, "at_word": 14},
         {"type": "money", "x": 0.6, "y": 0.88, "scale": 0.55, "at_word": 18}],
  sfx=[{"name": "pop", "at_word": 7}, {"name": "pop", "at_word": 13}, {"name": "pop", "at_word": 18}])
S("f05", "ending", "Y ahora te toca a ti: ¿qué es lo que más echarías de menos en un apagón mundial? Te leo en comentarios.",
  "salon", leo(x=0.5, action="talk", expression="excited", actions=[["w16", "point_down"]]),
  ov=[{"type": "label", "text": "COMENTA ABAJO", "x": 960, "y": 120, "size": 70, "at_word": 16, "arrow": "down"}],
  cam={"move": "zoom_burst"}, sfx=[{"name": "ding", "at_word": 16}])
S("f06", "ending", "Y si quieres más «¿qué pasaría si…?» como este, suscríbete a Hipotéticos. ¡Nos vemos en el próximo!",
  "salon", leo(x=0.5, action="wave", expression="happy"), tr="zoom", pause=0.5)

DESC = """¿Qué pasaría si mañana se apagara la electricidad en todo el planeta a la vez… y no volviera? ⚡

Leo lo cuenta minuto a minuto, hora a hora, día a día, hasta un año entero sin luz, con datos reales: el apagón ibérico del 28 de abril de 2025, la ola de frío de Texas de 2021, la tormenta solar que tumbó Quebec en 1989 y el evento Carrington de 1859.

{CAPITULOS}

🧪 ALGUNOS DATOS DEL VÍDEO
• El 28 de abril de 2025, a las 12:33, la península ibérica perdió unos 15 GW de generación en cinco segundos, cerca del 60 % de la demanda española en ese momento (Gobierno de España).
• En España se quedaron parados más de cien trenes y hubo que evacuar a unos 35.000 pasajeros; solo en Madrid hubo 286 rescates en ascensores.
• Las baterías de respaldo de las antenas de móvil suelen durar entre 2 y 4 horas.
• Una nevera cerrada mantiene la comida segura unas 4 horas sin luz; un congelador lleno, unas 48 (USDA).
• La Vía Láctea está oculta para más de un tercio de la humanidad por la contaminación lumínica: el 60 % de los europeos y casi el 80 % de los norteamericanos no la ven (Falchi et al., 2016).
• Los hospitales acreditados en EE. UU. deben planificar 96 horas de autonomía; la UE recomienda que cada hogar aguante 72 horas por sí mismo (2025).
• En Fukushima (2011) el tsunami inundó los generadores diésel que refrigeraban los reactores.
• Muchas insulinas aguantan unos 28 días sin nevera entre 15 y 30 °C (FDA; depende del producto).
• La tormenta invernal de Texas de 2021 dejó sin luz a más de 4,5 millones de hogares y negocios; las cifras oficiales hablan de 246 muertes.
• En 1859, durante el evento Carrington, fallaron los telégrafos y saltaron chispas de los aparatos. En 1989, una tormenta solar tumbó la red de Quebec en unos 90 segundos.
• Los grandes transformadores pesan entre 100 y 400 toneladas y en 2024 tardaban de dos a cuatro años en entregarse.
• Unos 730 millones de personas siguen sin acceso a la electricidad (AIE, 2024).

⚠️ El apagón mundial es un escenario hipotético. El «medidor» de cuánto sigue funcionando es una estimación divulgativa, no un cálculo científico.

📚 Fuentes: La Moncloa (28/04/2025); Red Eléctrica; Ministerio de Transportes; El País; USDA FSIS; FCC; Falchi et al., Science Advances (2016); NFPA 99/110; The Joint Commission; Comisión Europea, Estrategia de Preparación de la Unión (2025); World Nuclear Association; OIEA; National Research Council; FDA; FERC/NERC (2021); Texas DSHS; NOAA Space Weather Prediction Center; NASA; Hydro-Québec; AEMET; Departamento de Energía de EE. UU. (2024); Riley (2012); Moriña et al. (2019); Smithsonian; Naciones Unidas; Agencia Internacional de la Energía.

💬 ¿Qué es lo que más echarías de menos en un apagón mundial? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #apagon #electricidad #tormentasolar #ciencia #documental"""

st.save("apagon-mundial", "¿Qué pasaría si se apagara la electricidad en todo el mundo?",
        "¿Qué pasaría si se apagara la electricidad en todo el mundo?", "ciencia", "¿Qué echarías más de menos?", {
            "format": "landscape",
            "title": "¿Qué pasaría si se apagara la electricidad en todo el mundo? ⚡",
            "hashtags": ["#quepasariasi", "#apagon", "#documental"],
            "tags": ["qué pasaría si", "apagón", "apagón mundial", "sin electricidad", "apagón españa", "28 de abril",
                     "tormenta solar", "evento carrington", "quebec 1989", "red eléctrica", "kit de emergencia",
                     "72 horas", "vía láctea", "contaminación lumínica", "fukushima", "texas 2021", "supervivencia",
                     "ciencia", "documental", "hipotéticos", "qué pasaría si se va la luz"],
            "pinned_comment": "¿Qué es lo que más echarías de menos en un apagón mundial? ⚡👇",
            "description": DESC,
            "target_seconds": [840, 1080],
            "custom_thumbnail": True,
            "chapters": {"i01": "Intro: el día que se apagó España", "m01": "Minuto 1: semáforos, ascensores y metro",
                         "h01": "Hora 1: sin cobertura, sin tarjeta, sin gasolina",
                         "n01": "Noche 1: la Vía Láctea… y el agua", "d01": "Día 3: neveras, tiendas y hospitales",
                         "s01": "Semana 1: nucleares, granjas y la radio", "me01": "Mes 1: frío, calor y trueque",
                         "a01": "Año 1: de vuelta a 1882", "c01": "¿Podría pasar? Las tormentas solares",
                         "r01": "Cómo se vuelve a encender la red", "f01": "Resumen y kit de emergencia"},
        }, mood="mystery")
