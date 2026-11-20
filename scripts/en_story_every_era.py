"""Episode 3 — How Long Would You Last in Every Era of History?

Format chosen from the niche research (data/stickman_en/research/): tiered ranking "How Long You'd Last in
Every …" (13.2M and 3.8M views). One chapter per level, a survival dial and a verdict per level.

Run:  python3 scripts/en_story_every_era.py
      python -m fabrica --channel stickman_en make stories_en/every-era.json
"""
from storykit_en import GROUND, F, Story, cast

st = Story()
sc = st.sc
ch = st.chapter


def stan(**kw):
    kw.setdefault("outfit", "suit")
    kw.setdefault("outfit_color", "navy")
    return cast("stan", **kw)


PAPER = {"type": "paper"}
LINED = {"type": "paper", "lines": True, "floor": False}
STORY = {"type": "fiction", "text": "WHAT IF"}


def level(n, name):
    return {"type": "counter", "label": f"LEVEL {n}", "value": f"· {name}", "corner": "tr", "size": 44}


def verdict(value, label, x=0.75, y=0.55):
    return {"type": "dial", "x": x, "y": y, "value": value, "label": label, "scale": 1.2, "enter": "pop"}


SRC = {
    "lgm": "Clark et al., 'The Last Glacial Maximum', Science 325 (2009)",
    "tierney": "Tierney et al., 'Glacial cooling and climate sensitivity', Nature 584 (2020)",
    "hypo": "UK NHS, 'Hypothermia'; US CDC, 'Hypothermia'",
    "hg": "Mark Nathan Cohen, Health and the Rise of Civilization (1989)",
    "aera": "Ancient Egypt Research Associates (Mark Lehner) — Giza workers' town",
    "hawass": "Zahi Hawass, excavations of the pyramid builders' tombs at Giza",
    "asc": "Anglo-Saxon Chronicle, entry for 793 (Lindisfarne)",
    "viking": "National Museum of Denmark, 'Viking hygiene' (combs, tweezers, ear spoons)",
    "longship": "Viking Ship Museum, Roskilde (Skuldelev ships)",
    "horrox": "Rosemary Horrox (ed.), The Black Death (Manchester University Press, 1994)",
    "benedictow": "Ole J. Benedictow, The Black Death 1346-1353 (Boydell, 2004)",
    "rediker": "Marcus Rediker, Villains of All Nations: Atlantic Pirates in the Golden Age (2004)",
    "johnson": "Captain Charles Johnson, A General History of the Pyrates (1724) — Bartholomew Roberts' articles",
    "scurvy": "James Lind, A Treatise of the Scurvy (1753); NHS, 'Scurvy'",
    "factory_act": "UK Parliament, 'The 1833 Factory Act'",
    "chadwick": "Edwin Chadwick, Report on the Sanitary Condition of the Labouring Population (1842)",
    "iwm_somme": "Imperial War Museums, 'The first day of the Somme'",
    "iwm_trench": "Imperial War Museums, 'What life was like in the trenches of WW1'",
    "iwm_dead": "Imperial War Museums / CWGC — roughly 1 in 8 British soldiers who served in WW1 died",
    "who": "World Health Organization, World Health Statistics (global life expectancy ~73 years)",
    "unwpp": "UN World Population Prospects 2024",
    "mezhyrich": "Pidoplichko / Soffer — mammoth-bone dwellings at Mezhyrich, Ukraine (c. 15,000 years ago)",
    "needles": "d'Errico et al., 'The origin and evolution of sewing technologies in Eurasia and North America' (2018)",
    "gangs": "AERA / Mark Lehner — work-gang names ('Friends of Khufu', 'Drunkards of Menkaure')",
    "absence": "British Museum EA 5634 — absence register from Deir el-Medina (c. 1250 BC)",
    "horns": "National Museum of Denmark — no Viking-age horned helmets (Gjermundbu helmet)",
    "decameron": "Giovanni Boccaccio, The Decameron (introduction, 1348-53)",
    "quarantine": "Gensini et al., 'The concept of quarantine in history' (J. Infection, 2004)",
    "plank": "Rediker (2004); David Cordingly, Under the Black Flag (1995)",
    "blackbeard": "North Carolina Dept. of Natural and Cultural Resources — Blackbeard killed at Ocracoke, 22 Nov 1718",
    "fines": "E. P. Thompson, 'Time, Work-Discipline and Industrial Capitalism' (1967)",
    "iwm_post": "Imperial War Museums — around 2 billion letters were sent to and from the front",
    "rations": "Imperial War Museums — British soldiers' rations (bully beef, biscuits, tea)",
    "alcuin": "Alcuin of York, letter to King Æthelred of Northumbria (793)",
    "predators": "Stuart & Lister, Pleistocene megafauna of Europe (cave lions, wolves, bears)",
    "rome": "Mary Beard, SPQR (2015); Juvenal, Satire 3",
}

# ================================================================================================ INTRO
sc("x01", "hook", "Imagine you're pulled out of your bed tonight and dropped into the past. No phone, no money, no skills. Just you, in your pajamas.", {
    "background": {"type": "solid", "color": "navy", "rays": True},
    "cast": [stan(x=0.5, action="cower", expression="scared", scale=1.5, outfit="tunic", outfit_color="sky",
                  enter="drop")],
    "overlays": [STORY],
    "camera": {"move": "punch"}},
    claims=[F("Time travel is a thought experiment", "Narrative device", "fiction")],
    sfx=[{"name": "whoosh", "at": 0.1}, {"name": "hit", "at": 0.4, "gain_db": -6}], transition="cut")

sc("x02", "hook", "The question is simple: how long would you last? We'll go through eight eras, from the Ice Age to today, and rate each one.", {
    "background": PAPER,
    "cast": [stan(x=0.22, action="talk", expression="neutral")],
    "overlays": [{"type": "timeline", "items": ["ICE", "EGYPT", "VIKING", "PLAGUE", "PIRATE", "FACTORY", "WW1", "NOW"],
                  "at": 0, "w": 1300, "y": 0.2, "colors": ["sky", "yellow", "red", "lime", "navy", "darkgrey",
                                                            "grey", "green"]}],
    "props": [verdict(0.5, "your odds", 0.62, 0.72)]})

sc("x02b", "hook", "A few rules. You get local clothes, and you magically understand the language. Everything else, you have to figure out yourself.", {
    "background": PAPER,
    "cast": [stan(x=0.25, action="hold_up", expression="happy")],
    "overlays": [{"type": "checklist", "x": 0.45, "y": 0.22, "size": 56,
                  "items": [["local clothes", True], ["speak the language", True], ["phone, money, skills", False]],
                  "times": [1.6, 2.8, 5.0]}]})

