"""Genera stories/centro-de-la-tierra.json (primer vídeo de prueba, escrito a mano)."""
import json
from pathlib import Path

G = 1200 / 1920  # suelo del jardín
SUIT = {"outfit": "suit", "helmet": "dome"}

S = []


def sc(id, beat, narration, visual, claims=(), sfx=(), transition="whip", emphasis=(), pause=0.06):
    S.append({"id": id, "beat": beat, "narration": narration, "visual": visual, "claims": list(claims),
              "sfx": list(sfx), "transition": transition, "emphasis": list(emphasis), "pause_after": pause})


F = lambda text, source, kind="fact": {"text": text, "kind": kind, "source": source}

sc("s01", "hook", "Coges una pala y cavas hacia el centro de la Tierra.", {
    "background": {"type": "backyard", "ground": 1200, "hole": {"x": 545, "w": 250, "depth": 60, "grow": 40, "pile": 40, "pile_grow": 30}},
    "character": {"action": "dig", "expression": "determined", "x": 0.36, "y": G, "scale": 1.3},
    "props": [{"type": "debris", "x": 545, "y": 1190, "abs": True, "enter": "none", "layer": "front", "n": 14}],
    "overlays": [{"type": "title", "lines": ["¿HASTA EL CENTRO", "DE LA TIERRA?"], "y": 300, "size": 112}],
    "camera": {"move": "punch", "focus": [0.5, 0.5]}},
   sfx=[{"name": "dig", "at": 0.3}, {"name": "dig", "at": 0.92}, {"name": "dig", "at": 1.54}, {"name": "dig", "at": 2.16}],
   transition="cut", emphasis=["centro"])

sc("s02", "setup", "Problema: está a más de seis mil kilómetros.", {
    "background": {"type": "earth_section", "cx": 540, "cy": 1080, "R": 440, "hole": 0.0},
    "character": {"action": "shock", "expression": "surprised", "x": 0.5, "y": 616 / 1920, "scale": 0.3},
    "overlays": [{"type": "counter", "from": 0, "to": 6371, "suffix": " km", "at_word": 4, "over": 1.2, "y": 330,
                  "sub": "HASTA EL CENTRO"}],
    "camera": {"move": "pull_out", "zoom_from": 3.2, "zoom_to": 1.0, "focus": [0.5, 0.33]}},
   claims=[F("El radio medio de la Tierra es de unos 6.371 km", "NASA Earth Fact Sheet")],
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -4}, {"name": "ding", "at_word": 4}], transition="zoom",
   emphasis=["seis", "mil", "kilómetros"])

sc("s03", "setup", "A un metro por hora, tardarías más de setecientos años.", {
    "background": {"type": "backyard", "ground": 1200, "house_x": None,
                   "hole": {"x": 545, "w": 250, "depth": 200, "grow": 60, "pile": 120, "pile_grow": 40}},
    "character": {"action": "dig", "action_params": {"period": 0.3}, "expression": "determined", "x": 0.36, "y": G,
                  "scale": 1.3, "beard": [0, 1, 4.5], "expressions": [["w6", "tired"]]},
    "props": [{"type": "calendar", "x": 0.78, "y": 0.2, "from": 2026, "to": 2753, "over": 3.8, "at": 0.2, "label": "AÑO"},
              {"type": "clock", "x": 0.24, "y": 0.2, "scale": 0.8, "speed": 9, "at": 0.1},
              {"type": "debris", "x": 545, "y": 1190, "abs": True, "enter": "none", "layer": "front", "n": 20}],
    "camera": {"move": "static"}},
   claims=[F("6.371 km a 1 metro por hora ≈ 727 años sin parar", "Cálculo: 6.371.000 m ÷ 8.760 h/año", "estimate")],
   sfx=[{"name": "clock", "at": 0.1, "gain_db": -2}, {"name": "dig", "at": 0.5}, {"name": "dig", "at": 1.1},
        {"name": "dig", "at": 1.7}, {"name": "dig", "at": 2.3}],
   emphasis=["setecientos", "años"])

