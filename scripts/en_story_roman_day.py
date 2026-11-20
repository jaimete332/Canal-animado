"""Episode 2 — What Did Ancient Romans Actually Do All Day?

Format chosen from the niche research (data/stickman_en/research/): curiosity question about everyday life
("What Did Ancient Humans Actually Do All Day?" — 19M views), 10-12 min, chapters by hour of the day.

Run:  python3 scripts/en_story_roman_day.py
      python -m fabrica --channel stickman_en make stories_en/roman-day.json
"""
from storykit_en import GROUND, F, Story, cast

st = Story()
sc = st.sc
ch = st.chapter

TUNIC = {"outfit": "tunic", "outfit_color": (0.85, 0.75, 0.55)}


def stan(**kw):
    return cast("stan", **{**TUNIC, **kw})


def toga(id_, **kw):
    return cast(id_, outfit="toga", **kw)


def rich(**kw):
    return cast("patron", outfit="toga", hat_color="purple", belly=0.8, beard="short", **kw)


def legion(id_="soldier", **kw):
    return cast(id_, outfit="armor", hat="legion", **kw)


def rome(**kw):
    return {"type": "rome", **kw}


PAPER = {"type": "paper"}
LINED = {"type": "paper", "lines": True, "floor": False}
STORY = {"type": "fiction", "text": "STAN'S STORY"}


def hour(label):
    return {"type": "counter", "label": label, "value": "", "corner": "tr", "size": 46}


SRC = {
    "martial": "Martial, Epigrams 4.8 (the hours of a Roman day)",
    "juvenal": "Juvenal, Satire 3",
    "beard": "Mary Beard, SPQR: A History of Ancient Rome (2015)",
    "carcopino": "Jérôme Carcopino, Daily Life in Ancient Rome (1940)",
    "angela": "Alberto Angela, A Day in the Life of Ancient Rome (2009)",
    "pompeii": "Pompeii Archaeological Park (thermopolium of Regio V; carbonised bread)",
    "res_gestae": "Augustus, Res Gestae 15 (grain distributions)",
    "strabo": "Strabo, Geography 5.3.7 (Augustus' building height limit)",
    "suetonius": "Suetonius, Life of Augustus 30 & 89; Life of Julius Caesar",
    "lex": "Lex Iulia Municipalis (Tabula Heracleensis), cart ban in daytime",
    "koloski": "Ann Olga Koloski-Ostrow, The Archaeology of Sanitation in Roman Italy (2015)",
    "fagan": "Garrett Fagan, Bathing in Public in the Roman World (1999)",
    "circus": "Humphrey, Roman Circuses (1986); Pliny the Elder, Natural History 36.102",
    "colosseum": "Parco archeologico del Colosseo",
    "britannica": "Encyclopaedia Britannica, 'Roman hour' / 'ancient Rome'",
    "frontinus": "Frontinus, De aquaeductu (Rome's aqueducts)",
    "suet_vesp": "Suetonius, Life of Vespasian 23 ('pecunia non olet')",
    "school": "Stanley Bonner, Education in Ancient Rome (1977)",
    "graffiti": "Rebecca Benefiel, Ancient Graffiti Project (Washington and Lee University)",
    "nundinae": "Encyclopaedia Britannica, 'nundinae' (Roman market day)",
    "cloaca": "Encyclopaedia Britannica, 'Cloaca Maxima'",
    "diocles": "CIL VI 10048 (inscription of the charioteer Gaius Appuleius Diocles)",
    "barber": "Alberto Angela, A Day in the Life of Ancient Rome (2009), on barbershops",
    "dogs": "Pompeii Archaeological Park, 'Cave canem' mosaic (House of the Tragic Poet)",
    "lararium": "Harriet Flower, The Dancing Lares and the Serpent in the Garden (2017)",
    "family": "Suzanne Dixon, The Roman Family (1992)",
    "saturnalia": "Macrobius, Saturnalia; Encyclopaedia Britannica, 'Saturnalia'",
    "dice": "Digest 11.5 (gambling laws); Martial 5.84 & 14.1 (dice at the Saturnalia)",
}

# ================================================================================================ INTRO
sc("r01", "hook", "Rome, around the year one hundred. The biggest city on Earth wakes up, and almost a million people need to get something done today.", {
    "background": rome(time="dusk"),
    "props": [{"type": "crowd", "x": 0.42, "y": 0.95, "n": 14, "cols": 7, "action": "walk", "gap": 90,
               "fig_scale": 0.5, "outfit": "tunic", "outfit_color": "tan", "at": 3.0}],
    "overlays": [{"type": "title", "text": "ROME · AD 100", "y": 0.15, "at": 0.3}],
    "camera": {"move": "pull_out", "zoom_from": 1.25}},
    claims=[F("Rome's population in the early Empire is commonly estimated at close to a million", SRC["beard"],
              "estimate")],
    transition="cut")

sc("r02", "hook", "So what did they actually do all day? Where did they eat, work, wash… and, let's be honest, go to the toilet?", {
    "background": PAPER,
    "cast": [stan(x=0.3, action="think", expression="thinking", scale=1.5)],
    "overlays": [{"type": "checklist", "x": 0.52, "y": 0.22, "size": 58,
                  "items": [["eat?", None], ["work?", None], ["wash?", None], ["toilet?!", None]],
                  "times": [3.0, 3.5, 4.0, 5.6]}]})

sc("r03", "hook", "Let's follow one ordinary Roman from sunrise to midnight. Meet Stan. Or, as his neighbors call him, Stanius.", {
    "background": rome(),
    "cast": [stan(x=0.4, action="wave", expression="grin", at_word=10, enter="pop")],
    "overlays": [{"type": "label", "text": "STANIUS", "x": 0.4, "y": 0.2, "to_x": 0.4, "to_y": 0.38, "at_word": 15},
                 STORY]},
    claims=[F("Stanius is a fictional Roman", "Narrative device", "fiction")],
    sfx=[{"name": "pop", "at_word": 10}])

sc("r04", "hook", "And by the end, you'll know whether you'd rather be a Roman… or stay exactly where you are.", {
    "background": {"type": "split", "left": "sky", "right": (0.95, 0.88, 0.75), "left_label": "TODAY",
                   "right_label": "ROME"},
    "cast": [cast("you", "modern", x=0.25, action="shrug", expression="neutral"),
             stan(x=0.75, action="cheer", expression="grin", facing=-1)]},
    transition="wipe")

# ================================================================================================ CH1 HOME
ch("Waking Up in an Apartment Block")
sc("h01", "setup", "Stanius doesn't live in a villa with a garden. Like most Romans, he rents a small room in an apartment block called an insula.", {
    "background": rome(insulae=[(380, 5), (760, 4)], temple=False),
    "cast": [stan(x=0.15, action="point", expression="happy", action_params={"height": 0.6})],
    "overlays": [{"type": "label", "text": "insula = apartment block", "x": 0.75, "y": 0.2, "to_x": 0.5,
                  "to_y": 0.3, "at_word": 20}],
    "camera": {"move": "pan_up", "amount": 120}},
    claims=[F("Most of Rome's population lived in rented flats in multi-storey insulae", SRC["beard"])],
    transition="wipe")

sc("h02", "setup", "Some of these buildings were so tall and so badly built that Emperor Augustus put a height limit on them: about twenty meters.", {
    "background": rome(insulae=[(380, 6)], temple=False),
    "cast": [cast("augustus", outfit="toga", hat="laurel", x=0.75, action="point", facing=-1, expression="angry")],
    "overlays": [{"type": "stat", "value": "~20 m", "caption": "max height (70 Roman feet)", "x": 0.75, "y": 0.25,
                  "size": 130, "at_word": 16}],
    "camera": {"move": "push_in"}},
    claims=[F("Augustus limited the height of buildings in Rome to 70 Roman feet (about 20 m)", SRC["strabo"])],
    sfx=[{"name": "ding", "at_word": 16}])

