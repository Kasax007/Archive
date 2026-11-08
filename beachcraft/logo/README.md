# Beach Craft – Logo für CurseForge

Projekt-Logo (CurseForge 1010922). Es zeigt einen kleinen isometrischen Strand-Chunk aus den echten Texturen des Mods:
- eine Palmeninsel aus Sand und Muschelsand mit einer Palme (Stamm aus Palm Log, Kokosnuss-Blätter) und Pflanzen (Hibiskus, Plumeria, Strandgras)
- ein Floß aus Raft Foundation mit Mast, rot-weiß gestreiftem Segel und Wimpel
- flaches, türkises Wasser über dem Meeresboden

Dazu kommen die eckige Minecraft-Sonne, Wolken und Möwen. Der Titel „BEACH CRAFT“ ist in Luckiest Guy gesetzt: weiß mit navyblauer Kontur wie auf der CurseForge-Seite.

| Datei | Wofür |
| --- | --- |
| `logo_1024.png` | **Upload auf CurseForge** (Projekt-Logo; quadratisch, CurseForge rundet die Ecken selbst) |
| `logo_512.png`, `logo_400.png`, `logo_256.png` | Kleinere Fassungen (Outreach, Social, Banner) |
| `icon_1024.png` | Die Szene ohne Schrift (z. B. als Mod-Icon im Spiel, `assets/raft/icon.png`) |
| `preview.png` | So sieht das Logo bei 256, 128 und 64 px auf heller und dunkler Seite aus |

Neu erzeugen (dauert ~3 s; `--preview` rendert ohne dreifaches Supersampling):

```
python3 beachcraft/logo/make_logo.py /home/user/Kasax_Raft_Mod fonts beachcraft/logo
```

- Die Vanilla-Texturen (Sand, Sandstein, Wasser) kommen aus dem Client-Jar im Loom-Cache (`$MC_JAR`).
- Die Szene (Insel-Höhen, Palme, Floß) steht in `scene()`, der Hintergrund in `backdrop()`.
- Beim Floß sitzen die Mast- und Segelkoordinaten in `MAST`.