sc("s04", "setup", "Así que imagina un taladro gigante y un traje indestructible.", {
    "background": {"type": "burst", "c1": "#7B4DFF", "c2": "#9D7BFF"},
    "character": {"action": "drill", "action_params": {"intensity": 0.4}, "expression": "excited", "x": 0.5, "y": 0.62,
                  "scale": 1.35, "enter": "pop", **SUIT},
    "props": [{"type": "sparks", "x": 0.5, "y": 0.5, "n": 26, "enter": "none"}],
    "overlays": [{"type": "fiction", "text": "Traje y taladro imposibles: a partir de aquí la aventura es ficción", "y": 250}],
    "camera": {"move": "zoom_burst"}},
   claims=[F("Ningún traje ni máquina actual resistiría este viaje", "Licencia narrativa", "fiction")],
   sfx=[{"name": "sparkle", "at": 0.0}, {"name": "pop", "at": 0.05}, {"name": "drill", "at": 1.8, "gain_db": -3}],
   transition="flash", emphasis=["imagina", "indestructible"])

DRILL = {"action": "drill", "expression": "excited", "x": 0.5, "y": 0.56, "scale": 1.15, **SUIT}

sc("s05", "development", "A cuatro kilómetros pasas la mina más profunda del mundo.", {
    "background": {"type": "strata", "depth_from": 0.5, "depth_to": 4, "scroll": 650},
    "character": dict(DRILL),
    "props": [{"type": "lamp", "x": 0.86, "y": 0.14, "enter": "none"},
              {"type": "sign", "x": 0.84, "y": 0.5, "text": "MINA\nMPONENG", "w": 300, "size": 50, "at_word": 4, "enter": "drop"},
              {"type": "cart", "x": 0.83, "y": 0.66, "scale": 0.7, "at_word": 4, "enter": "slide_right"},
              {"type": "debris", "x": 540, "y": 1240, "abs": True, "enter": "none", "n": 16, "color": "#6B5B53"}],
    "overlays": [{"type": "depth", "from": 0.5, "to": 4}],
    "camera": {"move": "push_in", "shake": 0.35}},
   claims=[F("La mina Mponeng (Sudáfrica) supera los 4 km de profundidad, la más profunda del mundo",
             "AngloGold Ashanti / Guinness World Records")],
   sfx=[{"name": "drill", "at": 0.0, "gain_db": -6}, {"name": "pop", "at_word": 4}],
   emphasis=["cuatro", "kilómetros"])

sc("s06", "development", "La roca ya quema: unos sesenta grados.", {
    "background": {"type": "strata", "depth_from": 4, "depth_to": 6, "scroll": 300, "heat": 0.35},
    "character": {"action": "sweat", "expression": "hot", "x": 0.5, "y": 0.6, "scale": 1.2, "sweat": 1, **SUIT},
    "props": [{"type": "thermometer", "x": 0.83, "y": 0.42, "level": 0.55, "text": "60 °C", "at_word": 4},
              {"type": "heatwaves", "x": 0.5, "y": 0.3, "enter": "none"}],
    "overlays": [{"type": "depth", "from": 4, "to": 6}],
    "camera": {"move": "push_in", "zoom_to": 1.18, "focus": [0.5, 0.42]}},
   claims=[F("La roca en el fondo de Mponeng alcanza unos 60-66 °C", "AngloGold Ashanti; Wikipedia 'Mponeng'")],
   sfx=[{"name": "sizzle", "at": 0.3, "gain_db": -6}, {"name": "pop", "at_word": 4}],
   transition="slide", emphasis=["sesenta", "grados"])

sc("s07", "development", "A doce kilómetros superas el pozo de Kola, el agujero más profundo jamás hecho.", {
    "background": {"type": "strata", "depth_from": 6, "depth_to": 12.2, "scroll": 700},
    "character": {**DRILL, "x": 0.42, "actions": [["w7", "wave"]], "expressions": [["w7", "happy"]],
                  "path": [[0, 0.5, 0.56], ["w7", 0.42, 0.56]]},
    "props": [{"type": "pipe", "x": 0.82, "y": 0.0, "end": 960, "at_word": 3, "enter": "drop"}],
    "overlays": [{"type": "depth", "from": 6, "to": 12.26},
                 {"type": "label", "text": "POZO DE KOLA · 12,2 km", "x": 620, "y": 250, "size": 58, "at_word": 6,
                  "bg": "#E8392F"}],
    "camera": {"move": "pan_right", "amount": 120, "shake": 0.25}},
   claims=[F("El pozo superprofundo de Kola (Rusia) llegó a 12.262 m, el agujero más profundo jamás perforado",
             "Wikipedia 'Kola Superdeep Borehole'; ICDP")],
   sfx=[{"name": "drill", "at": 0.0, "gain_db": -6}, {"name": "fall", "at_word": 3, "gain_db": -6},
        {"name": "ding", "at_word": 6}],
   emphasis=["doce", "kola"])