sc("h03", "setup", "Here's the twist: in Rome, the higher you lived, the poorer you were. No elevator, no running water, and the best view of any fire.", {
    "background": PAPER,
    "props": [{"type": "board", "x": 0.3, "y": 0.25, "text": "TOP FLOOR\ncheap · cramped · dangerous", "w": 560,
               "color": "red", "text_color": "white", "at_word": 6},
              {"type": "board", "x": 0.3, "y": 0.7, "text": "GROUND FLOOR\nshops & rich flats", "w": 560,
               "color": "lime", "at_word": 2},
              {"type": "fire", "x": 0.75, "y": 0.6, "at_word": 22}],
    "cast": [stan(x=0.72, y=0.92, action="panic", expression="scared", at_word=22)]},
    claims=[F("Upper floors of insulae were the cheapest and most dangerous; ground floors held shops and better flats",
              SRC["carcopino"])],
    sfx=[{"name": "sizzle", "at_word": 22}])

sc("h04", "setup", "Fires were so common that Augustus created a corps of around seven thousand firefighters and night watchmen, the vigiles.", {
    "background": rome(time="dusk"),
    "cast": [cast("vigil", outfit="tunic", outfit_color="red", hat="legion", item="bucket", x=0.35,
                  action="run", path=[[0, 0.1, GROUND], [5, 0.6, GROUND]], expression="determined"),
             cast("vigil2", outfit="tunic", outfit_color="red", hat="legion", item="axe", x=0.2, action="run",
                  path=[[0.6, -0.05, GROUND], [5.5, 0.45, GROUND]], expression="determined")],
    "props": [{"type": "fire", "x": 0.85, "y": 0.84, "scale": 1.4}],
    "overlays": [{"type": "fact", "text": "The vigiles (AD 6): seven cohorts, roughly 7,000 men, fighting fires and "
                                          "patrolling at night.", "source": SRC["suetonius"], "at_word": 12}]},
    claims=[F("Augustus established the vigiles in AD 6: seven cohorts of firefighters/night watchmen", SRC["suetonius"])])

sc("h05", "setup", "Stanius wakes at dawn. Romans split the daylight into twelve hours, so a summer hour was much longer than a winter one.", {
    "background": rome(time="dusk", temple=False),
    "cast": [stan(x=0.4, action="idle", expression="sleepy", expressions=[["w4", "neutral"]], actions=[["w4", "shrug"]])],
    "props": [{"type": "board", "x": 0.75, "y": 0.4, "text": "summer hour ≈ 75 min\nwinter hour ≈ 45 min",
               "w": 600, "at_word": 14}],
    "overlays": [hour("HOUR 1 · DAWN")]},
    claims=[F("Romans divided daylight into 12 hours whose length varied with the season (~45-75 modern minutes)",
              SRC["britannica"])],
    transition="wipe")

sc("h05b", "setup", "First job of the day: water. Top-floor flats had no taps, so Stanius walks down to a public fountain on the corner.", {
    "background": rome(temple=False),
    "props": [{"type": "well", "x": 0.68, "y": 0.86}],
    "cast": [stan(x=0.35, action="walk", item="bucket", path=[[0, 0.15, GROUND], [4, 0.55, GROUND]],
                  expression="sleepy")]},
    claims=[F("Most insula residents fetched water from public fountains", SRC["frontinus"])])

sc("h05c", "setup", "That water traveled for miles. Rome was fed by a network of aqueducts, eleven of them by the third century.", {
    "background": {"type": "field", "season": "summer"},
    "props": [{"type": "column", "x": x, "y": 0.84, "h": 420} for x in (0.12, 0.3, 0.48, 0.66, 0.84)] +
             [{"type": "board", "x": 0.5, "y": 0.2, "text": "11 AQUEDUCTS", "w": 520, "at_word": 15}]},
    claims=[F("Ancient Rome was supplied by eleven aqueducts by the 3rd century AD", SRC["frontinus"])])

sc("h05d", "setup", "Then he empties last night's chamber pot. And here's a gross fact: urine was valuable. Laundries collected it to clean clothes.", {
    "background": rome(temple=False),
    "props": [{"type": "barrel", "x": 0.65, "y": 0.86}, {"type": "icon", "icon": "stink", "x": 0.65, "y": 0.62}],
    "cast": [stan(x=0.35, action="hold", item="bucket", expression="disgusted")]},
    claims=[F("Fullers (laundries) used collected urine for cleaning cloth", SRC["suet_vesp"])])

sc("h05e", "setup", "Emperor Vespasian even taxed it. When his son complained, he held up a coin and said: money doesn't smell.", {
    "background": rome(time="dusk"),
    "cast": [cast("vesp", outfit="toga", hat="laurel", belly=0.6, x=0.35, action="hold_up", item="coin",
                  expression="smug"),
             cast("titus", outfit="toga", x=0.65, facing=-1, action="facepalm", expression="disgusted")],
    "overlays": [{"type": "quote", "text": "Pecunia non olet. (Money doesn't smell.)", "by": "Vespasian, via Suetonius",
                  "y": 0.22, "at_word": 14, "size": 56}]},
    claims=[F("Vespasian taxed urine collection; 'pecunia non olet' is attributed to him", SRC["suet_vesp"])])

sc("h06", "setup", "Getting dressed takes seconds. He sleeps in his tunic. The famous toga? That's for formal occasions, and honestly, most people hated wearing it.", {
    "background": PAPER,
    "cast": [stan(x=0.3, action="shrug", expression="smug"),
             toga("rich2", x=0.7, action="sad", expression="tired", facing=-1, at_word=10, enter="pop")],
    "overlays": [{"type": "label", "text": "heavy wool, metres of it", "x": 0.75, "y": 0.18, "to_x": 0.7,
                  "to_y": 0.45, "at_word": 12}]},
    claims=[F("The toga was heavy formal wear; everyday clothing was the tunic", SRC["angela"])],
    sfx=[{"name": "pop", "at_word": 10}])

# ================================================================================================ CH2 MORNING
ch("Bread, Bosses and Free Grain")
sc("m01", "development", "Breakfast is small: a piece of bread, maybe cheese, some olives, or nothing at all.", {
    "background": PAPER,
    "props": [{"type": "item", "item": "bread", "x": 0.3, "y": 0.62, "scale": 4.5, "at_word": 4},
              {"type": "item", "item": "egg", "x": 0.5, "y": 0.62, "scale": 4.0, "at_word": 9},
              {"type": "icon", "icon": "x", "x": 0.72, "y": 0.62, "scale": 1.6, "at_word": 13}],
    "overlays": [hour("HOUR 1")]},
    claims=[F("The Roman breakfast (ientaculum) was light, often bread with cheese or fruit, or skipped", SRC["angela"])],
    transition="wipe")

sc("m02", "development", "Bread came from bakeries. Archaeologists have even found real Roman loaves, burned to charcoal in Pompeii, still cut into eight slices.", {
    "background": rome(temple=False),
    "props": [{"type": "item", "item": "bread", "x": 0.55, "y": 0.6, "scale": 5.0},
              {"type": "amphora", "x": 0.85, "y": 0.86}],
    "cast": [cast("baker", outfit="apron", outfit_color="white", x=0.3, action="hold", item="bread",
                  expression="happy")],
    "overlays": [{"type": "fact", "text": "Carbonised loaves from AD 79 survive at Pompeii, scored into 8 segments.",
                  "source": SRC["pompeii"], "at_word": 8}]},
    claims=[F("Carbonised loaves scored into eight segments were found at Pompeii", SRC["pompeii"])])

sc("m03", "development", "Then comes a strange morning ritual: the salutatio. Thousands of Romans rush across the city just to say good morning to their boss.", {
    "background": {"type": "manor", "manor_x": 0.7},
    "props": [{"type": "crowd", "x": 0.4, "y": 0.92, "n": 10, "cols": 10, "action": "idle", "gap": 70,
               "fig_scale": 0.55, "outfit": "toga"}],
    "cast": [rich(x=0.75, action="wave", expression="smug", facing=-1)],
    "overlays": [{"type": "title", "text": "THE SALUTATIO", "y": 0.15, "at_word": 6}]},
    claims=[F("Clients paid a morning call (salutatio) on their patron", SRC["beard"])],
    transition="wipe")

