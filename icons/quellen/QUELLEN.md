# Quellen, die in keinem Repo liegen

Diese Dateien braucht `build_pack.py`. Sie stammen aus veröffentlichten Modpack-Dateien oder wurden neu gezeichnet;
abgelegt am 13.11.2026. Die Modpack-Dateien liegen auf dem CurseForge-CDN unter
`mediafilez.forgecdn.net/files/<erste vier Ziffern der Datei-Nr.>/<Rest ohne führende Nullen>/<Dateiname>`.

| Datei | Herkunft | sha1 |
| --- | --- | --- |
| `challenge-craft_logo_3240.png` | Challenge Craft Modpack 26.3 v4.2 (CurseForge-Datei 9508554, Modrinth-Version QwknCvxT): `overrides/config/fancymenu/assets/final.png` | `db8678049e4ff10d4774a3130874f0d5c2f875c6` |
| `challenge-craft_schriftzug_2040x427.png` | dieselbe Modpack-Datei: `overrides/config/fancymenu/assets/cc_wordmark.png` | `865bf7ab23b31b4e7f6ed64f1f9aea2c5129b80b` |
| `challenge-craft_by-kasax_2048x298.png` | dieselbe Modpack-Datei: `overrides/config/fancymenu/assets/by_kasax.png` | `0692827bb70b77801b57b2539b6cce6262c00dc5` |
| `dreamcraft-forge_schriftzug_1440x1080.png` | Dreamcraft Forge 1.19.2-1.0.2 (CurseForge-Datei 3983512): `overrides/config/drippyloadingscreen/logofabricnostars.png` (der Name täuscht: das Bild zeigt „DREAMCRAFT FORGE“) | `8f4b84e6857f01e8479059676a4096e511cbdb7b` |
| `dreamcraft_fenster-icon_32.png` | Dreamcraft 1.20.1-1.0.39 (CurseForge-Datei 5042444): `overrides/config/fancymenu/minecraftwindow/icons/icon32x32.png` | `c77816093871d3cb785113cb4d2d9a82e1db4861` |
| `dreamcraft_fenster-icon_16.png` | dieselbe Datei: `…/minecraftwindow/icons/icon16x16.png` | `b367f9b9537fdb2b1d51c52bbf40f0e0eca9b738` |
| `tamacraft_icon_render_1024.png` | neu gezeichnet mit `icons/render_tamacraft.py` aus `tools/petart/icon.py` im Repo `tamagotchi` (Commit 4f10738), bei 4096 px gezeichnet und auf 1024 px verkleinert | `672fb7b9d9bee8a617de91c185c4616892934940` |

## Was in den alten Packs sonst noch lag

Durchgesehen am 13.11.2026: Dreamcraft Fabric 1.17.1, 1.18.1, 1.19, 1.19.2 und 1.20.1, Dreamcraft Forge 1.19.2,
Lightspeed Performance 1.0.1 und 1.0.2, Beautifully 1.0.3, Challenge Craft Modpack v4.2 (CurseForge und Modrinth).

- Das Logo „DREAMCRAFT FABRIC“ mit Mond und Sternen liegt im Repo von Quest Icons
  (`assets/questsicons/textures/item/logo_fabric.png`) und in den alten Packs als `welcome.png`.
- Der Schriftzug ohne Mond und Sterne (`logofabricnostars.png` in den Fabric-Packs) ist bildgleich mit
  `loading_logo.png` im Pack für 26.3.
- Lightspeed Performance, Beautifully und Dreamcraft 1.17.1 enthalten keine Bilder.
- Eine größere Fassung des Dreamcraft-Icons (800 px) oder des Quest-Icons-Icons (800 px) war nirgends dabei.