sc("x03", "hook", "And fair warning: some of these levels end very quickly. Let's go.", {
    "background": PAPER,
    "cast": [stan(x=0.4, action="shrug", expression="worried", actions=[["w9", "point"]])],
    "camera": {"move": "push_in", "focus": "stan"}},
    transition="wipe")

# ================================================================================================ L1 ICE AGE
ch("Level 1: The Ice Age")
sc("i01", "development", "Level one. Twenty thousand years ago, at the peak of the last Ice Age. Huge ice sheets cover much of the north.", {
    "background": {"type": "ice_age"},
    "cast": [stan(x=0.4, action="shiver", expression="scared", outfit="tunic", outfit_color="sky")],
    "overlays": [level(1, "ICE AGE"), {"type": "title", "text": "~20,000 YEARS AGO", "y": 0.15, "at_word": 2}]},
    claims=[F("The Last Glacial Maximum was roughly 26,000-19,000 years ago", SRC["lgm"])],
    transition="wipe")

sc("i02", "development", "Scientists estimate the whole planet was around six degrees Celsius colder on average. In Europe, winters were brutal.", {
    "background": {"type": "ice_age", "weather": "snow"},
    "overlays": [{"type": "stat", "value": "-6°C", "caption": "global average vs. pre-industrial", "y": 0.35,
                  "size": 190, "color": "blue", "at_word": 7}]},
    claims=[F("Global mean temperature at the LGM was about 6°C below pre-industrial", SRC["tierney"], "estimate")],
    sfx=[{"name": "ding", "at_word": 7}])

sc("i03", "development", "Your first problem isn't the mammoths. It's the cold. In freezing, wet conditions, hypothermia can kill an unprotected person within hours.", {
    "background": {"type": "ice_age", "weather": "snow"},
    "props": [{"type": "mammoth", "x": 0.78, "y": 0.86, "scale": 0.8, "walk": True,
               "move": [[0, 1.2, 0.86], [5, 0.78, 0.86]]}],
    "cast": [stan(x=0.3, action="shiver", expression="scared", outfit="tunic", outfit_color="sky")],
    "overlays": [{"type": "meter", "label": "BODY HEAT", "from": 0.8, "to": 0.15, "time": 5.0, "y": 0.12}]},
    claims=[F("Hypothermia can become life-threatening within hours in cold, wet exposure", SRC["hypo"])])

sc("i04", "development", "To survive, you'd need fire, fur clothing, and a group. Ice Age people lived in small bands, hunting reindeer, horses and mammoths together.", {
    "background": {"type": "cave"},
    "cast": [cast("hunter1", outfit="fur", hat="fur_hood", item="spear", x=0.25, action="talk", expression="happy"),
             cast("hunter2", outfit="fur", hat="fur_hood", x=0.7, action="sit", expression="neutral", facing=-1),
             stan(x=0.45, action="shiver", expression="worried", outfit="tunic", outfit_color="sky")]},
    claims=[F("Upper Palaeolithic people lived in small hunter-gatherer bands hunting large game", SRC["hg"])])

sc("i05", "development", "Here's the surprise: if they took you in, life wasn't all misery. Many hunter-gatherers were tall, strong and well fed, with plenty of free time.", {
    "background": {"type": "cave"},
    "cast": [stan(x=0.4, action="eat", expression="happy", outfit="fur"),
             cast("hunter1", outfit="fur", hat="fur_hood", x=0.65, action="laugh", expression="laughing",
                  facing=-1)]},
    claims=[F("Skeletal evidence suggests many pre-agricultural foragers were relatively tall and well nourished",
              SRC["hg"], "estimate")])

sc("i05b", "development", "Food is mostly meat and fat, plus fish, roots and berries when the season allows. Bone marrow was a prized treat.", {
    "background": {"type": "cave"},
    "props": [{"type": "plate", "x": 0.55, "y": 0.86, "food": "meat", "scale": 1.6}],
    "cast": [stan(x=0.35, action="eat", expression="happy", outfit="fur")]},
    claims=[F("Ice Age diets in cold regions relied heavily on animal foods, supplemented by plants and fish",
              SRC["hg"])])

sc("i05c", "development", "Some groups even built huts out of mammoth bones. In Ukraine, archaeologists found shelters made from the bones of dozens of mammoths.", {
    "background": {"type": "ice_age"},
    "props": [{"type": "skull", "x": 0.55, "y": 0.86, "scale": 1.3}, {"type": "skull", "x": 0.65, "y": 0.86, "scale": 1.1},
              {"type": "mammoth", "x": 0.85, "y": 0.86, "scale": 0.6}],
    "cast": [stan(x=0.3, action="point", expression="surprised", outfit="fur")]},
    claims=[F("Mammoth-bone dwellings are known from sites such as Mezhyrich, Ukraine", SRC["mezhyrich"])])

sc("i05d", "development", "And one of the most important inventions of the age? The sewing needle, made of bone. It let people make tight, warm clothes.", {
    "background": LINED,
    "props": [{"type": "item", "item": "staff", "x": 0.5, "y": 0.75, "scale": 1.6, "rot": 1.2}],
    "overlays": [{"type": "fact", "text": "Eyed bone needles appear in the Upper Palaeolithic, enabling fitted clothing.",
                  "source": SRC["needles"], "at": 2.0}]},
    claims=[F("Eyed bone needles appear in the Upper Palaeolithic", SRC["needles"])])

sc("i05e", "development", "And you're not at the top of the food chain yet. Cave lions, wolves and cave bears shared this world with you.", {
    "background": {"type": "ice_age", "time": "dusk"},
    "props": [{"type": "dog", "x": 0.7, "y": 0.9, "color": "grey", "scale": 1.3, "walk": True,
               "move": [[0, 1.1, 0.9], [4, 0.72, 0.9]]}],
    "cast": [stan(x=0.3, action="cower", expression="scared", outfit="fur")]},
    claims=[F("Ice Age Europe had cave lions, wolves and cave bears", SRC["predators"])])

sc("i06", "development", "But you don't know how to hunt, track or make a spear. Alone, you'd last days. With a friendly band, maybe years.", {
    "background": {"type": "ice_age", "cave": True},
    "cast": [stan(x=0.3, action="hold", item="spear", expression="worried", outfit="fur")],
    "props": [verdict(0.18, "DAYS (alone)", 0.72, 0.62)]},
    sfx=[{"name": "ding", "at": 3.0}])

