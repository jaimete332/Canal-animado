"""Episode 1 — Could You Survive a Year as a Medieval Peasant? (England, 1348)

Run:  python3 scripts/en_story_medieval_peasant.py
      python -m fabrica --channel stickman_en make stories_en/medieval-peasant-1348.json
"""
from storykit_en import GROUND, F, Story, cast

st = Story()
sc = st.sc
ch = st.chapter

# ---- recurring cast & sets ---------------------------------------------------------------------------------
TUNIC = {"outfit": "tunic", "outfit_color": (0.55, 0.42, 0.3)}


def stan(**kw):
    return cast("stan", **{**TUNIC, **kw})


def maud(**kw):
    return cast("maud", "peasant_woman", **kw)


def wat(**kw):
    return cast("wat", "child", **kw)


def lord(**kw):
    return cast("lord", "lord", **kw)


def reeve(**kw):
    return cast("reeve", "reeve", **kw)


def priest(**kw):
    return cast("priest", "priest", **kw)


def village(season="spring", **kw):
    return {"type": "village", "season": season, **kw}


def field(season="spring", crops=0.0, **kw):
    return {"type": "field", "season": season, "crops": crops, **kw}


def hut(season="spring", **kw):
    return {"type": "interior", "season": season, **kw}


PAPER = {"type": "paper"}
LINED = {"type": "paper", "lines": True, "floor": False}
WHATIF = {"type": "fiction", "text": "STAN'S STORY"}


def month(m, n):
    return {"type": "counter", "label": m, "value": f"· MONTH {n}", "corner": "tr", "size": 46}


def odds(a, b, at=0.4):
    return {"type": "meter", "label": "STAN'S SURVIVAL ODDS", "from": a, "to": b, "at": at, "y": 0.11, "w": 640}


SRC = {
    "dyer": "Christopher Dyer, Making a Living in the Middle Ages (Yale, 2002)",
    "bennett": "H. S. Bennett, Life on the English Manor (Cambridge, 1937)",
    "eh": "English Heritage, 'Medieval peasant houses'",
    "horrox": "Rosemary Horrox (ed.), The Black Death (Manchester University Press, 1994)",
    "benedictow": "Ole J. Benedictow, The Black Death 1346-1353 (Boydell, 2004)",
    "mortimer": "Ian Mortimer, The Time Traveller's Guide to Medieval England (2008)",
    "calendar": "Royal Museums Greenwich, 'When did New Year's Day change to 1 January?'",
    "statute": "Ordinance of Labourers (1349) & Statute of Labourers (1351), UK Parliament",
    "cdc": "CDC, 'Plague: symptoms and transmission'",
    "famine": "William Chester Jordan, The Great Famine (Princeton, 1996)",
    "bl": "British Library, 'Medieval medicine and the plague doctor'",
    "bathing": "Katherine Harvey, The Fires of Lust / Smithsonian, 'Medieval people did bathe'",
}

# =========================================================================================================
# INTRO
# =========================================================================================================
sc("i01", "hook", "It's the morning of March twenty-fifth, 1348, and you just woke up on a pile of straw.", {
    "background": hut("spring", dark=0.25, hearth_x=0.7),
    "props": [{"type": "bed", "x": 0.42, "y": 0.9, "scale": 1.3, "enter": "none"},
              {"type": "icon", "icon": "z", "x": 0.42, "y": 0.72, "until": 2.6},
              {"type": "chicken", "x": 0.85, "y": 0.94, "at": 2.0}],
    "cast": [stan(x=0.48, y=0.86, action="sleep", expression="sleepy",
                  actions=[["w12", "sit"]], expressions=[["w12", "surprised"]])],
    "overlays": [{"type": "title", "text": "MARCH 25, 1348", "y": 0.16, "at": 0.4}],
    "camera": {"move": "push_in", "zoom_to": 1.12, "focus": [0.45, 0.65]}},
    claims=[F("Stan waking up in 1348 is a dramatization", "Narrative device", "fiction")],
    sfx=[{"name": "pop", "at_word": 12}], transition="cut")

sc("i02", "hook", "Congratulations. You are a medieval peasant, and your mission is simple: survive one year.", {
    "background": village("spring"),
    "cast": [stan(x=0.5, action="shrug", expression="worried", actions=[["w9", "idle"]])],
    "overlays": [{"type": "title", "lines": ["MISSION:", "SURVIVE 1 YEAR"], "colors": ["red", "ink"],
                  "y": 0.16, "at_word": 9}, WHATIF],
    "camera": {"move": "push_in"}},
    sfx=[{"name": "ding", "at_word": 9}])

sc("i03", "hook", "Oh, and happy New Year! In medieval England, the year officially started on March twenty-fifth.", {
    "background": PAPER,
    "props": [{"type": "calendar", "x": 0.68, "y": 0.75, "month": "MARCH", "day": 25, "at_word": 4, "scale": 1.3,
               "loop": "bob"}],
    "cast": [stan(x=0.3, action="cheer", expression="grin", actions=[["w5", "point"]], expressions=[["w5", "happy"]],
                  facing=1)],
    "overlays": [{"type": "fact", "text": "From the 1100s until 1752, England's legal year began on 25 March (Lady Day).",
                  "source": SRC["calendar"], "at_word": 8}]},
    claims=[F("England's civil/legal year began on 25 March until 1752", SRC["calendar"])],
    sfx=[{"name": "sparkle", "at": 0.3}, {"name": "pop", "at_word": 4}], transition="wipe")

sc("i04", "hook", "Now, I'm going to be honest with you. Of all the years you could have picked…", {
    "background": PAPER,
    "cast": [stan(x=0.5, action="talk", expression="neutral", scale=1.4)],
    "camera": {"move": "push_in", "zoom_to": 1.18, "focus": "stan"}})

sc("i04b", "hook", "Here's how this works: every chapter, Stan's survival odds go up or down, depending on what life throws at him.", {
    "background": PAPER,
    "cast": [stan(x=0.25, action="talk", expression="happy", actions=[["w12", "point_up"]])],
    "overlays": [odds(0.9, 0.95, 0.5), {"type": "label", "text": "keep an eye on this", "x": 0.68, "y": 0.3,
                                         "to_x": 0.62, "to_y": 0.13, "at": 1.2}]})

sc("i05", "hook", "this is the worst one. By the end of it, a huge part of England will be dead.", {
    "background": {"type": "solid", "color": (0.25, 0.08, 0.1)},
    "props": [{"type": "skull", "x": 0.5, "y": 0.62, "scale": 2.0, "at_word": 2, "loop": "pulse"}],
    "overlays": [odds(0.9, 0.5, 1.0)],
    "camera": {"move": "punch", "impacts": ["w2"]}},
    claims=[F("The Black Death reached England in 1348", SRC["horrox"])],
    sfx=[{"name": "boom", "at_word": 2, "gain_db": -4}], transition="cut")

sc("i06", "hook", "So let's see what it takes to make it through 1348, one season at a time. Ready? Let's go.", {
    "background": village("spring"),
    "cast": [stan(x=0.25, action="walk", path=[[0, 0.15, GROUND], [4.5, 0.55, GROUND]],
                  expression="determined", actions=[["w16", "cheer"]])],
    "overlays": [{"type": "timeline", "items": ["SPRING", "SUMMER", "AUTUMN", "WINTER"], "at": 0, "y": 0.1}],
    "camera": {"move": "pan_right", "amount": 120}},
    transition="wipe")

# =========================================================================================================
# CHAPTER 1 — HOME
# =========================================================================================================
ch("Your New Home")
sc("h01", "setup", "Let's start with your house. It's one room, built from a wooden frame packed with mud and straw.", {
    "background": village("spring"),
    "props": [{"type": "hut", "x": 0.6, "y": 0.84, "scale": 1.4, "enter": "pop"},
              ],
    "cast": [stan(x=0.2, action="point", expression="happy", action_params={"height": 0.3})],
    "overlays": [{"type": "label", "text": "wattle & daub", "x": 0.83, "y": 0.42, "to_x": 0.7, "to_y": 0.6,
                  "at_word": 11},
                 {"type": "label", "text": "thatched roof", "x": 0.86, "y": 0.18, "to_x": 0.7, "to_y": 0.3,
                  "at_word": 4}],
    "camera": {"move": "push_in", "focus": [0.55, 0.55]}},
    claims=[F("Peasant houses were timber-framed with wattle-and-daub walls and thatched roofs", SRC["eh"])],
    transition="wipe")

sc("h02", "setup", "There's no chimney. The fire burns in the middle of the floor, and the smoke just… finds its way out.", {
    "background": hut("spring", hearth_x=0.5),
    "cast": [stan(x=0.25, action="sick", expression="disgusted", actions=[["w15", "facepalm"]])],
    "props": [{"type": "icon", "icon": "stink", "x": 0.5, "y": 0.45, "at_word": 12}],
    "camera": {"move": "pan_up", "amount": 120, "zoom": 1.08}},
    claims=[F("Most peasant houses had an open central hearth and no chimney", SRC["eh"])],
    sfx=[{"name": "sizzle", "at": 0.2, "gain_db": -10}])

sc("h03", "setup", "The floor is packed earth covered in straw, which is cozy, right up until you meet the rats.", {
    "background": hut("spring", hearth_x=0.75),
    "cast": [stan(x=0.35, action="idle", expression="happy", actions=[["w13", "cower"]],
                  expressions=[["w13", "scared"]])],
    "props": [{"type": "rat", "x": 0.75, "y": 0.95, "walk": True, "at_word": 13,
               "move": [[0, 1.1, 0.95], [1.4, 0.62, 0.95]]}],
    "camera": {"move": "static"}},
    sfx=[{"name": "boing", "at_word": 15}])