sc("s08", "development", "Allí tardaron veinte años. Tú, cinco minutos.", {
    "background": {"type": "strata", "depth_from": 12.2, "depth_to": 12.3, "scroll": 0},
    "character": {"action": "smug", "expression": "smug", "x": 0.4, "y": 0.6, "scale": 1.25, **SUIT},
    "props": [{"type": "pipe", "x": 0.82, "y": 0.0, "end": 960, "enter": "none"},
              {"type": "calendar", "x": 0.8, "y": 0.68, "scale": 0.75, "from": 1970, "to": 1989, "over": 1.6, "label": "KOLA"}],
    "overlays": [{"type": "timer", "text": "5 MIN", "x": 220, "y": 380, "at_word": 5}],
    "camera": {"move": "push_in", "focus": [0.4, 0.45]}},
   claims=[F("La perforación de Kola duró de 1970 a 1989", "Wikipedia 'Kola Superdeep Borehole'")],
   sfx=[{"name": "clock", "at": 0.0, "gain_db": -8}, {"name": "ding", "at_word": 5}],
   transition="slide", emphasis=["veinte", "cinco"])

sc("s09", "development", "Y aun así, solo has arañado la corteza.", {
    "background": {"type": "earth_section", "cx": 540, "cy": 1080, "R": 440, "hole": 0.01, "highlight": "crust"},
    "character": {"visible": False},
    "overlays": [{"type": "counter", "from": 0, "to": 0.19, "decimals": 2, "suffix": " %", "y": 330, "over": 0.8,
                  "sub": "DEL CAMINO RECORRIDO", "size": 140},
                 {"type": "label", "text": "TÚ", "x": 540, "y": 560, "size": 50, "arrow": "down", "at": 0.3}],
    "camera": {"move": "pull_out", "zoom_from": 1.6, "zoom_to": 1.0, "focus": [0.5, 0.33]}},
   claims=[F("12 km son menos del 0,2 % de los 6.371 km hasta el centro", "Cálculo: 12,2 / 6.371", "estimate")],
   sfx=[{"name": "boing", "at": 0.4, "gain_db": -3}], transition="zoom", emphasis=["corteza"])

sc("s10", "development", "A unos treinta y cinco kilómetros llegas al manto. Y sorpresa:", {
    "background": {"type": "mantle", "flow_arrows": False},
    "character": {**DRILL, "y": 0.6, "actions": [["w9", "shock"]], "expressions": [["w9", "surprised"]]},
    "overlays": [{"type": "depth", "from": 12, "to": 35, "over": 1.2},
                 {"type": "label", "text": "EL MANTO", "x": 540, "y": 330, "size": 80, "at_word": 8, "bg": "#E8392F"}],
    "camera": {"move": "push_in", "shake": 0.3}},
   claims=[F("La corteza continental mide entre 30 y 50 km de grosor", "USGS")],
   sfx=[{"name": "drill", "at": 0.0, "gain_db": -6}, {"name": "riser", "at_word": 9, "gain_db": -3}],
   emphasis=["manto", "sorpresa"])

sc("s11", "development", "No, no es un mar de lava.", {
    "background": {"type": "mantle", "flow_arrows": False},
    "character": {"action": "shock", "expression": "shock", "x": 0.5, "y": 0.68, "scale": 1.2, **SUIT},
    "overlays": [{"type": "myth", "text": "MAR DE LAVA", "y": 400, "stamp_at": 0.95}],
    "camera": {"move": "punch", "impacts": [1.13]}},
   claims=[F("El manto no es lava líquida", "USGS; National Geographic")],
   sfx=[{"name": "hit", "at": 1.12, "gain_db": -2}], transition="cut", emphasis=["lava"])

sc("s12", "development", "Es roca sólida, a más de mil grados, que fluye como un chicle gigante.", {
    "background": {"type": "mantle", "flow_arrows": True},
    "character": {"action": "squished", "expression": "worried", "x": 0.5, "y": 0.62, "scale": 1.2, **SUIT},
    "overlays": [{"type": "fact", "text": "El manto es roca sólida que fluye unos centímetros al año", "y": 240, "at_word": 2}],
    "camera": {"move": "push_in", "zoom_to": 1.1}},
   claims=[F("El manto es roca sólida a 1.000-4.000 °C que fluye unos cm al año (convección)", "USGS; Britannica 'Mantle'")],
   sfx=[{"name": "gulp", "at_word": 12}, {"name": "rumble", "at": 0.3, "gain_db": -6}], transition="slide",
   emphasis=["sólida", "chicle"])

