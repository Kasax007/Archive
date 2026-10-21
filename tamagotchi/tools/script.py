"""Sprechtext und Schnittplan der beiden Tamagotchi-Videos (Video-Inhalt: Englisch).

Pro Absatz ein Eintrag:
  id     Kennung (A1 ... / B1 ...)
  ch     Kapiteltitel (Long-form, erscheint oben zu Beginn des Kapitels), sonst None
  text   gesprochener Text; *Wort* = farbiges Akzentwort in den Untertiteln (hoechstens ein Akzent pro Satzstueck)
  shots  [(Shot, Anker)]: Ordnernamen unter $SP/film/tama/. Anker = Phrase des Absatzes, an der der Shot beginnt
         (None = Absatzanfang). Ein Shot mit '?' am Ende ist optional (nur wenn der Ordner existiert).
         Mehrfach vorkommende Shots werden an anderen Stellen des Materials abgespielt.
  sfx    [(Wort/Phrase, Ton, Lautstaerke)] Zusatzgeraeusche exakt auf einem gesprochenen Wort
  hook   Titel oben im Bild waehrend des ersten Shots (nur Short)
"""

SHORT = [
    dict(id='A1', ch=None, hook='A *DRAGON* IN MINECRAFT?!',
         text="This tiny *dragon* was hiding in a desert pyramid, and now it's my *best friend*!",
         shots=[('hook_petting', None)]),
    dict(id='A2', ch=None,
         text="There are *ten* rare pets hiding in Minecraft's structures, and every one is only there by *chance*.",
         shots=[('lineup_dolly', None)]),
    dict(id='A3', ch=None,
         text="Tame one with a *Tamagotchi Heart*, and it follows you *everywhere*.",
         shots=[('tame_heart', None)], sfx=[('everywhere', 'pet/celebrate1', 0.5)]),
    dict(id='A4', ch=None,
         text="Give it a *chest*, and it carries a *backpack* for you.",
         shots=[('backpack_on', None)]),
    dict(id='A5', ch=None,
         text="Feed it, play with it, and keep it *clean*, just like a real *Tamagotchi*.",
         shots=[('bowl_eat', None), ('laser_chase', 'play with it'), ('bath', 'and keep it')]),
    dict(id='A6', ch=None,
         text="Every pet has a *talent*. This golem sniffs out *diamonds*, and the dragons can actually *fly*!",
         shots=[('ore_glow', None), ('fly_follow', 'and the dragons')]),
    dict(id='A7', ch=None,
         text="And when you're almost dead, your pet brings you a *golden apple*.",
         shots=[('feed_owner', None)]),
    dict(id='A8', ch=None, end=True,
         text="*Tamagotchi*. Free on *CurseForge*!",
         shots=[('endcard', None)]),
]

LONG = [
    dict(id='B1', ch=None,
         text="Minecraft, but you can find, tame and raise your own little *pets*. Let me show you this cute mod.",
         shots=[('lineup_dolly', None)]),
    dict(id='B2', ch='FINDING *PETS*',
         text="Ten rare pets hide in Minecraft's structures. The *Desert Dragon* lives in pyramids, the Jungle Dragon in "
              "jungle temples, and the Tide Dragon at ocean monuments. A *penguin* hides in igloos, and a living "
              "*treasure chest* waits in trial chambers.",
         shots=[('pyramid_wild', None), ('jungle_wild?', 'the Jungle Dragon'), ('monument_wild?', 'and the Tide Dragon'),
                ('igloo_penguin', 'A penguin hides'), ('mimic_chamber', 'and a living')]),
    dict(id='B3', ch='*TAMING*',
         text="Not every structure has one, so every find is *special*. Craft a *Tamagotchi Heart*, give it to the pet, "
              "and it trusts you forever.",
         shots=[('tame_heart', None)], sfx=[('trusts', 'pet/tame1', 0.55)]),
    dict(id='B4', ch='*CARE*',
         text="From now on it needs you. Hunger, fun, energy and hygiene make up its *mood*, and the *Tama Pager* "
              "beeps whenever your pet needs something.",
         shots=[('pet_screen', None)], sfx=[('beeps', 'pager/beep1', 0.5), ('needs something', 'pager/beep2', 0.5)]),
    dict(id='B5', ch=None,
         text="Luckily, your pets take care of themselves when you build them a little *home*. They eat from the food "
              "bowl, splash around in the bath, bounce on the mushroom, run in the *wheel*, and sleep in their beds.",
         shots=[('bowl_eat', None), ('bowl_eat', 'They eat from'), ('bath', 'splash around'), ('bounce', 'bounce on'),
                ('wheel', 'run in'), ('bed_sleep', 'and sleep')]),
    dict(id='B6', ch='*PLAY*',
         text="You can play with them too. Pets chase the *laser pointer*, and when you pet them, they show you their "
              "*heart eyes*.",
         shots=[('laser_chase', None), ('petting_closeups', 'and when you pet')]),
    dict(id='B7', ch='THE *BACKPACK*',
         text="Give your pet a chest and it carries a *backpack* with twenty-seven slots. Put *golden apples* inside, "
              "and when your health gets low, your pet brings you one.",
         shots=[('backpack_on', None), ('feed_owner', 'and when your health')]),
    dict(id='B8', ch='*TALENTS*',
         text="Every pet has its own *talent*. The Desert Dragon roasts your food, the Pebble Golem sniffs out *ores*, "
              "the Frost Penguin freezes water under your feet, and the Ember Pup swims through *lava*.",
         shots=[('roast', None), ('ore_glow', 'the Pebble Golem'), ('frost_steps', 'the Frost Penguin'),
                ('lava_swim', 'and the Ember Pup')]),
    dict(id='B9', ch='*ADVENTURES*',
         text="The dragons can even *fly* after you. In a fight, your pet has your back, and it never dies. It just "
              "curls up into an *egg*, and you can wake it up again.",
         shots=[('fly_follow', None), ('fight', 'In a fight'), ('faint_egg', 'It just curls')]),
    dict(id='B10', ch=None,
         text="They *dance* to music, warm up at campfires, and hide from thunderstorms.",
         shots=[('dance', None), ('campfire_warm', 'warm up')]),
    dict(id='B11', ch='THE *TAMACON*',
         text="And if you ever forget something, just craft the *Tamacon*, your little guide to everything.",
         shots=[('tamacon_book', None)]),
    dict(id='B12', ch=None, end=True,
         text="*Tamagotchi* is free on CurseForge. Link in the *description*!",
         shots=[('endcard', None)]),
]