sc("h04", "setup", "And you're not alone. Meet your wife, Maud, and your son, Wat.", {
    "background": hut("spring", hearth_x=0.82),
    "cast": [stan(x=0.25, action="wave", expression="happy"),
             maud(x=0.5, facing=-1, at=1.4, enter="pop", action="wave", expression="happy"),
             wat(x=0.66, facing=-1, at=2.6, enter="pop", action="jump", expression="grin")],
    "overlays": [{"type": "label", "text": "Maud", "x": 0.5, "y": 0.28, "at": 1.6},
                 {"type": "label", "text": "Wat", "x": 0.66, "y": 0.45, "at": 2.8}],
    "camera": {"move": "push_in"}},
    claims=[F("Stan's family is fictional", "Narrative device", "fiction")],
    sfx=[{"name": "pop", "at": 1.4}, {"name": "pop", "at": 2.6}])

sc("h05", "setup", "Also living with you: a pig, a few chickens, and, if you're lucky, a cow.", {
    "background": hut("spring", hearth=False),
    "props": [{"type": "pig", "x": 0.25, "y": 0.92, "at_word": 5, "scale": 1.1},
              {"type": "chicken", "x": 0.48, "y": 0.92, "at_word": 8},
              {"type": "chicken", "x": 0.56, "y": 0.95, "at_word": 8, "flip": -1},
              {"type": "cow", "x": 0.78, "y": 0.92, "at_word": 14, "scale": 1.05}],
    "cast": [stan(x=0.1, action="shrug", expression="smug", scale=1.1)],
    "camera": {"move": "static"}},
    sfx=[{"name": "pop", "at_word": 5}, {"name": "pop", "at_word": 8}, {"name": "pop", "at_word": 14}])

sc("h06", "setup", "In many longhouses, the animals lived at one end of the building. Their body heat kept everyone warm.", {
    "background": PAPER,
    "props": [{"type": "hut", "x": 0.5, "y": 0.84, "scale": 1.8, "smoke": False},
              {"type": "cow", "x": 0.68, "y": 0.84, "scale": 0.7, "at_word": 5},
              {"type": "icon", "icon": "heart", "x": 0.68, "y": 0.5, "at_word": 12, "loop": "bob"}],
    "overlays": [{"type": "fact", "text": "Longhouses sheltered people and livestock under one roof, often with "
                                          "a cross-passage between them.", "source": SRC["dyer"], "at_word": 3}]},
    claims=[F("In some regions peasants lived in longhouses shared with livestock", SRC["dyer"])])

sc("h07", "setup", "The smell? Let's just say you stop noticing it after a week.", {
    "background": hut("spring", hearth_x=0.8),
    "cast": [stan(x=0.4, action="itch", expression="smug", actions=[["w6", "laugh"]], expressions=[["w6", "laughing"]])],
    "props": [{"type": "icon", "icon": "stink", "x": 0.2, "y": 0.84}, {"type": "pig", "x": 0.2, "y": 0.93}],
    "camera": {"move": "push_in", "focus": "stan"}})

# =========================================================================================================
# CHAPTER 2 — WHO OWNS YOU
# =========================================================================================================
ch("Who Owns You?")
sc("o01", "setup", "Here's the first bad news. You don't really own anything. Not the land, not the house…", {
    "background": village("spring"),
    "cast": [stan(x=0.35, action="talk", expression="neutral", expressions=[["w5", "worried"]])],
    "props": [{"type": "icon", "icon": "x", "x": 0.6, "y": 0.5, "at_word": 9},
              {"type": "icon", "icon": "x", "x": 0.75, "y": 0.5, "at_word": 13}],
    "camera": {"move": "push_in"}},
    sfx=[{"name": "pop", "at_word": 9}, {"name": "pop", "at_word": 13}], transition="wipe")

sc("o02", "setup", "and in a way, not even yourself. Because this guy does.", {
    "background": {"type": "manor", "manor_x": 0.66},
    "cast": [stan(x=0.18, action="sad", expression="sad"),
             lord(x=0.5, facing=-1, at_word=6, enter="slide_left", action="laugh", expression="smug")],
    "overlays": [{"type": "label", "text": "Sir Hugh, your lord", "x": 0.5, "y": 0.2, "to_x": 0.5, "to_y": 0.4,
                  "at_word": 8}],
    "camera": {"move": "push_in", "focus": [0.4, 0.55]}},
    claims=[F("Sir Hugh is a fictional lord", "Narrative device", "fiction")],
    sfx=[{"name": "whoosh", "at_word": 6}])

sc("o03", "setup", "You're a villein, an unfree peasant. You're bound to Sir Hugh's manor, and you can't just leave.", {
    "background": {"type": "manor", "manor_x": 0.7},
    "cast": [stan(x=0.25, action="walk", path=[[1.5, 0.25, GROUND], [3.5, 0.05, GROUND]], expression="worried",
                  actions=[["w14", "idle"]]),
             lord(x=0.55, facing=-1, action="point", expression="angry", at=0.0,
                  say=[{"text": "Where do you think you're going?", "at_word": 14}])],
    "overlays": [{"type": "title", "text": "VILLEIN = UNFREE", "y": 0.15, "at_word": 2, "until_word": 13}]},
    claims=[F("Villeins were unfree tenants legally bound to their lord's manor", SRC["bennett"])])

sc("o04", "setup", "In exchange for your strips of land, you owe him work. Often two or three days a week, every week.", {
    "background": field("spring", crops=0.1),
    "cast": [stan(x=0.4, action="dig", item="hoe", expression="tired"),
             reeve(x=0.78, facing=-1, action="idle", expression="neutral")],
    "overlays": [{"type": "counter", "label": "UNPAID WORK:", "value": "2-3 DAYS / WEEK", "corner": "tr",
                  "at_word": 13, "color": "red", "size": 48}],
    "camera": {"move": "pan_right", "amount": 100}},
    claims=[F("Villeins typically owed 'week-work' on the lord's demesne, often 2-3 days per week",
              SRC["bennett"] + "; " + SRC["dyer"])],
    sfx=[{"name": "dig", "at": 0.5}, {"name": "dig", "at": 1.6}, {"name": "ding", "at_word": 13}])

sc("o05", "setup", "That's free labor on his fields, called the demesne, while your own crops wait.", {
    "background": PAPER,
    "props": [{"type": "strips", "x": 0.5, "y": 0.78, "scale": 0.95, "mine": [2, 9], "reveal": 3.0}],
    "overlays": [{"type": "label", "text": "the lord's demesne", "x": 0.28, "y": 0.15, "to_x": 0.35, "to_y": 0.4,
                  "at_word": 6},
                 {"type": "label", "text": "your strips", "x": 0.75, "y": 0.15, "to_x": 0.66, "to_y": 0.4,
                  "at_word": 10}]},
    claims=[F("The lord's demesne was farmed using villeins' labor services", SRC["bennett"])])

sc("o06", "setup", "Making sure you actually show up is the reeve, a fellow peasant with a clipboard energy.", {
    "background": field("spring", crops=0.1),
    "cast": [reeve(x=0.6, facing=-1, action="hold", expression="smug", scale=1.4),
             stan(x=0.25, action="idle", expression="worried")],
    "overlays": [{"type": "label", "text": "the reeve", "x": 0.6, "y": 0.13, "to_x": 0.6, "to_y": 0.27,
                  "at_word": 7}],
    "camera": {"move": "push_in", "focus": "reeve"}},
    claims=[F("The reeve was a villager chosen to oversee work on the manor", SRC["bennett"])])

sc("o07", "setup", "And the fees. Oh, the fees. Want your daughter to marry? Pay the lord a fine, called merchet.", {
    "background": {"type": "manor"},
    "cast": [stan(x=0.3, action="hold", item="coin", expression="sad"),
             lord(x=0.62, facing=-1, action="count", expression="happy")],
    "overlays": [{"type": "money", "text": "-merchet", "x": 0.33, "y": 0.45, "at_word": 15}],
    "camera": {"move": "static"}},
    claims=[F("Merchet was a fine paid to the lord when an unfree woman married", SRC["bennett"])],
    sfx=[{"name": "ding", "at_word": 15}])

sc("o08", "setup", "When you die, he takes your best animal. That one is called heriot.", {
    "background": village("spring"),
    "props": [{"type": "cow", "x": 0.55, "y": 0.86, "move": [[0.8, 0.55, 0.86], [3.4, 0.9, 0.86]], "walk": True}],
    "cast": [lord(x=0.75, facing=-1, action="walk", path=[[0.8, 0.7, GROUND], [3.4, 1.05, GROUND]],
                  expression="smug"),
             stan(x=0.2, action="sad", expression="crying")],
    "overlays": [{"type": "money", "text": "-heriot (best cow)", "x": 0.6, "y": 0.4, "at_word": 10}]},
    claims=[F("Heriot: on a tenant's death the lord took the best beast", SRC["bennett"])],
    sfx=[{"name": "ding", "at_word": 10}])

