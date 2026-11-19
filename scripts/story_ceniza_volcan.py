"""Guion: ¿Qué le pasaría a tu cuerpo si respiraras ceniza de volcán 1 año?

Estructura en escalada (hora 1 → día 1 → semana 1 → mes 1 → año 1), según data/research/style_guide.json.
"""
from storykit import F, Story

st = Story()
sc = st.sc
ASH = {"type": "ashfall", "abs": True, "x": 0, "y": 0, "layer": "front", "enter": "none"}


def leo(**kw):
    d = {"x": 0.5, "y": 0.8, "scale": 1.25}
    d.update(kw)
    return d


def ash(**kw):
    return {**ASH, **kw}


def lbl(txt, bg="#E8392F", **kw):
    return {"type": "label", "text": txt, "x": 540, "y": 300, "size": 72, "bg": bg, **kw}


sc("v01", "hook", "Nieva gris: es ceniza de volcán. Y la respirarás un año entero.", {
    "background": {"type": "volcano", "ash": 0.55},
    "character": leo(action="look_up", expression="wow", actions=[["w6", "shock"]], expressions=[["w6", "scared"]]),
    "props": [ash(density=110)],
    "overlays": [{"type": "title", "lines": ["¿1 AÑO", "RESPIRANDO", "CENIZA?"], "y": 250, "size": 112}],
    "camera": {"move": "punch", "impacts": ["w6"]}},
   sfx=[{"name": "rumble", "at": 0.0, "gain_db": -8}, {"name": "hit", "at_word": 6, "gain_db": -6}],
   transition="cut", emphasis=["ceniza", "año"])

sc("v02", "setup", "Primero, lo que no es: la ceniza no es humo.", {
    "background": {"type": "volcano", "ash": 0.4, "erupt": True},
    "character": leo(x=0.32, action="talk", expression="smug"),
    "props": [{"type": "question", "x": 0.76, "y": 0.42, "char": "?", "at_word": 6}, ash(density=60)],
    "overlays": [{"type": "myth", "text": "ES HUMO", "stamp": "¡FALSO!", "y": 380, "stamp_at": 1.0, "at_word": 6}],
    "camera": {"move": "push_in"}},
   sfx=[{"name": "pop", "at_word": 6}], transition="whip", emphasis=["humo"])

sc("v03", "setup", "Son trocitos de roca y de cristal volcánico, más pequeños que un grano de arena.", {
    "background": {"type": "burst", "c1": "#8A7F78", "c2": "#B5ABA3"},
    "character": {"visible": False},
    "props": [{"type": "magnifier", "x": 0.5, "y": 0.52, "scale": 1.5, "view": "ash", "enter": "pop"}],
    "overlays": [{"type": "fact", "text": "Ceniza volcánica: fragmentos de roca, minerales y vidrio de menos de 2 mm",
                  "at_word": 3, "y": 230}],
    "camera": {"move": "push_in", "zoom_to": 1.18}},
   claims=[F("La ceniza volcánica son fragmentos de roca, minerales y vidrio volcánico de menos de 2 mm", "USGS, Volcano Hazards Program")],
   sfx=[{"name": "sparkle", "at_word": 6}], transition="zoom", emphasis=["cristal"])

sc("v04", "development", "Hora uno: te pican los ojos. Esos cristalitos rayan como papel de lija.", {
    "background": {"type": "volcano", "ash": 0.6},
    "character": leo(action="sweat", expression="worried", actions=[["w4", "shock"]], expressions=[["w4", "angry"]]),
    "props": [ash(density=130)],
    "overlays": [lbl("HORA 1", "#2B6BE8"),
                 {"type": "fact", "text": "La ceniza puede producir abrasiones en la córnea y conjuntivitis", "at_word": 6,
                  "y": 410}],
    "camera": {"move": "push_in", "zoom_to": 1.3, "focus": [0.5, 0.45]}},
   claims=[F("El contacto de la ceniza con los ojos puede producir abrasiones en la córnea y conjuntivitis",
             "Dirección General de Salud Pública, Gobierno de Canarias (2021)")],
   sfx=[{"name": "crack", "at_word": 9, "gain_db": -6}], emphasis=["ojos", "lija"])

