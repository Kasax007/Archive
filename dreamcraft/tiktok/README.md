# Dreamcraft 26.3 – Promo-TikTok

Schneller Short (ca. 44 s, 1080×1920, 30 fps, Englisch) für das Modpack Dreamcraft auf Minecraft 26.3.
Hook: Luftaufnahme einer Burg mit Titel „MINECRAFT 26.3 MODPACK“. Dann folgen Menü, Quest-Buch, Kirschblüten-Dorf,
Feuer-Magier, Mutant, Küche, Tech Reborn, Floß mit Hai, Nether und End. Endkarte: „FREE ON CURSEFORGE“.

| Datei | Inhalt |
| --- | --- |
| `dreamcraft_tiktok_captions_music.mp4` / `_captions_nomusic.mp4` | Untertitel eingebrannt, mit / ohne Musik |
| `dreamcraft_tiktok_clean_music.mp4` / `_clean_nomusic.mp4` | ohne Untertitel |
| `dreamcraft_tiktok.srt`, `dreamcraft_tiktok_voice.m4a` | Untertitel, reine Sprachspur |
| `dreamcraft_tiktok_post.txt` | Titel, Beschreibung, Link, Musik-Credit („Overworld“, Kevin MacLeod, CC BY 4.0), Hashtags |
| `dreamcraft_tiktok_contact_sheet.png` | Kontaktbogen |
| `stills/endcard_short.png` | Endkarte |

## Neu bauen

Die Werkzeuge sind aus `tamagotchi/tools` übernommen und angepasst (`dc.py` statt `tama.py`). Der Sprecher ist
Kokoro `am_michael` mit Tempo 0,95, im Schnitt ×1,06. Jeder Absatz wird mit Whisper geprüft.

```sh
SP=<Scratchpad>; export SP HF_HOME=$SP/hf VIRTUAL_ENV=$SP/tts
uv venv -p python3.12 $SP/tts && uv pip install torch kokoro soundfile faster-whisper "misaki[en]" pillow numpy "av==16.1.0" \
  "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
$SP/tts/bin/python tools/tts_kokoro.py short     # Stimme
python3 -I tools/endcard.py                       # Endkarte (Menü-Assets des Packs + Standbilder)
$SP/tts/bin/python tools/dc.py --plan             # Schnittplan
$SP/tts/bin/python tools/dc.py --deliver          # Render + Kopie hierher
```

Das Footage liegt in `$SP/film/<shot>/f%05d.png`. Gefilmt wird mit dem Film-Harness im Modpack-Repo
(`Modpack-Development`, Branch `26.3`, `tools/dctest`, `-Pscene=film`).
Shots: castle, village, vista, magic, mutant, kitchen, tech, raft, shark, nether, end, questbook, menu.
Dazu kommt `menu_land`, ein Hochformat-Ausschnitt aus dem Querformat-Standbild des Menüs, weil das Menü im
Hochformat gequetscht aussieht.
