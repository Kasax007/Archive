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

# Review-Video (fuer den Nutzer zum Pruefen, nicht zum Posten): alle Features mit den echten Spielgeraeuschen.
# pause = zusaetzliche Sekunden ohne Stimme nach dem Absatz, damit man die Geraeusche hoert.
REVIEW = [
    dict(id='R1', ch=None,
         text="This is *Tamagotchi*: ten rare pets to find, tame and take care of. Here is every feature, with the real "
              "*game sounds*.",
         shots=[('lineup_dolly', None)]),
    dict(id='R2', ch='FINDING *PETS*',
         text="The pets hide in structures: a *dragon* in the desert pyramid, a penguin in an igloo, and a living "
              "*treasure chest* in trial chambers.",
         shots=[('pyramid_wild', None), ('igloo_penguin', 'a penguin'), ('mimic_chamber', 'and a living')], pause=0.8),
    dict(id='R3', ch='*TAMING*',
         text="Give a wild pet a *Tamagotchi Heart*, and it trusts you.",
         shots=[('tame_heart', None)], pause=1.6),
    dict(id='R4', ch=None,
         text="Pet it with an empty hand, and it shows you *heart eyes*.",
         shots=[('petting_closeups', None), ('hook_petting', 'and it shows')], pause=1.2),
    dict(id='R5', ch='*CARE*',
         text="Every pet has four needs: hunger, fun, energy and hygiene. The *Tama Pager* tells it to stay or follow, "
              "and it beeps when a pet needs you.",
         shots=[('pet_screen', None), ('pager_sit', 'The Tama Pager')], pause=0.6),
    dict(id='R6', ch=None,
         text="Pets eat from the *food bowl*, and they splash around in the *bath*.",
         shots=[('bowl_eat', None), ('bath', 'and they splash')], pause=1.0),
    dict(id='R6b', ch=None,
         text="They snore in their beds, and they love a good *brushing*.",
         shots=[('bed_sleep', None), ('brush', 'and they love')], pause=1.4),
    dict(id='R7', ch='*PLAY*',
         text="They chase the *laser pointer*, jump at the feather wand, and fetch the *squeaky ball*.",
         shots=[('laser_chase', None), ('feather_wand', 'jump at'), ('fetch_ball', 'and fetch')], pause=3.5),
    dict(id='R8', ch=None,
         text="They bounce on the *mushroom*, run in the running wheel, and sharpen their claws on the scratching post.",
         shots=[('bounce', None), ('wheel', 'run in'), ('scratch_post', 'and sharpen')], pause=1.4),
    dict(id='R9', ch='THE *BACKPACK*',
         text="A chest becomes a *backpack*. Put golden apples inside, and when you are hurt, your pet brings you one.",
         shots=[('backpack_on', None), ('feed_owner', 'Put golden')], pause=1.4),
    dict(id='R10', ch='*TALENTS*',
         text="Every pet has a *talent*: the Desert Dragon roasts food, the Pebble Golem finds ores, the penguin freezes "
              "water, and the Ember Pup swims in *lava*.",
         shots=[('roast', None), ('ore_glow', 'the Pebble Golem'), ('frost_steps', 'the penguin'), ('lava_swim', 'and the Ember')],
         pause=0.8),
    dict(id='R11', ch='*ADVENTURES*',
         text="Dragons *fly* after you, and in a fight, your pets have your *back*.",
         shots=[('fly_follow', None), ('fight', 'and in a fight')], pause=1.0),
    dict(id='R11b', ch=None,
         text="And they never die. They faint into an *egg* instead.",
         shots=[('faint_egg', None)], pause=1.0),
    dict(id='R12', ch='NEW: *PLUSHIES*',
         text="New in this update: *plushies* of all ten pets. Squeeze them!",
         shots=[('plush_shelf', None), ('plush_squeeze', 'Squeeze')], pause=1.6),
    dict(id='R13', ch=None,
         text="Lonely pets *cuddle* them, and a pet sleeps better next to a plush of its own kind.",
         shots=[('plush_cuddle', None), ('plush_sleep', 'and a pet')], pause=1.0),
    dict(id='R14', ch='NEW: *GADGETS*',
         text="Put a Tama Egg into the *incubator*, and thirty seconds later your pet hatches, fully healed.",
         shots=[('incubator_in', None), ('incubator_hatch', 'and thirty')], pause=2.2),
    dict(id='R15', ch=None,
         text="Press a button, and the *treat dispenser* shoots a treat to your hungriest pet.",
         shots=[('treat_dispenser', None)], pause=2.2),
    dict(id='R16', ch=None,
         text="Bored pets open the *toy box* and play with the toys inside.",
         shots=[('toy_box_open', None), ('toy_box_play', 'and play')], pause=1.8),
    dict(id='R17', ch=None,
         text="And the *pet flap* lets your pets through, but nobody else.",
         shots=[('pet_flap', None)], pause=1.8),
    dict(id='R18', ch='NEW: *DECORATION*',
         text="The *portrait* paints your nearest pet, with its name on the plate. Click again for the next pet, or use a dye.",
         shots=[('portrait_paint', None)], pause=1.4),
    dict(id='R19', ch=None,
         text="The *egg lamp* is a little night light, and beds, baskets, lamps and portraits take *any dye*.",
         shots=[('egg_lamp', None), ('dye_bed', 'and beds')], pause=1.4),
    dict(id='R20', ch='LITTLE *MOMENTS*',
         text="Pets *dance* to music and warm up at the campfire.",
         shots=[('dance', None), ('campfire_warm', 'and warm')], pause=1.2),
    dict(id='R21', ch='THE *TAMACON*',
         text="And if you forget something, just read the *Tamacon*, your little guide to everything.",
         shots=[('tamacon_book', None)], pause=0.8),
    dict(id='R22', ch=None, end=True,
         text="That's *Tamagotchi*. Thanks for watching!",
         shots=[('endcard', None)]),
]

SCRIPTS = dict(short=SHORT, long=LONG, review=REVIEW)

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
    review=dict(
        title="Tamagotchi - every feature with the real game sounds (review cut, not for posting)",
        body="""Review cut for checking the mod before release: every feature of Tamagotchi 1.1 with the sounds the game
really plays (recorded while filming), the new plushies, incubator, treat dispenser, toy box, pet flap, portrait,
egg lamp and dyes included.
""",
        tags=""),
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
