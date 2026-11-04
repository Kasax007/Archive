"""Sprechtext und Schnittplan der Beach-Craft-3.0-Doku (Video-Inhalt: Englisch). Ruhiges, langsames Format: jede Welt,
jede Struktur samt Kisten-Loot, jede Kreatur, jeder Block und jedes Item mit seiner Funktion, am Ende der Weg eines
Spielers durch die Story bis zum Leviathan.

Pro Absatz:
  id     Kennung
  ch     Kapiteltitel (oben, zu Beginn des Kapitels), sonst None
  text   gesprochener Text; *Wort* = farbiges Akzentwort in den Untertiteln
  shots  [(Shot, Anker)]: Name unter $SP/doc3/shots (Standbild .jpg oder Clip-Ordner). Anker = Phrase, an der der Shot
         beginnt (None = Absatzanfang). Ein Shot-Name mit '?' am Ende ist optional.
  pause  Sekunden Pause nach dem Absatz (Raum fuer Bild und echte Spielgeraeusche)
  music  Musikstueck ab diesem Absatz (siehe MUSIC in doc.py)
"""

DOC = [
    # ------------------------------------------------------------------ opening
    dict(id='O1', ch=None, music='manatees',
         text="Far beyond the overworld lies the *Endless Sea*. Warm islands, bright reefs, a drowned city, "
              "and a trench so deep that the sunlight never reaches its floor.",
         shots=[('o_aerial_pan', None), ('p_solace_top2', 'a drowned city'), ('c_angler_dark', 'so deep')], pause=1.0),
    dict(id='O2', ch=None,
         text="This is *Beach Craft three point oh*, Tides of the Deep, for Minecraft twenty six point three. "
              "In this film we take our time. We visit every biome, every place and every creature, "
              "we look at the blocks and items and how they work, and at the end we follow the whole story, "
              "the way a player would.",
         shots=[('f_raft_sail', None), ('b_kelp_under_a', 'every biome'), ('i_tab_voyage', 'we look at'), ('s_stranded', 'at the end')], pause=1.2),

    # ------------------------------------------------------------------ the way in
    dict(id='W1', ch='THE WAY *IN*',
         text="The journey starts in the overworld. On sandy beaches stand short, dark stumps of *driftwood*.",
         shots=[('w_beach', None)], pause=0.6),
    dict(id='W2', ch=None,
         text="Four driftwood logs around one ancient energy make four portal frames. "
              "The energy comes from ancient broken rings, which hide in shipwreck treasure and ocean ruins.",
         shots=[('w_beach2', None), ('i_raft_1', 'The energy comes')], pause=0.6),
    dict(id='W3', ch=None,
         text="The frame is built like a nether portal, and the *energy staff* lights it.",
         shots=[('w_light', None)], pause=1.0),
    dict(id='W4', ch=None,
         text="Step through, and you arrive on a driftwood platform *high above the waves*, with a portal back home.",
         shots=[('w_trip', None), ('w_arrive', 'high above')], pause=1.2),

    # ------------------------------------------------------------------ the world
    dict(id='B0', ch='THE *WORLD*',
         text="The Endless Sea is an *archipelago*: open water, islands, reefs and deep trenches, "
              "spread over twelve biomes.",
         shots=[('o_aerial', None), ('o_islands', 'islands, reefs')], pause=0.8),
    dict(id='B1', ch=None,
         text="The *Endless Sea* itself is deep blue, open water. Kelp and seagrass grow on the floor, "
              "and bubble vents send columns of air up to the surface.",
         shots=[('b_ocean_top', None), ('b_ocean_under', 'Kelp and seagrass')], pause=0.8),
    dict(id='B2', ch=None,
         text="In the *kelp forest*, the kelp grows very tall, and patches of glow kelp light the green water. "
              "Barnacles cover the rocks.",
         shots=[('b_kelp_under_b', None)], pause=0.8),
    dict(id='B3', ch=None,
         text="The *coral shallows* are warm and clear. Between the reefs sit sea anemones, giant clams, starfish "
              "and spiny sea urchins, and pebbles of sea glass lie in the sand.",
         shots=[('b_shallows_under_a', None), ('b_shallows_under_b', 'Between the reefs'), ('b_shells', 'and pebbles')], pause=0.8),
    dict(id='B4', ch=None,
         text="The *glowing lagoon* is rare and dim. Glowing anemones, tube worms and glow kelp fill it with soft light.",
         shots=[('b_lagoon_top', None), ('b_lagoon_under', 'Glowing anemones')], pause=0.8),
    dict(id='B5', ch=None,
         text="The *drowned shelf* is a flat, murky floor covered in concrete rubble: the ground of a city "
              "that the sea swallowed.",
         shots=[('b_shelf_under', None)], pause=0.8),
    dict(id='B6', ch=None,
         text="The *abyssal trench* is the deepest water of all. Down there it is almost black, and only tube worms "
              "and glowing anemones light the basalt.",
         shots=[('b_trench_floor', None)], pause=0.8),
    dict(id='B7', ch=None,
         text="The *wreck graveyard* is foggy, grey water, full of sunken ships.",
         shots=[('b_graveyard2', None), ('b_graveyard', 'full of sunken')], pause=0.8),
    dict(id='B8', ch=None,
         text="In the *frost floes*, icebergs and ice floes drift on cold, clear water.",
         shots=[('b_frost_a', None), ('b_frost_floe', 'drift on')], pause=0.8),
    dict(id='B9', ch=None,
         text="The *palm isles* have sandy beaches with shell sand, palm trees, beach grass and tall sea oats. "
              "Hibiscus and bird of paradise flowers grow between them, and seashells and sea glass wash up on the shore.",
         shots=[('b_palm_a', None), ('b_palm_close', 'Hibiscus')], pause=0.8),
    dict(id='B10', ch=None,
         text="*Jungle isles* are warm and wet, with jungle trees, bamboo, tropical ferns and wild pineapple bushes.",
         shots=[('b_jungle', None), ('b_jungle2', 'tropical ferns')], pause=0.8),
    dict(id='B11', ch=None,
         text="*Mangrove isles* are low and muddy, with tangled roots and lily pads.",
         shots=[('i_nature_1', None)], pause=0.8),
    dict(id='B12', ch=None,
         text="And the *volcanic isles* are dark and rough: black sand, volcanic ash, pumice and basalt columns.",
         shots=[('b_volcano_a', None), ('b_volcano_b', 'black sand')], pause=1.0),
    dict(id='B13', ch=None,
         text="Some of these natural blocks do something. A *giant clam* opens and closes, and an open clam "
              "gives you a pearl. A new one grows in time.",
         shots=[('b_clam', None)], pause=1.2),
    dict(id='B14', ch=None,
         text="A *sea urchin* hurts when you touch it, and drops spines. A wild *pineapple bush* is ripe when its fruit "
              "turns golden. And a *bubble vent* makes a bubble column, where divers can catch their breath.",
         shots=[('b_reef_close', None), ('i_nature_2', 'A wild')], pause=1.2),

    # ------------------------------------------------------------------ places
    dict(id='P0', ch='THE *PLACES*', music='infinite',
         text="The sea is full of places to explore: seven places of the story, and twelve smaller ones. "
              "Almost all of them have chests, each with its own loot.",
         shots=[('p_rig_b', None), ('p_galleon_treasure', 'Almost all')], pause=1.6),
    dict(id='P1', ch=None,
         text="The *old lighthouse* stands on a rocky base. A spiral stair leads up to the lantern room with its great lens, "
              "and next to it are the keeper's cottage and a small dock with buoys.",
         shots=[('p_lighthouse_d', None), ('p_lighthouse_c', 'A spiral stair'), ('p_lighthouse_storage', 'and next to it')], pause=1.8),
    dict(id='P2', ch=None,
         text="*Saltmere* is an abandoned fishing village on stilts above the reef, with huts, rope bridges, "
              "a little market and a shrine.",
         shots=[('p_saltmere_c', None), ('p_saltmere_in_a', 'with huts'), ('p_saltmere_market', 'and a shrine')], pause=1.8),
    dict(id='P3', ch=None,
         text="*Helix Research Station* rests on the sea floor: glass domes and tunnels, an airlock, labs with research "
              "terminals, aquariums, and a flooded wing.",
         shots=[('p_helix_out', None), ('p_helix_in', 'an airlock'), ('p_helix_storage', 'and a flooded wing')], pause=1.8),
    dict(id='P4', ch=None,
         text="*Port Solace* is the drowned city. Asphalt streets with wrecked cars, a plaza with a statue, and skyscrapers, "
              "some so tall that their broken tops reach above the waves. In the middle stands the City Hall tower.",
         shots=[('p_solace_tower', None), ('p_solace_top', 'some so tall')], pause=0.8),
    dict(id='P5', ch=None,
         text="The *Ashen Forge* is a temple of the Tidewardens, built into the slope of a volcano, "
              "with channels of lava, a giant forge, and a vault behind a bridge over the fire.",
         shots=[('p_forge_out2', None), ('p_forge_out', 'with channels'), ('p_forge_in', 'and a vault')], pause=0.8),
    dict(id='P6', ch=None,
         text="The *Coral Temple* rises from the reef, overgrown and half flooded, with a courtyard, colonnades, "
              "statues and an inner sanctum.",
         shots=[('p_temple_a', None), ('p_temple_in', 'with a courtyard'), ('p_temple_chest', 'and an inner')], pause=1.8),
    dict(id='P7', ch=None,
         text="And deep in the trench waits the *Abyssal Sanctum*. Its walls cannot be broken, and only one key "
              "opens its seal.",
         shots=[('p_sanctum_b', None), ('p_sanctum_seal', 'Its walls')], pause=1.0),
    dict(id='P8', ch=None,
         text="A pirate *galleon* lies tilted on the floor, with broken masts, cannons, a captain's cabin "
              "and a cargo hold. Its chests hold gold coins, cannonballs and cutlasses, and sometimes a treasure chart.",
         shots=[('p_galleon_a', None), ('p_galleon_chest', 'Its chests')], pause=2.0),
    dict(id='P9', ch=None,
         text="A rusty *cargo ship* broke in two, and spilled its shipping containers across the floor.",
         shots=[('p_cargo_a', None), ('p_cargo_chest', 'across the floor')], pause=2.0),
    dict(id='P10', ch=None,
         text="Small *fishing boats* sank with their nets and crates.",
         shots=[('p_fishing_r0', None), ('p_fishing_barrel', 'and crates')], pause=2.0),
    dict(id='P11', ch=None,
         text="The pirate Saltjaw hid his *cove* inside a rocky island: a sea entrance, a dock with a ship, "
              "and a treasure room full of gold.",
         shots=[('p_cove_a', None), ('p_cove_ship', 'a sea entrance'), ('p_cove_loot', 'and a treasure')], pause=2.0),
    dict(id='P12', ch=None,
         text="The *rusted rig* stands on steel legs high above the open sea, with cranes, containers, a helipad, "
              "a radio mast and a wind turbine.",
         shots=[('p_rig_a', None), ('p_rig_deck', 'with cranes'), ('p_rig_chest', 'a radio mast')], pause=2.0),
    dict(id='P13', ch=None,
         text="Crashed *planes* rest on the sea floor, an airliner and a seaplane.",
         shots=[('p_plane_b', None), ('p_plane_crate', 'an airliner')], pause=2.0),
    dict(id='P14', ch=None,
         text="Small Tidewarden *ruins* lie scattered on the reefs: columns, arches and broken statues.",
         shots=[('p_ruins_a', None), ('p_ruins_chest', 'columns')], pause=2.0),
    dict(id='P15', ch=None,
         text="On palm isles you find tiny *castaway camps*, with a shelter, a campfire and an SOS in the sand.",
         shots=[('p_camp_a', None), ('p_camp_loot', 'with a shelter')], pause=2.0),
    dict(id='P16', ch=None,
         text="*Abandoned rafts* drift on the open sea, with a sail, a chest and a little farm.",
         shots=[('p_raft_b', None), ('p_raft_chest', 'with a sail')], pause=2.0),
    dict(id='P17', ch=None,
         text="In the frost floes, a research hut sits on the ice: the *iceberg outpost*.",
         shots=[('p_iceberg_b', None), ('p_iceberg_chest', 'the iceberg outpost')], pause=2.0),
    dict(id='P18', ch=None,
         text="*Beach shacks* are little bars, with deck chairs, umbrellas and tiki torches.",
         shots=[('p_shack_b', None), ('p_shack_crate', 'and tiki torches')], pause=2.0),
    dict(id='P19', ch=None,
         text="And a *buoy field* marks a channel, with a supply crate chained between the buoys.",
         shots=[('p_buoy_a', None), ('p_buoy_crate', 'chained between')], pause=2.2),

    # ------------------------------------------------------------------ creatures
    dict(id='C0', ch='THE *CREATURES*', music='jellyfish',
         text="The sea is full of life. Most creatures are peaceful. A few of them bite back.",
         shots=[('c_jelly_reef', None)], pause=0.6),
    dict(id='C1', ch=None,
         text="*Bruce the shark* hunts anyone who swims. On your raft you are safe, but your raft is not: "
              "he circles it and bites the edge foundations, until one breaks. Reinforced foundations are never bitten.",
         shots=[('c_p_shark', None), ('c_sharks', 'On your raft')], pause=1.0),
    dict(id='C2', ch=None,
         text="The *hammerhead* is bigger and tougher, and lives in the deep, open sea.",
         shots=[('c_p_hammerhead', None), ('c_hammerhead_deep', 'the deep')], pause=0.8),
    dict(id='C3', ch=None,
         text="The *whale* is a gentle giant. It cruises a few blocks below the surface, comes up to breathe and spout, "
              "and sings now and then.",
         shots=[('f_almanac_whale', None)], pause=1.2),
    dict(id='C4', ch=None,
         text="*Manta rays* glide through the warm shallows in slow, wide loops.",
         shots=[('c_p_manta', None), ('c_manta?', 'glide through')], pause=1.0),
    dict(id='C5', ch=None,
         text="*Jellyfish* drift and pulse. Moon jellies are white, crimson jellies red, and glow jellies light up the dark "
              "lagoons. Their touch stings, unless you wear a wetsuit.",
         shots=[('c_p_jelly_moon', None), ('c_p_jelly_crimson', 'crimson jellies'), ('c_p_jelly_glow', 'the dark lagoons'), ('c_jelly_glow', 'Their touch')], pause=1.0),
    dict(id='C6', ch=None,
         text="In the darkness of the trench, the *anglerfish* waits with its glowing lure, then darts forward to bite.",
         shots=[('c_p_angler', None)], pause=1.0),
    dict(id='C7', ch=None,
         text="*Moray eels* hide in holes in the reefs and ruins, with only their head showing, "
              "and lunge at anyone who swims too close.",
         shots=[('c_p_moray', None)], pause=1.0),
    dict(id='C8', ch=None,
         text="On the beaches, *crabs* scuttle sideways. Sprint towards one, and it digs itself into the sand.",
         shots=[('c_p_crab_red', None), ('c_p_crab_blue', 'Sprint towards'), ('c_crab_dig', 'and it digs')], pause=1.0),
    dict(id='C9', ch=None,
         text="*Ember crabs* live on the volcanic isles. Up close they attack, and set you on fire.",
         shots=[('c_p_ember', None), ('c_ember', 'Up close')], pause=1.0),
    dict(id='C10', ch=None,
         text="*Seagulls* fly in flocks over islands and rafts. They peck at crops and snatch food from the ground, "
              "unless a scarecrow stands nearby.",
         shots=[('c_p_gull', None)], pause=1.0),
    dict(id='C11', ch=None,
         text="*Penguins* waddle over the frost floes, slide on their bellies and dive for fish.",
         shots=[('c_penguin', None)], pause=1.0),
    dict(id='C12', ch=None,
         text="*Sea otters* float on their backs in the kelp forest and crack shells on their bellies. "
              "Feed one a seashell, and it follows you, and brings you pearls.",
         shots=[('c_otter', None)], pause=1.0),
    dict(id='C13', ch=None,
         text="And the *drowned corsairs* are the cursed crew of the pirate Saltjaw. They swim, fight with cutlasses, "
              "and even climb onto rafts.",
         shots=[('c_p_corsair', None)], pause=1.2),

    # ------------------------------------------------------------------ blocks and items
    dict(id='I0', ch='BLOCKS AND *ITEMS*', music='wholesome',
         text="Beach Craft adds more than three hundred blocks and items. They are sorted into six new creative tabs, "
              "plus the tab of Beach Craft two.",
         shots=[('i_tab_building', None), ('i_tab_story', '@5.5')], pause=0.6),
    dict(id='I1', ch=None,
         text="*Building*: weathered and teak wood, sea glass, coral stone and tidestone, cracked concrete and asphalt, "
              "steel hulls, beams, catwalks, shipping containers and portholes.",
         shots=[('i_building_1', None), ('i_building_2', '@5'), ('i_building_3', '@10'), ('i_building_4', '@15'), ('i_building_5', '@20')], pause=14.0),
    dict(id='I2', ch=None,
         text="*Decoration*: paper lanterns in nine colours, string lights, buoys and neon tubes, furniture, "
              "treasure chests and everything a pirate needs.",
         shots=[('i_decor_1', None), ('i_decor_2', '@5'), ('i_decor_3', '@10'), ('i_decor_4', '@15')], pause=10.0),
    dict(id='I3', ch=None,
         text="*Nature*: the sands, plants and sea life of the biomes, and the things they give you.",
         shots=[('i_nature_1', None), ('i_nature_2', '@5')], pause=2.5),
    dict(id='I4', ch=None,
         text="*Voyage*: the boats, the expedition raft with its upgrades, and the diving gear.",
         shots=[('i_voyage_1', None)], pause=1.5),
    dict(id='I5', ch=None,
         text="*Creatures*: the spawn eggs, and what the creatures drop.",
         shots=[('i_creatures_1', None), ('i_creatures_2', '@5')], pause=5.5),
    dict(id='I6', ch=None,
         text="*Tides of the Deep*: the story items, the four sigils, the blocks of the sanctum, and the treasures of the Leviathan.",
         shots=[('i_story_1', None), ('i_story_2', '@5.5')], pause=1.2),
    dict(id='I7', ch=None,
         text="And the *Raft* tab of Beach Craft two: driftwood and palm wood, raft foundations, the survival tools, "
              "titanium and the machines.",
         shots=[('i_raft_2', None), ('i_raft_3', '@5'), ('i_raft_4', '@10'), ('i_raft_5', '@15')], pause=10.0),
    dict(id='I8', ch=None,
         text="The *expedition raft* is made from six foundations, two rope and a paddle. It is a big three by three raft, "
              "with four seats and twenty seven storage slots. It never sinks, it never tips over, and sharks cannot hurt it.",
         shots=[('f_raft_place', None), ('f_raft_ride', 'It is a big')], pause=0.8),
    dict(id='I9', ch=None,
         text="*Upgrades* go right onto the raft, and every one of them shows. The sail makes it faster, "
              "the engine more than twice as fast, the cargo crate adds storage, lanterns light it up, "
              "and the anchor holds it in place.",
         shots=[('f_raft_upgrade', None), ('f_raft_menu', 'the cargo crate')], pause=1.0),
    dict(id='I10', ch=None,
         text="The *palm boat* and the *driftwood raft* work like vanilla boats, with or without a chest, "
              "and in a boat, the paddle gives you a push.",
         shots=[('f_boats', None)], pause=0.8),
    dict(id='I11', ch=None,
         text="For the deep there is *diving gear*. The diving helmet lets you see far under water, and with an oxygen tank "
              "you breathe from the tank. A gauge shows how much air is left.",
         shots=[('f_dive', None), ('f_dive_gauge', 'A gauge')], pause=0.8),
    dict(id='I12', ch=None,
         text="Crafted with an angler lure, the helmet gets a *lamp*, and the dark trench becomes visible.",
         shots=[('f_lamp_off', None), ('b_trench_floor', 'and the dark')], pause=0.8),
    dict(id='I13', ch=None,
         text="The *wetsuit* lets you mine faster under water and keeps jellyfish away, *flippers* make you swim much faster, "
              "and the full set gives you dolphin's grace.",
         shots=[('f_suit', None)], pause=0.8),
    dict(id='I14', ch=None,
         text="The *air compressor* refills tanks, with energy or with its hand crank.",
         shots=[('f_compressor', None)], pause=0.6),
    dict(id='I15', ch=None,
         text="The *harpoon gun* shoots harpoons, eight damage under water, and the *sea scooter* pulls you through the deep.",
         shots=[('f_harpoon', None), ('f_scooter', 'and the')], pause=1.0),
    dict(id='I16', ch=None,
         text="The *ship cannon* fires cannonballs about forty blocks far, without breaking any blocks.",
         shots=[('f_cannon_still', None), ('f_cannon_fp', 'fires')], pause=1.4),
    dict(id='I17', ch=None,
         text="The *wind turbine* makes energy high above the sea, just like the solar panel. Cables carry it "
              "to batteries and machines.",
         shots=[('f_turbine', None), ('f_battery', 'Cables')], pause=0.8),
    dict(id='I18', ch=None,
         text="Chairs, cushions and deck chairs can be *sat on*, and the *hammock* is a real bed: it sets your spawn point.",
         shots=[('f_sit', None), ('f_hammock', 'and the')], pause=0.8),
    dict(id='I19', ch=None,
         text="And when it gets dark, the *lights* come alive.",
         shots=[('f_lights_pan', None)], pause=1.6),
    dict(id='I20', ch=None,
         text="The tools of raft survival are still here. The *item catcher* fishes debris out of the water, "
              "the *water purifier* turns sea water into fresh water, and the *simple grill* cooks two foods at once.",
         shots=[('f_deck', None), ('f_purifier', 'the water purifier'), ('f_grill', 'and the simple grill')], pause=0.6),
    dict(id='I21', ch=None,
         text="*Crop plots* never dry out, pineapples grow from their crowns, and a *scarecrow* keeps the seagulls away.",
         shots=[('f_crops', None)], pause=0.6),
    dict(id='I22', ch=None,
         text="The machines of Beach Craft two still run on energy: the *quarry*, the *chunk destroyer*, "
              "and the brick and titanium *furnaces*.",
         shots=[('f_machines', None)], pause=0.8),
    dict(id='I23', ch=None,
         text="The *Seafarer's Almanac* explains everything, chapter by chapter, with a page for every creature.",
         shots=[('f_almanac_index', None), ('f_almanac_diving', 'chapter by chapter')], pause=0.8),
    dict(id='I24', ch=None,
         text="*Research terminals* still show the logs of the expedition, and old *radios* crackle with broadcasts "
              "from long ago.",
         shots=[('f_terminal', None), ('f_radio_use', 'and old')], pause=1.2),

    # ------------------------------------------------------------------ the story
    dict(id='S0', ch='THE *STORY*', music='journey',
         text="Now let us follow the story, the way a player would. From here on, there are spoilers.",
         shots=[('s_platform', None)], pause=0.8),
    dict(id='S1', ch=None,
         text="On the arrival platform waits a *castaway chest*: a note from Captain Rhea Marlow, the expedition journal, "
              "a chart, and a basic kit to survive.",
         shots=[('w_arrive_still', None), ('s_chest', 'a note from')], pause=2.0),
    dict(id='S2', ch=None,
         text="The *expedition journal* always knows the next goal. The first one is the Old Lighthouse.",
         shots=[('s_journal', None)], pause=0.8),
    dict(id='S3', ch=None,
         text="With a raft and the chart, you set sail.",
         shots=[('b_ocean_top', None)], pause=1.2),
    dict(id='S4', ch=None,
         text="In the keeper's cottage lies the logbook of *Tobias Fenn*, and a chart to the stilt village of Saltmere.",
         shots=[('s_lighthouse', None)], pause=2.0),
    dict(id='S5', ch=None,
         text="In Saltmere, the elder's hut holds Nana Kalea's letters, a diving helmet and the next chart. "
              "And behind the statue in the shrine lies the first sigil: the *Coral Sigil*.",
         shots=[('s_saltmere_elder', None), ('s_saltmere_shrine', 'And behind')], pause=2.0),
    dict(id='S6', ch=None,
         text="Deep below, at Helix Station, the terminals of *Dr. Imara Voss* tell how the expedition drilled into the abyss, "
              "and woke something. Her lab vault holds the *Pearl Sigil*.",
         shots=[('s_helix_log', None), ('s_pearl', 'Her lab vault')], pause=1.8),
    dict(id='S7', ch=None,
         text="In Port Solace, Mayor Crane sealed the *Storm Sigil* in a vault near the top of the City Hall tower.",
         shots=[('s_storm', None)], pause=2.0),
    dict(id='S8', ch=None,
         text="In the Ashen Forge, the *Ember Sigil* waits beyond the river of fire.",
         shots=[('s_ember', None)], pause=2.0),
    dict(id='S9', ch=None,
         text="With all four sigils, the altar of the Coral Temple forges the *Tidewarden Key*.",
         shots=[('s_altar', None), ('s_altar_after', 'forges')], pause=1.2),
    dict(id='S10', ch=None,
         text="The key opens the *Tide Seal* of the Abyssal Sanctum. Behind it lies a dome full of air, around a deep pool.",
         shots=[('s_seal', None), ('s_dome', 'Behind it')], pause=1.0),
    dict(id='S11', ch=None, music='deep',
         text="At the altar on the edge of the pool, the key wakes the *Leviathan*, a colossal sea serpent "
              "with six hundred health.",
         shots=[('s_wake_close', None), ('s_wake_wide', 'a colossal')], pause=1.4),
    dict(id='S12', ch=None,
         text="It circles in the pool, where nothing can hurt it. It rises, and spits *brine bolts*.",
         shots=[('s_fight1', None), ('s_fight2', 'It rises')], pause=1.0),
    dict(id='S13', ch=None,
         text="It leaps across the stone ring, slams down, and lies *stranded* for four seconds. That is the moment to strike.",
         shots=[('s_stranded', None), ('s_lunge_close', 'That is the moment')], pause=1.0),
    dict(id='S14', ch=None,
         text="Below half health, it roars and calls the *tidelings*, and stirs a *whirlpool* that pulls you towards the pool. "
              "Below a quarter, it gets faster still.",
         shots=[('s_roar', None), ('c_p_tideling', 'the tidelings'), ('s_roar_close', 'Below a quarter')], pause=1.2),
    dict(id='S15', ch=None,
         text="When it falls, it leaves the *Heart of the Tide*, leviathan scales, and its trophy.",
         shots=[('s_death', None), ('i_story_2', 'and its trophy')], pause=1.4),
    dict(id='S16', ch=None, music='hope',
         text="Placed in the water, the Heart of the Tide gives every swimmer nearby conduit power and dolphin's grace. "
              "Four scales, titanium and a trident make the *Tidebreaker*.",
         shots=[('s_heart', None), ('s_tidebreaker', 'Four scales')], pause=0.8),
    dict(id='S17', ch=None,
         text="And the journal has one last entry. *The sea is calm.* Thank you, keeper of the tides.",
         shots=[('s_end', None)], pause=1.6),
    dict(id='E1', ch=None, end=True,
         text="This was *Beach Craft three point oh*. Free on *CurseForge*, the link is in the description.",
         shots=[('endcard', None)]),
]