sc("v05", "development", "Por eso en La Palma pedían gafas, y no lentillas.", {
    "background": {"type": "volcano", "ash": 0.6, "town": True},
    "character": leo(action="present", expression="determined"),
    "props": [{"type": "sign", "x": 0.75, "y": 0.46, "text": "GAFAS SÍ\nLENTILLAS NO", "w": 400, "size": 50, "at_word": 5,
               "scale": 1.3}, ash(density=90)],
    "overlays": [lbl("LA PALMA · 2021", "#E8392F")],
    "camera": {"move": "static"}},
   claims=[F("Durante la erupción de La Palma (2021) se recomendó usar gafas en lugar de lentillas", "PEVOLCA; Sanidad, Gobierno de Canarias")],
   sfx=[{"name": "ding", "at_word": 5}], transition="slide", emphasis=["gafas"])

sc("v06", "development", "Día uno: te pica la garganta y toses. Tu nariz atrapa los granos más gordos.", {
    "background": {"type": "volcano", "ash": 0.7},
    "character": leo(action="shock", expression="dizzy", actions=[["w7", "talk"]], expressions=[["w7", "worried"]]),
    "props": [ash(density=150)],
    "overlays": [lbl("DÍA 1", "#9D7BFF"),
                 {"type": "fact", "text": "La ceniza irrita nariz y garganta; la nariz frena las partículas grandes",
                  "at_word": 8, "y": 410}],
    "camera": {"move": "punch", "impacts": ["w5"]}},
   claims=[F("La ceniza irrita nariz y garganta y provoca tos; las partículas gruesas quedan en nariz y garganta",
             "IVHHN, «Los peligros de la ceniza volcánica para la salud»")],
   sfx=[{"name": "boing", "at_word": 5, "gain_db": -6}], emphasis=["toses", "nariz"])

sc("v07", "development", "Pero los más finos, como polvo de talco, bajan hasta el fondo del pulmón.", {
    "background": {"type": "burst", "c1": "#5CE1E6", "c2": "#8FF0F5"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.6, "scale": 1.35, "dirt": 0.25, "inflow": True, "enter": "pop"}],
    "overlays": [{"type": "fact", "text": "Las partículas de menos de 10 micras llegan a lo más hondo del pulmón",
                  "at_word": 7, "y": 230}],
    "camera": {"move": "pan_down", "amount": 160}},
   claims=[F("Las partículas de menos de 10 micras (y sobre todo las de menos de 4) penetran hasta el pulmón profundo",
             "IVHHN; OMS (PM10)")],
   sfx=[{"name": "whoosh", "at_word": 7}], transition="zoom", emphasis=["fondo"])

sc("v08", "development", "Semana uno: la mascarilla FFP2 se vuelve tu mejor amiga.", {
    "background": {"type": "volcano", "ash": 0.75},
    "character": leo(action="celebrate", expression="happy", extras={"mask": True}),
    "props": [ash(density=150)],
    "overlays": [lbl("SEMANA 1", "#22B573"),
                 {"type": "fact", "text": "La más recomendable: FFP2 o N95, bien ajustada a la cara", "at_word": 4, "y": 410}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("Frente a la ceniza, la mascarilla más eficaz es la FFP2 o N95, bien ajustada", "Instituto Nacional de Toxicología, Ministerio de Justicia (2021)")],
   sfx=[{"name": "sparkle", "at_word": 4}], transition="flash", emphasis=["mascarilla"])

sc("v09", "development", "Si tienes asma, aquí empieza lo serio: la ceniza puede desatar crisis.", {
    "background": {"type": "burst", "c1": "#E8392F", "c2": "#FF6B5C"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.58, "scale": 1.3, "dirt": 0.5, "enter": "none", "loop": "shake"}],
    "overlays": [{"type": "fact", "label": "OJO", "text": "Las personas con asma o bronquitis son las más vulnerables",
                  "at_word": 3, "y": 230}],
    "camera": {"move": "push_in", "shake": 0.2}},
   claims=[F("Las personas con asma, bronquitis u otras enfermedades respiratorias son las más afectadas por la ceniza",
             "IVHHN; USGS")],
   sfx=[{"name": "hit", "at_word": 7, "gain_db": -6}], emphasis=["asma"])

sc("v10", "development", "Mes uno: llueve, y la ceniza mojada pesa tanto que puede hundir tejados.", {
    "background": {"type": "volcano", "ash": 0.95, "town": True, "near": False},
    "character": leo(x=0.5, y=0.86, scale=1.0, action="shock", expression="scared"),
    "props": [ash(density=90, color=(0.25, 0.25, 0.3), speed=600, size=(2, 5)),
              {"type": "pow", "x": 0.25, "y": 0.62, "text": "¡CRAC!", "at_word": 11, "scale": 0.8}],
    "overlays": [lbl("MES 1", "#FF8A00"),
                 {"type": "fact", "text": "La ceniza mojada pesa mucho más y puede hundir tejados", "at_word": 7, "y": 410}],
    "camera": {"move": "punch", "impacts": ["w11"]}},
   claims=[F("La ceniza mojada es mucho más pesada y su acumulación puede hacer que se hundan los tejados", "USGS, Volcanic Ash Impacts")],
   sfx=[{"name": "crack", "at_word": 11, "gain_db": -3}], transition="whip", emphasis=["tejados"])