# ================================================================================================ L2 EGYPT
ch("Level 2: Building the Pyramids")
sc("e01", "development", "Level two. Egypt, around twenty-five sixty BC. The Great Pyramid of Giza is going up, and you've just been put on a work crew.", {
    "background": {"type": "desert"},
    "cast": [stan(x=0.3, action="pull", expression="tired", outfit="tunic", outfit_color="white")],
    "props": [{"type": "sack", "x": 0.18, "y": 0.86, "label": "STONE", "color": "stone"}],
    "overlays": [level(2, "EGYPT")]},
    claims=[F("The Great Pyramid of Giza was built c. 2560 BC (reign of Khufu)", SRC["aera"])],
    transition="wipe")

sc("e02", "development", "Forget the movies. The builders were most likely not slaves, but paid workers, many of them farmers doing a rotation.", {
    "background": {"type": "desert"},
    "cast": [cast("w1", outfit="tunic", outfit_color="white", x=0.3, action="pull", expression="determined"),
             cast("w2", outfit="tunic", outfit_color="white", x=0.45, action="pull", expression="determined"),
             stan(x=0.6, action="pull", expression="tired", outfit="tunic", outfit_color="white")],
    "overlays": [{"type": "caption", "text": "Myth: \"the pyramids were built by slaves\"", "at": 0.3}]},
    claims=[F("Archaeology at Giza indicates the pyramid builders were organized, paid and fed laborers, not slaves",
              SRC["aera"] + "; " + SRC["hawass"])])

sc("e03", "development", "And you'd be fed. Archaeologists found their town, with bakeries and breweries. The pay was bread and beer.", {
    "background": {"type": "desert", "pyramids": True},
    "props": [{"type": "item", "item": "bread", "x": 0.55, "y": 0.62, "scale": 4.0, "at_word": 15},
              {"type": "item", "item": "mug", "x": 0.72, "y": 0.62, "scale": 3.6, "at_word": 17}],
    "cast": [stan(x=0.3, action="cheer", expression="grin", outfit="tunic", outfit_color="white")]},
    claims=[F("The workers' town at Giza had bakeries and breweries; rations included bread and beer", SRC["aera"])],
    sfx=[{"name": "pop", "at_word": 15}, {"name": "pop", "at_word": 17}])

sc("e04", "development", "Even medical care. Skeletons from the workers' cemetery show broken bones that were set and healed.", {
    "background": LINED,
    "props": [{"type": "skull", "x": 0.5, "y": 0.6, "scale": 1.6}],
    "overlays": [{"type": "fact", "text": "Builders' tombs at Giza show healed fractures and even signs of surgery.",
                  "source": SRC["hawass"], "at": 1.0}]},
    claims=[F("Skeletons of Giza workers show healed fractures, indicating medical care", SRC["hawass"])])

sc("e04b", "development", "The workers were organized into gangs with team names. Graffiti left inside the pyramids include names like Friends of Khufu.", {
    "background": {"type": "desert"},
    "props": [{"type": "board", "x": 0.68, "y": 0.45, "text": "FRIENDS OF KHUFU", "w": 520, "color": (0.98, 0.9, 0.7)}],
    "cast": [cast("w1", outfit="tunic", outfit_color="white", x=0.25, action="cheer", expression="grin"),
             stan(x=0.4, action="cheer", expression="grin", outfit="tunic", outfit_color="white")]},
    claims=[F("Work-gang names such as 'Friends of Khufu' appear in graffiti at Giza", SRC["gangs"])])

sc("e04c", "development", "At the next pyramid, one gang called itself the Drunkards of Menkaure. Which tells you something about the beer ration.", {
    "background": {"type": "desert"},
    "props": [{"type": "board", "x": 0.68, "y": 0.45, "text": "DRUNKARDS OF MENKAURE", "w": 600,
               "color": (0.98, 0.9, 0.7)}],
    "cast": [stan(x=0.35, action="laugh", item="mug", expression="laughing", outfit="tunic", outfit_color="white")]},
    claims=[F("A gang name 'Drunkards of Menkaure' is attested", SRC["gangs"])])

sc("e04d", "development", "And about a thousand years later, at another royal work site, we have attendance records with excuses for skipping work.", {
    "background": LINED,
    "props": [{"type": "scroll", "x": 0.5, "y": 0.92, "lines": ["ABSENT:", "· brewing beer", "· stung by a scorpion",
                                                                 "· embalming his brother", "· eye trouble"],
               "w": 620, "h": 560, "size": 46}]},
    claims=[F("A Deir el-Medina absence register lists reasons such as brewing beer, scorpion stings and eye trouble",
              SRC["absence"])])

sc("e05", "development", "The danger is the work itself: dragging blocks of over two tons, in the heat, all day. Backs, knees and fingers paid the price.", {
    "background": {"type": "desert"},
    "props": [{"type": "board", "x": 0.6, "y": 0.75, "text": "2.5 TONS", "w": 300, "color": "stone",
               "move": [[0, 0.75, 0.75], [6, 0.6, 0.75]]}],
    "cast": [stan(x=0.35, action="pull", expression="tired", outfit="tunic", outfit_color="white")]},
    claims=[F("Most Great Pyramid blocks average around 2.5 tonnes", SRC["aera"], "estimate")])

sc("e06", "development", "Verdict: tough, but you'd probably survive for years. Level two is one of the safest on this list.", {
    "background": {"type": "desert"},
    "cast": [stan(x=0.3, action="cheer", expression="grin", outfit="tunic", outfit_color="white")],
    "props": [verdict(0.75, "YEARS", 0.7, 0.62)]},
    sfx=[{"name": "ding", "at": 1.0}])

# ================================================================================================ L3 VIKINGS
ch("Level 3: A Viking Raid")
sc("v01", "development", "Level three. The year 793. You wake up on a Viking longship heading for the monastery of Lindisfarne in England.", {
    "background": {"type": "deck", "viking": True, "time": "grey", "weather": "rain"},
    "cast": [stan(x=0.35, action="sick", expression="sick", outfit="tunic", outfit_color="red"),
             cast("viking", hat="viking", beard="long", outfit="tunic", outfit_color="blue", item="axe", x=0.15,
                  action="laugh", expression="laughing")],
    "overlays": [level(3, "VIKINGS")]},
    claims=[F("The Viking raid on Lindisfarne in 793 is often taken as the start of the Viking Age", SRC["asc"])],
    transition="wipe")

