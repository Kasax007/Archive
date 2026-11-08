# 05 – Challenge Craft: Bug- und Feature-Check (November 2026)

Challenge Craft ist dein großer Mod mit 51 Challenges, Casino und dem KI-Gegner Bob (Repo
`Kasax007/Kasax_Challenge_Craft`, CurseForge-Projekt 1508454). In dieser Runde gab es **keine neue Version**, sondern
einen gründlichen Bug-Check. Der vollständige Bericht steht im Repo unter **`docs/BUGCHECK-2026-11.md`**.

| Eckdaten | |
| --- | --- |
| Branch | `bugcheck-2026-11` (abgezweigt von `26.3-lockout-bot`, Stand 1.1.3), letzter Commit `1474c3d`, gepusht |
| Version | `mod_version` bleibt **1.1.3** – nichts veröffentlicht |
| Changelog-Entwurf | `docs/curseforge/changelog-1.1.4.md` (für die nächste Version, falls du sie freigibst) |
| Veröffentlichung | automatisch per `publish.yml`, sobald auf `26.3` oder `26.3-lockout-bot` `mod_version` geändert wird – deshalb wurde nichts gebumpt |

**Warum ein eigener Branch?** Nach deiner Regel wird nie direkt auf `26.3` gepusht. Der Branch sammelt die Fixes, bis
du entscheidest, ob und wann sie als 1.1.4 erscheinen.

## Was geprüft wurde

- **Build** (`build`, `compileFilmJava`, `compileGametestJava`): ok, keine neuen Warnungen.
- **Game-Tests** (als Dedicated Server, Maschine stark ausgelastet): vorher 194/195 grün (`brawl_enderman_slope`
  rot, bekannt wackelig). Nach den Fixes 197/197 grün. Der letzte volle Lauf hatte 196/198 – rot nur zwei
  Bob-Kampfszenen (`sniper_duel`, `brawl_enderman`), die mit den Änderungen nichts zu tun haben; einzeln nachgeprüft
  waren beide grün.
- **Client** (Film-Harness unter Xvfb): Hub und Challenge-Auswahl mit echten Klicks auf die Karten; Client-Log ohne
  Fehler der Mod.
- **Dedicated Server** mit `CHALLENGECRAFT_VERIFY_IDS=1`: startet ohne Client-Klassen (in 3,4 s). Das Registry-Audit
  fand eine ungültige ID (Punkt 9 unten), danach „OK — every id resolves“ (1495 IDs).
- **Ressourcen per Skript:** jede Sprachschlüssel-Familie (51 Challenges, Perks, Lockout-Ziele, Casino) in `en_us` und
  `de_de` mit gleichen Platzhaltern; alle Modelle, Texturen, Blockstates, Item-Definitionen vorhanden; Loot-Tabellen
  und Rezepte laden ohne Fehler.
- **Gelesen:** alle Server-Empfänger für Client-Pakete, die Infinite Chest komplett, Casino-Eingaben, Void Trail,
  Red Light, Dice, die Mixin-Aufteilung Client/Server und die Maustasten in allen Screens (26.3/SDL: links = 1).
  Bob nur stichprobenartig.

## Was behoben wurde (10 Punkte)

| # | Bereich | Problem | Fix | Geprüft |
| --- | --- | --- | --- | --- |
| 1 | **Infinite Chest** | Klick-Pakete galten für jede geladene Truhe, ohne offenes Menü und aus jeder Entfernung (fremde Truhen leerbar); das Menü blieb ewig gültig; Entnehmen/Ablegen markierte die Truhe nie als geändert, nach einem Neuladen kamen entnommene Items zurück (**Dupe**) oder abgelegte waren weg; Linksklick nahm immer 64 (auch 64 Schwerter) | nur die offene Truhe in Reichweite; Menü schließt wie bei einer Kiste; jede Änderung wird gespeichert; Linksklick = ein Stapel | im Spiel: neuer Game-Test `challenge_fix_tests_infinite_chest_clicks` (gegen den alten Code 8 von 10 Prüfungen rot) |
| 2 | **Crafter** | Der Vanilla-Crafter umging die Level- und Kauf-Sperre und baute Infinite Chest (Level 20 + Perk) und Casino-Geräte (einmal beim Croupier kaufen) für jeden | neuer `mixin/CrafterGateMixin.java`: der Crafter baut sie nicht mehr; Hand-Crafting unverändert | im Spiel: `challenge_fix_tests_crafter_makes_no_gated_items` |
| 3 | **Dice** | Im Einzelspieler schaltet der Client-Sync die Challenge-Flags kurz aus und an; `setActive(false)` löschte dabei alle gewürfelten Block-Budgets (LAN-Beitritt, Einstellungen geändert) | wie bei Red Light erst nach 1 s „aus“ bzw. beim Server-Stopp | im Spiel: `challenge_fix_tests_dice_budget_survives_sync` |
| 4 | **Roulette** | absurde Chip-Zahl (nur mit verändertem Client) lief ins Negative und zahlte aus; Block wurde vor der Reichweite geprüft | Prüfungen korrigiert | nur gelesen |
| 5 | **Kasse** | fremder Text ging an `Identifier.parse` und warf Fehler (Log-Spam) | nur bekannte IDs | nur gelesen |
| 6 | **ChallengePacket** | Decoder reservierte Listen in der Größe, die ein Client schickt | begrenzt | nur gelesen |
| 7 | Kleinkram | Name des Würfel-Entitys fehlte (`entity.challengecraft.dice`, beide Sprachen); tote Loot-Tabelle im alten Ordner `loot_tables/` | ergänzt bzw. entfernt | nur gelesen (Jar geprüft) |
| 8 | **Challenge-Auswahl** | Der Zähler „aktiv/gesamt“ neben jedem Abschnitt blieb nach einem Klick stehen („0/7“ trotz drei aktiver Challenges) | wird jetzt beim Zeichnen gezählt (Welt-Erstellung und `/challenges`) | im Client (Film-Bilder) |
| 9 | **Block-Survey** | `minecraft:chain` heißt in 26.3 `minecraft:iron_chain`; Progressive Block Drops übersprang den Eintrag still | Eintrag entfernt | Server-Start mit ID-Audit |
| 10 | **Film-Harness** | Szene `ui_select` klickte mit Taste 0 (in 26.3 keine Taste) und fand seit dem Scroll-Panel keine Karte mehr | `MOUSE_BUTTON_LEFT` und Suche im Panel: 59 Karten, Klicks schalten sichtbar um | im Client |