sc("o09", "setup", "Need flour? You must grind your grain at his mill, and he keeps a cut of it.", {
    "background": field("spring"),
    "props": [{"type": "mill", "x": 0.68, "y": 0.84, "scale": 1.15},
              {"type": "sack", "x": 0.42, "y": 0.86, "label": "GRAIN", "scale": 0.9}],
    "cast": [stan(x=0.25, action="push", expression="tired")],
    "overlays": [{"type": "money", "text": "-1 scoop for the lord", "x": 0.42, "y": 0.45, "at_word": 13}],
    "camera": {"move": "push_in"}},
    claims=[F("Tenants were often obliged to use the lord's mill and pay a toll (multure) in grain", SRC["dyer"])])

sc("o10", "setup", "And then there's the Church, which takes a tithe: one tenth of everything you produce.", {
    "background": {"type": "church"},
    "cast": [priest(x=0.65, facing=-1, action="hold", item="bag", expression="happy"),
             stan(x=0.3, action="sad", expression="sad")],
    "overlays": [{"type": "stat", "value": 10, "suffix": "%", "caption": "of your harvest → the Church", "y": 0.3,
                  "at_word": 10, "size": 170}]},
    claims=[F("A tithe of one tenth of produce was owed to the Church", SRC["dyer"])],
    sfx=[{"name": "ding", "at_word": 10}], transition="wipe")

sc("o13", "setup", "Break the rules, and you'll end up in the manor court, where your own neighbors help decide your fine.", {
    "background": {"type": "manor"},
    "cast": [lord(x=0.7, facing=-1, action="sit_talk", expression="angry"),
             reeve(x=0.52, facing=-1, action="hold", expression="neutral"),
             stan(x=0.25, action="cower", expression="worried")],
    "props": [{"type": "table", "x": 0.68, "y": 0.86, "w": 420, "items": ["book"]}],
    "overlays": [{"type": "title", "text": "THE MANOR COURT", "y": 0.14, "at_word": 7}]},
    claims=[F("Manor courts, with juries of tenants, fined villagers for breaches of custom", SRC["bennett"])],
    transition="wipe")

sc("o14", "setup", "Typical crimes? Letting your pig wander into the lord's crops, or brewing ale that's too weak.", {
    "background": field("spring", crops=0.4),
    "props": [{"type": "pig", "x": 0.6, "y": 0.92, "walk": True, "move": [[0, 0.3, 0.92], [3, 0.65, 0.92]]},
              {"type": "item", "item": "mug", "x": 0.85, "y": 0.6, "scale": 2.2, "at_word": 12}],
    "cast": [stan(x=0.15, action="panic", expression="scared")],
    "overlays": [{"type": "money", "text": "-6d fine", "x": 0.6, "y": 0.4, "at": 1.6}]},
    claims=[F("Common manor-court offences included straying animals and breaches of the assize of ale",
              SRC["bennett"])],
    sfx=[{"name": "boing", "at": 1.0}])

sc("o15", "setup", "And if someone shouts that a crime has happened, everyone must drop what they're doing and chase the culprit.", {
    "background": village("spring"),
    "cast": [cast("thief", "peasant", x=0.7, action="run", expression="scared", item="bag",
                  path=[[0, 0.55, GROUND], [5.5, 1.1, GROUND]]),
             stan(x=0.3, action="run", expression="angry", item="pitchfork",
                  path=[[1.2, 0.1, GROUND], [5.5, 0.85, GROUND]]),
             cast("p1", "peasant", x=0.1, action="run", expression="angry", at=2.0,
                  path=[[2.0, -0.1, GROUND], [5.5, 0.6, GROUND]])],
    "overlays": [{"type": "title", "text": "THE HUE AND CRY!", "y": 0.15, "at": 0.8, "color": "red"}],
    "camera": {"move": "pan_right", "amount": 220}},
    claims=[F("The 'hue and cry' obliged villagers to pursue suspected criminals", SRC["mortimer"])],
    sfx=[{"name": "whoosh", "at": 1.2}])

sc("o11", "setup", "Add it all up, and a big share of your work never feeds your own family.", {
    "background": {"type": "chalkboard"},
    "overlays": [{"type": "bars", "title": "Where your year's effort goes (rough idea)", "x": 0.2, "y": 0.3,
                  "items": [["Lord's fields", 3, "red", "2-3 days/week"], ["Tithe", 1, "gold", "10%"],
                            ["Rent & fees", 1, "orange", "many"], ["Your family", 3, "teal", "what's left"]],
                  "max": 3.6}]},
    claims=[F("Labor services, rents, fines and tithe took a large share of a villein's output; exact shares "
              "varied by manor", SRC["dyer"], "estimate")])

sc("o16", "setup", "Some of your rent isn't even paid in money. It's paid in hens at Christmas and eggs at Easter.", {
    "background": {"type": "manor"},
    "props": [{"type": "chicken", "x": 0.45, "y": 0.9, "at_word": 12},
              {"type": "chicken", "x": 0.52, "y": 0.92, "at_word": 12, "flip": -1},
              {"type": "item", "item": "egg", "x": 0.62, "y": 0.86, "scale": 2.0, "at_word": 16},
              {"type": "item", "item": "egg", "x": 0.68, "y": 0.86, "scale": 2.0, "at_word": 16}],
    "cast": [stan(x=0.25, action="hold", expression="neutral"), reeve(x=0.82, facing=-1, action="count",
                                                                       expression="smug")]},
    claims=[F("Rents in kind such as 'Christmas hens' and Easter eggs were common manorial dues", SRC["bennett"])],
    sfx=[{"name": "pop", "at_word": 12}, {"name": "pop", "at_word": 16}])

sc("o17", "setup", "Your one legal escape? Run to a chartered town and live there for a year and a day without being caught. Then you're free.", {
    "background": {"type": "town"},
    "cast": [stan(x=0.3, action="sneak", expression="worried", path=[[0, 0.05, GROUND], [4, 0.45, GROUND]],
                  actions=[["w18", "cheer"]], expressions=[["w18", "grin"]])],
    "props": [{"type": "calendar", "x": 0.78, "y": 0.75, "month": "1 YEAR", "day": "+1", "at_word": 11,
               "scale": 1.1}],
    "overlays": [{"type": "fact", "text": "A villein who lived unclaimed in a privileged town for a year and a day "
                                          "could gain his freedom.", "source": "Glanvill, Treatise on the Laws "
                                                                                "of England (c. 1188)",
                  "at_word": 6, "x": 0.03, "y": 0.04, "w": 820}]},
    claims=[F("A villein residing unclaimed for a year and a day in a privileged town could become free",
              "Glanvill, Treatise on the Laws of England (c. 1188)")])

sc("o12", "setup", "Still, it's not all misery. Sundays and dozens of holy days are days off from field work.", {
    "background": village("spring"),
    "cast": [stan(x=0.35, action="dance", expression="laughing"), maud(x=0.6, facing=-1, action="dance",
                                                                       expression="happy")],
    "props": [{"type": "icon", "icon": "sparkle", "x": 0.48, "y": 0.45}],
    "overlays": [{"type": "fact", "tag": "FACT", "text": "Sundays plus dozens of church feast days were holidays.",
                  "source": SRC["mortimer"], "at_word": 9}]},
    claims=[F("Sundays and many holy days (feast days) were rest days", SRC["mortimer"])],
    sfx=[{"name": "sparkle", "at": 0.3}])

# =========================================================================================================
# CHAPTER 3 — SPRING
# =========================================================================================================
ch("Spring: Mud, Oxen and Porridge")
sc("p01", "development", "It's spring, so it's time to plough. Your village farms huge open fields divided into long strips.", {
    "background": field("spring", crops=0.0),
    "overlays": [month("APRIL", 2), {"type": "timeline", "at": 0, "y": 0.1}],
    "props": [{"type": "plough", "x": 0.3, "y": 0.9, "move": [[0, 0.1, 0.9], [6, 0.5, 0.9]]}],
    "cast": [stan(x=0.12, action="push", path=[[0, 0.02, GROUND + 0.04], [6, 0.42, GROUND + 0.04]],
                  expression="determined")],
    "camera": {"move": "pan_right", "amount": 160}},
    claims=[F("Many English villages farmed open fields divided into strips", SRC["dyer"])],
    transition="wipe")

sc("p02", "development", "Your strips are scattered all over, so the good soil and the bad soil get shared around.", {
    "background": PAPER,
    "props": [{"type": "strips", "x": 0.5, "y": 0.8, "mine": [1, 5, 10], "reveal": 1.0, "scale": 1.05}],
    "overlays": [{"type": "label", "text": "yours!", "x": 0.5, "y": 0.13, "to_x": 0.3, "to_y": 0.35, "at": 1.0}]},
    claims=[F("A peasant's holding was scattered in strips across the fields", SRC["dyer"])])

sc("p03", "development", "A typical villein family might hold around thirty acres, but plenty of families had much less.", {
    "background": PAPER,
    "cast": [stan(x=0.25, action="talk", expression="neutral")],
    "overlays": [{"type": "stat", "value": "~30 acres", "caption": "a 'yardland' (virgate) — if you were lucky",
                  "x": 0.62, "y": 0.4, "size": 150, "at_word": 7}]},
    claims=[F("A standard villein holding (virgate/yardland) was often around 30 acres, varying by region; many "
              "held half that or less", SRC["dyer"] + "; " + SRC["bennett"], "estimate")])