sc("m04", "development", "That boss is your patron, a rich man who protects you. You're his client. You bring him loyalty, votes and applause.", {
    "background": {"type": "manor", "manor_x": 0.72},
    "cast": [stan(x=0.3, action="bow", expression="happy", outfit="toga"),
             rich(x=0.62, action="talk", expression="smug", facing=-1)],
    "overlays": [{"type": "label", "text": "patron", "x": 0.62, "y": 0.18, "to_x": 0.62, "to_y": 0.32, "at_word": 4},
                 {"type": "label", "text": "client", "x": 0.3, "y": 0.4, "to_x": 0.3, "to_y": 0.55, "at_word": 15}]},
    claims=[F("Roman patronage: clients owed their patron support and attendance", SRC["beard"])])

sc("m05", "development", "In return, he might give you a small gift of food or cash, and help you if you get into trouble.", {
    "background": {"type": "manor", "manor_x": 0.72},
    "cast": [rich(x=0.62, action="hold", item="bag", expression="happy", facing=-1),
             stan(x=0.3, action="cheer", expression="grin", outfit="toga")],
    "overlays": [{"type": "money", "text": "+ sportula", "x": 0.32, "y": 0.4, "at": 1.0}]},
    claims=[F("Patrons gave clients a handout (sportula) of food or money", SRC["martial"] + "; " + SRC["juvenal"])],
    sfx=[{"name": "ding", "at": 1.0}])

sc("m06", "development", "Many poor citizens also collect free grain from the state. Under Augustus, around two hundred thousand men received it every month.", {
    "background": rome(),
    "props": [{"type": "sack", "x": 0.55, "y": 0.86, "label": "FREE GRAIN", "scale": 1.3},
              {"type": "crowd", "x": 0.3, "y": 0.95, "n": 8, "cols": 8, "gap": 60, "fig_scale": 0.45,
               "outfit": "tunic", "outfit_color": "tan"}],
    "overlays": [{"type": "stat", "value": 200000, "caption": "citizens on the grain dole", "y": 0.25,
                  "x": 0.62, "size": 140, "at_word": 13}]},
    claims=[F("Augustus records grain distributions to some 200,000+ citizens", SRC["res_gestae"])],
    sfx=[{"name": "ding", "at_word": 13}])

sc("m07", "development", "Kids, meanwhile, go to school before sunrise. A teacher, often in a rented corner of the street, drills reading, writing and arithmetic.", {
    "background": rome(time="dusk", temple=False),
    "cast": [cast("teacher", outfit="toga", beard="long", x=0.7, action="point", item="scroll", facing=-1,
                  expression="angry"),
             cast("kid1", "child", x=0.3, action="sit", expression="sleepy"),
             cast("kid2", "child", x=0.45, action="sit", expression="tired")],
    "props": [{"type": "stool", "x": 0.3, "y": 0.84}, {"type": "stool", "x": 0.45, "y": 0.84}]},
    claims=[F("Roman primary teachers (litteratores) often taught in rented spaces from very early morning",
              SRC["school"])])

sc("m08", "development", "And teachers were famous for one thing: hitting students. The poet Horace remembered his teacher as Orbilius the flogger.", {
    "background": rome(time="dusk", temple=False),
    "cast": [cast("teacher", outfit="toga", beard="long", x=0.65, action="swing", item="crook", facing=-1,
                  expression="angry"),
             cast("kid1", "child", x=0.35, action="cower", expression="scared")],
    "overlays": [{"type": "label", "text": "\"plagosus Orbilius\"", "x": 0.65, "y": 0.18, "at_word": 15}]},
    claims=[F("Horace called his teacher Orbilius 'plagosus' (fond of flogging)", "Horace, Epistles 2.1.70")])

# ================================================================================================ CH3 WORK
ch("Work (But Only Until Lunch)")
sc("w01", "development", "Now, work. And here's the part you'll love: for many Romans, the working day was basically over by early afternoon.", {
    "background": rome(),
    "cast": [stan(x=0.4, action="dance", expression="laughing")],
    "overlays": [hour("HOUR 3")]},
    claims=[F("Many Romans' business day ended around midday or early afternoon", SRC["martial"] + "; " + SRC["carcopino"])],
    transition="wipe")

sc("w02", "development", "The poet Martial described the routine: the first two hours for greetings, the third for lawyers, then business until the sixth or seventh hour.", {
    "background": {"type": "chalkboard"},
    "overlays": [{"type": "bars", "title": "A Roman day, according to Martial", "x": 0.3, "y": 0.27,
                  "items": [["Hours 1-2", 2, "yellow", "greetings"], ["Hour 3", 1, "orange", "lawyers & courts"],
                            ["Hours 4-6", 3, "teal", "business"], ["Hour 7", 1, "lime", "rest"],
                            ["Hours 8-9", 2, "blue", "exercise & baths"], ["Hour 9+", 2, "red", "dinner"]],
                  "max": 3.4, "bar_h": 70, "gap": 24}]},
    claims=[F("Martial's Epigram 4.8 sets out the hours of a Roman day", SRC["martial"])])

sc("w03", "development", "Stanius works in a shop on the ground floor of an insula. Rome's streets were lined with tiny workshops open to the pavement.", {
    "background": rome(insulae=[(-40, 3), (300, 3), (640, 3), (980, 3)], temple=False),
    "cast": [stan(x=0.3, action="dig", item="hammer", expression="determined"),
             cast("buyer", outfit="tunic", outfit_color="teal", x=0.55, action="talk", facing=-1,
                  expression="neutral")],
    "props": [{"type": "table", "x": 0.3, "y": 0.9, "w": 300, "items": ["bucket", "mug"]}]},
    claims=[F("Ground floors of insulae held tabernae (shops and workshops) open to the street", SRC["angela"])],
    sfx=[{"name": "dig", "at": 0.4}, {"name": "dig", "at": 1.5}])

sc("w04", "development", "Bakers, barbers, shoemakers, metalworkers. If you needed something, there was a guy for that within one block.", {
    "background": rome(temple=False),
    "props": [{"type": "crowd", "x": 0.5, "y": 0.95, "n": 6, "cols": 6, "gap": 260, "fig_scale": 0.85,
               "action": "talk", "outfit": "apron", "outfit_color": "white", "color": "ink"}],
    "overlays": [{"type": "checklist", "x": 0.06, "y": 0.18, "size": 50,
                  "items": [["bakers", True], ["barbers", True], ["shoemakers", True], ["metalworkers", True]],
                  "times": [0.2, 0.8, 1.4, 2.2]}]})

sc("w05", "development", "Meanwhile, the richer men head to the Forum, the center of politics, law and gossip.", {
    "background": rome(temple_x=0.6, temple_scale=1.15, insulae=[]),
    "cast": [toga("senator", x=0.2, action="talk", expression="smug", hat_color="purple"),
             toga("lawyer", x=0.85, action="point", expression="angry", facing=-1)],
    "overlays": [{"type": "title", "text": "THE FORUM", "y": 0.12, "at_word": 6}]},
    claims=[F("The Forum Romanum was the center of political, legal and commercial life", SRC["beard"])])

sc("w06", "development", "Court cases were public entertainment. Crowds gathered to cheer and boo the lawyers like a sports match.", {
    "background": rome(temple_x=0.6, temple_scale=1.15, insulae=[]),
    "props": [{"type": "crowd", "x": 0.35, "y": 0.95, "n": 12, "cols": 6, "action": "cheer", "gap": 80,
               "fig_scale": 0.5, "outfit": "toga"}],
    "cast": [toga("lawyer", x=0.75, action="angry", expression="angry", facing=-1,
                  say=[{"text": "Objection!", "at": 1.2, "kind": "shout"}])]},
    claims=[F("Trials in the Forum drew large audiences", SRC["beard"])],
    sfx=[{"name": "pop", "at": 1.2}])