sc("v01b", "development", "The raid shocked Europe. The scholar Alcuin wrote that never before had such terror appeared in Britain.", {
    "background": {"type": "church"},
    "cast": [cast("monk", outfit="robe", outfit_color="brown", hat="tonsure", x=0.5, action="cower", expression="scared")],
    "overlays": [{"type": "quote", "text": "Never before has such terror appeared in Britain…", "by": "Alcuin of York, 793",
                  "y": 0.25, "size": 56, "at": 1.0}]},
    claims=[F("Alcuin wrote of the Lindisfarne raid's unprecedented terror", SRC["alcuin"])])

sc("v02", "development", "First problem: the ship. It's open to the sky. No cabin, no roof. You sleep on deck, in the rain, wrapped in a wool blanket.", {
    "background": {"type": "deck", "viking": True, "time": "night", "weather": "rain"},
    "props": [{"type": "bed", "x": 0.4, "y": 0.9, "scale": 1.3}],
    "cast": [stan(x=0.45, y=0.88, action="sleep", expression="tired")]},
    claims=[F("Viking longships were open boats without enclosed cabins", SRC["longship"])])

sc("v03", "development", "Second surprise: your crewmates are cleaner than you expected. Vikings carried combs, tweezers and even little ear-cleaning spoons.", {
    "background": {"type": "deck", "viking": True, "time": "grey"},
    "cast": [cast("viking", hat="viking", beard="long", outfit="tunic", outfit_color="blue", x=0.5, action="scratch",
                  expression="smug", scale=1.5)],
    "overlays": [{"type": "fact", "text": "Combs are among the most common Viking-age finds.", "source": SRC["viking"],
                  "at": 2.0}]},
    claims=[F("Viking-age finds include many combs, tweezers and ear spoons", SRC["viking"])])

sc("v03b", "development", "And sorry to disappoint you: no horned helmets. That's a nineteenth-century costume idea. Real Viking helmets were plain iron caps.", {
    "background": {"type": "deck", "viking": True},
    "cast": [cast("viking", hat="viking", beard="long", outfit="tunic", outfit_color="blue", x=0.5, action="shrug",
                  expression="smug", scale=1.5)],
    "props": [{"type": "icon", "icon": "x", "x": 0.75, "y": 0.4, "at": 1.2}],
    "overlays": [{"type": "caption", "text": "Myth: \"Vikings wore horned helmets\"", "at": 0.3}]},
    claims=[F("No horned helmets are known from the Viking Age; the image comes from 19th-century art and opera",
              SRC["horns"])])

sc("v03c", "development", "Food on board: dried fish, salted meat, hard bread, and water or sour milk. For days at a time.", {
    "background": {"type": "deck", "viking": True, "time": "grey"},
    "props": [{"type": "barrel", "x": 0.65, "y": 0.86}, {"type": "item", "item": "bread", "x": 0.5, "y": 0.6, "scale": 3.0}],
    "cast": [stan(x=0.3, action="eat", expression="disgusted", outfit="tunic", outfit_color="red")]},
    claims=[F("Viking voyage provisions included dried fish, salted meat and bread", SRC["longship"])])

sc("v04", "development", "Then the raid itself. If you hang back with the ships, you might be fine. If you're in the front line, with no training, you're in serious trouble.", {
    "background": {"type": "field", "season": "summer", "time": "grey"},
    "props": [{"type": "church", "x": 0.75, "y": 0.84, "scale": 0.8}],
    "cast": [cast("viking", hat="viking", beard="long", outfit="tunic", outfit_color="blue", item="axe", x=0.45,
                  action="run", path=[[0, 0.2, GROUND], [5, 0.6, GROUND]], expression="angry"),
             stan(x=0.15, action="cower", expression="scared", outfit="tunic", outfit_color="red")]},
    sfx=[{"name": "rumble", "at": 0.5}])

sc("v05", "development", "Verdict: a few weeks, maybe a season, depending on how good you are at hiding behind a shield.", {
    "background": {"type": "deck", "viking": True},
    "cast": [stan(x=0.3, action="cower", expression="worried", outfit="tunic", outfit_color="red")],
    "props": [verdict(0.4, "WEEKS", 0.7, 0.62)]},
    sfx=[{"name": "ding", "at": 1.0}])

ch("Bonus Level: Ancient Rome")
sc("r01", "development", "Quick bonus level: ancient Rome, around the year one hundred. If you saw our Roman video, you already know the deal.", {
    "background": {"type": "rome"},
    "cast": [stan(x=0.35, action="wave", expression="grin", outfit="toga")],
    "overlays": [{"type": "counter", "label": "BONUS", "value": "· ROME", "corner": "tr", "size": 44}]},
    transition="wipe")

sc("r02", "development", "Work ends around lunch, the baths are cheap, and there's free grain if you're a citizen. Pretty good so far.", {
    "background": {"type": "baths"},
    "cast": [stan(x=0.45, y=0.95, action="laugh", expression="laughing", outfit="tunic", outfit_color="white")]},
    claims=[F("Roman citizens received grain distributions; public baths were cheap", SRC["rome"])])

sc("r03", "development", "The catch: fires, collapsing apartment blocks, and the noise. Verdict: years, as long as you avoid the top floor.", {
    "background": {"type": "rome", "time": "night"},
    "props": [{"type": "fire", "x": 0.8, "y": 0.84}, verdict(0.7, "YEARS", 0.45, 0.6)],
    "cast": [stan(x=0.18, action="facepalm", expression="tired", outfit="tunic", outfit_color="white")]},
    claims=[F("Fires and building collapses were common hazards in Rome", SRC["rome"])],
    sfx=[{"name": "ding", "at": 3.0}])

# ================================================================================================ L4 PLAGUE
ch("Level 4: The Black Death")
sc("b01", "development", "Level four. England, summer 1348. If you watched our medieval peasant video, you know exactly what's coming.", {
    "background": {"type": "village", "season": "summer", "time": "grey"},
    "cast": [stan(x=0.4, action="idle", expression="worried", outfit="tunic", outfit_color="brown", hat="hood")],
    "props": [{"type": "rat", "x": 0.7, "y": 0.93, "walk": True, "move": [[0, 1.1, 0.93], [3, 0.7, 0.93]]}],
    "overlays": [level(4, "BLACK DEATH")]},
    transition="wipe")