sc("p04", "development", "Nobody owns enough oxen to pull a heavy plough alone, so neighbors share their animals.", {
    "background": field("spring"),
    "props": [{"type": "plough", "x": 0.35, "y": 0.92, "scale": 1.0}],
    "cast": [stan(x=0.2, action="push", expression="tired"),
             cast("neighbor", "peasant", x=0.75, facing=-1, action="wave", expression="happy", scale=1.2)],
    "camera": {"move": "push_in"}},
    claims=[F("Plough teams were often assembled by several tenants pooling their oxen", SRC["dyer"])])

sc("p05", "development", "Each year, one big field rests, called fallow, so the soil can recover.", {
    "background": PAPER,
    "props": [{"type": "board", "x": 0.25, "y": 0.5, "text": "FIELD 1\nwheat", "color": "wheat", "w": 420,
               "at": 0.3},
              {"type": "board", "x": 0.5, "y": 0.5, "text": "FIELD 2\noats & peas", "color": "lime", "w": 420,
               "at": 0.8},
              {"type": "board", "x": 0.75, "y": 0.5, "text": "FIELD 3\nresting", "color": "white", "w": 420,
               "at_word": 5}],
    "overlays": [{"type": "title", "text": "THE THREE-FIELD SYSTEM", "y": 0.14}]},
    claims=[F("Crop rotation with a fallow field (two- and three-field systems) was common", SRC["dyer"])],
    sfx=[{"name": "pop", "at": 0.3}, {"name": "pop", "at": 0.8}, {"name": "pop", "at_word": 5}])

sc("p06", "development", "You work from sunrise until the light is gone. So, what's for lunch?", {
    "background": field("spring", time="dusk"),
    "cast": [stan(x=0.4, action="dig", item="hoe", expression="tired", actions=[["w9", "idle"]],
                  expressions=[["w9", "happy"]])],
    "camera": {"move": "push_in", "focus": "stan"}},
    sfx=[{"name": "dig", "at": 0.4}, {"name": "dig", "at": 1.5}])

sc("p07", "development", "Pottage. A thick stew of grains, peas, beans and whatever vegetables are growing.", {
    "background": hut("spring", hearth_x=0.45),
    "props": [{"type": "pot", "x": 0.45, "y": 0.86, "scale": 1.3}],
    "cast": [maud(x=0.68, facing=-1, action="stir", expression="happy"),
             stan(x=0.2, action="idle", expression="happy", item="bread")],
    "overlays": [{"type": "title", "text": "POTTAGE", "y": 0.15, "at_word": 0}]},
    claims=[F("Pottage of grains and pulses was a staple of the peasant diet", SRC["dyer"])],
    sfx=[{"name": "sizzle", "at": 0.2, "gain_db": -10}])

sc("p08", "development", "Tomorrow? Pottage. The day after? You guessed it.", {
    "background": hut("spring", hearth_x=0.45),
    "props": [{"type": "pot", "x": 0.45, "y": 0.86, "scale": 1.3}],
    "cast": [stan(x=0.25, action="eat", expression="tired", expressions=[["w4", "sad"]])],
    "overlays": [{"type": "counter", "label": "POTTAGE STREAK:", "from": 1, "to": 47, "time": 2.0}]})

sc("p09", "development", "Add dark bread made from rye or barley, and a little cheese, eggs, or bacon when you can get them.", {
    "background": PAPER,
    "props": [{"type": "item", "item": "bread", "x": 0.2, "y": 0.62, "scale": 4.5, "at": 0.2},
              {"type": "item", "item": "egg", "x": 0.42, "y": 0.62, "scale": 4.5, "at_word": 13},
              {"type": "plate", "x": 0.64, "y": 0.66, "food": "meat", "scale": 2.4, "at_word": 15},
              {"type": "icon", "icon": "?", "x": 0.84, "y": 0.62, "at_word": 17, "size": 130}]},
    claims=[F("Bread from rye, barley or mixed grains, with some dairy, eggs and occasional bacon", SRC["dyer"])],
    sfx=[{"name": "pop", "at_word": 1}, {"name": "pop", "at_word": 13}, {"name": "pop", "at_word": 15}])

sc("p10", "development", "And to drink? Ale. Lots of it. Weak, cloudy ale was a daily food, not a party drink.", {
    "background": village("spring"),
    "cast": [stan(x=0.4, action="drink", item="mug", expression="happy", actions=[["w5", "cheer"]],
                  expressions=[["w5", "laughing"]])],
    "overlays": [{"type": "fact", "text": "Ale was a staple: brewed mostly by women ('alewives') and regulated by "
                                          "the Assize of Bread and Ale.", "source": SRC["bennett"], "at_word": 6}]},
    claims=[F("Ale was a dietary staple, commonly brewed by women", SRC["bennett"]),
            F("The Assize of Bread and Ale regulated prices and quality", SRC["bennett"])],
    sfx=[{"name": "gulp", "at": 0.6}])

sc("p11", "development", "People did drink water too. But ale was safer, tastier, and it filled you up.", {
    "background": field("spring"),
    "props": [{"type": "well", "x": 0.72, "y": 0.84}],
    "cast": [stan(x=0.4, action="hold", item="mug", expression="smug")],
    "overlays": [{"type": "caption", "text": "Myth: \"medieval people never drank water\" — they did.", "at_word": 0}]},
    claims=[F("Medieval people did drink water; ale was nonetheless a staple calorie source", SRC["mortimer"])])

sc("p14", "development", "Maud works just as hard as you. She brews, spins wool, makes cheese, keeps the animals, and helps in the fields.", {
    "background": hut("spring", hearth_x=0.82, window_x=0.08),
    "props": [{"type": "barrel", "x": 0.2, "y": 0.86, "at_word": 7}, {"type": "sheep", "x": 0.6, "y": 0.9,
                                                                       "at_word": 9, "scale": 0.8}],
    "cast": [maud(x=0.38, action="stir", expression="determined", actions=[["w13", "carry"]])],
    "overlays": [{"type": "checklist", "x": 0.62, "y": 0.18, "size": 46,
                  "items": [["brew ale", True], ["spin wool", True], ["make cheese", True], ["animals", True],
                            ["field work", True]], "times": [1.6, 2.4, 3.1, 3.9, 4.8]}]},
    claims=[F("Peasant women brewed, spun, made dairy produce, tended livestock and worked in the fields",
              SRC["bennett"] + "; " + SRC["dyer"])],
    transition="wipe")

sc("p15", "development", "And Wat? At seven, he's already working: collecting firewood, minding geese, and scaring birds off the seeds.", {
    "background": field("spring", crops=0.2),
    "cast": [wat(x=0.4, action="panic", expression="angry")],
    "props": [{"type": "icon", "icon": "anger", "x": 0.4, "y": 0.45},
              {"type": "chicken", "x": 0.7, "y": 0.92, "move": [[2, 0.7, 0.92], [4, 1.1, 0.7]]},
              {"type": "chicken", "x": 0.8, "y": 0.92, "move": [[2.2, 0.8, 0.92], [4.2, 1.2, 0.6]]}],
    "overlays": [{"type": "caption", "text": "medieval scarecrow: an actual child", "at": 3.0}]},
    claims=[F("Children did tasks such as gathering fuel, tending animals and bird-scaring", SRC["dyer"])],
    sfx=[{"name": "boing", "at": 2.0}])

sc("p16", "development", "Your clothes are simple: a wool tunic, linen underneath, and a hood. You own maybe two outfits.", {
    "background": PAPER,
    "cast": [stan(x=0.5, action="hold", expression="smug", hat="hood", hat_color="tan", scale=1.5)],
    "overlays": [{"type": "label", "text": "wool tunic", "x": 0.75, "y": 0.55, "to_x": 0.54, "to_y": 0.6,
                  "at_word": 5},
                 {"type": "label", "text": "hood", "x": 0.72, "y": 0.2, "to_x": 0.53, "to_y": 0.27,
                  "at_word": 11},
                 {"type": "label", "text": "linen underneath", "x": 0.25, "y": 0.4, "to_x": 0.45, "to_y": 0.55,
                  "at_word": 8}]},
    claims=[F("Peasants wore woollen outer garments over linen undergarments", SRC["mortimer"])])

sc("p17", "development", "And then there's the hungry gap: late spring, when last year's food is running out, and the new crops aren't ready yet.", {
    "background": hut("spring", hearth_x=0.88, dark=0.15),
    "props": [{"type": "barrel", "x": 0.2, "y": 0.86}, {"type": "sack", "x": 0.32, "y": 0.86, "scale": 0.6,
                                                         "label": ""}],
    "cast": [stan(x=0.5, action="sad", expression="tired"), wat(x=0.66, action="idle", expression="sad")],
    "overlays": [{"type": "meter", "label": "FOOD STORES", "from": 0.4, "to": 0.08, "y": 0.12, "time": 3.0}]},
    claims=[F("Late spring/early summer was the leanest time before the new harvest", SRC["dyer"])])

sc("p12", "development", "Your parents remember the Great Famine of 1315 to 1317. Years of rain, rotting crops, and hunger.", {
    "background": field("autumn", weather="rain", time="grey"),
    "cast": [cast("dad", "peasant", x=0.4, action="sad", expression="crying", color=(0.4, 0.4, 0.45)),
             cast("mum", "peasant_woman", x=0.6, facing=-1, action="sad", expression="sad", color=(0.4, 0.4, 0.45))],
    "overlays": [{"type": "tint", "color": (0.45, 0.35, 0.2), "alpha": 0.35},
                 {"type": "title", "text": "1315-1317", "y": 0.15, "at_word": 7}]},
    claims=[F("The Great Famine of 1315-1317 followed years of torrential rain and failed harvests",
              SRC["famine"])],
    transition="fade")