sc("w07", "development", "And of course, not everyone worked for themselves. Rome was full of enslaved people, doing everything from mining to teaching children.", {
    "background": rome(time="grey", temple=False),
    "cast": [cast("slave", outfit="rags", outfit_color=(0.6, 0.55, 0.45), x=0.4, action="carry",
                  expression="tired", path=[[0, 0.2, GROUND], [6, 0.55, GROUND]])],
    "props": [{"type": "amphora", "x": 0.8, "y": 0.86}],
    "overlays": [{"type": "fact", "text": "Enslaved people were a large share of Rome's population; estimates for "
                                          "Roman Italy range widely (often 10-20% or more).", "source": SRC["beard"],
                  "at": 1.0}]},
    claims=[F("Slavery was widespread in Rome; estimates of the enslaved share of Italy's population vary widely",
              SRC["beard"], "estimate")])

sc("w08", "development", "Every eighth day, the routine changes: it's market day, the nundinae. Romans effectively lived in an eight-day week.", {
    "background": {"type": "town", "stalls": True},
    "cast": [stan(x=0.3, action="walk", path=[[0, 0.15, GROUND], [5, 0.5, GROUND]], expression="happy", item="bag")],
    "overlays": [{"type": "timeline", "items": ["A", "B", "C", "D", "E", "F", "G", "H"], "at": 7, "from_at": 0,
                  "w": 1100, "colors": ["lightgrey"] * 7 + ["yellow"], "y": 0.1}]},
    claims=[F("Rome had an eight-day market cycle (nundinae), lettered A-H in calendars", SRC["nundinae"])])

sc("w09", "development", "Many workers also stop at the barber. Barbershops were gossip central, and a clean shave was the fashion, until Emperor Hadrian made beards cool again.", {
    "background": rome(temple=False),
    "props": [{"type": "stool", "x": 0.4, "y": 0.86}],
    "cast": [stan(x=0.4, y=0.84, action="sit", expression="worried"),
             cast("barber", outfit="apron", outfit_color="white", x=0.58, action="stir", item="sickle", facing=-1,
                  expression="happy", say=[{"text": "Did you hear about the senator…", "at": 2.0}]),
             cast("hadrian", outfit="toga", hat="laurel", beard="short", x=0.85, facing=-1, action="idle",
                  expression="smug", at_word=21, enter="pop")]},
    claims=[F("Barbershops were social hubs; Hadrian popularized beards among Roman men", SRC["barber"])])

sc("w10", "development", "And everywhere you walk, the walls are covered in writing. In Pompeii alone, there are thousands of ancient graffiti.", {
    "background": rome(temple=False),
    "props": [{"type": "board", "x": 0.3, "y": 0.45, "text": "VOTE FOR GAIUS!", "w": 440, "color": (0.98, 0.95, 0.85)},
              {"type": "board", "x": 0.62, "y": 0.3, "text": "Stanius was here", "w": 420, "color": (0.98, 0.95, 0.85),
               "at": 1.5}],
    "overlays": [{"type": "fact", "text": "Pompeii preserves thousands of painted notices and scratched graffiti.",
                  "source": SRC["graffiti"], "at_word": 14, "x": 0.5, "y": 0.62, "w": 760}]},
    claims=[F("Thousands of graffiti and painted notices survive at Pompeii", SRC["graffiti"])])

sc("w11", "development", "Election ads, love notes, insults, and the timeless classic: somebody was here.", {
    "background": rome(temple=False),
    "props": [{"type": "board", "x": 0.25, "y": 0.35, "text": "Vote Gaius!", "w": 330, "at": 0.2},
              {"type": "board", "x": 0.5, "y": 0.5, "text": "Marcus ♥ Spendusa", "w": 380, "at": 0.8},
              {"type": "board", "x": 0.75, "y": 0.35, "text": "Lucius is a thief", "w": 380, "at": 1.4},
              {"type": "board", "x": 0.5, "y": 0.2, "text": "Gaius was here", "w": 360, "at": 2.6}]},
    claims=[F("Pompeian graffiti include election notices, love messages, insults and 'X was here'", SRC["graffiti"])],
    sfx=[{"name": "pop", "at": 0.2}, {"name": "pop", "at": 0.8}, {"name": "pop", "at": 1.4}, {"name": "pop", "at": 2.6}])

# ================================================================================================ CH4 LUNCH
ch("Fast Food, Roman Style")
sc("l01", "development", "Lunch time. Most apartments had no proper kitchen, because cooking fires in a wooden-floored block were a terrible idea.", {
    "background": rome(),
    "cast": [stan(x=0.4, action="scratch", expression="thinking")],
    "props": [{"type": "icon", "icon": "x", "x": 0.7, "y": 0.5, "at_word": 7}],
    "overlays": [hour("HOUR 6 · NOON")]},
    claims=[F("Many insula flats lacked kitchens; residents relied on street food", SRC["angela"])],
    transition="wipe")

sc("l02", "development", "So Romans ate out, at a thermopolium: a street counter with big jars of hot food built right into it. Basically, Roman fast food.", {
    "background": rome(temple=False),
    "props": [{"type": "table", "x": 0.55, "y": 0.9, "w": 520, "items": ["pot", "pot", "pot"], "item_scale": 0.55}],
    "cast": [cast("cook", outfit="apron", outfit_color="white", x=0.62, action="stir", expression="happy",
                  facing=-1),
             stan(x=0.25, action="point", expression="grin")],
    "overlays": [{"type": "title", "text": "THERMOPOLIUM", "y": 0.13, "at_word": 6}]},
    claims=[F("Thermopolia were street counters with built-in jars (dolia) serving hot food and drink", SRC["pompeii"])])

sc("l03", "development", "In Pompeii, archaeologists found one with its painted counter still bright, and traces of duck, pork, snails and fish in the jars.", {
    "background": PAPER,
    "props": [{"type": "table", "x": 0.5, "y": 0.85, "w": 700, "items": ["pot", "pot", "pot", "pot"], "item_scale": 0.6},
              {"type": "chicken", "x": 0.25, "y": 0.5, "at_word": 15, "scale": 0.9},
              {"type": "pig", "x": 0.45, "y": 0.5, "at_word": 16, "scale": 0.8},
              {"type": "item", "item": "egg", "x": 0.62, "y": 0.45, "scale": 2.5, "at_word": 17}],
    "overlays": [{"type": "fact", "text": "Regio V thermopolium (excavated 2019-20): remains of duck, pig, goat, "
                                          "snails and fish.", "source": SRC["pompeii"], "at_word": 4,
                  "x": 0.55, "y": 0.04, "w": 780}]},
    claims=[F("The Regio V thermopolium at Pompeii contained remains of duck, pig, goat, snails and fish",
              SRC["pompeii"])])

sc("l04", "development", "And on almost everything, Romans poured garum: a sauce made from fish left to ferment in the sun. Delicious. Allegedly.", {
    "background": rome(temple=False),
    "props": [{"type": "amphora", "x": 0.6, "y": 0.86, "scale": 1.3},
              {"type": "icon", "icon": "stink", "x": 0.6, "y": 0.6, "at_word": 14}],
    "cast": [stan(x=0.3, action="eat", expression="happy", expressions=[["w19", "disgusted"]])],
    "overlays": [{"type": "label", "text": "GARUM", "x": 0.75, "y": 0.35, "to_x": 0.63, "to_y": 0.62, "at_word": 7}]},
    claims=[F("Garum, a fermented fish sauce, was a ubiquitous Roman condiment", SRC["angela"])])

sc("l04b", "development", "Some people linger in a popina, a cheap bar, playing dice. Technically, gambling was illegal, except during one festival.", {
    "background": {"type": "interior", "wall": (0.7, 0.55, 0.42), "hearth": False},
    "props": [{"type": "table", "x": 0.5, "y": 0.88, "w": 420, "items": ["mug", "coin"]}],
    "cast": [stan(x=0.3, action="sit_talk", expression="smug"),
             cast("gambler", outfit="tunic", outfit_color="teal", x=0.7, y=0.84, action="sit", expression="angry",
                  facing=-1)]},
    claims=[F("Gambling at dice was generally prohibited except during the Saturnalia", SRC["dice"])])

