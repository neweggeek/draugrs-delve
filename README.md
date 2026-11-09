# Draugr's Delve

A souls-like pixel dungeon side scroller that runs in the browser, on phone or PC. Ten areas, each built around one enemy and the lesson it teaches, ending with the Draugr Jarl.

![Key art](docs/concept/keyart.png)

## Play
Open `index.html` in any modern browser. No install, no build.
Keep the `docs/music` folder next to it for the title music (without it the game falls back to generated music).

| Action | PC | Phone |
|---|---|---|
| Move | A / D or arrows | pad |
| Jump | W / Space | JUMP |
| Attack (hold for heavy) | J or left click | ATK |
| Block (tap just before a hit to parry) | K or right click | BLOCK |
| Roll | L or Shift | ROLL |
| Drink flask | Q | HEAL |
| Cast fireball (after beating the Jarl) | F | FIRE |
| Rest at bonfire, open chest | E | USE |
| Drop through ledge | S | |
| Pause / sound | Esc / M | sound button |
| Switch 3D / 2D view | V | 2D / 3D button |

## Features
- 3D view: the dungeon is drawn in 3D with WebGL (blocks with depth, torch light, a camera looking down the hall), while the sprites stay pixel art. Press V or tap the 2D / 3D button for the classic flat view. Falls back to 2D if the browser has no WebGL.
- Stamina-based combat: light and heavy attacks, block, parry and riposte, roll with i-frames, guard break.
- Ten areas, one enemy type each: rats, bats, thralls, archers, spiders, slimes, wisps, shamblers, shieldbearers, the Jarl.
- Bonfires: rest to heal, refill flasks, level up and change gear. Resting brings monsters back.
- Die and your XP stays where you fell. Get back to it or lose it.
- Three classes (Knight, Berserker, Rogue), stat leveling (VIT, END, STR), gear from chests and the boss.
- Beat the Jarl to learn Fireball: a ranged spell that costs stamina, for your next run through the areas.
- Title screen theme (`docs/music/dungeon_music_preview.mp3`), generated dungeon music with a different key and mood per area, plus a boss theme.
- Progress saves in the browser.

## Test
```
pip install playwright
python -m playwright install chromium   # or set CHROME=/path/to/chrome
python tests/smoke_test.py
```

## Repo
- `index.html`: the game
- `tests/`: headless checks
- `tools/`: art and music generators used for the concept phase
- `docs/`: design notes, concept art, music