sc("p13", "development", "So every spring, you plant, you pray, and you hope the weather behaves.", {
    "background": {"type": "church"},
    "cast": [stan(x=0.4, action="pray", expression="worried"), maud(x=0.6, action="pray", expression="worried")],
    "camera": {"move": "push_in"}},
    transition="fade")

# =========================================================================================================
# CHAPTER 4 — MYTHS
# =========================================================================================================
ch("Wait… Were They Really That Dirty?")
sc("m01", "development", "Quick myth check. You've probably heard that medieval people never washed. Not true.", {
    "background": LINED,
    "cast": [stan(x=0.3, action="talk", expression="neutral", actions=[["w12", "point_up"]])],
    "props": [{"type": "icon", "icon": "x", "x": 0.7, "y": 0.6, "at_word": 12, "scale": 1.5}],
    "overlays": [{"type": "title", "text": "MYTH BUSTING", "y": 0.15, "color": "red"}]},
    sfx=[{"name": "pop", "at_word": 12}], transition="wipe")

sc("m02", "development", "Washing your hands and face every morning was normal, and towns had public bathhouses, called stews.", {
    "background": {"type": "town"},
    "props": [{"type": "tub", "x": 0.6, "y": 0.92, "scale": 1.3, "at_word": 11},
              {"type": "item", "item": "bucket", "x": 0.25, "y": 0.9, "scale": 1.5}],
    "cast": [stan(x=0.35, action="scratch", expression="happy", actions=[["w11", "point"]])],
    "overlays": [{"type": "label", "text": "a 'stew' (bathhouse)", "x": 0.82, "y": 0.35, "to_x": 0.65, "to_y": 0.7,
                  "at_word": 14}]},
    claims=[F("Daily washing of hands and face was customary; towns had public bathhouses ('stews')",
              SRC["bathing"] + "; " + SRC["mortimer"])])

sc("m03", "development", "And the idea that everyone died at thirty? That average is dragged down by children.", {
    "background": PAPER,
    "overlays": [{"type": "stat", "value": "30?", "caption": "average life expectancy at birth", "y": 0.38,
                  "at_word": 6, "color": "red"}],
    "cast": [stan(x=0.18, action="shrug", expression="thinking", scale=1.1)]},
    claims=[F("Low average life expectancy at birth was driven by high infant and child mortality",
              SRC["dyer"], "estimate")])

sc("m04", "development", "Sadly, around one in three children didn't reach adulthood. But if you did, reaching your fifties or sixties was normal.", {
    "background": LINED,
    "overlays": [{"type": "people", "n": 9, "k": 3, "cols": 9, "color": (0.5, 0.5, 0.55), "dim": "ink",
                  "from_end": False, "y": 0.6, "caption": "≈ 1 in 3 children didn't make it to adulthood",
                  "fig_scale": 0.6}]},
    claims=[F("Roughly a third of children may have died before adulthood; adults commonly lived into their 50s-60s",
              SRC["dyer"] + "; " + SRC["mortimer"], "estimate")])

sc("m05", "development", "So, rule one of surviving 1348: get past childhood. Good news: you already did.", {
    "background": village("spring"),
    "cast": [stan(x=0.45, action="cheer", expression="grin")],
    "overlays": [{"type": "checklist", "items": [["Survive childhood", True]], "x": 0.6, "y": 0.35, "at_word": 4},
                 odds(0.5, 0.6)]},
    sfx=[{"name": "ding", "at_word": 11}])

# =========================================================================================================
# CHAPTER 5 — SUMMER & THE PLAGUE
# =========================================================================================================
ch("Summer: Something Is Coming")
sc("s01", "development", "Summer. The crops are growing, the hay needs cutting, and the village is busy.", {
    "background": field("summer", crops=0.7),
    "cast": [stan(x=0.3, action="swing", item="scythe", expression="happy"),
             maud(x=0.6, facing=-1, action="carry", expression="happy", action_params={"walking": False}),
             wat(x=0.78, action="jump", expression="grin")],
    "overlays": [month("JUNE", 4), {"type": "timeline", "at": 1, "from_at": 0, "y": 0.1}]},
    sfx=[{"name": "whoosh", "at": 0.6, "gain_db": -6}], transition="wipe")

sc("s02", "development", "But around the end of June, a ship docks at Melcombe, a port in Dorset.", {
    "background": {"type": "field", "season": "summer", "ground": "sand"},
    "props": [{"type": "sea", "x": 0.5, "y": 0.84}, {"type": "ship", "x": 0.55, "y": 0.86, "scale": 1.0,
                                                      "move": [[0, 1.2, 0.86], [3.5, 0.55, 0.86]]}],
    "overlays": [{"type": "title", "text": "MELCOMBE, DORSET", "y": 0.15, "at_word": 10},
                 {"type": "counter", "label": "JUNE", "value": "1348", "corner": "tr"}],
    "camera": {"move": "pan_left", "amount": 120}},
    claims=[F("The Black Death arrived in England at Melcombe (Weymouth), Dorset, in June 1348", SRC["horrox"])],
    transition="fade")

sc("s03", "climax", "On board is something nobody can see: plague. The Black Death has reached England.", {
    "background": {"type": "field", "season": "summer", "ground": "sand", "time": "grey"},
    "props": [{"type": "sea", "x": 0.5, "y": 0.84}, {"type": "ship", "x": 0.55, "y": 0.86},
              {"type": "rat", "x": 0.4, "y": 0.9, "walk": True, "move": [[0.5, 0.5, 0.9], [2.5, 0.2, 0.9]]},
              {"type": "germ", "x": 0.7, "y": 0.45, "at_word": 7, "scale": 1.6, "loop": "bob"}],
    "overlays": [{"type": "tint", "color": (0.2, 0.35, 0.1), "alpha": 0.3, "at_word": 7},
                 {"type": "title", "text": "THE BLACK DEATH", "color": "red", "y": 0.15, "at_word": 9}],
    "camera": {"move": "push_in", "zoom_to": 1.15, "impacts": ["w7"]}},
    claims=[F("Plague (the Black Death) spread through England from summer 1348", SRC["horrox"])],
    sfx=[{"name": "rumble", "at_word": 7}, {"name": "boom", "at_word": 9, "gain_db": -6}], transition="cut")

sc("s04", "climax", "It's caused by a bacterium, Yersinia pestis, carried by fleas that live on rats, and on people.", {
    "background": {"type": "solid", "color": (0.16, 0.2, 0.16)},
    "props": [{"type": "germ", "x": 0.25, "y": 0.6, "scale": 2.0},
              {"type": "rat", "x": 0.6, "y": 0.7, "scale": 2.0, "at_word": 11},
              {"type": "fleas", "x": 0.6, "y": 0.6, "n": 9, "at_word": 8, "scale": 2.5}],
    "overlays": [{"type": "label", "text": "Yersinia pestis", "x": 0.25, "y": 0.2, "to_x": 0.25, "to_y": 0.38,
                  "at_word": 5, "outline_color": "ink", "color": "white"},
                 {"type": "label", "text": "fleas", "x": 0.82, "y": 0.25, "to_x": 0.63, "to_y": 0.35, "at_word": 8,
                  "outline_color": "ink", "color": "white"}]},
    claims=[F("Plague is caused by Yersinia pestis, transmitted by fleas from rats; human-to-human spread "
              "(including via human fleas/lice and pneumonic form) is also discussed by historians",
              SRC["cdc"] + "; " + SRC["benedictow"])],
    sfx=[{"name": "pop", "at_word": 11}])

sc("s05", "climax", "Of course, nobody in 1348 knows that. Doctors blame bad air, the stars, or God's anger.", {
    "background": {"type": "town", "time": "grey"},
    "cast": [cast("doc", "modern", x=0.3, outfit="robe", outfit_color="purple", hat="cap", hat_color="purple",
                  action="talk", expression="thinking", item="book"),
             stan(x=0.7, facing=-1, action="scratch", expression="worried")],
    "props": [{"type": "icon", "icon": "?", "x": 0.7, "y": 0.35, "at_word": 6}],
    "overlays": [{"type": "checklist", "x": 0.06, "y": 0.2, "items": [["bad air (miasma)", None],
                                                                     ["the stars", None], ["God's anger", None]],
                  "times": [1.8, 2.6, 3.4], "size": 48}]},
    claims=[F("Contemporaries blamed corrupted air (miasma), planetary conjunctions and divine punishment",
              SRC["horrox"])])

sc("s06", "climax", "And no, the famous beaked plague doctor mask wasn't around yet. That shows up in the sixteen hundreds.", {
    "background": LINED,
    "cast": [cast("doctor", "doctor", x=0.5, action="idle", expression="neutral", scale=1.4)],
    "props": [{"type": "icon", "icon": "x", "x": 0.72, "y": 0.4, "at_word": 8, "scale": 1.3}],
    "overlays": [{"type": "title", "text": "WRONG CENTURY!", "color": "red", "y": 0.15, "at_word": 8},
                 {"type": "fact", "text": "The beaked costume is described in the 1600s, not 1348.",
                  "source": SRC["bl"], "at_word": 12, "x": 0.03, "y": 0.68, "w": 640}]},
    claims=[F("The beaked plague-doctor costume dates from the 17th century", SRC["bl"])],
    sfx=[{"name": "boing", "at_word": 8}], transition="wipe")