SCRIPTS = dict(doc=DOC)

# Aussprache (nur fuer den Sprecher)
SAY = {'CurseForge': 'Curse Forge', 'Saltjaw': 'Salt-jaw', 'Saltmere': 'Salt-meer', 'Tidewardens': 'Tide-wardens',
       'Tidewarden': 'Tide-warden', 'Imara': 'Ee-mara', 'Kalea': 'Ka-lay-a', 'Voss': 'Voss', 'tidelings': 'tide-lings',
       'Tidebreaker': 'Tide-breaker', 'Almanac': 'Almanack', 'Moray': 'More-ay', 'moray': 'more-ay', 'Solace': 'Sollis'}
HEARD = {'curseforge': ['curseforge', 'curseforged'],
         'beach': ['beach', 'beech', 'beechcraft', 'beachcraft'],
         'craft': ['craft', 'beechcraft', 'beachcraft'],
         'saltjaw': ['saltjaw', 'saltjaws', 'saltjar', 'saltja', 'saltjah'],
         'saltmere': ['saltmere', 'saltmeer', 'saltmir', 'saltmear', 'saltmare', 'saltmier'],
         'tidewardens': ['tidewardens', 'tidewarden', 'tidwardens'],
         'tidewarden': ['tidewarden', 'tidewardens'],
         'imara': ['imara', 'amara', 'emara', 'imarra', 'imora'],
         'kalea': ['kalea', 'kaleia', 'kalaya', 'kaleah', 'calea', 'kalaia'],
         'voss': ['voss', 'vos', 'vohs'],
         'tidelings': ['tidelings', 'tidlings', 'tidalings'],
         'tidebreaker': ['tidebreaker', 'tidbreaker'],
         'almanac': ['almanac', 'almanack'],
         'marlow': ['marlow', 'marlo', 'marlowe'],
         'fenn': ['fenn', 'fen', 'finn'],
         'helix': ['helix'],
         'solace': ['solace', 'salas', 'solis', 'sollis', 'solice', 'sollys', 'solys'],
         'colours': ['colours', 'colors'],
         'hammerhead': ['hammerhead', 'hammerheads'],
         'seafarers': ['seafarers', 'seafarer'],
         'dolphins': ['dolphins', 'dolphin'],
         'morays': ['morays', 'moray'],
         'moray': ['moray', 'morey', 'moreay', 'murray', 'moore', 'morray'],
         'isles': ['isles', 'aisles', 'isle', 'aisle', 'iles'],
         'floes': ['floes', 'flows', 'flow', 'floe'],
         'grey': ['grey', 'gray'],
         'twelve': ['twelve', '12'],
         'reefs': ['reefs', 'reef'],
         'oh': ['oh', 'o', '0']}
NUMS = {'26.3': 'twenty six point three', '3.0': 'three point oh', '600': 'six hundred', '300': 'three hundred', '40': 'forty'}

POST = dict(
    doc=dict(
        title="Beach Craft 3.0 - Tides of the Deep: a calm documentary of the whole mod",
        body="""A slow, calm walk through everything in Beach Craft 3.0 "Tides of the Deep" for Minecraft 26.3 (Fabric):
the biomes of the Endless Sea, all nineteen structures and their loot, every creature, every block and item and
how it works (the expedition raft, diving gear, the air compressor, the cannon, the wind turbine and more), and at
the end the whole story from the castaway chest to the fight against the Leviathan. Recorded in the game, with the real
game sounds.

Chapters:
00:00 The Endless Sea
{chapters}
""",
        tags="#minecraft #minecraftmods #beachcraft #raft #ocean #moddedminecraft #curseforge #fabric"),
)
