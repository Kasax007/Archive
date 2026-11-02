# Beach Craft (Raft) 2.0.1 – Prüfbericht zum Review-Video

Grundlage: Code-Analyse aller Bereiche (Portal/Reise, Überleben, Hai/Titan, Technik/Deko), jeweils von einem
zweiten Durchgang gegen den Code geprüft. Danach wurde jedes Feature im Spiel gefilmt (`beachcraft_review_*.mp4`).
Gefundene Fehler sind in 2.0.1 behoben, siehe `Kasax_Raft_Mod/docs/curseforge/changelog-2.0.1+26.3.md`.

## Was es gibt (Reihenfolge wie im Video)

| Feature | Zu sehen im Video | Stand |
| --- | --- | --- |
| Treibholz-Stümpfe an Sandstränden, Treibholz-Setzling | Strand, Knochenmehl | ok (Stümpfe sind blattlos, so gewollt) |
| Ancient Broken Ring / Crystal in Schatz-Loot, Ring → Ancient Energy | Truhe, Hochofen | ok; 1 Disc statt bis zu 5 (behoben) |
| Portalrahmen (4 Stück pro Rezept), Energy Staff | Crafter | ok; Rahmen droppt jetzt mit jeder Axt (behoben) |
| Portal anzünden mit Hinweisen, Reise, Plattform über dem Meer | Oberwelt → Raft-Dimension | ok; kaputtes Rückportal jetzt reparierbar, Ausgang sucht freien Platz (behoben) |
| Raft Teleporter | Oberwelt → Steinblock im Meer | ok; landet symmetrisch, nicht in Höhlen, Block für alle sichtbar (behoben) |
| Inseln mit Palmen, Kokosnüsse pflücken | Sandinsel | ok; Kokosnüsse wachsen nach ~20 min nach (vorher ~95 h, behoben) |
| Treibgut (Strömung von Westen) | Floß | ok; „Fässer“ gibt es nicht, nur einzelne Beute-Stapel (Text korrigiert) |
| Plastic Hook | Gegenstände fliegen heran | ok |
| Item Catcher + Netz → Ocean Garbage | GUI | ok; kein Geister-Item mehr, Slots geprüft (behoben). Grenze: fängt nur eine Sorte gleichzeitig |
| Trash Cube | Ofen, Würfel öffnen | ok |
| Seil, Seilrolle, Segeltuch | 2x2-Crafting | **Segeltuch war nicht herstellbar** (Rezept-Konflikt, behoben: 2 Seil über 2 weißer Wolle) |
| Strickleiter | Klettern | ok |
| Wasserreiniger | GUI: Eimer → 3 Frischwasser | ok; Trichter holt leeren Eimer, Pfeil ohne Rest (behoben) |
| Frischwasser, Kokosmilch, Piña Colada | Trinken mit HUD | ok; Piña Colada gibt Schüssel zurück, Frischwasser 1 Keule (behoben) |
| Simple Grill | 2 Speisen gleichzeitig | ok; nimmt kein Essen mehr weg bei falschem Item (behoben) |
| Crop Plot | Wachstum vs. Ackerland, kein Zertrampeln | ok (~50 % schneller) |
| Scarecrow | Platzieren | ok; Kopf schaut jetzt in Körperrichtung (behoben) |
| Hai Bruce | Schwimmt, greift Schwimmer an, Drops, Trophäe | **spawnte nie natürlich** (behoben); hört auf, wenn man aufs Floß klettert (behoben) |
| Receiver | Richtung + Entfernung zum Treibholz | ok (zeigt Treibholz, keine Inseln/Wracks – Texte korrigiert) |
| Paddel | Boot-Schub | **schob das Boot nicht** (nur der Server bekam den Schub, Boote steuert aber der Client; erst im Video aufgefallen, behoben) |
| Titan: Erz, Rohtitan, Barren, Blöcke, Gitter | Abbau mit Diamantspitzhacke, Hochofen | ok; Erz gibt jetzt XP (behoben). **Titan-Werkzeuge gibt es nicht** (Texte korrigiert) |
| Titan-Rüstung | Set-Bonus-Effekte | ok; Effekte enden kurz nach Ablegen (behoben) |
| Metalldetektor | Meldung in der Aktionsleiste | ok (findet nur Titanerz direkt darunter) |
| Musik-Discs | Jukebox | ok; Länge stimmt jetzt (behoben) |
| Solarpanel, Batterie, Kabel | Laden, GUI, Tech-Reborn-Lampe | ok; kein Energie-Ping-Pong mehr (behoben) |
| Steinbruch | Baut 11x11 ab | ok; speichert Fortschritt, Shulker-Inhalt bleibt (behoben) |
| Ziegel- und Titanofen | GUI | ok; Tooltips zeigen Zahlen (behoben) |
| Deko: Palmen-/Treibholz-Sets, Strohdach, Segel, Schrott/Plastik, Steuerrad, Flagge, Laternen | Floß | ok; Holz brennt im Ofen und fängt Feuer (behoben) |

## Bewusst nicht geändert (Design-Fragen für dich)

- Der Titanofen verdoppelt jedes Schmelzergebnis (100 %), auch Ancient Energy.
- Maschinen verlieren gespeicherte Energie beim Abbauen.
- Der Chunk Destroyer kostet 100.000 FE auch für leere Säulen.
- Der Item Catcher hat nur einen Ausgabe-Slot.
- Der Treibholz-Setzling ist fast nur über Treibgut-Beute zu bekommen.
- Die Ankunfts-Plattform liegt auf Y 209: Wer hinunterfällt, landet im Meer.
- Das Plastic Hook zieht auch durch Wände.
- Die Raft-Dimension nutzt die Geländeform der Oberwelt mit Meeresspiegel 100. Wo die Oberwelt Berge hätte, ragen
  deshalb große Steinmassive aus dem „endlosen Meer“, z. B. bei x 6000 / z 3000. Die Sandinseln mit Palmen sind die
  flacheren Hügel. Soll das Meer offener werden (flachere Geländeform), oder bleibt es so?