sc("s07", "climax", "By July the plague is spreading inland. Village by village, the news arrives before the disease does.", {
    "background": {"type": "map", "seed": 5},
    "props": [{"type": "germ", "x": 0.42, "y": 0.78, "scale": 0.9, "at": 0.2},
              {"type": "germ", "x": 0.5, "y": 0.66, "scale": 0.8, "at": 1.4},
              {"type": "germ", "x": 0.58, "y": 0.55, "scale": 0.8, "at": 2.6},
              {"type": "germ", "x": 0.47, "y": 0.42, "scale": 0.8, "at": 3.8},
              {"type": "hut", "x": 0.62, "y": 0.62, "scale": 0.25, "smoke": False}],
    "overlays": [{"type": "label", "text": "Stan's village", "x": 0.8, "y": 0.45, "to_x": 0.64, "to_y": 0.55,
                  "at": 1.0}, month("JULY", 5)],
    "camera": {"move": "push_in", "zoom_to": 1.1}},
    claims=[F("Plague spread from Dorset across southern England through summer and autumn 1348", SRC["horrox"])],
    sfx=[{"name": "pop", "at": 0.2}, {"name": "pop", "at": 1.4}, {"name": "pop", "at": 2.6}])

sc("s07b", "climax", "It reaches Bristol in August, and London by the autumn. Wherever people travel, it travels too.", {
    "background": {"type": "map", "seed": 5},
    "props": [{"type": "sign", "x": 0.3, "y": 0.62, "text": "BRISTOL\nAUGUST", "post": False, "w": 300, "h": 140,
               "size": 40, "at_word": 2},
              {"type": "sign", "x": 0.72, "y": 0.52, "text": "LONDON\nAUTUMN", "post": False, "w": 300, "h": 140,
               "size": 40, "at_word": 7},
              {"type": "arrow", "x": 0.4, "y": 0.6, "dx": 330, "dy": -90, "at_word": 7, "color": "red"},
              {"type": "cart", "x": 0.55, "y": 0.86, "scale": 0.6, "moving": True,
               "move": [[0, 0.3, 0.86], [5.5, 0.8, 0.86]]}]},
    claims=[F("Plague reached Bristol by August 1348 and London by autumn 1348", SRC["horrox"] + "; " + SRC["benedictow"])],
    sfx=[{"name": "pop", "at_word": 2}, {"name": "pop", "at_word": 7}])

sc("s08", "climax", "The symptoms are terrifying: fever, and painful swellings called buboes in the armpits or groin.", {
    "background": hut("summer", dark=0.35, hearth_x=0.8),
    "props": [{"type": "bed", "x": 0.45, "y": 0.9, "scale": 1.3}],
    "cast": [cast("neighbor", "peasant", x=0.48, y=0.87, action="lie", expression="sick")],
    "overlays": [{"type": "checklist", "x": 0.6, "y": 0.2, "title": "SYMPTOMS",
                  "items": [["high fever", None], ["swollen 'buboes'", None], ["exhaustion", None]],
                  "times": [1.5, 3.0, 4.5], "size": 50}]},
    claims=[F("Bubonic plague causes fever and swollen lymph nodes (buboes) in groin, armpit or neck", SRC["cdc"])],
    transition="fade")

sc("s09", "climax", "Many of the sick die within a week. Some recover. Nobody knows why.", {
    "background": hut("summer", dark=0.45, hearth=False),
    "props": [{"type": "hourglass", "x": 0.75, "y": 0.8, "period": 4}],
    "cast": [maud(x=0.35, action="pray", expression="crying"), stan(x=0.18, action="sad", expression="sad")],
    "camera": {"move": "push_in"}},
    claims=[F("Many bubonic plague victims died within about a week; some survived", SRC["horrox"])],
    sfx=[{"name": "clock", "at": 0.5, "gain_db": -8}])

sc("s09b", "climax", "Stan's family stays home, prays, and waits. Every cough in the night sounds like a death sentence.", {
    "background": hut("autumn", dark=0.5, hearth_x=0.5),
    "cast": [stan(x=0.3, action="shiver", expression="scared"), maud(x=0.68, facing=-1, action="pray",
                                                                      expression="worried"),
             wat(x=0.8, facing=-1, action="cower", expression="scared")],
    "overlays": [{"type": "vignette", "alpha": 0.6}, WHATIF],
    "camera": {"move": "push_in", "zoom_to": 1.12}},
    sfx=[{"name": "clock", "at": 0.3, "gain_db": -10}])

sc("s10", "climax", "By autumn, the plague is in your village. Your neighbor goes first. Then the priest.", {
    "background": village("autumn", time="grey"),
    "props": [{"type": "cross", "x": 0.62, "y": 0.86, "at_word": 9},
              {"type": "cross", "x": 0.75, "y": 0.86, "at_word": 12},
              {"type": "bell", "x": 0.85, "y": 0.35, "scale": 0.8}],
    "cast": [stan(x=0.3, action="sad", expression="crying")],
    "overlays": [{"type": "tint", "color": (0.2, 0.2, 0.3), "alpha": 0.25}],
    "camera": {"move": "push_in"}},
    claims=[F("Parish clergy, who visited the dying, suffered very high death rates", SRC["horrox"])],
    sfx=[{"name": "ding", "at_word": 9, "gain_db": -6}, {"name": "ding", "at_word": 12, "gain_db": -6}])

sc("s14", "climax", "People try everything. Processions, prayers, bonfires, fleeing to the countryside. Nothing seems to work.", {
    "background": village("autumn", time="grey"),
    "props": [{"type": "fire", "x": 0.8, "y": 0.86, "at_word": 5}],
    "cast": [priest(x=0.3, action="walk", item="cross" if False else "candle", expression="worried",
                    path=[[0, 0.15, GROUND], [5, 0.45, GROUND]]),
             cast("p1", "peasant", x=0.1, action="pray", expression="crying", color=(0.3, 0.3, 0.35)),
             cast("p2", "peasant_woman", x=0.6, action="run", expression="scared", at_word=7,
                  path=[[2.5, 0.6, GROUND], [5.5, 1.1, GROUND]])]},
    claims=[F("Responses included religious processions, prayer and flight", SRC["horrox"])],
    transition="fade")

sc("s15", "climax", "Graveyards fill up so fast that new burial grounds are opened, like the one at East Smithfield in London.", {
    "background": {"type": "church"},
    "props": [{"type": "grave", "x": 0.2, "y": 0.92, "scale": 0.8}, {"type": "grave", "x": 0.35, "y": 0.9, "scale": 0.8, "at": 0.6},
              {"type": "grave", "x": 0.5, "y": 0.92, "scale": 0.8, "at": 1.2}, {"type": "grave", "x": 0.65, "y": 0.9, "scale": 0.8, "at": 1.8},
              {"type": "grave", "x": 0.8, "y": 0.92, "scale": 0.8, "at": 2.4}],
    "overlays": [{"type": "fact", "text": "East Smithfield, London: an emergency cemetery opened for plague victims "
                                          "in 1348-49.", "source": "Museum of London Archaeology", "at_word": 13}]},
    claims=[F("East Smithfield was an emergency Black Death cemetery in London (1348-49)",
              "Museum of London Archaeology")],
    sfx=[{"name": "pop", "at": 0.6}, {"name": "pop", "at": 1.2}, {"name": "pop", "at": 1.8}])

sc("s11", "climax", "Across England, somewhere between a third and a half of the population dies. Possibly more.", {
    "background": LINED,
    "overlays": [{"type": "people", "n": 10, "k": 5, "cols": 10, "color": (0.6, 0.6, 0.64), "dim": "ink",
                  "reveal_at": 1.6, "y": 0.6, "caption": "Out of every 10 people, 3 to 5 died", "fig_scale": 0.6}]},
    claims=[F("Estimates of Black Death mortality in England range from about a third to a half or more; "
              "Benedictow argues for ~60%", SRC["horrox"] + "; " + SRC["benedictow"], "estimate")],
    transition="wipe")

sc("s12", "climax", "Whole families vanish. Some villages are simply abandoned.", {
    "background": village("autumn", time="dusk", n_clouds=2),
    "props": [{"type": "grave", "x": 0.3, "y": 0.9, "scale": 0.8}, {"type": "grave", "x": 0.45, "y": 0.92, "scale": 0.8},
              {"type": "grave", "x": 0.6, "y": 0.9, "scale": 0.8}],
    "overlays": [{"type": "vignette", "alpha": 0.6}],
    "camera": {"move": "pull_out"}},
    claims=[F("Some settlements were deserted after the plague, though many 'lost villages' declined over a "
              "longer period", SRC["dyer"])],
    transition="fade")

sc("s13", "climax", "And Stan? Stan gets lucky. Maud and Wat too. Nobody really knows why some survived.", {
    "background": village("autumn"),
    "cast": [stan(x=0.35, action="idle", expression="sad", expressions=[["w4", "happy"]], actions=[["w4", "cheer"]]),
             maud(x=0.55, action="idle", expression="happy", at_word=5, enter="pop"),
             wat(x=0.68, action="jump", expression="grin", at_word=7, enter="pop")],
    "overlays": [odds(0.35, 0.8, 0.6)]},
    claims=[F("Stan's family surviving is fictional", "Narrative device", "fiction")],
    sfx=[{"name": "pop", "at_word": 5}, {"name": "pop", "at_word": 7}], transition="fade")