sc("l04c", "development", "That festival was the Saturnalia, in December. Gifts, parties, and for a few days, masters even served dinner to their slaves.", {
    "background": rome(season="winter", time="dusk"),
    "cast": [rich(x=0.6, action="carry", expression="happy", facing=-1, action_params={"walking": False}),
             cast("servant", outfit="tunic", outfit_color="white", x=0.35, action="laugh", expression="laughing")],
    "props": [{"type": "icon", "icon": "sparkle", "x": 0.5, "y": 0.4}],
    "overlays": [{"type": "title", "text": "SATURNALIA", "y": 0.14, "color": "red", "at_word": 3}]},
    claims=[F("During the Saturnalia gifts were exchanged and social roles were temporarily reversed", SRC["saturnalia"])])

sc("l05", "development", "After lunch, a nap. The sixth hour, around noon, was rest time, and our word siesta may come from the Latin sexta hora.", {
    "background": rome(time="day"),
    "props": [{"type": "bed", "x": 0.4, "y": 0.9, "scale": 1.5}, {"type": "icon", "icon": "z", "x": 0.4, "y": 0.66}],
    "cast": [stan(x=0.46, y=0.88, action="sleep", expression="sleepy")],
    "overlays": [{"type": "title", "lines": ["SEXTA HORA", "→ SIESTA?"], "colors": ["ink", "red"], "y": 0.14,
                  "at_word": 17}]},
    claims=[F("'Siesta' derives from Latin sexta (hora), the sixth hour", "Real Academia Española, etymology of 'siesta'")])

# ================================================================================================ CH5 BATHS
ch("The Baths: Rome's Social Network")
sc("b01", "development", "Then comes the best part of the Roman day: the baths. Around the eighth or ninth hour, the whole city heads to the thermae.", {
    "background": {"type": "baths"},
    "cast": [stan(x=0.15, action="walk", path=[[0, 0.05, GROUND], [4, 0.35, GROUND]], expression="happy",
                  actions=[["w8", "cheer"]])],
    "overlays": [hour("HOUR 8"), {"type": "title", "text": "THE BATHS", "y": 0.14, "at_word": 8}]},
    claims=[F("Romans typically bathed in the afternoon (8th-9th hour)", SRC["martial"])],
    transition="wipe")

sc("b02", "development", "Entry was cheap, often just a quarter of an as, the smallest coin around. Even poor people could afford it.", {
    "background": {"type": "baths"},
    "props": [{"type": "coin", "x": 0.6, "y": 0.6, "scale": 1.6, "text": "¼"}],
    "cast": [stan(x=0.3, action="hold", item="coin", expression="happy")]},
    claims=[F("Admission to the public baths cost a quadrans (a quarter of an as)", SRC["fagan"])])

sc("b03", "development", "Romans didn't use soap. They rubbed olive oil on their skin, then scraped it off, with the dirt, using a curved metal tool called a strigil.", {
    "background": {"type": "baths"},
    "cast": [stan(x=0.45, y=0.95, action="scratch", item="sickle", expression="smug")],
    "overlays": [{"type": "label", "text": "strigil", "x": 0.7, "y": 0.3, "to_x": 0.5, "to_y": 0.45, "at_word": 22}]},
    claims=[F("Bathers oiled their skin and scraped it clean with a strigil", SRC["fagan"])])

sc("b04", "development", "Then a circuit of rooms: warm, then hot like a sauna, then a plunge in the cold pool to finish.", {
    "background": PAPER,
    "props": [{"type": "board", "x": 0.2, "y": 0.5, "text": "TEPIDARIUM\nwarm", "color": "yellow", "w": 380,
               "at_word": 6},
              {"type": "board", "x": 0.5, "y": 0.5, "text": "CALDARIUM\nhot", "color": "red", "text_color": "white",
               "w": 380, "at_word": 8},
              {"type": "board", "x": 0.8, "y": 0.5, "text": "FRIGIDARIUM\ncold!", "color": "sky", "w": 380,
               "at_word": 14}],
    "overlays": [{"type": "title", "text": "THE BATH CIRCUIT", "y": 0.15}]},
    claims=[F("Baths had warm (tepidarium), hot (caldarium) and cold (frigidarium) rooms", SRC["fagan"])],
    sfx=[{"name": "pop", "at_word": 6}, {"name": "pop", "at_word": 8}, {"name": "splash", "at_word": 14}])

sc("b05", "development", "But the baths weren't really about getting clean. They were about people. You exercised, gossiped, made deals, ate snacks and got invited to dinner.", {
    "background": {"type": "baths"},
    "cast": [stan(x=0.25, action="laugh", expression="laughing"),
             cast("friend", outfit="tunic", outfit_color="teal", x=0.45, action="talk", expression="happy", facing=-1),
             rich(x=0.75, action="wave", expression="happy", facing=-1, at=3.0, enter="pop")]},
    claims=[F("The baths were major social venues for exercise, conversation and networking", SRC["fagan"])])

sc("b06", "development", "Some were enormous. The later Baths of Caracalla covered several hectares and could hold well over a thousand bathers at once.", {
    "background": {"type": "baths"},
    "props": [{"type": "crowd", "x": 0.5, "y": 0.97, "n": 20, "cols": 10, "gap": 70, "fig_scale": 0.4}],
    "overlays": [{"type": "stat", "value": "1,600+", "caption": "bathers at once (Baths of Caracalla, AD 216)",
                  "y": 0.28, "size": 150, "at_word": 13}]},
    claims=[F("The Baths of Caracalla could accommodate an estimated 1,600 bathers", SRC["fagan"], "estimate")],
    sfx=[{"name": "ding", "at_word": 13}])

sc("b06b", "development", "Men and women usually bathed at separate times or in separate sections. Mixed bathing happened, and some emperors tried to ban it.", {
    "background": {"type": "baths"},
    "cast": [cast("w1", "peasant_woman", x=0.3, action="talk", expression="happy", hat=None),
             cast("w2", "peasant_woman", x=0.5, action="laugh", expression="laughing", facing=-1, hat=None)],
    "overlays": [{"type": "caption", "text": "Hadrian reportedly separated the sexes in the baths (Historia Augusta)",
                  "at": 3.0}]},
    claims=[F("Bathing was often segregated by time or section; Hadrian is reported to have banned mixed bathing",
              "Historia Augusta, Life of Hadrian 18; " + SRC["fagan"])])

sc("b07", "development", "Hygiene, though? Questionable. The water wasn't changed very often, and a Roman doctor might send sick patients to the same pool.", {
    "background": {"type": "baths"},
    "cast": [stan(x=0.5, y=0.97, action="idle", expression="disgusted"),
             cast("sick", outfit="tunic", outfit_color="lime", x=0.7, y=0.97, action="sick", expression="sick")],
    "props": [{"type": "icon", "icon": "stink", "x": 0.6, "y": 0.7}, {"type": "germ", "x": 0.42, "y": 0.75,
                                                                         "scale": 0.7, "at": 2.0}]},
    claims=[F("Water in public baths was not frequently changed; medical writers recommended bathing for the sick",
              SRC["fagan"])])

# ================================================================================================ CH6 TOILETS
ch("The Toilets You Don't Want to Know About")
sc("t01", "development", "Speaking of questionable. Let's talk toilets. Rome had public latrines with long stone benches and a row of holes, side by side.", {
    "background": {"type": "baths"},
    "props": [{"type": "latrine", "x": 0.5, "y": 0.9, "scale": 1.2}],
    "cast": [stan(x=0.35, y=0.82, action="sit", expression="worried"),
             cast("n1", outfit="tunic", outfit_color="teal", x=0.55, y=0.82, action="sit_talk", expression="happy"),
             cast("n2", outfit="toga", x=0.75, y=0.82, action="sit", expression="smug")]},
    claims=[F("Roman public latrines had multi-seat benches without partitions", SRC["koloski"])],
    transition="wipe")

