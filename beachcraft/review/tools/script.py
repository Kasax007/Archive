"""Sprechtext und Schnittplan des Beach-Craft-Reviews (Video-Inhalt: Englisch). Zweck: der Nutzer sieht jedes Feature des
Mods einmal funktionieren und erklaert (Format wie tamagotchi/tools/script.py, Review-Schnitt).

Pro Absatz:
  id     Kennung
  ch     Kapiteltitel (oben, zu Beginn des Kapitels), sonst None
  text   gesprochener Text; *Wort* = farbiges Akzentwort in den Untertiteln
  shots  [(Shot, Anker)]: Ordner unter $SP/film/bc/. Anker = Phrase, an der der Shot beginnt (None = Absatzanfang).
  pause  Sekunden Pause nach dem Absatz (Raum fuer die echten Spielgeraeusche)
"""

REVIEW = [
    dict(id='R1', ch=None,
         text="This is *Beach Craft* for Minecraft twenty six point three. In this review I show you every feature of the mod, "
              "so you can see what it does, and that it works.",
         shots=[('bc_raft_tour', None)], pause=0.6),
    dict(id='R2', ch='GETTING *THERE*',
         text="Dark *driftwood* stumps stand on sandy beaches, and a driftwood sapling grows a new one with bone meal. "
              "Their logs build the portal.",
         shots=[('bc_beach', None)], pause=0.6),
    dict(id='R3', ch=None,
         text="Shipwreck treasure, buried treasure and ocean ruins hide *ancient broken rings*, and shipwrecks also hold ancient crystals.",
         shots=[('bc_loot', None)], pause=0.4),
    dict(id='R4', ch=None,
         text="A furnace or a blast furnace melts each ring into *ancient energy*.",
         shots=[('bc_energy', None)], pause=0.6),
    dict(id='R5', ch=None,
         text="Four driftwood logs around one ancient energy make four *portal frames*. Energy, crystal and a stick make the *energy staff*.",
         shots=[('bc_craft_portal', None)], pause=0.4),
    dict(id='R6', ch=None,
         text="The staff tells you when you click the wrong block, or when the frame is not finished. "
              "Once the frame is complete, one click *lights the portal*.",
         shots=[('bc_portal_light', None)], pause=1.0),
    dict(id='R7', ch=None,
         text="Step inside, and you arrive on a small driftwood platform *high above the endless sea*, with a portal back home.",
         shots=[('bc_portal_trip', None), ('bc_portal_arrive', 'and you arrive')], pause=0.8),
    dict(id='R8', ch=None,
         text="The *raft teleporter* skips the portal. It drops you on a stone block, right on the water.",
         shots=[('bc_teleporter', None), ('bc_teleporter_arrive', 'It drops you')], pause=0.8),
    dict(id='R9', ch='THE ENDLESS *SEA*',
         text="The raft ocean has sandy islands with *palm trees*. A palm sapling grows with bone meal, "
              "and you can pick *coconuts* right off the leaves.",
         shots=[('bc_island', None)], pause=0.8),
    dict(id='R10', ch=None,
         text="The current carries *debris* past you from the west: plastic, scrap metal, planks, palm leaves, and now and then some lost loot.",
         shots=[('bc_debris', None)], pause=0.6),
    dict(id='R11', ch=None,
         text="Hold right click with the *plastic hook*, and the floating items fly straight to you.",
         shots=[('bc_hook', None)], pause=0.8),
    dict(id='R12', ch=None,
         text="An *item catcher* in the water collects debris on its own. "
              "With a *net* inside, it also fishes unrefined ocean garbage out of the sea.",
         shots=[('bc_catcher', None), ('bc_catcher_net', 'With a net')], pause=0.6),
    dict(id='R13', ch=None,
         text="Smelt the garbage into a *trash cube*. Every cube you open pops out one to three random items.",
         shots=[('bc_trash', None), ('bc_trash_open', 'Every cube')], pause=1.2),
    dict(id='R14', ch='*SURVIVE*',
         text="Two palm leaves make *rope*. Four rope make a rope coil, and rope on white wool makes *sail canvas*.",
         shots=[('bc_rope', None)], pause=0.6),
    dict(id='R15', ch=None,
         text="*Rope ladders* can be climbed like normal ladders.",
         shots=[('bc_ladder', None)], pause=0.8),
    dict(id='R16', ch=None,
         text="The *water purifier* burns coal or wood, and turns a water bucket into three bottles of *fresh water*.",
         shots=[('bc_purifier_out', None), ('bc_purifier', 'and turns')], pause=0.8),
    dict(id='R17', ch=None,
         text="Fresh water fills you up a little, *coconut milk* heals you, and a *pina colada* makes you fast "
              "for two and a half minutes. You even get the bowl back.",
         shots=[('bc_drinks', None)], pause=0.8),
    dict(id='R18', ch=None,
         text="The *simple grill* cooks two foods at once, faster than a campfire.",
         shots=[('bc_grill', None), ('bc_grill_done', 'faster than')], pause=1.0),
    dict(id='R19', ch=None,
         text="Crops on a *crop plot* grow about half again as fast as on wet farmland. "
              "The plot never dries out, and you *cannot trample* it.",
         shots=[('bc_crops', None), ('bc_trample', 'The plot never')], pause=0.8),
    dict(id='R20', ch=None,
         text="A *scarecrow* keeps hostile mobs from spawning within twenty four blocks, and protects farmland within eight. "
              "Its head now always faces you.",
         shots=[('bc_scarecrow', None)], pause=0.6),
    dict(id='R21', ch='BRUCE THE *SHARK*',
         text="*Bruce the shark* lives in the raft ocean.",
         shots=[('bc_shark', None)], pause=0.6),
    dict(id='R22', ch=None,
         text="As long as you stay on your raft, he leaves you alone. Jump into the water, and *he attacks*.",
         shots=[('bc_shark_attack', None)], pause=1.0),
    dict(id='R23', ch=None,
         text="Beat him for *shark meat* and *shark teeth*. Three teeth and three planks make a shark jaw trophy for your wall.",
         shots=[('bc_shark_drops', None), ('bc_trophy', 'Three teeth')], pause=0.6),
    dict(id='R24', ch='*EXPLORE*',
         text="The *receiver* shows the direction and distance to the nearest floating driftwood.",
         shots=[('bc_receiver', None)], pause=0.8),
    dict(id='R25', ch=None,
         text="In a boat, the *paddle* gives you a strong push forward.",
         shots=[('bc_paddle', None)], pause=1.0),
    dict(id='R26', ch=None,
         text="*Titanium* ore hides deep under the sea floor, and needs a diamond pickaxe. Smelt the raw titanium into ingots.",
         shots=[('bc_titanium', None), ('bc_titanium_smelt', 'Smelt the raw')], pause=0.6),
    dict(id='R27', ch=None,
         text="A full set of *titanium armor* gives you water breathing, dolphin's grace and conduit power.",
         shots=[('bc_armor', None)], pause=0.8),
    dict(id='R28', ch=None,
         text="The *metal detector* tells you how deep the next titanium ore below you is.",
         shots=[('bc_detector', None)], pause=0.6),
    dict(id='R29', ch=None,
         text="And three *music discs* hide in shipwreck treasure.",
         shots=[('bc_disc', None)], pause=1.4),
    dict(id='R30', ch='*POWER*',
         text="Makeshift *solar panels* charge the makeshift *battery*, and cables carry the energy to machines, even to Tech Reborn.",
         shots=[('bc_power', None), ('bc_battery', 'and cables')], pause=0.6),
    dict(id='R31', ch=None,
         text="The *quarry* digs out an eleven by eleven area, block by block, into the chest on top.",
         shots=[('bc_quarry', None)], pause=0.8),
    dict(id='R32', ch=None,
         text="The *brick furnace* smelts faster than a normal one, and the *titanium furnace* is extremely fast and even doubles every result.",
         shots=[('bc_furnaces', None)], pause=0.6),
    dict(id='R33', ch='*BUILD*',
         text="For building there are *palm* and *driftwood* wood, palm thatch, sail canvas, scrap metal and plastic blocks, "
              "a ship wheel, a flag and coconut lanterns.",
         shots=[('bc_deco', None)], pause=0.6),
    dict(id='R34', ch='FIXED IN *2.0.1*',
         text="While making this review, I found and fixed more than twenty bugs: sharks that never spawned, the sail canvas recipe, "
              "the scarecrow's head, the item catcher, wood that did not burn, and more. The full list is in the changelog.",
         shots=[('bc_raft_tour', None)], pause=0.6),
    dict(id='R35', ch=None, end=True,
         text="That's *Beach Craft*. Free on *CurseForge*!",
         shots=[('endcard', None)]),
]