sc("b02", "development", "The Black Death. Somewhere between a third and a half of the population, possibly more, is about to die.", {
    "background": LINED,
    "overlays": [{"type": "people", "n": 10, "k": 5, "cols": 10, "color": (0.6, 0.6, 0.64), "dim": "ink",
                  "reveal_at": 1.6, "y": 0.6, "caption": "3 to 5 out of every 10 people died"}]},
    claims=[F("Black Death mortality in England is estimated at a third to a half or more", SRC["horrox"] + "; " +
              SRC["benedictow"], "estimate")])

sc("b03", "development", "Your advantage? You know about germs. Avoid fleas and rats, don't crowd around the sick, and leave the city if you can.", {
    "background": {"type": "village", "season": "summer"},
    "cast": [stan(x=0.4, action="point_up", expression="smug", outfit="tunic", outfit_color="brown")],
    "overlays": [{"type": "checklist", "x": 0.58, "y": 0.2, "size": 52,
                  "items": [["avoid fleas & rats", True], ["avoid crowds", True], ["leave the city", True]],
                  "times": [3.0, 4.6, 5.6]}]})

sc("b03b", "development", "People who could afford it did exactly that. In Florence, the writer Boccaccio described the rich fleeing to their country villas.", {
    "background": {"type": "field", "season": "summer"},
    "props": [{"type": "cart", "x": 0.45, "y": 0.92, "moving": True, "load": ["sack", "barrel"],
               "move": [[0, 0.1, 0.92], [6, 0.8, 0.92]]}],
    "cast": [cast("rich", outfit="robe", outfit_color="purple", hat="cap", hat_color="red", x=0.6, action="walk",
                  path=[[0, 0.25, GROUND], [6, 0.95, GROUND]], expression="worried")]},
    claims=[F("Boccaccio describes people fleeing plague-stricken Florence for the countryside", SRC["decameron"])])

sc("b03c", "development", "Within a few decades, cities started inventing quarantine: forty days of isolation for ships and travelers.", {
    "background": {"type": "field", "season": "summer", "ground": "sand"},
    "props": [{"type": "sea", "x": 0.5, "y": 0.84}, {"type": "ship", "x": 0.55, "y": 0.86, "scale": 0.8},
              {"type": "calendar", "x": 0.2, "y": 0.75, "month": "QUARANTINE", "day": 40, "scale": 1.0}]},
    claims=[F("Quarantine measures emerged in the late 14th century (Ragusa 1377; later 40-day 'quaranta giorni')",
              SRC["quarantine"])])

sc("b04", "development", "Your disadvantage? Everyone thinks you're very strange, and there's no cure. Verdict: honestly, a coin flip.", {
    "background": {"type": "village", "season": "autumn", "time": "dusk"},
    "props": [{"type": "coin", "x": 0.3, "y": 0.6, "scale": 1.8}, verdict(0.5, "COIN FLIP", 0.7, 0.62)],
    "cast": []},
    sfx=[{"name": "ding", "at": 2.0}])

# ================================================================================================ L5 PIRATES
ch("Level 5: A Pirate Ship")
sc("p01", "development", "Level five. The Caribbean, around 1718, the Golden Age of Piracy. You've just signed on to a pirate crew.", {
    "background": {"type": "deck", "pirate_flag": True},
    "cast": [stan(x=0.35, action="cheer", expression="grin", outfit="sailor", hat="tricorn"),
             cast("captain", outfit="tunic", outfit_color="red", hat="tricorn", beard="long", item="sword", x=0.65,
                  action="laugh", facing=-1, expression="laughing")],
    "overlays": [level(5, "PIRATES")]},
    claims=[F("The 'Golden Age of Piracy' peaked c. 1715-1725", SRC["rediker"])],
    transition="wipe")

sc("p02", "development", "Surprisingly, pirate ships were democratic. Crews voted for their captain and signed written rules, called articles.", {
    "background": {"type": "deck", "pirate_flag": True},
    "props": [{"type": "scroll", "x": 0.65, "y": 0.9, "lines": ["ARTICLES", "", "1. Every man has a vote",
                                                                 "2. Fair share of prizes", "3. No gambling for money",
                                                                 "4. Lights out at 8"],
               "w": 520, "h": 560, "size": 40}],
    "cast": [stan(x=0.25, action="hold", item="letter", expression="happy", outfit="sailor")]},
    claims=[F("Pirate crews elected captains and agreed written articles (e.g., Bartholomew Roberts' articles)",
              SRC["johnson"] + "; " + SRC["rediker"])])

sc("p03", "development", "There was even compensation for injuries. Lose a leg in battle, and the crew paid you from the common fund.", {
    "background": {"type": "deck", "pirate_flag": True},
    "props": [{"type": "coins", "x": 0.65, "y": 0.9, "pile": 12, "scale": 1.4}],
    "cast": [stan(x=0.35, action="count", expression="smug", outfit="sailor")]},
    claims=[F("Pirate articles specified compensation for lost limbs", SRC["johnson"])])

sc("p04", "development", "But the real killer at sea wasn't cannon fire. It was disease. Scurvy, from a lack of vitamin C, and tropical fevers.", {
    "background": {"type": "deck", "time": "grey"},
    "cast": [stan(x=0.4, action="sick", expression="sick", outfit="sailor")],
    "props": [{"type": "germ", "x": 0.7, "y": 0.5, "scale": 1.2}],
    "overlays": [{"type": "fact", "text": "Scurvy (vitamin C deficiency) and fevers killed far more sailors than combat.",
                  "source": SRC["scurvy"], "at": 2.0}]},
    claims=[F("Disease, including scurvy, killed more sailors than combat in the age of sail", SRC["scurvy"])])

sc("p04b", "development", "The food? Hard ship's biscuit, often with weevils, salted meat, and whatever you could steal. Fresh fruit was gold.", {
    "background": {"type": "deck", "time": "grey"},
    "props": [{"type": "barrel", "x": 0.7, "y": 0.86}, {"type": "item", "item": "bread", "x": 0.45, "y": 0.6, "scale": 3.0},
              {"type": "fleas", "x": 0.45, "y": 0.62, "n": 5, "scale": 1.2}],
    "cast": [stan(x=0.25, action="eat", expression="disgusted", outfit="sailor")]},
    claims=[F("Shipboard diets relied on hardtack and salted meat; biscuits often had weevils", SRC["scurvy"])])

sc("p04c", "development", "Walking the plank? Mostly a myth. Pirates had nastier punishments, like marooning: being left on a tiny island with a pistol and some water.", {
    "background": {"type": "field", "season": "summer", "ground": "sand", "sun": True},
    "props": [{"type": "sea", "x": 0.5, "y": 0.84}, {"type": "palm", "x": 0.6, "y": 0.84}],
    "cast": [stan(x=0.4, action="sad", expression="crying", outfit="sailor")],
    "overlays": [{"type": "caption", "text": "Walking the plank: very rarely, if ever, recorded", "at": 0.3}]},
    claims=[F("Walking the plank is rarely attested; marooning was a recorded pirate punishment",
              SRC["plank"] + "; " + SRC["johnson"])])