sc("s13", "development", "A dos mil novecientos kilómetros... el suelo desaparece.", {
    "background": {"type": "mantle", "flow_arrows": False},
    "character": {**DRILL, "y": 0.5, "actions": [["w5", "fall"]], "expressions": [["w5", "scared"]],
                  "path": [[0, 0.5, 0.5], ["w5", 0.5, 0.5], ["end-0", 0.5, 1.25]], "path_ease": "linear"},
    "props": [{"type": "speedlines", "x": 0.5, "y": 0.5, "at_word": 5, "enter": "none", "layer": "front"}],
    "overlays": [{"type": "depth", "from": 35, "to": 2900, "over": 1.6}],
    "camera": {"move": "static", "impacts": ["w5"], "shake": 0.25}},
   claims=[F("El límite entre manto y núcleo externo está a unos 2.900 km", "USGS")],
   sfx=[{"name": "drill", "at": 0.0, "gain_db": -6}, {"name": "crack", "at_word": 4}, {"name": "fall", "at_word": 5}],
   emphasis=["desaparece"])

sc("s14", "climax", "¡Plof! Caes en un océano de hierro líquido.", {
    "background": {"type": "outer_core", "surface": 1150},
    "character": {"action": "swim", "expression": "surprised", "x": 0.5, "y": 0.66, "scale": 1.1, "enter": "drop",
                  "expressions": [["w3", "wow"]], **SUIT},
    "props": [{"type": "splash", "x": 540, "y": 1160, "abs": True, "at": 0.45, "enter": "none", "layer": "front"}],
    "overlays": [{"type": "label", "text": "NÚCLEO EXTERNO", "x": 540, "y": 380, "size": 74, "at_word": 4, "bg": "#F08A24"},
                 {"type": "depth", "from": 2900, "to": 3100}],
    "camera": {"move": "punch", "impacts": [0.45]}},
   claims=[F("El núcleo externo es hierro y níquel líquidos, entre 2.900 y 5.150 km", "USGS; NASA")],
   sfx=[{"name": "splash", "at": 0.42}], transition="circle", emphasis=["hierro", "líquido"])

sc("s16", "climax", "Más abajo, el núcleo interno: tan caliente como la superficie del Sol.", {
    "background": {"type": "inner_core", "cy": 1550, "r": 620},
    "character": {"action": "float", "expression": "wow", "x": 0.5, "y": 0.72, "scale": 0.95, **SUIT},
    "props": [{"type": "vs", "x": 0.5, "y": 0.27, "at_word": 5, "scale": 0.95,
               "left": {"title": "NÚCLEO", "value": "~6.000 °C", "sub": "interno", "color": "#F08A24"},
               "right": {"title": "SOL", "value": "~5.500 °C", "sub": "superficie", "color": "#FFB347"}},
              {"type": "sparks", "x": 0.5, "y": 0.85, "enter": "none"}],
    "overlays": [{"type": "depth", "from": 5150, "to": 6000}],
    "camera": {"move": "pan_up", "amount": 120}},
   claims=[F("El núcleo interno sólido está a unos 5.400-6.000 °C, comparable a la superficie del Sol (~5.500 °C)",
             "ESRF, Anzellini et al., Science 2013")],
   sfx=[{"name": "sizzle", "at": 0.2, "gain_db": -8}, {"name": "pop", "at_word": 5}], emphasis=["sol"])

sc("s17", "climax", "La presión supera los tres millones de atmósferas. Tu casco cruje.", {
    "background": {"type": "inner_core", "cy": 1650, "r": 700},
    "character": {"action": "squished", "expression": "scared", "x": 0.5, "y": 0.66, "scale": 1.2,
                  "cracks": [0, 1, 3.6], **SUIT},
    "props": [{"type": "pressure", "x": 540, "y": 960, "abs": True, "r": 470, "enter": "none"}],
    "overlays": [{"type": "counter", "from": 0, "to": 3600000, "suffix": " atm", "over": 1.3, "y": 300, "size": 120,
                  "sub": "DE PRESIÓN"}],
    "camera": {"move": "push_in", "shake": 0.4, "impacts": ["w10"]}},
   claims=[F("La presión en el centro es de unos 360 GPa (~3,6 millones de atmósferas)", "USGS; Dziewonski & Anderson (PREM)")],
   sfx=[{"name": "rumble", "at": 0.0, "gain_db": -4}, {"name": "crack", "at_word": 9}, {"name": "crack", "at_word": 10}],
   emphasis=["tres", "millones", "cruje"])