SCRIPTS = dict(review=REVIEW)

# Aussprache (nur fuer den Sprecher)
SAY = {'CurseForge': 'Curse Forge', 'pina colada': 'peena colada', 'Tech Reborn': 'Tech Reborn'}
HEARD = {'curseforge': ['curseforge', 'curseforged'],
         'beach': ['beach', 'beech', 'beechcraft', 'beachcraft'],
         'craft': ['craft', 'beechcraft', 'beachcraft'],
         'pina': ['pina', 'pena', 'peena', 'pinna', 'piña'],
         'colada': ['colada', 'collada', 'coladas'],
         'bruce': ['bruce', 'bruces'],
         'reborn': ['reborn'],
         'dolphins': ['dolphins', 'dolphin'],
         'scarecrows': ['scarecrows', 'scarecrow']}
NUMS = {'26.3': 'twenty six point three', '24': 'twenty four', '11 by 11': 'eleven by eleven', '2.0.1': 'two point oh point one',
        '20': 'twenty', '8': 'eight', '3': 'three'}

POST = dict(
    review=dict(
        title="Beach Craft 2.0 for Minecraft 26.3 - every feature in one review",
        body="""A review of everything in Beach Craft (the Raft mod) for Minecraft 26.3: the driftwood portal, the raft ocean,
debris, the plastic hook, the item catcher, trash cubes, the water purifier, the grill, crop plots, the scarecrow,
Bruce the shark, the receiver, the paddle, titanium, the metal detector, solar power, the quarry, the furnaces and
all the decoration - recorded with the real game sounds.
""",
        tags="#minecraft #minecraftmods #raft #beachcraft #moddedminecraft #curseforge"),
)