SCRIPTS = dict(short=SHORT, long=LONG)

# Wie der Sprecher einzelne Woerter sagt (Kokoro/misaki: [Wort](/IPA/); nur die Aussprache, Untertitel behalten den Skripttext).
# Die Betonung wurde mit Whisper geprueft (Tamacon/Tama Pager wurden sonst als "tarmac on" / "time I'll page" verstanden).
SAY = {'Tama': '[Tama](/tˈæmə/)', 'Pager': '[Pager](/pˈeɪʤɚ/)', 'Tamagotchi': '[Tamagotchi](/tˈɑməɡˈɑʧi/)',
       'Tamacon': '[Tama](/tˈɑmɑ/)[con](/kˌɑn/)', 'CurseForge': 'Curse Forge'}
# Fuer die Whisper-Pruefung: gehoerte Schreibweisen, die als Treffer fuer das Skriptwort zaehlen
HEARD = {'tamagotchi': ['tamagotchi', 'tamagochi', 'tamagotchy', 'tamagotche', 'tamagotchis', 'tamagotcha', 'tamagachi', 'tomagotchi',
                        'tamagotsi', 'tamagoci', 'tamagotshi', 'tamagotchee'],
         'tamacon': ['tamacon', 'tamakon', 'tamakan', 'tamacan', 'tamakhan', 'tamacom', 'tamikon', 'tomacon', 'tamacan', 'tamaconn'],
         'tama': ['tama', 'tamah', 'tomah', 'tamma'],
         'heart': ['heart', 'hard', 'hart'],
         'pager': ['pager', 'pagers', 'pageyour', 'pageer', 'pagerr'],
         'curseforge': ['curseforge', 'curseforged', 'cursefordge']}

POST = dict(
    short=dict(
        title="This tiny dragon was hiding in a desert pyramid... #minecraft #minecraftmods",
        body="""Ten rare pets hide in Minecraft's structures: dragons, a penguin, a living treasure chest and more.
Tame them, feed them, play with them, give them a backpack. Every pet has its own talent.

Tamagotchi is a free Minecraft mod on CurseForge (link in bio / description).
""",
        tags="#minecraft #minecraftmods #tamagotchi #minecraftpets #cutepets #moddedminecraft #curseforge #gaming #fyp"),
    long=dict(
        title="Minecraft, but you can tame and raise your own pets (Tamagotchi mod showcase)",
        body="""Ten rare pets hide in Minecraft's structures: the Desert Dragon, the Jungle Dragon, the Tide Dragon, a Frost
Penguin, the Ember Pup, a Pebble Golem and more. Tame them with a Tamagotchi Heart, keep them fed, clean and happy,
play with them, give them a backpack and take them on adventures. Every pet has its own talent - and they never die,
they just curl up into an egg.

Chapters: Finding pets - Taming - Care - Play - Backpack - Talents - Adventures - The Tamacon
""",
        tags="#minecraft #minecraftmods #tamagotchi #minecraftpets #cutepets #moddedminecraft #curseforge #gaming"),
)