sc("t02", "development", "No walls, no doors, no privacy. You just sat next to your neighbor and, well, chatted.", {
    "background": {"type": "baths"},
    "props": [{"type": "latrine", "x": 0.5, "y": 0.9, "scale": 1.2}],
    "cast": [stan(x=0.35, y=0.82, action="sit", expression="disgusted"),
             cast("n1", outfit="tunic", outfit_color="teal", x=0.55, y=0.82, action="sit_talk", expression="laughing",
                  say=[{"text": "So, how's the family?", "at": 2.4}])]})

sc("t03", "development", "Instead of toilet paper, there was probably a sponge on a stick, shared, and rinsed in a channel of water. Historians still argue about the details.", {
    "background": PAPER,
    "cast": [stan(x=0.3, action="hold", item="broom", expression="disgusted", scale=1.5)],
    "overlays": [{"type": "label", "text": "the xylospongium", "x": 0.65, "y": 0.25, "to_x": 0.36, "to_y": 0.35,
                  "at_word": 8},
                 {"type": "fact", "tag": "DEBATED", "text": "Some scholars think the sponge-stick was mainly for "
                                                            "cleaning the latrine itself.", "source": SRC["koloski"],
                  "at_word": 22, "x": 0.5, "y": 0.6, "w": 760}]},
    claims=[F("A sponge on a stick (xylospongium) is linked to Roman latrines; its exact use is debated", SRC["koloski"])])

sc("t04", "development", "And sometimes, the sewer gases caught fire. Romans even prayed to Fortuna, the goddess of luck, before going in.", {
    "background": {"type": "baths"},
    "props": [{"type": "latrine", "x": 0.5, "y": 0.9, "scale": 1.2}, {"type": "fire", "x": 0.5, "y": 0.86,
                                                                         "at_word": 6, "scale": 0.8}],
    "cast": [stan(x=0.2, action="pray", expression="scared")]},
    claims=[F("Sewer gases could ignite in latrines; images of Fortuna appear near latrines", SRC["koloski"])],
    sfx=[{"name": "boom", "at_word": 6, "gain_db": -6}])

sc("t05", "development", "Where did it all go? Into the Cloaca Maxima, the Great Sewer, one of the oldest sewers in the world. Parts of it still work today.", {
    "background": {"type": "cave", "fire": False, "paintings": False},
    "props": [{"type": "river", "x": 0.5, "y": 0.92, "w": 1600}, {"type": "rat", "x": 0.3, "y": 0.86, "walk": True,
                                                                   "move": [[0, 0.1, 0.86], [5, 0.6, 0.86]]}],
    "overlays": [{"type": "title", "text": "CLOACA MAXIMA", "y": 0.14, "at_word": 6, "color": "white",
                  "outline_color": "ink"}]},
    claims=[F("The Cloaca Maxima is one of the world's earliest sewers and parts remain in use", SRC["cloaca"])],
    sfx=[{"name": "splash", "at": 0.5, "gain_db": -6}])

# ================================================================================================ CH7 DINNER
ch("Dinner: Couches for the Rich, Bread for Everyone Else")
sc("d01", "development", "Late afternoon is time for the main meal, the cena. For the rich, it's a show.", {
    "background": {"type": "manor", "time": "dusk"},
    "cast": [rich(x=0.5, action="laugh", expression="laughing")],
    "overlays": [hour("HOUR 9")]},
    claims=[F("The cena was the main meal, taken in the late afternoon", SRC["martial"])],
    transition="wipe")

sc("d02", "development", "Guests lay on couches around the table, leaning on one elbow, while slaves brought course after course.", {
    "background": {"type": "interior", "wall": (0.82, 0.45, 0.35), "hearth": False, "window": False},
    "props": [{"type": "table", "x": 0.5, "y": 0.88, "w": 640, "items": ["plate", "mug", "plate"]}],
    "cast": [rich(x=0.3, y=0.9, action="lie", expression="happy"),
             cast("g2", outfit="toga", x=0.62, y=0.9, action="lie", expression="laughing"),
             cast("servant", outfit="tunic", outfit_color="white", x=0.85, action="carry", expression="tired",
                  action_params={"walking": False}, facing=-1)]},
    claims=[F("Wealthy Romans dined reclining on couches (triclinium)", SRC["angela"])])

sc("d03", "development", "Stanius doesn't have couches. He grabs bread, a bowl of bean or grain porridge, some wine mixed with water, and calls it a night.", {
    "background": rome(time="dusk", temple=False),
    "props": [{"type": "plate", "x": 0.6, "y": 0.86, "food": "porridge", "scale": 1.6},
              {"type": "item", "item": "mug", "x": 0.75, "y": 0.84, "scale": 2.2}],
    "cast": [stan(x=0.35, action="eat", expression="happy", item="bread")]},
    claims=[F("Ordinary Romans ate grain porridge (puls), bread and legumes, and drank wine mixed with water",
              SRC["angela"])])

sc("d04", "development", "By the way, Romans almost always mixed their wine with water. Drinking it straight was considered a little barbaric.", {
    "background": PAPER,
    "cast": [stan(x=0.3, action="drink", item="mug", expression="smug"),
             cast("gaul", outfit="tunic", outfit_color="green", beard="long", hair="messy", x=0.7, action="drink",
                  item="mug", expression="laughing", facing=-1)],
    "overlays": [{"type": "label", "text": "civilized", "x": 0.3, "y": 0.2, "at": 0.8},
                 {"type": "label", "text": "barbarian", "x": 0.7, "y": 0.2, "at_word": 13}]},
    claims=[F("Romans and Greeks considered drinking undiluted wine uncivilized", SRC["angela"])])

ch("Gods, Family and Pets")
sc("f01", "development", "Back home, every Roman house had a little shrine called a lararium, for the household gods.", {
    "background": {"type": "interior", "wall": (0.85, 0.5, 0.38), "hearth": False},
    "props": [{"type": "temple", "x": 0.6, "y": 0.62, "scale": 0.35}, {"type": "item", "item": "candle", "x": 0.6,
                                                                         "y": 0.64, "scale": 1.6}],
    "cast": [stan(x=0.3, action="pray", expression="neutral")],
    "overlays": [{"type": "label", "text": "lararium", "x": 0.82, "y": 0.25, "to_x": 0.66, "to_y": 0.42, "at_word": 10}]},
    claims=[F("Roman homes kept a lararium shrine to the household gods (Lares)", SRC["lararium"])],
    transition="wipe")

sc("f02", "development", "A pinch of food, a few drops of wine, a little prayer. Religion wasn't just temples. It was part of breakfast.", {
    "background": {"type": "interior", "wall": (0.85, 0.5, 0.38), "hearth": False},
    "props": [{"type": "temple", "x": 0.6, "y": 0.62, "scale": 0.35}],
    "cast": [stan(x=0.4, action="hold", item="bread", expression="happy")]},
    claims=[F("Daily offerings of food and wine were made at the household shrine", SRC["lararium"])])

sc("f03", "development", "The family was ruled by the oldest man, the paterfamilias. Legally, he had enormous power over everyone in the house, even adult sons.", {
    "background": {"type": "manor"},
    "cast": [cast("pater", outfit="toga", beard="long", belly=0.4, x=0.5, action="point", expression="angry",
                  scale=1.6),
             cast("son", outfit="toga", x=0.2, action="cower", expression="worried")]},
    claims=[F("The paterfamilias held extensive legal authority (patria potestas) over his household", SRC["family"])])

sc("f04", "development", "Women couldn't vote or hold office. But many ran the household money, owned property and businesses, and some became very rich.", {
    "background": rome(temple=False),
    "cast": [cast("matrona", "peasant_woman", outfit_color="purple", hat=None, x=0.4, action="count", expression="smug",
                  item="bag"),
             stan(x=0.7, action="shrug", expression="neutral", facing=-1)],
    "overlays": [{"type": "checklist", "x": 0.06, "y": 0.18, "size": 48,
                  "items": [["vote", False], ["hold office", False], ["own property", True], ["run a business", True]],
                  "times": [0.6, 1.2, 3.4, 4.2]}]},
    claims=[F("Roman women could not vote or hold office but could own property and run businesses", SRC["family"])])