# =========================================================================================================
# CHAPTER 6 — AUTUMN
# =========================================================================================================
ch("Autumn: The Harvest Nobody Can Bring In")
sc("a01", "development", "Now it's harvest time, the most important weeks of the year. But half the workers are gone.", {
    "background": field("autumn", crops=1.0),
    "cast": [stan(x=0.35, action="swing", item="sickle", expression="tired")],
    "overlays": [month("SEPTEMBER", 7), {"type": "timeline", "at": 2, "from_at": 1, "y": 0.1}],
    "camera": {"move": "pan_right", "amount": 140}},
    transition="wipe")

sc("a02", "development", "Chroniclers describe crops rotting in the fields and animals wandering with nobody to look after them.", {
    "background": field("autumn", crops=1.0, time="grey"),
    "props": [{"type": "sheep", "x": 0.3, "y": 0.92, "move": [[0, 0.2, 0.92], [5, 0.4, 0.92]]},
              {"type": "cow", "x": 0.7, "y": 0.9, "walk": True, "move": [[0, 0.85, 0.9], [5, 0.65, 0.9]]}],
    "overlays": [{"type": "quote", "text": "Sheep and cattle strayed through the fields and among the crops, and "
                                           "there was no one to drive them off.",
                  "by": "Henry Knighton, chronicler (paraphrased)", "y": 0.3, "size": 50, "w": 1350}]},
    claims=[F("Henry Knighton described livestock wandering untended after the plague", SRC["horrox"])])

sc("a03", "development", "Which means, for the first time in your life, you have something the lord desperately needs.", {
    "background": {"type": "manor"},
    "cast": [stan(x=0.3, action="idle", expression="smug"),
             lord(x=0.62, facing=-1, action="cower", expression="worried")],
    "props": [{"type": "icon", "icon": "!", "x": 0.3, "y": 0.4, "at_word": 10}],
    "camera": {"move": "push_in"}},
    sfx=[{"name": "ding", "at_word": 10}])

sc("a04", "development", "Your labor. Workers are suddenly rare, so they start demanding higher wages.", {
    "background": {"type": "manor"},
    "cast": [stan(x=0.3, action="point", expression="determined",
                  say=[{"text": "Double pay. Or do it yourself.", "at": 1.2}]),
             lord(x=0.66, facing=-1, action="angry", expression="angry")],
    "overlays": [{"type": "counter", "label": "WAGES:", "from": 1, "to": 3, "suffix": "d / day", "time": 1.6,
                  "icon": "coin", "at_word": 8}]},
    claims=[F("After the Black Death labor shortages pushed wages sharply upward", SRC["dyer"])],
    sfx=[{"name": "ding", "at_word": 8}])

sc("a05", "development", "The government panics. In 1349, a new law tries to freeze wages at pre-plague levels.", {
    "background": {"type": "castle"},
    "cast": [cast("king", "king", x=0.4, action="angry", expression="angry", item="scroll")],
    "props": [{"type": "scroll", "x": 0.72, "y": 0.86, "lines": ["ORDINANCE OF", "LABOURERS, 1349", "",
                                                                  "No raises.", "No moving.", "Back to work!"],
               "w": 460, "h": 540, "size": 44, "at_word": 7}],
    "overlays": [{"type": "fact", "text": "The Ordinance of Labourers (1349) and Statute of Labourers (1351) tried to "
                                          "cap wages.", "source": SRC["statute"], "at": 2.0, "x": 0.03, "y": 0.04}]},
    claims=[F("The Ordinance of Labourers (1349) and Statute of Labourers (1351) attempted to fix wages at "
              "pre-plague levels", SRC["statute"])],
    transition="wipe")

sc("a05b", "development", "On many manors, lords also start swapping your labor services for a simple money rent. Fewer days working his fields.", {
    "background": {"type": "manor"},
    "cast": [stan(x=0.3, action="hold", item="coin", expression="happy"),
             lord(x=0.66, facing=-1, action="shrug", expression="worried")],
    "overlays": [{"type": "checklist", "x": 0.55, "y": 0.18, "size": 50,
                  "items": [["2-3 days of unpaid work", False], ["a cash rent instead", True]], "times": [1.5, 3.2]}]},
    claims=[F("After the Black Death labor services were increasingly commuted to money rents", SRC["dyer"])])

sc("a06", "development", "It doesn't really work. Lords quietly break it themselves, because otherwise their crops rot.", {
    "background": field("autumn", crops=1.0),
    "cast": [lord(x=0.6, facing=-1, action="hold", item="bag", expression="worried"),
             stan(x=0.3, action="count", expression="happy")],
    "overlays": [{"type": "money", "text": "+3d", "x": 0.32, "y": 0.4, "at": 1.4}]},
    claims=[F("Wage laws were widely evaded as employers competed for scarce labor", SRC["dyer"])],
    sfx=[{"name": "ding", "at": 1.4}])

sc("a08", "development", "There's also empty land now. Holdings whose families died are suddenly available, and some survivors grab them.", {
    "background": PAPER,
    "props": [{"type": "strips", "x": 0.5, "y": 0.8, "mine": [1, 2, 5, 6, 10], "reveal": 2.5, "scale": 1.0}],
    "cast": [stan(x=0.12, action="cheer", expression="grin", at=2.5, enter="pop")],
    "overlays": [{"type": "label", "text": "more strips for Stan!", "x": 0.5, "y": 0.13, "to_x": 0.45, "to_y": 0.35,
                  "at": 2.8}]},
    claims=[F("Vacant holdings after the plague were taken up by survivors, often on better terms", SRC["dyer"])],
    sfx=[{"name": "sparkle", "at": 2.5}])

sc("a09", "development", "It's a strange feeling. The worst year in memory is also the first time peasants hold some real power.", {
    "background": field("autumn", crops=0.0, time="dusk"),
    "cast": [stan(x=0.45, action="think", expression="thinking", scale=1.4)],
    "camera": {"move": "push_in", "focus": "stan"}},
    transition="fade")

sc("a07", "development", "Before winter, you thresh the grain, store it, and pay your tithe. Again.", {
    "background": village("autumn"),
    "props": [{"type": "sack", "x": 0.55, "y": 0.86, "label": "GRAIN"},
              {"type": "sack", "x": 0.65, "y": 0.86, "label": "GRAIN", "at": 0.8},
              {"type": "barrel", "x": 0.75, "y": 0.86, "at": 1.6}],
    "cast": [stan(x=0.3, action="dig", item="club", expression="determined"),
             priest(x=0.88, facing=-1, at_word=10, enter="slide_left", action="hold", item="bag",
                    expression="happy")],
    "overlays": [{"type": "money", "text": "-10%", "x": 0.85, "y": 0.4, "at_word": 11}]},
    sfx=[{"name": "dig", "at": 0.3}, {"name": "dig", "at": 1.0}, {"name": "whoosh", "at_word": 10}])

# =========================================================================================================
# CHAPTER 7 — WINTER
# =========================================================================================================
ch("Winter: Salt, Smoke and Christmas")
sc("w01", "development", "November is slaughter month. Animals you can't feed through winter are killed, and their meat is salted.", {
    "background": village("winter", snowfall=False),
    "props": [{"type": "barrel", "x": 0.6, "y": 0.86}, {"type": "pig", "x": 0.8, "y": 0.88},
              {"type": "sack", "x": 0.45, "y": 0.86, "label": "SALT", "color": "white", "at_word": 15}],
    "cast": [stan(x=0.3, action="idle", expression="neutral")],
    "overlays": [month("NOVEMBER", 9), {"type": "timeline", "at": 3, "from_at": 2, "y": 0.1}]},
    claims=[F("Livestock were slaughtered in late autumn and the meat salted or smoked for winter", SRC["dyer"])],
    transition="wipe")

sc("w02", "development", "Winter is long, dark and cold. The whole family sleeps close together by the fire.", {
    "background": hut("winter", hearth_x=0.5, dark=0.2),
    "props": [{"type": "bed", "x": 0.3, "y": 0.9, "scale": 1.7}, {"type": "icon", "icon": "z", "x": 0.3, "y": 0.66}],
    "cast": [stan(x=0.4, y=0.88, action="sleep", expression="sleepy", scale=1.1),
             maud(x=0.4, y=0.84, action="sleep", expression="sleepy", scale=1.1),
             cast("wat", "child", x=0.75, action="shiver", expression="scared", scale=1.1)],
    "camera": {"move": "push_in"}},
    sfx=[{"name": "sizzle", "at": 0.2, "gain_db": -12}])

sc("w03", "development", "But then comes the best part of the year: Christmas. Twelve whole days of it.", {
    "background": village("winter"),
    "cast": [stan(x=0.4, action="cheer", expression="grin"), wat(x=0.6, action="jump", expression="grin")],
    "overlays": [{"type": "title", "lines": ["12 DAYS", "OF CHRISTMAS"], "colors": ["red", "green"], "y": 0.15,
                  "at_word": 11}]},
    claims=[F("The twelve days of Christmas were a major holiday period", SRC["bennett"])],
    sfx=[{"name": "sparkle", "at_word": 11}])

