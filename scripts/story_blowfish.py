"""Anuncio: Leo con la sudadera Blowfish cruza el espejo del mundo de cómic al mundo real.

El segmento «humano real» (b07) usa assets/blowfish/humano.mp4 si existe (vídeo vertical de una
persona con la sudadera diciendo la frase). Si no existe, se muestra la foto real del producto y la
frase la dice otra voz (Elvira). Ver assets/blowfish/GUION_HUMANO.md.
"""
from storykit import Story

st = Story()
sc = st.sc
LEO = {"outfit": "blowfish"}
G = 1360 / 1920
FRONT, BACK = "assets/blowfish/sudadera_frente.jpg", "assets/blowfish/sudadera_espalda.jpg"
HUMAN = "assets/blowfish/humano.mp4"
MINT, NAVY = "#C4EDC9", "#1B2A3D"

sc("b01", "hook", "Este es Leo. Vive en un mundo de cómic, donde todo está dibujado…", {
    "background": {"type": "comic", "ground": 1360},
    "character": {"action": "wave", "expression": "excited", "x": 0.5, "y": G, "scale": 1.4, "enter": "drop", **LEO},
    "props": [{"type": "pow", "x": 0.78, "y": 0.2, "text": "¡HOLA!", "at": 0.5}],
    "camera": {"move": "punch", "impacts": [0.65]}},
   sfx=[{"name": "boom", "at": 0.6, "gain_db": -8}, {"name": "pop", "at": 0.5}], transition="cut",
   emphasis=["leo", "cómic"])

sc("b02", "setup", "…menos una cosa: su sudadera Blowfish.", {
    "background": {"type": "comic", "ground": 1360, "speedlines": True},
    "character": {"action": "pose", "expression": "smug", "x": 0.5, "y": G, "scale": 1.4, **LEO},
    "props": [{"type": "pow", "x": 0.24, "y": 0.22, "text": "¡WOW!", "at_word": 4, "color": MINT,
               "text_color": NAVY, "tilt": 0.1}],
    "camera": {"move": "push_in", "zoom_from": 1.0, "zoom_to": 2.4, "focus": [0.55, 0.59]}},
   sfx=[{"name": "sparkle", "at_word": 4}, {"name": "whoosh", "at": 0.1}], transition="zoom",
   emphasis=["blowfish"])

sc("b03", "development", "Y espera a ver la espalda.", {
    "background": {"type": "comic", "ground": 1360},
    "character": {"action": "idle", "expression": "excited", "x": 0.5, "y": G, "scale": 1.45, "actions": [["w2", "turn"]],
                  **LEO},
    "props": [{"type": "pow", "x": 0.78, "y": 0.22, "text": "¡ZAS!", "at_word": 3}],
    "camera": {"move": "push_in", "zoom_from": 1.0, "zoom_to": 1.6, "focus": [0.5, 0.56]}},
   sfx=[{"name": "whoosh", "at_word": 2}, {"name": "pop", "at_word": 3}], transition="whip", emphasis=["espalda"])

sc("b04", "development", "«Incluso el viaje más largo empieza con un solo paso».", {
    "background": {"type": "comic", "ground": 1360},
    "character": {"action": "turn", "expression": "happy", "x": 0.5, "y": G, "scale": 1.45, **LEO},
    "overlays": [{"type": "prop", "prop": {"type": "jp_text", "x": 0.5, "y": 0.17, "text": "一番長い旅も、一歩から始まる",
                                           "size": 74, "enter": "fade", "enter_dur": 0.6, "color": MINT}}],
    "camera": {"move": "push_in", "zoom_from": 1.6, "zoom_to": 1.9, "focus": [0.5, 0.56]}},
   sfx=[{"name": "ding", "at": 0.1}], transition="cut", emphasis=["paso"])

sc("b05", "development", "Así que Leo da ese paso…", {
    "background": {"type": "comic", "ground": 1360},
    "character": {"action": "walk_back", "expression": "happy", "x": 0.5, "y": 0.92, "scale": 1.2,
                  "path": [[0, 0.5, 0.92], ["end-0", 0.5, 0.74]], "scale_keys": [[0, 1.2], ["end-0", 0.85]], **LEO},
    "props": [{"type": "mirror", "x": 0.5, "y": 0.42, "scale": 0.95, "image": FRONT, "clip": HUMAN, "enter": "drop", "img_dy": 40}],
    "camera": {"move": "push_in", "zoom_to": 1.08, "focus": [0.5, 0.45]}},
   sfx=[{"name": "boom", "at": 0.6, "gain_db": -8}, {"name": "sparkle", "at": 0.9}], transition="slide",
   emphasis=["paso"])

