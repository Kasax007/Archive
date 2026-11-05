"""Sprechtext und Schnittplan der Beach-Craft-Doku v2 (Querformat, 3.0.1). Aufbau wie tools/script.py von v1:
id, ch (Kapiteltitel), text (*Wort* = Akzent), shots [(Shot, Anker-Phrase)], pause, music."""

DOC = [
    # ------------------------------------------------------------------ opening
    dict(id='O1', ch=None, music='manatees',
         text="Far beyond the overworld lies the *Endless Sea*. Warm islands, bright reefs, a drowned city, "
              "and a trench so deep that the sunlight never reaches its floor.",
         shots=[('o_dawn', None), ('p_solace_air', 'a drowned city'), ('b_trench', 'a trench so deep')], pause=1.0),
    dict(id='O2', ch=None,
         text="This is *Beach Craft three point one*, Tides of the Deep, for Minecraft twenty six point three. "
              "In this film we take our time. We visit every biome, every place and every creature, "
              "we look at the blocks and items and how they work, and at the end we follow the whole story, "
              "the way a player would.",
         shots=[('b_palm_air', None), ('b_kelp', 'every biome'), ('i_tab_voyage', 'we look at'), ('s_seal', 'at the end')],
         pause=1.2),

    # ------------------------------------------------------------------ the way in
    dict(id='W1', ch='THE WAY *IN*',
         text="The journey starts in the overworld. On sandy beaches stand short, dark stumps of *driftwood*.",
         shots=[('w_beach', None)], pause=0.8),
    dict(id='W2', ch=None,
         text="Four driftwood logs around one ancient energy make four portal frames. The energy comes from "
              "ancient broken rings, which hide in shipwreck treasure and ocean ruins.",
         shots=[('w_stump', None), ('w_frame', 'The energy comes')], pause=0.8),
    dict(id='W3', ch=None,
         text="The frame is built like a nether portal, and the *energy staff* lights it.",
         shots=[('w_light', None)], pause=1.2),
    dict(id='W4', ch=None,
         text="Step through, and you arrive on a driftwood platform high above the waves, with a portal back home.",
         shots=[('w_trip', None), ('w_arrive', 'and you arrive')], pause=1.4),

    # ------------------------------------------------------------------ the world
    dict(id='B0', ch='THE *WORLD*', music='voyage',
         text="The Endless Sea is an *archipelago*: open water, islands, reefs and deep trenches, spread over twelve "
              "biomes. The sun rises and sets here, just like in the overworld.",
         shots=[('b_archi', None), ('b_daynight', 'The sun rises')], pause=1.0),
    dict(id='B0b', ch=None,
         text="The sea sounds alive, too: waves and wind, creaking wood, the calls of its creatures, and a piece of "
              "music for every place.",
         shots=[('b_ocean', None), ('o_dawn', 'and a piece')], pause=0.8),
    dict(id='B1', ch=None,
         text="The *Endless Sea* itself is deep blue, open water. Kelp and seagrass grow on the floor, and bubble "
              "vents send columns of air up to the surface.",
         shots=[('b_ocean', None), ('b_vent', 'and bubble')], pause=0.8),
    dict(id='B2', ch=None,
         text="In the *kelp forest*, the kelp grows very tall, and patches of glow kelp light the green water. "
              "Barnacles cover the rocks.",
         shots=[('b_kelp', None)], pause=0.8),
    dict(id='B3', ch=None,
         text="The *coral shallows* are warm and clear. Between the reefs sit sea anemones, giant clams, starfish "
              "and spiny sea urchins, and pebbles of sea glass lie in the sand.",
         shots=[('b_coral', None), ('c_manta', 'giant clams'), ('b_urchin', 'spiny sea urchins')], pause=0.8),
    dict(id='B4', ch=None,
         text="The *glowing lagoon* is rare and dim. Glowing anemones, tube worms and glow kelp fill it with soft light.",
         shots=[('b_lagoon', None)], pause=0.8),
    dict(id='B5', ch=None,
         text="The *drowned shelf* is a flat, murky floor covered in concrete rubble: the ground of a city that "
              "the sea swallowed.",
         shots=[('b_shelf', None), ('p_solace_street', 'the ground of')], pause=0.8),
    dict(id='B6', ch=None,
         text="The *abyssal trench* is the deepest water of all. Down there it is almost black, and only tube "
              "worms and glowing anemones light the basalt.",
         shots=[('b_trench', None)], pause=0.8),
    dict(id='B7', ch=None,
         text="The *wreck graveyard* is foggy, grey water, full of sunken ships.",
         shots=[('b_wrecks', None)], pause=0.8),
    dict(id='B8', ch=None,
         text="In the *frost floes*, icebergs and ice floes drift on cold, clear water.",
         shots=[('b_floes', None)], pause=0.8),
    dict(id='B9', ch=None,
         text="The *palm isles* have sandy beaches with shell sand, palm trees, beach grass and tall sea oats. "
              "Hibiscus, plumeria, aloe and beach morning glory grow between them, and seashells and sea glass "
              "wash up on the shore.",
         shots=[('b_palm_air', None), ('b_seaoats', 'tall sea oats'), ('b_hibiscus', 'Hibiscus'),
                ('b_plumeria', 'plumeria'), ('b_aloe', 'aloe and'), ('b_hibiscus', 'beach morning')], pause=0.8),
    dict(id='B10', ch=None,
         text="*Jungle isles* are warm and wet, with jungle trees and bamboo, tropical ferns, orchids, red "
              "heliconias, birds of paradise and wild pineapple bushes.",
         shots=[('b_jungle_air', None), ('b_orchid', 'orchids'), ('b_heliconia', 'red heliconias'), ('b_bird', 'birds of paradise')], pause=0.8),
    dict(id='B11', ch=None,
         text="*Mangrove isles* are low and muddy, with tangled roots, lily pads and white spider lilies.",
         shots=[('b_mangrove', None), ('b_spiderlily', 'white spider')], pause=0.8),
    dict(id='B12', ch=None,
         text="And the *volcanic isles* are dark and rough: black sand, volcanic ash, pumice and basalt columns.",
         shots=[('b_volcano', None), ('c_ember', 'pumice and')], pause=1.0),
    dict(id='B13', ch=None,
         text="Some of these natural blocks do something. A *giant clam* opens and closes, and an open clam gives "
              "you a pearl. A new one grows in time.",
         shots=[('b_clam_open', None), ('b_coral', 'A new one')], pause=0.8),
    dict(id='B14', ch=None,
         text="A *sea urchin* hurts when you touch it, and drops spines. A wild pineapple bush is ripe when its "
              "fruit turns golden. And a bubble vent makes a bubble column, where divers can catch their breath.",
         shots=[('b_urchin', None), ('b_pineapple', 'A wild pineapple'), ('b_vent', 'And a bubble')], pause=1.4),

    # ------------------------------------------------------------------ the places
    dict(id='P0', ch='THE *PLACES*', music='infinite',
         text="The sea is full of places to explore: seven places of the story, and twelve smaller ones. Almost all "
              "of them have chests, each with its own loot.",
         shots=[('p_saltmere_air', None), ('p_rig_air', 'Almost all')], pause=0.8),
    dict(id='P1', ch=None,
         text="The *old lighthouse* stands on a rocky base. A spiral stair leads up to the lantern room with its "
              "great lens, and next to it are the keeper's cottage and a small dock with buoys.",
         shots=[('p_lighthouse_air', None), ('p_lighthouse_lens', 'A spiral stair'), ('p_lighthouse_dock', 'and next to it')],
         pause=0.8),
    dict(id='P2', ch=None,
         text="*Saltmere* is an abandoned fishing village on stilts above the reef, with huts, rope bridges, "
              "a little market and a shrine.",
         shots=[('p_saltmere_air', None), ('p_saltmere_deck', 'with huts')], pause=0.8),
    dict(id='P3', ch=None,
         text="*Helix Research Station* rests on the sea floor: glass domes and tunnels, an airlock, labs with "
              "research terminals, aquariums, and a flooded wing.",
         shots=[('p_helix_air', None), ('p_helix_in', 'labs with')], pause=0.8),
    dict(id='P4', ch=None,
         text="*Port Solace* is the drowned city. Asphalt streets with wrecked cars, a plaza with a statue, and "
              "skyscrapers, some so tall that their broken tops reach above the waves. In the middle stands the "
              "City Hall tower.",
         shots=[('p_solace_air', None), ('p_solace_street', 'Asphalt streets'), ('p_solace_towers', 'and skyscrapers'),
                ('p_solace_hall', 'In the middle')], pause=0.8),
    dict(id='P5', ch=None,
         text="The *Ashen Forge* is a temple of the Tidewardens, built into the slope of a volcano, with channels "
              "of lava, a giant forge, and a vault behind a bridge over the fire.",
         shots=[('p_forge_air', None), ('p_forge_in', 'with channels'), ('p_forge_bridge', 'and a vault')], pause=0.8),
    dict(id='P6', ch=None,
         text="The *Coral Temple* rests on the reef floor, deep enough to stay under water: overgrown and flooded, "
              "with a courtyard, colonnades, statues and an inner sanctum.",
         shots=[('p_temple_air', None), ('p_temple_in', 'with a courtyard')], pause=0.8),
    dict(id='P7', ch=None,
         text="And deep in the trench waits the *Abyssal Sanctum*. Its walls cannot be broken, and only one key "
              "opens its seal.",
         shots=[('p_sanctum', None), ('s_seal', 'and only one key')], pause=1.2),
    dict(id='P8', ch=None,
         text="A *pirate galleon* lies tilted on the floor, with broken masts, cannons, a captain's cabin and a "
              "cargo hold. Its chests hold gold coins, cannonballs and cutlasses, and sometimes a treasure chart.",
         shots=[('p_galleon', None), ('p_galleon_chest', 'Its chests')], pause=0.8),
    dict(id='P9', ch=None,
         text="A rusty *cargo ship* broke in two, and spilled its shipping containers across the floor.",
         shots=[('p_cargo', None)], pause=0.8),
    dict(id='P10', ch=None,
         text="Small *fishing boats* sank with their nets and crates.",
         shots=[('p_fishing', None)], pause=0.8),
    dict(id='P11', ch=None,
         text="The pirate Saltjaw hid his *cove* inside a rocky island: a sea entrance, a dock with a ship, and a "
              "treasure room full of gold.",
         shots=[('p_cove_air', None), ('p_cove_chest', 'and a treasure')], pause=0.8),
    dict(id='P12', ch=None,
         text="The *rusted rig* stands on steel legs high above the open sea, with cranes, containers, a helipad, "
              "a radio mast and a wind turbine.",
         shots=[('p_rig_air', None), ('p_rig_deck', 'with cranes')], pause=0.8),
    dict(id='P13', ch=None,
         text="Crashed *planes* rest on the sea floor, an airliner and a seaplane.",
         shots=[('p_plane', None)], pause=0.8),
    dict(id='P14', ch=None,
         text="Small Tidewarden *ruins* lie scattered on the reefs: columns, arches and broken statues.",
         shots=[('p_ruins', None)], pause=0.8),
    dict(id='P15', ch=None,
         text="On palm isles you find tiny *castaway camps*, with a shelter, a campfire and an SOS in the sand.",
         shots=[('p_camp', None), ('p_camp_chest', 'and an SOS')], pause=0.8),
    dict(id='P16', ch=None,
         text="*Abandoned rafts* drift on the open sea, with a sail, a chest and a little farm.",
         shots=[('p_raft', None)], pause=0.8),
    dict(id='P17', ch=None,
         text="In the frost floes, a research hut stands on a drifting iceberg: the *iceberg outpost*.",
         shots=[('p_iceberg_air', None), ('p_iceberg_hut', 'a research hut')], pause=0.8),
    dict(id='P18', ch=None,
         text="*Beach shacks* are little bars, with deck chairs, umbrellas and tiki torches.",
         shots=[('p_shack', None)], pause=0.8),
    dict(id='P19', ch=None,
         text="And a *buoy field* marks a channel, with a supply crate chained between the buoys.",
         shots=[('p_buoy', None), ('p_buoy_crate', 'with a supply')], pause=1.4),

    # ------------------------------------------------------------------ creatures
    dict(id='C0', ch='THE *CREATURES*', music='jellyfish',
         text="The sea is full of life. Most creatures are peaceful. A few of them bite back.",
         shots=[('c_manta', None)], pause=0.8),
    dict(id='C1', ch=None,
         text="*Bruce* the shark hunts anyone who swims. On your raft you are safe, but your raft is not: he circles "
              "it and bites the edge foundations, until one breaks. Reinforced foundations are never bitten.",
         shots=[('c_shark', None), ('b_ocean', 'Reinforced')], pause=0.8),
    dict(id='C2', ch=None,
         text="The *hammerhead* is bigger and tougher, and lives in the deep, open sea.",
         shots=[('c_hammer', None)], pause=0.8),
    dict(id='C3', ch=None,
         text="The *whale* is a gentle giant. It cruises a few blocks below the surface, comes up to breathe and "
              "spout, and sings now and then.",
         shots=[('c_whale', None)], pause=1.0),
    dict(id='C4', ch=None,
         text="*Manta rays* glide through the warm shallows in slow, wide loops.",
         shots=[('c_manta', None)], pause=0.8),
    dict(id='C5', ch=None,
         text="*Jellyfish* drift and pulse. Moon jellies are white, crimson jellies red, and glow jellies light up "
              "the dark lagoons. Their touch stings, unless you wear a wetsuit.",
         shots=[('c_jelly', None), ('b_lagoon', 'and glow jellies')], pause=0.8),
    dict(id='C6', ch=None,
         text="In the darkness of the trench, the *anglerfish* waits with its glowing lure, then darts forward to bite.",
         shots=[('c_angler', None)], pause=0.8),
    dict(id='C7', ch=None,
         text="*Moray eels* hide in holes in the reefs and ruins, with only their head showing, and lunge at anyone "
              "who swims too close.",
         shots=[('c_moray', None), ('p_ruins', 'and lunge')], pause=0.8),
    dict(id='C8', ch=None,
         text="On the beaches, *crabs* scuttle sideways. Sprint towards one, and it digs itself into the sand.",
         shots=[('c_crab', None), ('c_crab_dig', 'Sprint towards')], pause=0.8),
    dict(id='C9', ch=None,
         text="*Ember crabs* live on the volcanic isles. Up close they attack, and set you on fire.",
         shots=[('c_ember', None)], pause=0.8),
    dict(id='C10', ch=None,
         text="*Seagulls* fly in flocks over islands and rafts. They peck at crops and snatch food from the ground, "
              "unless a scarecrow stands nearby.",
         shots=[('c_gulls', None), ('c_gull_peck', 'They peck')], pause=0.8),
    dict(id='C11', ch=None,
         text="*Penguins* waddle over the frost floes, slide on their bellies and dive for fish.",
         shots=[('c_penguin', None)], pause=0.8),
    dict(id='C12', ch=None,
         text="*Sea otters* float on their backs in the kelp forest and crack shells on their bellies. Feed one a "
              "seashell, and it follows you, and brings you pearls.",
         shots=[('c_otter', None), ('b_kelp', 'Feed one')], pause=0.8),
    dict(id='C13', ch=None,
         text="And the *drowned corsairs* are the cursed crew of the pirate Saltjaw. They swim, fight with "
              "cutlasses, and even climb onto rafts.",
         shots=[('c_corsair', None), ('c_corsair_fight', 'fight with')], pause=1.4),

    # ------------------------------------------------------------------ blocks and items
    dict(id='I23', ch='BLOCKS AND *ITEMS*', music='wholesome',
         text="Now to the blocks and items, in the order a player finds them. First the *Seafarer's Almanac*: it "
              "explains everything, chapter by chapter, with a page for every creature.",
         shots=[('f_almanac', None), ('f_almanac_page', 'with a page')], pause=0.8),
    dict(id='I20', ch=None,
         text="The tools of raft survival are still here. The item catcher fishes debris out of the water, the "
              "water purifier turns sea water into fresh water, and the simple grill cooks two foods at once.",
         shots=[('f_deck', None), ('f_catcher', 'The item catcher'), ('f_grill', 'and the simple grill')], pause=0.8),
    dict(id='I21', ch=None,
         text="Crop plots never dry out, pineapples grow from their crowns, and a *scarecrow* keeps the seagulls away.",
         shots=[('f_crops', None)], pause=0.8),
    dict(id='I7', ch=None,
         text="And the *Raft* tab of Beach Craft two: driftwood and palm wood, raft foundations, the survival tools, "
              "titanium and the machines.",
         shots=[('i_tab_raft', None)], pause=1.0),
    dict(id='I10', ch=None,
         text="The *palm boat* and the driftwood raft work like vanilla boats, with or without a chest, and in a "
              "boat, the paddle gives you a push.",
         shots=[('f_boats', None)], pause=0.8),
    dict(id='I8', ch=None,
         text="The *expedition raft* is made from six foundations, two rope and a paddle. It is a big three by three "
              "raft, with four seats and twenty seven storage slots. It never sinks, it never tips over, and sharks "
              "cannot hurt it.",
         shots=[('f_raft_place', None), ('f_raft_sail', 'It never sinks')], pause=0.8),
    dict(id='I9', ch=None,
         text="Upgrades go right onto the raft, and every one of them shows. The sail makes it faster, the engine "
              "more than twice as fast, the cargo crate adds storage, lanterns light it up, and the anchor holds it "
              "in place.",
         shots=[('f_raft_upgrades', None), ('f_raft_sail', 'and the anchor')], pause=0.8),
    dict(id='I11', ch=None,
         text="For the deep there is *diving gear*. The diving helmet lets you see far under water, and with an "
              "oxygen tank you breathe from the tank. A gauge shows how much air is left.",
         shots=[('f_dive', None), ('f_gauge', 'A gauge')], pause=0.8),
    dict(id='I13', ch=None,
         text="The *wetsuit* lets you mine faster under water and keeps jellyfish away, flippers make you swim much "
              "faster, and the full set gives you dolphin's grace.",
         shots=[('f_dive', None), ('f_gauge', 'and the full set')], pause=0.8),
    dict(id='I12', ch=None,
         text="Crafted with an angler lure, the helmet gets a *lamp*, and the dark trench becomes visible.",
         shots=[('f_lamp', None)], pause=0.8),
    dict(id='I14', ch=None,
         text="The *air compressor* refills tanks, with energy or with its hand crank.",
         shots=[('f_compressor', None)], pause=0.8),
    dict(id='I15', ch=None,
         text="The *harpoon gun* shoots harpoons, eight damage under water, and the *sea scooter* pulls you through "
              "the deep, for almost four minutes on one charge.",
         shots=[('f_harpoon', None), ('f_scooter', 'and the sea')], pause=0.8),
    dict(id='I17', ch=None,
         text="The *wind turbine* makes energy high above the sea, and the solar panel by day. Cables carry it to "
              "batteries and machines.",
         shots=[('f_turbine', None), ('f_deck', 'Cables carry')], pause=0.8),
    dict(id='I22', ch=None,
         text="The *machines* of Beach Craft two still run on energy: the quarry, the chunk destroyer, and the brick "
              "and titanium furnaces.",
         shots=[('f_machines', None)], pause=0.8),
    dict(id='I16', ch=None,
         text="The *ship cannon* fires cannonballs about forty blocks far, without breaking any blocks.",
         shots=[('f_cannon', None)], pause=0.8),
    dict(id='I1', ch=None,
         text="*Building*: weathered and teak wood, sea glass, coral stone and tidestone, cracked concrete and "
              "asphalt, steel hulls, beams, catwalks, shipping containers and portholes.",
         shots=[('i_tab_building', None), ('i_tab_building2', 'cracked concrete')], pause=0.6),
    dict(id='I2', ch=None,
         text="*Decoration*: paper lanterns in nine colours, string lights, buoys and neon tubes, furniture, "
              "treasure chests and everything a pirate needs.",
         shots=[('i_tab_decor', None), ('i_tab_decor2', 'furniture')], pause=0.6),
    dict(id='I3', ch=None,
         text="*Nature*: the sands, plants, flowers and sea life of the biomes, and the things they give you.",
         shots=[('i_tab_nature', None)], pause=0.6),
    dict(id='I18', ch=None,
         text="Chairs, cushions and deck chairs can be sat on, and the *hammock* is a real bed: it sets your spawn point.",
         shots=[('f_seats', None), ('f_hammock', 'and the hammock')], pause=0.8),
    dict(id='I19', ch=None,
         text="And when night falls, the *lights* come alive.",
         shots=[('b_night', None), ('f_lights', 'the lights')], pause=1.6),
    dict(id='I0', ch=None,
         text="All in all, Beach Craft adds more than three hundred blocks and items, sorted into six new creative "
              "tabs, plus the tab of Beach Craft two.",
         shots=[('i_tab_building', None)], pause=0.6),
    dict(id='I4', ch=None,
         text="*Voyage*: the boats, the expedition raft with its upgrades, and the diving gear.",
         shots=[('i_tab_voyage', None)], pause=0.6),
    dict(id='I5', ch=None,
         text="*Creatures*: the spawn eggs, and what the creatures drop.",
         shots=[('i_tab_creatures', None)], pause=0.6),
    dict(id='I6', ch=None,
         text="*Tides of the Deep*: the story items, the four sigils, the blocks of the sanctum, and the treasures "
              "of the Leviathan.",
         shots=[('i_tab_story', None)], pause=0.6),
    dict(id='I24', ch=None,
         text="*Research terminals* still show the logs of the expedition, and old radios crackle with broadcasts "
              "from long ago.",
         shots=[('f_terminal', None), ('f_radio', 'and old radios')], pause=1.6),

    # ------------------------------------------------------------------ 3.1: your own raft, the people of the sea
    dict(id='R0', ch='YOUR OWN *RAFT*', music='voyage',
         text="Since version three point one, you can also build your own raft, block by block: foundations on the "
              "water, a *helm*, and sails, oars or a motor to move it.",
         shots=[('r_found_place', None), ('r_found_grow', 'block by block'), ('r_build_motor', 'a helm'), ('r_build_sail', 'and sails')], pause=0.8),
    dict(id='R1', ch=None,
         text="Use the helm, and the raft *sets sail*. Everything on it sails along.",
         shots=[('r_setsail', None), ('r_sail_start', 'sets sail'), ('r_sail_orbit', 'Everything')], pause=0.8),
    dict(id='R2', ch=None,
         text="And everything on board keeps working at sea: *chests* and furnaces, growing crops, levers and lamps. "
              "You can even keep building.",
         shots=[('r_sail_helm', None), ('r_sea_furnace', 'chests and'), ('r_sea_wheat', 'growing crops'), ('r_sea_lever', 'levers and'), ('r_sea_place', 'You can even')], pause=0.8),
    dict(id='R3', ch=None,
         text="At the helm you steer with the movement keys. Use the wheel once more, and the raft *drops anchor* and "
              "turns back into blocks.",
         shots=[('r_sail_wide', None), ('r_anchor', 'Use the wheel'), ('r_anchored', 'turns back')], pause=1.4),
    dict(id='N0', ch='PEOPLE OF THE *SEA*', music='wholesome',
         text="A few people stayed behind on the Endless Sea. Talk to them, and they tell you who they are, what you "
              "should do next, and the rumours they have heard. Most of them trade, for pirate gold and pearls.",
         shots=[('n_fenn_place', None)], pause=0.8),
    dict(id='N1', ch=None,
         text="*Keeper Tobias Fenn* still lives in the cottage beside the old lighthouse. He welcomes you with a "
              "spyglass, points you on to Saltmere, buys your fish, and sells candles, lanterns and glowstone.",
         shots=[('n_fenn_talk', None), ('n_fenn_greet', 'He welcomes'), ('n_fenn_next', 'points you'), ('n_fenn_trade', 'buys your fish')],
         pause=1.0),
    dict(id='N2', ch=None,
         text="In Saltmere, *Nalu* keeps the shrine lamps of his grandmother burning. He gives you a potion of water "
              "breathing for the reef, and trades the crafts of the village for pearls: lanterns, rugs, wind chimes, "
              "and a spare diving helmet.",
         shots=[('n_nalu_place', None), ('n_nalu_work', 'keeps the shrine'), ('n_nalu_gift', 'He gives you'), ('n_nalu_trade', 'and trades')],
         pause=1.0),
    dict(id='N3', ch=None,
         text="*Old Tamo* has fished from the pier of Saltmere for sixty years. He hands you a supper of cooked cod, "
              "buys fish, crab claws and eel for pirate gold, and sells a lucky fishing rod, glow kelp, sea pickles "
              "and even a palm boat.",
         shots=[('n_tamo_work', None), ('n_tamo_greet', 'He hands you'), ('n_tamo_trade', 'buys fish')], pause=1.0),
    dict(id='N4', ch=None,
         text="*Doctor Imara Voss* cracked the Tide Seal, and now she studies the tablets in the storeroom of the "
              "Ashen Forge. She does not trade, but she gives you a potion of fire resistance for the river of lava, "
              "and another one if you lose it.",
         shots=[('n_voss_work', None), ('n_voss_greet', 'She does not'), ('n_voss_gift', 'a potion of fire')], pause=1.0),
    dict(id='N6', ch=None,
         text="*Kai* is the castaway who wrote the SOS. He waits by his campfire and hopes you brought biscuits, and "
              "he trades everything that washes up, bottle letters, rope, plastic, scrap and supply barrels, for cookies.",
         shots=[('n_kai_work', None), ('n_kai_greet', 'He waits'), ('n_kai_trade', 'and he trades')], pause=1.0),
    dict(id='N5', ch=None,
         text="*Teo* runs the last bar on the Endless Sea. The first drink, a piña colada, is on the house. He sells "
              "drinks and island food, and buys pineapples, coconuts and rum.",
         shots=[('n_teo_work', None), ('n_teo_greet', 'The first drink'), ('n_teo_trade', 'He sells')], pause=1.0),
    dict(id='N8', ch=None,
         text="*Patience Okafor* is the chief engineer of the old rig, and the only crew left. She gives you a "
              "spare circuit board, sells scrap, redstone, cables, circuit boards, titanium and batteries, and buys "
              "copper, iron and plastic.",
         shots=[('n_okafor_work', None), ('n_okafor_gift', 'She gives you'), ('n_okafor_trade', 'sells scrap')], pause=1.0),

    dict(id='N7', ch=None,
         text="And *Doctor Elin Lund* studies the weather and the wildlife at the iceberg outpost. She offers you a cup of "
              "tea with honey, sells harpoons, wetsuits, flippers and oxygen tanks, and buys jellies, angler lures, "
              "shark teeth and leviathan scales.",
         shots=[('n_lund_talk', None), ('n_lund_greet', 'She offers you'), ('n_lund_trade', 'sells harpoons')], pause=1.6),
    # ------------------------------------------------------------------ the story
    dict(id='S0', ch='THE *STORY*', music='journey',
         text="Now let us follow the story, the way a player would. From here on, there are spoilers.",
         shots=[('w_arrive', None)], pause=1.0),
    dict(id='S1', ch=None,
         text="On the arrival platform waits a *castaway chest*: a note from Captain Rhea Marlow, the expedition "
              "journal, a chart, and a basic kit to survive.",
         shots=[('s_platform', None), ('s_chest', 'a note from')], pause=2.0),
    dict(id='S2', ch=None,
         text="The *expedition journal* always knows the next goal. The first one is the Old Lighthouse.",
         shots=[('s_journal', None)], pause=0.8),
    dict(id='S3', ch=None,
         text="With a raft and the chart, you set sail.",
         shots=[('f_raft_sail', None)], pause=1.2),
    dict(id='S4', ch=None,
         text="The lighthouse stands on its island. In the keeper's cottage lies the logbook of *Tobias Fenn*, "
              "and a chart to the stilt village of Saltmere.",
         shots=[('s_lighthouse_way', None), ('s_lighthouse_in', 'cottage lies'), ('s_lighthouse', 'and a chart')],
         pause=2.0),
    dict(id='S5', ch=None,
         text="In *Saltmere*, the elder's hut holds Nana Kalea's letters, a diving helmet and the next chart. "
              "And behind the statue in the shrine lies the first sigil: the *Coral Sigil*.",
         shots=[('p_saltmere_deck', None), ('s_saltmere_elder', 'holds Nana'), ('p_saltmere_shrine', 'And behind'),
                ('s_saltmere_shrine', 'the first sigil')], pause=1.4),
    dict(id='S6', ch=None,
         text="Deep below, at *Helix Station*, the terminals of Dr. Imara Voss tell how the expedition drilled into "
              "the abyss, and woke something. Her lab vault holds the *Pearl Sigil*.",
         shots=[('p_helix_in', None), ('s_helix_terminal', 'the terminals'), ('s_helix_vault', 'Her lab vault')], pause=1.4),
    dict(id='S7', ch=None,
         text="In *Port Solace*, Mayor Crane sealed the *Storm Sigil* in a vault near the top of the City Hall tower.",
         shots=[('p_solace_hall', None), ('s_solace_vault', 'in a vault')], pause=1.4),
    dict(id='S8', ch=None,
         text="In the *Ashen Forge*, the *Ember Sigil* waits beyond the river of fire.",
         shots=[('p_forge_bridge', None), ('s_forge_vault', 'waits beyond')], pause=1.4),
    dict(id='S9', ch=None,
         text="With all four sigils, the altar of the Coral Temple forges the *Tidewarden Key*.",
         shots=[('s_altar', None), ('s_altar_after', 'forges')], pause=1.2),
    dict(id='S10', ch=None,
         text="The key opens the *Tide Seal* of the Abyssal Sanctum. Behind it lies a dome full of air, around a "
              "deep pool.",
         shots=[('s_seal', None), ('s_dome', 'Behind it')], pause=1.0),
    dict(id='S11', ch=None, music='deep',
         text="At the altar on the edge of the pool, the key wakes the *Leviathan*, a colossal sea serpent with six "
              "hundred health.",
         shots=[('s_wake', None), ('s_lev_wide', 'a colossal')], pause=1.4),
    dict(id='S12', ch=None,
         text="It circles in the pool, where nothing can hurt it. It rises, and spits *brine bolts*.",
         shots=[('s_lev_circle', None), ('s_lev_wide', 'It rises')], pause=1.0),
    dict(id='S13', ch=None,
         text="It leaps across the stone ring, slams down, and lies *stranded* for four seconds. That is the moment "
              "to strike.",
         shots=[('s_lev_leap', None), ('s_lev_strike', 'That is the moment')], pause=1.0),
    dict(id='S14', ch=None,
         text="Below half health, it roars and calls the *tidelings*, and stirs a whirlpool that pulls you towards "
              "the pool. Below a quarter, it gets faster still.",
         shots=[('s_lev_roar', None), ('s_lev_circle', 'Below a quarter')], pause=1.2),
    dict(id='S15', ch=None,
         text="When it falls, it leaves the *Heart of the Tide*, leviathan scales, and its trophy.",
         shots=[('s_lev_death', None), ('s_rewards', 'leviathan scales')], pause=1.4),
    dict(id='S16', ch=None, music='hope',
         text="Placed in the water, the Heart of the Tide gives every swimmer nearby conduit power and dolphin's "
              "grace. Four scales, titanium and a trident make the *Tidebreaker*.",
         shots=[('s_heart', None), ('s_tidebreaker', 'Four scales')], pause=0.8),
    dict(id='S17', ch=None,
         text="And the journal has one last entry. The sea is calm. *Thank you, keeper of the tides.*",
         shots=[('s_end', None)], pause=1.6),
    dict(id='E1', ch=None, end=True,
         text="This was *Beach Craft three point one*. Free on *CurseForge*, the link is in the description.",
         shots=[('endcard', None)]),
]