sc("p04d", "development", "Even the most famous pirate of all, Blackbeard, lasted only about two years before he was killed in battle in 1718.", {
    "background": {"type": "deck", "pirate_flag": True, "time": "dusk"},
    "cast": [cast("blackbeard", outfit="tunic", outfit_color="ink", hat="tricorn", beard="long", item="sword",
                  x=0.5, action="angry", expression="angry", scale=1.6)]},
    claims=[F("Blackbeard's piracy lasted c. 1716-1718; he was killed at Ocracoke in November 1718", SRC["blackbeard"])])

sc("p05", "development", "And the navy was hunting pirates down. Historians estimate most pirate careers lasted only a year or two.", {
    "background": {"type": "deck"},
    "props": [{"type": "ship", "x": 0.85, "y": 0.6, "scale": 0.45, "sail": "white"}],
    "cast": [stan(x=0.35, action="cower", expression="scared", outfit="sailor", hat="tricorn")]},
    claims=[F("Most pirates' careers were short, typically one to two years", SRC["rediker"], "estimate")])

sc("p06", "development", "Verdict: if you pack limes, you could last a year or two. Which, for a pirate, is a decent career.", {
    "background": {"type": "deck", "pirate_flag": True},
    "props": [{"type": "item", "item": "apple", "x": 0.3, "y": 0.6, "scale": 3.0}, verdict(0.55, "1-2 YEARS", 0.7, 0.62)],
    "cast": []},
    claims=[F("Citrus prevents scurvy (Lind's trial, 1747)", SRC["scurvy"])],
    sfx=[{"name": "ding", "at": 2.0}])

# ================================================================================================ L6 FACTORY
ch("Level 6: The Industrial Revolution")
sc("f01", "development", "Level six. Manchester, England, the 1830s. The world's first great factory city, and you've just got a job in a cotton mill.", {
    "background": {"type": "factory"},
    "cast": [stan(x=0.35, action="push", expression="tired", outfit="overalls", hat="flat_cap")],
    "overlays": [level(6, "FACTORY")]},
    claims=[F("Manchester was the leading cotton-mill city of the Industrial Revolution", SRC["chadwick"])],
    transition="wipe")

sc("f02", "development", "Shifts of twelve hours or more, six days a week. The machines are deafening, the air is full of cotton dust.", {
    "background": {"type": "factory"},
    "cast": [stan(x=0.35, action="push", expression="tired", outfit="overalls", hat="flat_cap")],
    "overlays": [{"type": "counter", "label": "SHIFT:", "from": 0, "to": 12, "suffix": " hours", "time": 3.0,
                  "corner": "tl"}]},
    claims=[F("Early factory shifts commonly ran 12+ hours, six days a week", SRC["factory_act"])])

sc("f03", "development", "And children worked too. A new law in 1833 banned kids under nine from textile mills, which tells you how common it was before.", {
    "background": {"type": "factory"},
    "cast": [cast("kid", "child", x=0.4, action="push", expression="tired", outfit="overalls", hat="flat_cap"),
             cast("kid2", "child", x=0.6, action="carry", expression="sad", outfit="overalls")],
    "overlays": [{"type": "fact", "text": "1833 Factory Act: no children under 9 in textile mills; ages 9-13 limited "
                                          "to 9 hours a day.", "source": SRC["factory_act"], "at": 2.5}]},
    claims=[F("The 1833 Factory Act banned under-9s from textile mills and limited 9-13 year olds' hours",
              SRC["factory_act"])])

sc("f03b", "development", "And time itself becomes your boss. Be a few minutes late and you're fined part of your wages. Some factories locked the gates.", {
    "background": {"type": "factory"},
    "props": [{"type": "hourglass", "x": 0.72, "y": 0.8, "period": 3}],
    "cast": [stan(x=0.35, action="run", expression="scared", outfit="overalls", hat="flat_cap")],
    "overlays": [{"type": "money", "text": "-fine for lateness", "x": 0.4, "y": 0.4, "at": 2.0}]},
    claims=[F("Factory discipline imposed fines for lateness", SRC["fines"])])

sc("f03c", "development", "Dinner: bread, potatoes, maybe a little bacon, and lots of sweet tea. Cheap calories to keep you standing.", {
    "background": {"type": "interior", "wall": (0.55, 0.5, 0.46), "hearth": False, "dark": 0.2},
    "props": [{"type": "table", "x": 0.55, "y": 0.88, "w": 420, "items": ["bread", "mug", "plate"]}],
    "cast": [stan(x=0.3, action="eat", expression="tired", outfit="overalls")]},
    claims=[F("Working-class diets relied on bread, potatoes and sweetened tea", SRC["chadwick"])])

sc("f04", "development", "Home is a crowded, damp room, with shared toilets and dirty water. Cholera swept through these cities.", {
    "background": {"type": "town", "time": "grey"},
    "props": [{"type": "smokestack", "x": 0.85, "y": 0.84}, {"type": "germ", "x": 0.5, "y": 0.5, "scale": 1.0}],
    "cast": [stan(x=0.3, action="sick", expression="sick", outfit="overalls")]},
    claims=[F("Cholera epidemics struck British industrial cities in the 1830s-1840s", SRC["chadwick"])])

sc("f04b", "development", "The machines had no guards. Children crawled underneath running looms to sweep up cotton, and accidents were common.", {
    "background": {"type": "factory"},
    "cast": [cast("kid", "child", x=0.45, y=0.9, action="sneak", expression="scared", outfit="overalls")],
    "overlays": [{"type": "caption", "text": "\"scavengers\": children who cleaned under working machines", "at": 2.0}]},
    claims=[F("Child 'scavengers' cleaned beneath moving machinery in cotton mills", SRC["factory_act"])])

sc("f05", "development", "A government report in 1842 found that the average age at death for laborers in Manchester was just seventeen. Mostly because so many children died.", {
    "background": LINED,
    "cast": [stan(x=0.15, y=0.95, action="sad", expression="sad", outfit="overalls", hat="flat_cap", scale=1.1)],
    "overlays": [{"type": "stat", "value": 17, "caption": "average age at death, Manchester laborers (1842)",
                  "y": 0.38, "size": 220, "at": 0.8}]},
    claims=[F("Chadwick's 1842 report gave an average age at death of 17 for Manchester labourers' families",
              SRC["chadwick"])],
    sfx=[{"name": "ding", "at": 0.8}])