sc("v11", "development", "En La Palma la erupción duró ochenta y cinco días, y miles de personas tuvieron que irse.", {
    "background": {"type": "volcano", "ash": 0.7, "near": True, "town": True},
    "character": {"visible": False},
    "overlays": [{"type": "counter", "from": 0, "to": 85, "suffix": " DÍAS", "at_word": 5, "over": 0.8, "y": 330,
                  "size": 140, "sub": "ERUPCIÓN DE LA PALMA · 2021"},
                 {"type": "counter", "from": 0, "to": 7000, "prefix": "≈", "suffix": " EVACUADOS", "at_word": 11,
                  "over": 0.7, "y": 620, "size": 90}],
    "props": [ash(density=80)],
    "camera": {"move": "pull_out"}},
   claims=[F("La erupción de La Palma duró 85 días (19 sep – 13 dic 2021)", "IGN; PEVOLCA"),
           F("Unas 7.000 personas fueron evacuadas", "PEVOLCA")],
   sfx=[{"name": "tick", "at_word": 5}, {"name": "ding", "at_word": 11}], emphasis=["ochenta", "miles"])

sc("v12", "climax", "Año uno: ¿y tus pulmones? Aquí viene lo sorprendente.", {
    "background": {"type": "volcano", "ash": 0.85},
    "character": leo(action="think", expression="worried", extras={"mask": True},
                     actions=[["w5", "point_up"]], expressions=[["w5", "surprised"]]),
    "props": [ash(density=120)],
    "overlays": [lbl("AÑO 1", "#E8392F", size=86)],
    "camera": {"move": "push_in", "zoom_to": 1.2}},
   sfx=[{"name": "riser", "at": 0.2, "gain_db": -6}], transition="flash", emphasis=["sorprendente"])

sc("v13", "climax", "Tras el Monte Santa Helena, los médicos estudiaron a la gente y, en pulmones sanos, no vieron daños claros.", {
    "background": {"type": "burst", "c1": "#22B573", "c2": "#6EE7A8"},
    "character": {"visible": False},
    "props": [{"type": "lungs", "x": 0.5, "y": 0.6, "scale": 1.3, "dirt": 0.1, "enter": "pop"},
              {"type": "npc", "outfit": "plain", "hair": "#3A2A1A", "x": 0.18, "y": 0.86, "size": 0.9,
               "expression": "happy", "action": "present", "shirt": "#FFFFFF", "at_word": 6}],
    "overlays": [{"type": "fact", "text": "Monte Santa Helena (EE. UU., 1980): sin daño claro en pulmones sanos",
                  "at_word": 10, "y": 230}],
    "camera": {"move": "push_in"}},
   claims=[F("Los estudios tras la erupción del Monte Santa Helena (1980) concluyeron que la ceniza no parecía dañar los pulmones de personas sanas",
             "Buist et al., American Journal of Public Health (1986)")],
   sfx=[{"name": "sparkle", "at_word": 15}], transition="zoom", emphasis=["sanos"])

sc("v14", "climax", "El peligro de verdad es la sílice cristalina: respirada durante años, puede causar silicosis.", {
    "background": {"type": "burst", "c1": "#2B2B3A", "c2": "#4A4660"},
    "character": {"visible": False},
    "props": [{"type": "magnifier", "x": 0.35, "y": 0.6, "scale": 1.0, "view": "ash", "enter": "none"},
              {"type": "lungs", "x": 0.72, "y": 0.64, "scale": 0.8, "dirt": 0.9, "at_word": 9}],
    "overlays": [{"type": "fact", "label": "OJO", "text": "La sílice cristalina, inhalada durante años, puede causar silicosis",
                  "at_word": 5, "y": 230}],
    "camera": {"move": "push_in", "shake": 0.1}},
   claims=[F("La ceniza puede contener sílice cristalina, que inhalada de forma prolongada puede causar silicosis", "USGS; IVHHN")],
   sfx=[{"name": "rumble", "at_word": 5, "gain_db": -8}], emphasis=["sílice", "años"])