Spieler-Text dazu steht im Entwurf `docs/curseforge/changelog-1.1.4.md` („Infinite Chest … always saved“,
„Crafter: no longer crafts the Infinite Chest or the casino devices“, „Dice …“, „The House Always Wins …“,
„Challenge selection …“, „The thrown die shows its name“).

## Was offen ist (bewusst nicht geändert)

- **Infinite Chest, Transfer-API:** Trichter können nichts herausziehen (die Views geben bei `extract` immer 0
  zurück). Außerdem zählt `extract` mehrere Entnahmen in einer Transaktion nicht gegen und bucht über
  Close-Callbacks statt `SnapshotParticipant` – mit Rohr-Mods ein Dupe-Risiko. **Erst entscheiden, ob Herausziehen
  gewollt ist.**
- **Infinite Chest beim Abbauen:** Der ganze Inhalt fällt als Items heraus (bei Millionen Items Tausende Entities).
  Idee: Inhalt im Item behalten wie bei der Shulker-Kiste.
- **Infinite Chest, Update-Tag:** Jeder Client, der den Chunk lädt, bekommt den ganzen Inhalt, obwohl das GUI eigene
  Pakete nutzt.
- **XP vom Client:** Der Server übernimmt höhere Lifetime-XP vom Client (gewollt, damit Fortschritt mitwandert). Ein
  veränderter Client kann sich so Level und Sterne-Auren geben. Challenges/Perks wählen bleibt OP-pflichtig.
- **Lockout-Lobby:** Jeder Spieler kann Bob hinzufügen oder entfernen (unter Freunden ok, auf offenen Servern
  vielleicht OP-pflichtig machen).
- **Trivia:** Die richtige Antwort geht an den Client.
- **Roulette:** `ROULETTE_LEAVE` wird gesendet, aber vom Server nicht behandelt. Harmlos.
- **Bob (Early Development Stage):** nur stichprobenartig gelesen, keine klaren Fehler. Unter Volllast wackeln
  Kampfszenen (`brawl_enderman_slope`, `sniper_duel`, `brawl_enderman`); bei `sniper_duel` gingen im roten Lauf alle
  48 Pfeile daneben – vielleicht lohnt ein Blick aufs Zielen unter Lag.

## Die Entscheidung, die du treffen musst: der Crafter

Fix 2 ändert spürbar das Spielverhalten: **Der Crafter (der automatische Vanilla-Werkbank-Block) stellt keine
Infinite Chest und keine Casino-Geräte mehr her.**

- **Warum:** Diese Items sind absichtlich gesperrt – die Infinite Chest braucht Level 20 und einen Perk, die
  Casino-Geräte muss man einmal beim Croupier kaufen. Die Sperre sitzt am Ergebnis-Slot der Werkbank. Der Crafter
  klickt aber nie auf diesen Slot und hat die Sperre deshalb für jeden umgangen.
- **Folge:** Wer diese Items automatisch herstellen wollte, kann das nicht mehr. Von Hand geht es wie bisher.
- **Deine Optionen:**
  1. So lassen und mit 1.1.4 veröffentlichen (der Changelog-Entwurf beschreibt genau das).
  2. Den Crafter nur für Spieler sperren, die die Freischaltung nicht haben (bräuchte einen Besitzer für den Crafter –
     den gibt es in Vanilla nicht; aufwendiger).
  3. Den Fix zurücknehmen und die Umgehung als „Feature“ akzeptieren.
- **Wenn du 1.1.4 willst:** Branch prüfen und auf `26.3` bzw. `26.3-lockout-bot` übernehmen, dann `mod_version` auf
  1.1.4 setzen – das löst die automatische Veröffentlichung aus. Das ist nach außen sichtbar und braucht dein Go.

## Modpack v4.1 (8.11.2026)

Client 9507938, Server-Pack 9507939 (Projekt 1653698), Changelog nur „Bug fixes“. Inhalt wie v4 (Vanilla plus Challenge Craft),
nur `config/bhmenu/bhmenu.properties`: `partner_id=4395` (vorher 4385), `pack_id=27138` (vorher leer), Banner-Text mit
Code „Kasax007“ wie bei Dreamcraft. Gebaut aus den v4-Dateien von CurseForge (Skript und Dateien in `$SP/cc41`). Die
Modpack-Beschreibung (Branch `26.3-lockout-bot`) nennt jetzt den Eintrag „Need a server?“ in Multiplayer.