sc("f06", "development", "As an adult, though, you'd probably survive. Verdict: years, but long, grey, exhausting ones.", {
    "background": {"type": "factory"},
    "cast": [stan(x=0.3, action="sad", expression="tired", outfit="overalls", hat="flat_cap")],
    "props": [verdict(0.65, "YEARS", 0.72, 0.62)]},
    sfx=[{"name": "ding", "at": 2.0}])

# ================================================================================================ L7 WW1
ch("Level 7: The Trenches of World War One")
sc("t01", "climax", "Level seven. France, July 1916. You're a British soldier at the Battle of the Somme.", {
    "background": {"type": "trench"},
    "cast": [stan(x=0.4, action="shiver", expression="scared", outfit="uniform", hat="brodie", item="musket")],
    "overlays": [level(7, "WW1")]},
    claims=[F("The Battle of the Somme began on 1 July 1916", SRC["iwm_somme"])],
    transition="wipe")

sc("t02", "climax", "On the very first day, the British army suffered over fifty-seven thousand casualties, including about nineteen thousand dead. The worst day in its history.", {
    "background": {"type": "trench", "time": "dusk"},
    "overlays": [{"type": "stat", "value": 57470, "caption": "British casualties on 1 July 1916", "y": 0.3,
                  "size": 170, "color": "red", "at_word": 11}]},
    claims=[F("The British suffered 57,470 casualties, including 19,240 killed, on 1 July 1916", SRC["iwm_somme"])],
    sfx=[{"name": "boom", "at": 0.5, "gain_db": -6}, {"name": "ding", "at_word": 11}])

sc("t03", "climax", "Daily life was mud, rats, lice, and trench foot from standing in cold water for days.", {
    "background": {"type": "trench"},
    "props": [{"type": "rat", "x": 0.7, "y": 0.93, "walk": True, "move": [[0, 1.1, 0.93], [4, 0.6, 0.93]]},
              {"type": "fleas", "x": 0.35, "y": 0.75, "scale": 2.0}],
    "cast": [stan(x=0.35, action="itch", expression="disgusted", outfit="uniform", hat="brodie")]},
    claims=[F("Trench life involved rats, lice and trench foot", SRC["iwm_trench"])])

sc("t04", "climax", "But here's something most people don't know: soldiers didn't live in the front line all the time. They rotated, often spending only days at a time there.", {
    "background": {"type": "trench"},
    "cast": [stan(x=0.4, action="walk", expression="happy", outfit="uniform", hat="brodie",
                  path=[[0, 0.3, GROUND], [6, 1.1, GROUND]])],
    "overlays": [{"type": "timeline", "items": ["FRONT", "SUPPORT", "RESERVE", "REST"], "at": 3, "from_at": 0,
                  "w": 1000, "y": 0.1}]},
    claims=[F("Units rotated between front line, support, reserve and rest", SRC["iwm_trench"])])

sc("t04b", "climax", "Food was monotonous: canned corned beef, called bully beef, rock-hard biscuits, and endless tea.", {
    "background": {"type": "trench"},
    "props": [{"type": "item", "item": "mug", "x": 0.6, "y": 0.62, "scale": 3.0}],
    "cast": [stan(x=0.35, action="eat", expression="tired", outfit="uniform", hat="brodie")]},
    claims=[F("British rations included bully beef, biscuits and tea", SRC["rations"])])

sc("t04c", "climax", "But the mail always came. Around two billion letters traveled between Britain and the front during the war.", {
    "background": {"type": "trench"},
    "props": [{"type": "item", "item": "letter", "x": 0.55, "y": 0.6, "scale": 3.0}],
    "cast": [stan(x=0.35, action="hold", item="letter", expression="happy", outfit="uniform", hat="brodie")],
    "overlays": [{"type": "stat", "value": "2,000,000,000", "caption": "letters to and from the front", "y": 0.25,
                  "x": 0.62, "size": 100, "at": 3.0}]},
    claims=[F("Around 2 billion letters were sent between Britain and the front", SRC["iwm_post"], "estimate")])

sc("t05", "climax", "Overall, roughly one in eight British soldiers who served was killed. Terrible odds, but most men came home.", {
    "background": LINED,
    "overlays": [{"type": "people", "n": 8, "k": 1, "cols": 8, "color": "red", "dim": "ink", "y": 0.6,
                  "caption": "≈ 1 in 8 British soldiers who served died"}]},
    claims=[F("About 12% of British soldiers who served in WW1 were killed", SRC["iwm_dead"], "estimate")])

sc("t06", "climax", "Verdict: with no training, on the first day of the Somme? Possibly minutes. Across the whole war, you'd more likely make it.", {
    "background": {"type": "trench", "time": "dusk"},
    "cast": [stan(x=0.3, action="cower", expression="scared", outfit="uniform", hat="brodie")],
    "props": [verdict(0.08, "MINUTES?!", 0.72, 0.62)]},
    sfx=[{"name": "boom", "at": 1.0, "gain_db": -8}])

# ================================================================================================ L8 NOW
ch("Level 8: Right Now")
sc("n01", "ending", "And finally, level eight. You wake up back in your own bed. Today.", {
    "background": {"type": "interior", "wall": (0.8, 0.85, 0.92), "hearth": False, "time": "day"},
    "props": [{"type": "bed", "x": 0.45, "y": 0.9, "scale": 1.5}],
    "cast": [stan(x=0.5, y=0.88, action="sleep", expression="sleepy", actions=[["w5", "sit"]],
                  expressions=[["w5", "grin"]])],
    "overlays": [level(8, "TODAY")]},
    transition="fade")

sc("n02", "ending", "Global life expectancy today is around seventy-three years. For almost all of history, it was less than half of that.", {
    "background": {"type": "chalkboard"},
    "cast": [stan(x=0.12, y=0.95, action="talk", expression="happy", scale=1.15, color=(0.95, 0.95, 0.92),
                  head_fill=(0.17, 0.27, 0.22))],
    "overlays": [{"type": "bars", "title": "Life expectancy at birth (rough)", "x": 0.36, "y": 0.3,
                  "items": [["Most of history", 30, "grey", "~30 years"], ["Today (world)", 73, "green", "~73 years"]],
                  "max": 100, "bar_h": 90}]},
    claims=[F("Global life expectancy is about 73 years", SRC["who"] + "; " + SRC["unwpp"]),
            F("Historic life expectancy at birth was typically around 30, mainly due to child mortality",
              SRC["hg"], "estimate")])