sc("v15", "ending", "Aunque, por ahora, no hay casos documentados de silicosis por ceniza en erupciones recientes.", {
    "background": {"type": "volcano", "ash": 0.3, "erupt": False, "lava": False},
    "character": leo(action="shrug", expression="happy"),
    "props": [ash(density=30)],
    "overlays": [{"type": "fact", "text": "USGS: ningún caso documentado de silicosis por ceniza en las últimas décadas",
                  "at_word": 5, "y": 230}],
    "camera": {"move": "static"}},
   claims=[F("No hay casos documentados de silicosis atribuidos a ceniza volcánica en erupciones de las últimas décadas, aunque faltan estudios a largo plazo",
             "USGS, Volcanic Ash Health Effects")],
   sfx=[{"name": "ding", "at_word": 7}], transition="slide", emphasis=["documentados"])

sc("v16", "ending", "Así que, si un día nieva gris: mascarilla y gafas. ¿Tú te irías o te quedarías? Te leo en comentarios.", {
    "background": {"type": "volcano", "ash": 0.55},
    "character": leo(action="talk", expression="excited", extras={"mask": True}, scale=1.3,
                     actions=[["w16", "point_down"]]),
    "props": [ash(density=90), {"type": "mask", "x": 0.82, "y": 0.42, "scale": 0.6, "at_word": 7, "loop": "bob"}],
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 16, "arrow": "down"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at_word": 7}, {"name": "ding", "at_word": 16}], transition="zoom", pause=0.35)

DESC = """Nieva gris… y no es nieve: es ceniza de volcán. ¿Qué le pasaría a tu cuerpo si la respiraras durante un año? 🌋

Leo vive al pie de un volcán en erupción y descubre, hora a hora y mes a mes, lo que la ceniza hace en sus ojos, su garganta y sus pulmones.

🧪 DATOS REALES DEL VÍDEO
• La ceniza volcánica no es humo: son fragmentos de roca, minerales y vidrio volcánico de menos de 2 mm (USGS).
• Puede rayar la córnea y causar conjuntivitis; en La Palma se recomendó usar gafas en vez de lentillas.
• Irrita nariz y garganta. Las partículas de menos de 10 micras llegan a lo más hondo del pulmón.
• La mascarilla más eficaz es la FFP2 o N95, bien ajustada.
• Las personas con asma o bronquitis son las más vulnerables.
• La ceniza mojada pesa mucho y puede hundir tejados.
• La erupción de La Palma (2021) duró 85 días y obligó a evacuar a unas 7.000 personas.
• Tras el Monte Santa Helena (1980), los estudios no encontraron daño claro en pulmones sanos.
• La sílice cristalina de algunas cenizas, inhalada durante años, puede causar silicosis, aunque el USGS no tiene casos documentados por ceniza en erupciones recientes. Faltan estudios a largo plazo.

⚠️ Si vives cerca de una erupción, sigue siempre las indicaciones de Protección Civil.

📚 Fuentes: USGS Volcano Hazards Program, IVHHN, Gobierno de Canarias (Salud Pública y PEVOLCA), Instituto Geográfico Nacional, Instituto Nacional de Toxicología, American Journal of Public Health (1986).

💬 ¿Tú te irías o te quedarías? Te leo en comentarios.
🔔 Suscríbete a Hipotéticos para más «¿qué pasaría si…?».

Música y efectos de sonido originales del canal. Voz sintética.

#quepasariasi #volcan #cuerpohumano #lapalma #shorts"""

st.save("ceniza-de-volcan", "¿Qué le pasaría a tu cuerpo si respiraras ceniza de volcán 1 año?",
        "¿Qué le pasaría a tu cuerpo si respiraras ceniza de volcán 1 año?", "cuerpo",
        "¿Tú te irías o te quedarías?", {
            "title": "¿Qué pasaría si respiraras ceniza de volcán 1 año? 🌋",
            "hashtags": ["#quepasariasi", "#volcan", "#cuerpohumano", "#lapalma", "#shorts"],
            "tags": ["qué pasaría si", "ceniza volcánica", "volcán", "la palma", "cumbre vieja", "pulmones",
                     "silicosis", "mascarilla ffp2", "cuerpo humano", "curiosidades", "animación", "hipotéticos"],
            "pinned_comment": "¿Te irías o te quedarías al pie del volcán? 🌋👇",
            "description": DESC,
            "target_seconds": [50, 75],
            "thumbnail": {"scene": "v04", "t": 1.6, "lines": ["¿1 AÑO", "RESPIRANDO CENIZA?"],
                          "badge": "HORA 1: OJOS", "badge_pos": [540, 1640], "y": 260,
                          "character": {"action": "shock", "expression": "scared", "x": 0.5, "y": 0.82, "scale": 1.4},
                          "crop_y": 0.55, "h_shift": 800, "h_scale": 0.8},
        }, mood="mystery")