sc("b06", "climax", "y cruza al otro lado del espejo.", {
    "background": {"type": "comic", "ground": 1360},
    "character": {"action": "walk_back", "expression": "happy", "x": 0.5, "y": 0.74, "scale": 0.85,
                  "path": [[0, 0.5, 0.74], [1.0, 0.5, 0.6]], "scale_keys": [[0, 0.85], [1.0, 0.25]], **LEO},
    "props": [{"type": "mirror", "x": 0.5, "y": 0.42, "scale": 0.95, "image": FRONT, "clip": HUMAN, "enter": "none", "ripple_anim": True,
               "img_dy": 40},
              {"type": "sparks", "x": 0.5, "y": 0.5, "enter": "none", "layer": "front"}],
    "camera": {"move": "push_in", "zoom_from": 1.08, "zoom_to": 2.3, "focus": [0.5, 0.42]}},
   sfx=[{"name": "riser", "at": 0.0, "gain_db": -3}, {"name": "whoosh", "at_word": 4}], transition="cut",
   emphasis=["espejo"])

sc("b07", "climax", "¡Hola, Leo! Bienvenido al mundo real. Aquí tu sudadera existe de verdad.", {
    "background": {"type": "clip", "path": HUMAN,
                   "fallback": {"type": "photo", "path": FRONT, "bg": "#D7D7D7", "scale": 0.95, "kenburns": 0.1}},
    "character": {"action": "wave", "expression": "wow", "x": 0.18, "y": 0.97, "scale": 0.75, "enter": "rise", **LEO},
    "overlays": [{"type": "flash", "over": 0.35},
                 {"type": "label", "text": "MUNDO REAL", "x": 540, "y": 250, "size": 66, "bg": NAVY, "color": MINT,
                  "at": 0.3}],
    "camera": {"move": "push_in", "zoom_from": 1.0, "zoom_to": 1.06}},
   sfx=[{"name": "hit", "at": 0.0, "gain_db": -4}], transition="cut", emphasis=["real", "verdad"])
st.scenes[-1]["voice_clip"] = HUMAN
st.scenes[-1]["voice"] = {"voice": "es-ES-ElviraNeural", "rate": "+8%", "pitch": "+0Hz"}

sc("b08", "climax", "Azul marino, verde menta y una frase para recordarte que todo empieza con un paso.", {
    "background": {"type": "photo", "path": BACK, "bg": "#D7D7D7", "scale": 0.95, "kenburns": 0.12},
    "character": {"action": "turn", "expression": "happy", "x": 0.85, "y": 0.97, "scale": 0.7, **LEO},
    "props": [{"type": "jp_text", "x": 0.5, "y": 0.73, "text": "«El viaje más largo empieza con un paso»", "size": 46,
               "at_word": 7, "color": NAVY, "enter": "fade"}],
    "camera": {"move": "pan_up", "amount": 90, "zoom": 1.05}},
   sfx=[{"name": "whoosh", "at": 0.0, "gain_db": -6}], transition="slide", emphasis=["marino", "menta"])

sc("b09", "ending", "Blowfish Clothes. Da el primer paso.", {
    "background": {"type": "photo", "path": BACK, "bg": "#D7D7D7", "scale": 0.8, "cy": 0.6, "kenburns": 0.05},
    "character": {"action": "pose", "expression": "smug", "x": 0.82, "y": 0.97, "scale": 0.75, **LEO},
    "props": [{"type": "logo", "x": 0.5, "y": 0.16, "text": "BLOWFISH", "sub": "clothes®", "color": NAVY,
               "shadow": False, "width": 880, "enter": "pop"}],
    "overlays": [{"type": "label", "text": "DA EL PRIMER PASO", "x": 540, "y": 1560, "size": 60, "bg": NAVY,
                  "color": MINT, "at_word": 2}],
    "camera": {"move": "push_in", "zoom_to": 1.05}},
   sfx=[{"name": "ding", "at": 0.1}, {"name": "sparkle", "at_word": 2}], transition="zoom", pause=0.8)

DESC = """Leo vive en un mundo de cómic… hasta que su sudadera Blowfish le lleva al otro lado del espejo. 🐡✨

一番長い旅も、一歩から始まる — «Incluso el viaje más largo empieza con un solo paso».

Sudadera Blowfish Clothes® en azul marino con estampado en verde menta.

#publicidad #blowfish #blowfishclothes #streetwear #moda #ropa #hipoteticos"""

st.save("anuncio-blowfish", "Leo cruza el espejo con su sudadera Blowfish",
        "Anuncio Blowfish: Leo cruza del mundo de cómic al mundo real", "anuncio",
        "¿La quieres?", {
            "title": "Leo cruza el espejo… y llega al mundo real 🐡 | Blowfish Clothes",
            "hashtags": ["#publicidad", "#blowfish", "#blowfishclothes", "#streetwear", "#moda"],
            "tags": ["blowfish", "blowfish clothes", "sudadera", "streetwear", "moda", "marca emergente",
                     "animación", "anuncio", "hipotéticos"],
            "pinned_comment": "¿Qué te parece la sudadera de Leo? 🐡👇",
            "description": DESC,
            "target_seconds": [20, 45],
            "thumbnail": {"scene": "b04", "t": 0.8, "lines": ["LEO ESTRENA", "SUDADERA"],
                          "badge": "BLOWFISH®", "badge_color": NAVY, "badge_pos": [540, 1600], "y": 260,
                          "crop_y": 0.55, "h_shift": 840, "h_scale": 0.75},
        }, mood="funny")