sc("n03", "ending", "Verdict for level eight: decades. You're living in the safest era in human history, even on a bad day.", {
    "background": PAPER,
    "cast": [stan(x=0.3, action="cheer", expression="grin")],
    "props": [verdict(0.95, "DECADES", 0.7, 0.62)]},
    sfx=[{"name": "sparkle", "at": 1.0}])

sc("n04", "ending", "So, final ranking. The deadliest levels: the Ice Age alone, and the trenches on day one. The safest past era? Surprisingly, the pyramid site.", {
    "background": {"type": "chalkboard"},
    "cast": [stan(x=0.12, y=0.95, action="talk", expression="happy", scale=1.15, color=(0.95, 0.95, 0.92),
                  head_fill=(0.17, 0.27, 0.22))],
    "camera": {"move": "pan_right", "amount": 60, "zoom": 1.04},
    "overlays": [{"type": "bars", "title": "How long you'd last", "x": 0.34, "y": 0.18, "bar_h": 50, "gap": 14,
                  "items": [["Ice Age (alone)", 1, "red", "days"], ["WW1 (day one)", 0.5, "red", "minutes"],
                            ["Vikings", 2, "orange", "weeks"], ["Black Death", 3, "yellow", "coin flip"],
                            ["Pirates", 3.5, "yellow", "1-2 years"], ["Factory", 4.5, "lime", "years"],
                            ["Pyramids", 5, "green", "years"], ["Today", 6, "green", "decades"]], "max": 6.5}]},
    transition="wipe")

sc("n04b", "ending", "And notice the pattern. In almost every era, the biggest killer wasn't war or monsters. It was disease and cold, the boring stuff.", {
    "background": PAPER,
    "cast": [stan(x=0.3, action="think", expression="thinking")],
    "props": [{"type": "germ", "x": 0.6, "y": 0.6, "scale": 1.3}, {"type": "icon", "icon": "x", "x": 0.8, "y": 0.6}]},
    claims=[F("Infectious disease was the leading cause of death through most of history", SRC["hg"])])

sc("n04c", "ending", "So the next time you complain about your commute, remember: you could be dragging a two-ton block in the desert, or eating weevil biscuits on a pirate ship.", {
    "background": {"type": "split", "left": "sky", "right": (0.95, 0.85, 0.65), "left_label": "YOU", "right_label": "THEM"},
    "cast": [stan(x=0.25, action="shrug", expression="smug"),
             cast("worker", outfit="tunic", outfit_color="white", x=0.75, action="pull", expression="tired", facing=-1)]})

sc("n04d", "ending", "Modern life has its problems. But in terms of pure survival, we've never had it better.", {
    "background": PAPER,
    "cast": [stan(x=0.4, action="cheer", expression="grin", scale=1.5)],
    "props": [{"type": "icon", "icon": "sparkle", "x": 0.4, "y": 0.35}]})

sc("n05", "ending", "Now, which level would you choose to live in for a year? Tell me in the comments. My vote is the pyramids, purely for the free beer.", {
    "background": {"type": "desert"},
    "cast": [stan(x=0.4, action="drink", item="mug", expression="laughing", outfit="tunic", outfit_color="white",
                  scale=1.5)]})

sc("n06", "ending", "And if you enjoyed this, subscribe for more stickman history. See you in the next era.", {
    "background": PAPER,
    "cast": [stan(x=0.32, action="wave", expression="grin")],
    "props": [{"type": "board", "x": 0.7, "y": 0.45, "text": "SUBSCRIBE", "color": "red", "text_color": "white",
               "w": 520, "h": 150, "size": 78, "at_word": 5, "loop": "pulse"}]},
    sfx=[{"name": "pop", "at_word": 5}], pause=0.8)

st.save(
    "every-era",
    title="How Long Would You Last in Every Era of History?",
    idea="How long a modern person would survive if dropped into eight eras of history",
    question="Which era would you choose to live in for one year?",
    mood="tense",
    metadata={
        "title": "How Long Would You Last in Every Era of History?",
        "description_intro": (
            "You're pulled out of bed and dropped into the past — no phone, no money, no skills. How long would "
            "you last? Eight levels, from the Ice Age to today: a pyramid building site, a Viking raid, the Black "
            "Death, a pirate ship, a Victorian cotton mill and the trenches of the Somme — each one rated with a "
            "survival verdict.\n\nA stickman history ranking with real facts and sources."),
        "hashtags": ["#history", "#whatif", "#stickman"],
        "tags": ["how long would you last", "every era of history", "could you survive", "history", "ice age",
                 "pyramids", "vikings", "black death", "pirates", "industrial revolution", "ww1", "trenches",
                 "stickman", "stickman animation", "history animated", "time travel", "survival", "history ranking"],
        "pinned_comment": "Which era would you pick to live in for one year? 🤔 I'm going pyramids — free bread AND "
                          "beer. 👇",
        "chapter_moods": ["tense", "somber", "curious", "tense", "calm", "somber", "medieval", "calm", "tense", "calm"],
        "intro_chapter": "The Rules",
        "thumbnail": {
            "visual": {"background": {"type": "trench"},
                       "cast": [{"id": "stan", "outfit": "uniform", "hat": "brodie", "x": 0.72, "y": 0.96,
                                 "scale": 1.8, "facing": -1, "action": "cower", "expression": "scared"}],
                       "props": [{"type": "dial", "x": 0.88, "y": 0.42, "value": 0.08, "label": "", "scale": 1.0,
                                  "enter": "none"}]},
            "t": 1.0, "lines": ["HOW LONG", "WOULD YOU LAST?"], "colors": ["white", "yellow"],
            "badge": "8 ERAS RANKED", "badge_color": "red", "size": 112},
        "thumbnail_alts": [{
            "visual": {"background": {"type": "ice_age"},
                       "props": [{"type": "mammoth", "x": 0.86, "y": 0.9, "scale": 0.75, "enter": "none"}],
                       "cast": [{"id": "stan", "outfit": "tunic", "outfit_color": "sky", "x": 0.6, "y": 0.96,
                                 "scale": 1.8, "action": "shiver", "expression": "scared", "facing": -1}]},
            "t": 1.0, "lines": ["SURVIVE", "EVERY ERA?"], "colors": ["white", "yellow"],
            "badge": "ICE AGE TO TODAY", "badge_color": "teal", "size": 120}],
    },
)