sc("f05", "development", "Pets? Absolutely. Dogs guarded the door, and Romans also kept birds. Some rich ladies had pet nightingales and tiny lapdogs.", {
    "background": rome(temple=False),
    "props": [{"type": "dog", "x": 0.6, "y": 0.9}, {"type": "chicken", "x": 0.8, "y": 0.92}],
    "cast": [cast("kid", "child", x=0.4, action="laugh", expression="laughing")]},
    claims=[F("Romans kept dogs and birds as pets", SRC["dogs"])])

sc("f06", "development", "And children played with dolls, spinning tops, and knucklebones, a game a lot like jacks.", {
    "background": PAPER,
    "cast": [cast("kid", "child", x=0.35, action="sit", expression="grin"),
             cast("kid2", "child", x=0.6, action="sit_talk", expression="happy", facing=-1)],
    "props": [{"type": "item", "item": "egg", "x": 0.48, "y": 0.84, "scale": 1.2},
              {"type": "item", "item": "egg", "x": 0.5, "y": 0.86, "scale": 1.2}]},
    claims=[F("Roman children played with dolls, tops and knucklebones (tali)", SRC["school"])])

# ================================================================================================ CH8 GAMES
ch("Holidays: Chariots and Gladiators")
sc("g01", "climax", "Now, on festival days, the routine changes completely, and Rome had a lot of festival days.", {
    "background": rome(),
    "cast": [stan(x=0.4, action="cheer", expression="grin")],
    "props": [{"type": "icon", "icon": "sparkle", "x": 0.4, "y": 0.4}]},
    claims=[F("The Roman calendar had many festival days with public games (ludi)", SRC["beard"])],
    transition="wipe")

sc("g02", "climax", "The biggest crowd-pleaser wasn't the gladiators. It was chariot racing, at the Circus Maximus, which held around a hundred and fifty thousand people.", {
    "background": {"type": "arena"},
    "props": [{"type": "chariot", "x": 0.3, "y": 0.92, "move": [[0, -0.2, 0.92], [6, 1.2, 0.92]]}],
    "overlays": [{"type": "stat", "value": 150000, "caption": "spectators at the Circus Maximus (estimates vary)",
                  "y": 0.25, "size": 130, "at_word": 18}],
    "camera": {"move": "pan_right", "amount": 120}},
    claims=[F("The Circus Maximus held an estimated 150,000 or more spectators", SRC["circus"], "estimate")],
    sfx=[{"name": "rumble", "at": 0.5}, {"name": "ding", "at_word": 18}])

sc("g02b", "climax", "The satirist Juvenal sneered that all the Roman people wanted anymore was two things: bread and circuses.", {
    "background": {"type": "arena"},
    "props": [{"type": "item", "item": "bread", "x": 0.35, "y": 0.62, "scale": 4.0, "at_word": 14},
              {"type": "chariot", "x": 0.65, "y": 0.9, "scale": 0.8, "at_word": 16}],
    "overlays": [{"type": "title", "lines": ["PANEM ET", "CIRCENSES"], "colors": ["ink", "red"], "y": 0.14,
                  "at_word": 14}]},
    claims=[F("'Panem et circenses' comes from Juvenal, Satire 10", "Juvenal, Satire 10.81")])

sc("g03b", "climax", "And the top drivers were superstars. One charioteer, Diocles, won over a thousand races and earned around thirty-five million sesterces.", {
    "background": {"type": "arena"},
    "cast": [cast("diocles", outfit="tunic", outfit_color="red", hat="headband", x=0.4, action="cheer",
                  expression="grin", item="flag")],
    "props": [{"type": "coins", "x": 0.7, "y": 0.9, "pile": 20, "scale": 1.6, "at_word": 15}],
    "overlays": [{"type": "stat", "value": "35,000,000", "caption": "sesterces in prize money (inscription)",
                  "y": 0.25, "x": 0.62, "size": 110, "at_word": 15}]},
    claims=[F("Gaius Appuleius Diocles won 1,462 races and earned about 35.9 million sesterces", SRC["diocles"])],
    sfx=[{"name": "ding", "at_word": 15}])

sc("g03", "climax", "Fans supported teams by color: Reds, Whites, Greens and Blues. And yes, they rioted when they lost.", {
    "background": {"type": "arena"},
    "overlays": [{"type": "people", "n": 4, "k": 4, "cols": 4, "color": "red", "y": 0.62, "fig_scale": 1.0,
                  "caption": "REDS · WHITES · GREENS · BLUES"}],
    "props": [{"type": "icon", "icon": "anger", "x": 0.85, "y": 0.4, "at_word": 15}]},
    claims=[F("Chariot racing factions were the Reds, Whites, Greens and Blues", SRC["circus"])])

sc("g04", "climax", "Then there were the gladiators, at the Colosseum, which opened in the year eighty and could seat about fifty thousand.", {
    "background": {"type": "arena"},
    "cast": [legion("glad1", x=0.35, action="swing", item="gladius", expression="angry"),
             cast("glad2", outfit="armor", hat="helmet", item="spear", x=0.65, facing=-1, action="punch",
                  expression="determined")],
    "overlays": [{"type": "stat", "value": "~50,000", "caption": "seats in the Colosseum (opened AD 80)", "y": 0.25,
                  "size": 130, "at_word": 17}]},
    claims=[F("The Colosseum was inaugurated in AD 80 and seated around 50,000", SRC["colosseum"])],
    sfx=[{"name": "hit", "at": 1.0, "gain_db": -8}])

sc("g05", "climax", "But here's a surprise: most fights did not end in death. Gladiators were expensive to train, and their owners wanted them back.", {
    "background": {"type": "arena"},
    "cast": [legion("glad1", x=0.35, action="cheer", item="gladius", expression="grin"),
             cast("glad2", outfit="armor", hat="helmet", x=0.65, facing=-1, action="sit", expression="tired")],
    "overlays": [{"type": "caption", "text": "Myth: \"every fight was to the death\"", "at": 0.5}]},
    claims=[F("Most gladiator bouts did not end in death; gladiators were costly investments", SRC["beard"],
              "estimate")])

sc("g06", "climax", "The thumbs-down gesture from the movies? We're not actually sure which way the thumb pointed.", {
    "background": PAPER,
    "cast": [cast("emperor", outfit="toga", hat="laurel", x=0.5, action="hold_up", expression="thinking", scale=1.5)],
    "props": [{"type": "icon", "icon": "?", "x": 0.7, "y": 0.4, "at_word": 10}]},
    claims=[F("The exact 'pollice verso' gesture is uncertain", SRC["beard"])])

# ================================================================================================ CH9 NIGHT
ch("Night: The Loudest Time in Rome")
sc("n01", "climax", "Finally, night falls. Peace and quiet? Not in Rome.", {
    "background": rome(time="night"),
    "cast": [stan(x=0.4, action="idle", expression="sleepy")],
    "overlays": [hour("NIGHT")]},
    transition="fade")

sc("n02", "climax", "Julius Caesar had banned most wagons from the streets during daytime, so all the deliveries happened at night.", {
    "background": rome(time="night"),
    "props": [{"type": "cart", "x": 0.4, "y": 0.92, "moving": True, "load": ["sack", "barrel"],
               "move": [[0, -0.1, 0.92], [6, 0.9, 0.92]]},
              {"type": "horse", "x": 0.6, "y": 0.92, "walk": True, "scale": 0.8,
               "move": [[0, 0.1, 0.92], [6, 1.1, 0.92]]}],
    "overlays": [{"type": "fact", "text": "Caesar's law banned most wheeled carts inside Rome during the day.",
                  "source": SRC["lex"], "at": 1.0}]},
    claims=[F("Caesar's legislation restricted wheeled vehicles in Rome during daylight hours", SRC["lex"])],
    sfx=[{"name": "rumble", "at": 0.5}])

