# YouTube-Upload: Doku „Tides of the Deep“ (Beach Craft 3.1)

Alles zum Hochladen der Doku v2 (21:27, Englisch, eingebrannte Untertitel, Musik). Die Texte in den Kästen sind
fertig zum Einfügen.

## Welche Datei

- **Beste Qualität (empfohlen): die volle Fassung in 1080p mit 60 fps.** Sie liegt in diesem Ordner in 13 Teilen
  (`beachcraft3_documentary_v2_part01.mp4` … `part13.mp4`, zusammen etwa 610 MB, H.264 1920×1080, AAC 48 kHz).
  Zusammenfügen wie in der `README.md` (verlustfrei, ohne neues Rendern):

  ```sh
  printf "file '%s'\n" beachcraft3_documentary_v2_part*.mp4 > l.txt && ffmpeg -f concat -safe 0 -i l.txt -c copy beachcraft3_documentary_v2.mp4
  ```

  Die fertige Datei (~610 MB) und `l.txt` danach **nicht einchecken** (jede Datei im Repo bleibt unter 95 MB):
  hochladen und wieder löschen, oder den Befehl in einem Ordner außerhalb des Repos ausführen.
- **Vom Handy aus:** auf der Artifact-Seite „Tides of the Deep“ erst „Video laden“, dann „Als MP4 speichern“. Das ist
  die Handy-Fassung in 720p mit 30 fps (~202 MB). Sie reicht für YouTube, sieht aber weniger scharf aus.
- **Untertitel:** sind schon eingebrannt. `beachcraft3_documentary_v2.srt` kann zusätzlich als englische Untertitel
  hochgeladen werden (hilft der Suche); wer dann CC einschaltet, sieht den Text doppelt. Also optional.
- **Vorschaubild:** `stills/endcard.png` (1920×1080, 855 KB, unter der Grenze von 2 MB) oder ein eigenes Standbild.
- **Einstellungen:** Kategorie „Gaming“, Spiel „Minecraft“, nicht für Kinder, Sprache Englisch. Die Kapitel erzeugt
  YouTube selbst aus den Zeitmarken in der Beschreibung.

## Titel

```
Beach Craft 3.1 - Tides of the Deep: a calm documentary of the whole mod (with shaders)
```

## Beschreibung

```
A slow, calm walk through everything in Beach Craft 3.1 "Tides of the Deep" for Minecraft 26.3 (Fabric), filmed with shaders (Iris + Complementary Reimagined): the twelve biomes of the Endless Sea with day and night, all nineteen places and their loot, every creature, the blocks and items and how they work, building your own raft, the eight people of the sea, and at the end the whole story, from the castaway chest to the fight against the Leviathan. Spoilers from 18:13.

Chapters:
00:00 The Endless Sea
00:38 The Way In
01:18 The World
04:24 The Places
07:59 The Creatures
10:22 Blocks and Items
14:53 Your Own Raft
15:36 People of the Sea
18:13 The Story

Beach Craft is free on CurseForge: https://www.curseforge.com/minecraft/mc-mods/beach-craft
Play it in the Dreamcraft modpack: https://www.curseforge.com/minecraft/modpacks/dreamcraft-new
Needs Minecraft 26.3, Fabric Loader 0.19.5 or newer and Fabric API.

Music:
"Music for Manatees" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Living Voyage" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Infinite Perspective" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Jellyfish in Space" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Wholesome" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Enchanted Journey" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Thunderbird" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

"Eternal Hope" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

#minecraft #minecraftmods #beachcraft #raft #ocean #moddedminecraft #curseforge #fabric #shaders
```

## Tags

```
minecraft, minecraft mods, beach craft, beach craft mod, raft mod, minecraft raft, raft in minecraft, minecraft ocean mod, ocean survival, fabric mod, minecraft 26.3, modded minecraft, minecraft documentary, mod showcase, curseforge, minecraft shaders, complementary shaders, minecraft boss, leviathan, dreamcraft, tides of the deep
```

## Nach dem Hochladen

Die CurseForge-Seite (`Kasax_Raft_Mod/docs/curseforge/description.html`, Branch `26.3`) bettet das Video ein. Dort
steht zwischen `<!-- VIDEO START -->` und `<!-- VIDEO END -->` zweimal der Platzhalter `VIDEO_ID` (Player und Link
unter dem Vorschaubild): beide durch die ID des Videos ersetzen (der Teil nach `watch?v=`). Solange das Video nicht
online ist, den ganzen Block bis `<!-- VIDEO END -->` vor dem Einfügen in CurseForge weglassen.

## Woher die Angaben stammen

- Kapitelzeiten: `tools/script.py` (Kapitelanfänge) und die Artifact-Seite, gegen die SRT geprüft: der erste
  Untertitel jedes Kapitels beginnt bei 0:38, 1:18, 4:24, 7:59, 10:22, 14:53, 15:36 und 18:13. Länge der 13 Teile
  zusammen: 21:27.
- Musik: `tools/doc.py` (`MUSIC`/`CREDITS`), alle acht Stücke laufen im Film.
- Links: über die CurseForge-Projekt-IDs geprüft. Der Mod (1010922) hat den Slug `beach-craft` (nicht `raft`, das ist
  nur die Mod-ID), das Modpack Dreamcraft (545167) den Slug `dreamcraft-new`.