sc("s18", "climax", "Pero llegas al centro… y flotas.", {
    "background": {"type": "center"},
    "character": {"action": "float", "expression": "surprised", "x": 0.5, "y": 0.6, "scale": 1.2, "cracks": 1,
                  "expressions": [["w5", "wow"]], **SUIT},
    "camera": {"move": "push_in", "zoom_to": 1.15, "focus": [0.5, 0.48]}},
   sfx=[{"name": "sparkle", "at_word": 5}, {"name": "float", "at": 0.0}], transition="flash", emphasis=["flotas"])

sc("s19", "climax", "La gravedad tira igual en todas direcciones: no pesas nada.", {
    "background": {"type": "center"},
    "character": {"action": "float", "expression": "happy", "x": 0.5, "y": 0.62, "scale": 1.0, "cracks": 1,
                  "action_params": {"spin_rate": 0.6}, **SUIT},
    "props": [{"type": "gravity_arrows", "x": 540, "y": 1000, "abs": True, "r": 360, "at_word": 2}],
    "overlays": [{"type": "fact", "text": "En el centro de la Tierra la gravedad neta es prácticamente cero", "y": 230}],
    "camera": {"move": "static"}},
   claims=[F("En el centro de la Tierra la atracción de la masa se compensa: gravedad neta ≈ 0", "Teorema de las capas de Newton")],
   sfx=[{"name": "boing", "at_word": 2, "gain_db": -6}], emphasis=["nada"])

sc("s20", "ending", "Solo queda un problemilla: volver.", {
    "background": {"type": "strata", "depth_from": 30, "depth_to": 30, "scroll": -250, "heat": 0.5},
    "character": {"action": "look_up", "expression": "worried", "x": 0.5, "y": 0.66, "scale": 1.2, "cracks": 1,
                  "actions": [["w4", "shrug"]], "expressions": [["w4", "happy"]], **SUIT},
    "overlays": [{"type": "label", "text": "6.371 km HACIA ARRIBA", "x": 540, "y": 330, "size": 66, "at_word": 4, "bg": "#2B6BE8"}],
    "camera": {"move": "pan_down", "amount": 160}},
   sfx=[{"name": "boing", "at_word": 4}], transition="slide", emphasis=["volver"])

sc("s21", "ending", "¿Y tú, hasta dónde llegarías? Te leo en comentarios.", {
    "background": {"type": "burst", "c1": "#FFD23F", "c2": "#FFB300"},
    "character": {"action": "talk", "expression": "excited", "x": 0.5, "y": 0.6, "scale": 1.35, "enter": "pop",
                  "actions": [["w5", "point_down"]]},
    "overlays": [{"type": "label", "text": "COMENTA ABAJO", "x": 540, "y": 330, "size": 70, "at_word": 5, "arrow": "down",
                  "bg": "#E8392F"}],
    "camera": {"move": "zoom_burst"}},
   sfx=[{"name": "pop", "at": 0.05}, {"name": "ding", "at_word": 4}], transition="zoom", pause=0.3)

story = {
    "title": "¿Qué pasaría si cavaras hasta el centro de la Tierra?",
    "idea": "¿Qué pasaría si cavaras un agujero hasta el centro de la Tierra?",
    "slug": "centro-de-la-tierra",
    "category": "ciencia",
    "question": "¿Hasta qué capa crees que llegarías tú?",
    "music_mood": "adventure",
    "scenes": S,
    "metadata": {
        "title": "¿Y si cavaras hasta el centro de la Tierra? 🌍⛏️",
        "description_intro": "Coges una pala y cavas hacia el centro de la Tierra... ¿hasta dónde llegarías?",
        "hashtags": ["#centrodelatierra", "#ciencia", "#curiosidades"],
        "pinned_comment": "¿Hasta qué capa crees que llegarías tú? ¿Corteza, manto o núcleo? 👇",
        "thumbnail_text": "¿HASTA EL CENTRO DE LA TIERRA?",
        "thumbnail_scene": "s14",
    },
}
out = Path(__file__).resolve().parents[1] / "stories" / "centro-de-la-tierra.json"
out.write_text(json.dumps(story, indent=2, ensure_ascii=False), encoding="utf-8")
words = sum(len(s["narration"].split()) for s in S)
print(out, len(S), "escenas,", words, "palabras")