SCRIPTS = dict(doc=DOC)

# Aussprache, Whisper-Varianten und Zahlen wie in v1, dazu die neuen Woerter
import importlib.util as _u, os as _os
_spec = _u.spec_from_file_location('v1script', _os.path.join(_os.path.dirname(__file__), '..', '..', 'tools', 'script.py'))
_v1 = _u.module_from_spec(_spec)
_spec.loader.exec_module(_v1)
SAY = dict(_v1.SAY, plumeria='ploo-meria', heliconias='heli-conias', Okafor='Oh-ka-for', Nalu='Na-loo', Tamo='Ta-mo')
HEARD = dict(_v1.HEARD, heliconias=['helicanias', 'heliconias'], plumeria=['plumeria', 'plumaria'], tamo=['tomo', 'tamo'],
             doctor=['dr', 'doctor'], lund=['lund', 'lunde', 'lune', 'lunn'], rumours=['rumors', 'rumours'])
NUMS = dict(_v1.NUMS, **{'3.1': 'three point one'})
POST = dict(doc=dict(
    title="Beach Craft 3.1 - Tides of the Deep: a calm documentary of the whole mod (with shaders)",
    body="""A slow, calm walk through everything in Beach Craft 3.1 "Tides of the Deep" for Minecraft 26.3 (Fabric),
filmed with shaders (Iris + Complementary Reimagined): the biomes of the Endless Sea with day and night, all nineteen
structures and their loot, every creature, the blocks and items and how they work, building your own raft and meeting
the people of the sea, and at the end the whole story from the castaway chest to the fight against the Leviathan.

Chapters:
00:00 The Endless Sea
{chapters}
""",
    tags="#minecraft #minecraftmods #beachcraft #raft #ocean #moddedminecraft #curseforge #fabric #shaders"))