sc("n03", "climax", "Iron-rimmed wheels on stone, drivers shouting, animals braying. The poet Juvenal joked that in Rome, insomnia kills more people than disease.", {
    "background": rome(time="night"),
    "props": [{"type": "cart", "x": 0.6, "y": 0.92, "moving": True},
              {"type": "icon", "icon": "anger", "x": 0.3, "y": 0.4}],
    "cast": [stan(x=0.3, action="facepalm", expression="tired")],
    "overlays": [{"type": "quote", "text": "Most sick people here die from lack of sleep.",
                  "by": "Juvenal, Satire 3 (paraphrased)", "y": 0.25, "at_word": 12, "size": 54}]},
    claims=[F("Juvenal's Satire 3 complains of sleepless nights caused by traffic", SRC["juvenal"])],
    sfx=[{"name": "rumble", "at": 0.3}])

sc("n04", "climax", "And walking home in the dark was risky. No street lights, muggers, and people emptying chamber pots out of windows.", {
    "background": rome(time="night", temple=False),
    "cast": [stan(x=0.4, action="sneak", expression="scared", path=[[0, 0.15, GROUND], [6, 0.6, GROUND]],
                  item="torch")],
    "props": [{"type": "item", "item": "bucket", "x": 0.55, "y": 0.35, "at_word": 15,
               "move": [[0, 0.55, 0.3], [0.6, 0.55, 0.3]], "rot": 2.5}],
    "overlays": [{"type": "vignette", "alpha": 0.6}]},
    claims=[F("Juvenal describes night-time dangers: robbers and pots thrown from windows", SRC["juvenal"])],
    sfx=[{"name": "splash", "at_word": 18}])

sc("n04b", "climax", "Rich Romans hired slaves with torches to walk them home. Everyone else hurried, and kept a dog at home. Pompeii even has a mosaic that says: beware of the dog.", {
    "background": rome(time="night", temple=False),
    "props": [{"type": "dog", "x": 0.65, "y": 0.9}, {"type": "board", "x": 0.65, "y": 0.4, "text": "CAVE CANEM",
                                                      "w": 420, "at_word": 25}],
    "cast": [stan(x=0.3, action="walk", item="torch", expression="worried")]},
    claims=[F("The 'Cave canem' mosaic is in the House of the Tragic Poet, Pompeii", SRC["dogs"])])

sc("n05", "climax", "Stanius climbs his stairs to the top floor, blows out his oil lamp, and listens to the carts until he falls asleep.", {
    "background": {"type": "interior", "dark": 0.55, "hearth": False, "season": "summer", "time": "night"},
    "props": [{"type": "bed", "x": 0.45, "y": 0.9, "scale": 1.5}, {"type": "icon", "icon": "z", "x": 0.45,
                                                                      "y": 0.66, "at": 4.0}],
    "cast": [stan(x=0.5, y=0.88, action="sleep", expression="sleepy")]},
    transition="fade")

# ================================================================================================ ENDING
ch("So, Would You Survive a Roman Day?")
sc("e01", "ending", "So, let's sum up a Roman day. Up at dawn, greet the boss, work until lunch, nap, baths, dinner, and a very loud night.", {
    "background": PAPER,
    "cast": [stan(x=0.18, action="talk", expression="happy")],
    "overlays": [{"type": "checklist", "x": 0.36, "y": 0.14, "size": 50,
                  "items": [["dawn: bread & greetings", True], ["morning: work", True], ["noon: street food + nap", True],
                            ["afternoon: baths", True], ["evening: dinner", True], ["night: carts. so many carts.", False]],
                  "times": [1.5, 2.6, 3.3, 4.0, 4.6, 5.6]}]},
    transition="wipe")

sc("e02", "ending", "Honestly? The short working day and the baths sound amazing. The toilets, the fires and the top-floor apartments, not so much.", {
    "background": {"type": "split", "left": (0.8, 0.93, 0.8), "right": (0.98, 0.85, 0.82), "left_label": "AMAZING",
                   "right_label": "NOPE"},
    "props": [{"type": "icon", "icon": "check", "x": 0.25, "y": 0.6}, {"type": "icon", "icon": "x", "x": 0.75, "y": 0.6}],
    "cast": [stan(x=0.5, action="shrug", expression="thinking")]})

sc("e03", "ending", "So tell me in the comments: would you trade your life for one day as a Roman? And which part would you skip?", {
    "background": rome(),
    "cast": [stan(x=0.4, action="point", expression="grin", outfit="toga", hat="laurel", scale=1.5)],
    "props": [{"type": "icon", "icon": "?", "x": 0.62, "y": 0.4, "at_word": 18}]})

sc("e04", "ending", "And if you liked spending a day with Stanius, subscribe. Next time, we find out how long you'd last in every era of history.", {
    "background": PAPER,
    "cast": [stan(x=0.32, action="wave", expression="grin", actions=[["w10", "point"]])],
    "props": [{"type": "board", "x": 0.7, "y": 0.45, "text": "SUBSCRIBE", "color": "red", "text_color": "white",
               "w": 520, "h": 150, "size": 78, "at_word": 10, "loop": "pulse"}]},
    sfx=[{"name": "pop", "at_word": 10}], pause=0.8)

st.save(
    "roman-day",
    title="What Did Ancient Romans Actually Do All Day?",
    idea="A full day in the life of an ordinary Roman in ancient Rome, hour by hour",
    question="Would you trade your life for one day as a Roman? Which part would you skip?",
    mood="curious",
    metadata={
        "title": "What Did Ancient Romans Actually Do All Day?",
        "description_intro": (
            "Rome, around AD 100: a city of almost a million people. But what did an ordinary Roman actually do "
            "all day? Follow Stanius from dawn to midnight — the morning visit to his patron, free grain, a job "
            "that ends at lunchtime, street-food counters, the baths, the (very public) toilets, the Circus "
            "Maximus… and the loudest nights in the ancient world.\n\nA stickman history story with real facts "
            "and sources."),
        "hashtags": ["#history", "#ancientrome", "#stickman"],
        "tags": ["ancient rome", "roman daily life", "what did romans do all day", "day in the life", "roman empire",
                 "roman baths", "gladiators", "circus maximus", "ancient history", "stickman", "stickman animation",
                 "history animated", "roman toilets", "insula", "romans", "history explained", "pompeii"],
        "pinned_comment": "Would you trade your life for one day as a Roman? 🏛️ And which part would you skip — "
                          "the sponge on a stick, or the 3 a.m. carts? 👇",
        "chapter_moods": ["curious", "calm", "medieval", "curious", "calm", "medieval", "curious", "calm", "medieval",
                          "tense", "somber", "calm"],
        "intro_chapter": "Rome Wakes Up",
        "thumbnail": {
            "visual": {"background": {"type": "rome"},
                       "cast": [{"id": "stan", "outfit": "toga", "x": 0.72, "y": 0.95, "scale": 1.9, "facing": -1,
                                 "action": "laugh", "expression": "laughing", "hat": "laurel"}],
                       "props": [{"type": "amphora", "x": 0.92, "y": 0.95, "scale": 1.3, "enter": "none"}]},
            "t": 1.0, "lines": ["A ROMAN'S", "WHOLE DAY"], "colors": ["white", "yellow"],
            "badge": "WORK ENDS AT NOON?!", "badge_color": "red", "size": 120},
        "thumbnail_alts": [{
            "visual": {"background": {"type": "baths"},
                       "props": [{"type": "latrine", "x": 0.68, "y": 0.92, "scale": 1.1, "enter": "none"}],
                       "cast": [{"id": "stan", "outfit": "tunic", "outfit_color": [0.85, 0.75, 0.55], "x": 0.62,
                                 "y": 0.85, "scale": 1.6, "action": "sit", "expression": "disgusted", "facing": -1},
                                {"id": "n1", "outfit": "toga", "x": 0.82, "y": 0.85, "scale": 1.6, "action": "sit_talk",
                                 "expression": "laughing", "facing": -1}]},
            "t": 1.0, "lines": ["ROMAN", "TOILETS"], "colors": ["white", "yellow"],
            "badge": "NO WALLS. NO DOORS.", "badge_color": "teal", "size": 130}],
    },
)
