"""Sprechtext und Schnittplan des Dreamcraft-26.3-TikToks (Video-Inhalt: Englisch).

Pro Absatz ein Eintrag (Format wie tamagotchi/tools/script.py):
  id     Kennung
  text   gesprochener Text; *Wort* = farbiges Akzentwort in den Untertiteln (hoechstens ein Akzent pro Satzstueck)
  shots  [(Shot, Anker)]: Ordnernamen unter $SP/film/. Anker = Phrase, an der der Shot beginnt (None = Absatzanfang).
  sfx    [(Wort/Phrase, Ton, Lautstaerke)] Zusatzgeraeusche exakt auf einem gesprochenen Wort
  hook   Titel oben im Bild waehrend des ersten Shots
  capy   Hoehe der Untertitel dieses Absatzes (sonst unteres Drittel)
"""

SHORT = [
    dict(id='A1', hook='MINECRAFT *26.3* MODPACK',
         text="This is *Dreamcraft*, over *two hundred and fifty* mods, and it already runs on the *newest* Minecraft!",
         shots=[('castle', None), ('mutant', 'over two hundred'), ('nether', 'and it already runs')]),
    dict(id='A2', capy=330,
         text="It starts with a brand new *menu*, and a *story* with over one hundred and sixty quests guides you through every mod.",
         shots=[('menu_land', None), ('questbook', 'and a story'), ('kitchen', 'guides you')]),
    dict(id='A3',
         text="You explore giant *castles*, cozy *villages* and whole new worlds.",
         shots=[('castle', None), ('village', 'cozy villages')]),
    dict(id='A4',
         text="You become a *fire wizard*, and you fight huge *mutant* monsters.",
         shots=[('magic', None), ('mutant', 'and you fight')], sfx=[('mutant', 'mob/ravager/roar1', 0.35)]),
    dict(id='A5',
         text="You cook real *meals*, and you build *machines* that do the work for you.",
         shots=[('kitchen', None), ('tech', 'and you build')]),
    dict(id='A6',
         text="You even survive on a *raft* in an endless ocean, while a *shark* circles below you!",
         shots=[('raft', None), ('shark', 'while a shark')]),
    dict(id='A7',
         text="And the *Nether* and the *End* look completely new.",
         shots=[('nether', None), ('end', 'and the End')]),
    dict(id='A8', end=True,
         text="*Dreamcraft*. Free on *CurseForge*!",
         shots=[('endcard', None)]),
]

SCRIPTS = dict(short=SHORT)

# Aussprache (nur fuer den Sprecher; die Untertitel behalten den Skripttext)
SAY = {'CurseForge': 'Curse Forge', 'Dreamcraft': 'Dream craft'}
# Fuer die Whisper-Pruefung: gehoerte Schreibweisen, die als Treffer fuer das Skriptwort zaehlen
HEARD = {'dreamcraft': ['dreamcraft', 'dreamcrafts', 'dreamcraftt'],
         'curseforge': ['curseforge', 'curseforged', 'cursefordge'],
         'nether': ['nether', 'neither'],
         'mutant': ['mutant', 'mutants']}
# Zahlen, die Whisper als Ziffern schreibt
NUMS = {'250': 'two hundred and fifty', '160': 'one hundred and sixty', '26.3': 'twenty six point three'}

POST = dict(
    short=dict(
        title="This Minecraft modpack has over 250 mods... #minecraft #minecraftmods #modpack",
        body="""Dreamcraft is back on the newest Minecraft (26.3, Fabric): over 250 mods, a quest story through every mod,
castles, villages and new biomes, fire magic, mutant monsters, real cooking, tech machines, a whole raft ocean
with a shark - and the Nether and the End look completely new. Server pack included.

Dreamcraft is a free modpack on CurseForge (link in bio / description).
""",
        tags="#minecraft #minecraftmods #modpack #moddedminecraft #dreamcraft #curseforge #minecraftbuilding #gaming #fyp"),
)