sc("w04", "development", "Work on the lord's land stops, and on many manors, the lord even provides a feast for his tenants.", {
    "background": hut("winter", hearth_x=0.85),
    "props": [{"type": "table", "x": 0.5, "y": 0.9, "w": 720, "items": ["plate", "bread", "mug", "plate"],
               "item_scale": 0.9}],
    "cast": [stan(x=0.25, action="eat", expression="happy"), maud(x=0.42, action="laugh", expression="laughing"),
             lord(x=0.7, facing=-1, action="drink", item="mug", expression="happy")],
    "camera": {"move": "push_in"}},
    claims=[F("On many manors labor services were suspended at Christmas and lords provided a feast "
              "(sometimes the tenants contributed food)", SRC["bennett"])])

sc("w05", "development", "For a few days, there's meat, ale, and music. And then, slowly, the light returns.", {
    "background": village("winter", time="dusk"),
    "cast": [stan(x=0.35, action="dance", expression="laughing"), maud(x=0.55, facing=-1, action="dance",
                                                                       expression="happy")],
    "props": [{"type": "fire", "x": 0.75, "y": 0.86}]},
    sfx=[{"name": "sparkle", "at": 0.5}])

sc("w06", "development", "The rest of winter is quiet work indoors: mending tools, spinning, telling stories by the fire, and waiting for spring.", {
    "background": hut("winter", hearth_x=0.5),
    "cast": [stan(x=0.25, action="sit", item="hammer", expression="neutral"),
             maud(x=0.72, facing=-1, action="sit_talk", expression="happy"),
             wat(x=0.6, facing=-1, action="sit", expression="grin")],
    "props": [{"type": "stool", "x": 0.25, "y": 0.84}, {"type": "stool", "x": 0.72, "y": 0.84}],
    "camera": {"move": "push_in"}},
    claims=[F("Winter was used for indoor work such as repairs and spinning", SRC["dyer"])],
    transition="fade")

# =========================================================================================================
# CHAPTER 8 — FINAL SCORE
# =========================================================================================================
ch("Did You Survive?")
sc("f01", "ending", "March twenty-fourth, 1349. The last day of your year. Let's check the score.", {
    "background": village("spring"),
    "cast": [stan(x=0.3, action="idle", expression="happy"), maud(x=0.48, action="idle", expression="happy"),
             wat(x=0.6, action="idle", expression="grin")],
    "overlays": [{"type": "title", "text": "MARCH 24, 1349", "y": 0.15, "at_word": 0}]},
    transition="wipe")

sc("f02", "ending", "You survived the work, the fees, the pottage, the winter, and the deadliest pandemic in European history.", {
    "background": PAPER,
    "cast": [stan(x=0.2, action="point", expression="happy", action_params={"height": 0.2})],
    "overlays": [{"type": "checklist", "x": 0.42, "y": 0.18,
                  "items": [["the work", True], ["the fees", True], ["the pottage", True], ["the winter", True],
                            ["the Black Death", True]],
                  "times": [0.8, 1.6, 2.4, 3.3, 4.6], "size": 56}]},
    claims=[F("The Black Death is considered the deadliest pandemic in recorded European history", SRC["benedictow"])],
    sfx=[{"name": "ding", "at": 0.8}, {"name": "ding", "at": 1.6}, {"name": "ding", "at": 2.4},
         {"name": "ding", "at": 3.3}, {"name": "ding", "at": 4.6}])

sc("f02b", "ending", "Final tally: a penny or two a day before the plague, and up to three pennies after. Around three hundred bowls of pottage. And one very lucky family.", {
    "background": {"type": "chalkboard"},
    "overlays": [{"type": "bars", "title": "Stan's year in numbers", "x": 0.3, "y": 0.32,
                  "items": [["Wage before", 1.5, "grey", "1-2d/day"], ["Wage after", 3, "green", "up to 3d/day"],
                            ["Pottage", 3.4, "wheat", "~300 bowls"]], "max": 3.6}]},
    claims=[F("Unskilled daily wages of roughly 1-2d before 1348 rose substantially afterwards", SRC["dyer"],
              "estimate")])

sc("f03", "ending", "And here's the twist. Your world is about to change. With so few workers left, peasants start to push back.", {
    "background": village("spring"),
    "cast": [stan(x=0.3, action="angry", expression="determined"),
             cast("p1", "peasant", x=0.45, action="angry", expression="determined"),
             cast("p2", "peasant", x=0.6, action="angry", expression="angry", item="pitchfork")],
    "camera": {"move": "push_in"}},
    claims=[F("Post-plague labor scarcity strengthened peasants' bargaining position", SRC["dyer"])])

sc("f04", "ending", "In 1381, they rise up in the Peasants' Revolt. Within a few generations, serfdom in England fades away.", {
    "background": {"type": "castle", "time": "dusk"},
    "props": [{"type": "crowd", "x": 0.4, "y": 0.92, "n": 18, "cols": 9, "action": "angry", "gap": 80,
               "fig_scale": 0.45, "color": "ink", "outfit": "tunic"}],
    "overlays": [{"type": "title", "text": "1381: THE PEASANTS' REVOLT", "y": 0.15, "at_word": 1}],
    "camera": {"move": "push_in"}},
    claims=[F("The Peasants' Revolt took place in 1381", SRC["dyer"]),
            F("Villeinage largely disappeared in England by the 1500s", SRC["dyer"])],
    sfx=[{"name": "rumble", "at_word": 1, "gain_db": -6}])

sc("f05", "ending", "So, would you have survived 1348? And what's the first modern thing you'd miss?", {
    "background": PAPER,
    "cast": [stan(x=0.4, action="shrug", expression="thinking", scale=1.4)],
    "props": [{"type": "icon", "icon": "?", "x": 0.62, "y": 0.4, "at_word": 4}],
    "camera": {"move": "push_in", "focus": "stan"}})

sc("f06", "ending", "Tell me in the comments. And if you enjoyed surviving with Stan, subscribe. Next time, we go somewhere even worse.", {
    "background": PAPER,
    "cast": [stan(x=0.35, action="wave", expression="grin", actions=[["w10", "point"]])],
    "props": [{"type": "board", "x": 0.7, "y": 0.45, "text": "SUBSCRIBE", "color": "red", "text_color": "white",
               "w": 520, "h": 150, "size": 78, "at_word": 12, "loop": "pulse"}],
    "overlays": [{"type": "title", "text": "SEE YOU NEXT TIME!", "y": 0.15, "at_word": 15}]},
    sfx=[{"name": "pop", "at_word": 12}, {"name": "sparkle", "at_word": 15}], pause=0.8)

# ---- metadata ----------------------------------------------------------------------------------------------
st.save(
    "medieval-peasant-1348",
    title="Could You Survive a Year as a Medieval Peasant? (1348)",
    idea="What if you had to survive one year as a medieval English peasant in 1348",
    question="Would you have survived 1348? What's the first modern thing you'd miss?",
    mood="medieval",
    metadata={
        "title": "Could You Survive a Year as a Medieval Peasant? (1348)",
        "description_intro": (
            "You wake up on March 25th, 1348 — New Year's Day in medieval England — as Stan, an unfree peasant "
            "on a manor in Dorset. Your mission: survive one year. You'll deal with a lord who owns your labor, "
            "the tithe, endless pottage, the harvest… and the Black Death, which lands in England that very "
            "summer.\n\nA stickman history story with real facts and sources."),
        "hashtags": ["#history", "#medieval", "#stickman"],
        "tags": ["medieval peasant", "black death", "1348", "middle ages", "medieval history", "what if",
                 "stickman", "stickman animation", "history animated", "serfdom", "feudalism", "plague",
                 "could you survive", "medieval life", "peasant life", "english history", "animated history"],
        "pinned_comment": ("Would you have survived 1348? 🤔 And what's the first modern thing you'd miss? "
                           "Mine is definitely not-pottage. 👇"),
        "chapter_moods": ["medieval", "calm", "curious", "medieval", "calm", "somber", "curious", "calm", "medieval"],
        "intro_chapter": "Waking Up in 1348",
        "thumbnail": {
            "visual": {
                "background": {"type": "village", "season": "autumn", "time": "dusk"},
                "cast": [{"id": "stan", "outfit": "tunic", "outfit_color": [0.55, 0.42, 0.3], "x": 0.74,
                          "y": 0.92, "scale": 1.9, "action": "cower", "expression": "scared", "facing": -1}],
                "props": [{"type": "rat", "x": 0.52, "y": 0.96, "scale": 1.8, "enter": "none"},
                          {"type": "germ", "x": 0.9, "y": 0.3, "scale": 1.5, "enter": "none"},
                          {"type": "cross", "x": 0.55, "y": 0.84, "scale": 0.9, "enter": "none"}]},
            "t": 1.0, "lines": ["SURVIVE 1 YEAR", "AS A PEASANT"], "colors": ["white", "yellow"],
            "badge": "1348 = PLAGUE", "badge_color": "red", "size": 104},
        "thumbnail_alts": [{
            "visual": {"background": {"type": "interior", "season": "spring", "hearth_x": 0.8},
                       "cast": [{"id": "stan", "outfit": "tunic", "outfit_color": [0.55, 0.42, 0.3], "x": 0.7,
                                 "y": 0.95, "scale": 1.9, "action": "eat", "expression": "disgusted",
                                 "facing": -1}],
                       "props": [{"type": "pot", "x": 0.86, "y": 0.95, "scale": 1.4, "enter": "none"}]},
            "t": 0.8, "lines": ["POTTAGE.", "EVERY. DAY."], "colors": ["white", "yellow"],
            "badge": "1 YEAR IN 1348", "badge_color": "teal", "size": 120}],
    },
)
