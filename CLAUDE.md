# Draugr's Delve: notes for Claude Code

Souls-like pixel dungeon side scroller. Plain HTML5 canvas + WebAudio, no build step, no dependencies.

## Layout
- `index.html`: the whole game (HTML, CSS, JS in one file). This is the source of truth and the deliverable.
- `tests/smoke_test.py`: headless Playwright checks for every core mechanic. Run after every change.
- `tools/concept_art.py`: renders the concept key art and sprite PNGs from the same text-grid sprites.
- `tools/chiptune_tracks.py`: renders the original MP3 tracks in `docs/music/`.
- `docs/DESIGN.md`: game design: combat rules, enemy lessons, classes, gear, numbers.

## Run
- Play: open `index.html` in a browser (or `python -m http.server` and browse to it).
- Test: `python tests/smoke_test.py` (set `CHROME=/path/to/chrome` to use a system browser). Must print ALL PASSED.

## Code map (sections inside index.html, marked `// ===== name =====`)
Core setup, Bitmap font (3x5), Sprites (text grids in `GRIDS`, palette `PAL`), Levels (`LEVELS`, `buildLevel`),
physics (`moveBody`, one-way platforms `=`), Background prerender (`paintBg`: `bgWall` back wall, `bg` full 2D backdrop),
3D view (`V3`: WebGL draws the level as blocks on canvas `#g3` under the see-through 2D canvas), Audio (songs, `SFX`, generative music `GEN`/`genBar`),
Extra sprites, Hero sprites (`HERO` part grids, `paintHero` builds the hero each frame from head, armor torso, pose legs, swinging weapon and shield), Classes/gear (`CLASSES`, `ITEMS` with `rar` rarity and `b` stat bonus, `stat(k)`, `CH` = saved character), Input, Game state, Player (`updatePlayer`, `resolveHit`),
Enemies shared (`hitEnemy`, `startAtk`/`runAtk` attack phases wind/act/rec), Enemy mechanics (one `AI.x` + attack defs per enemy),
World (`updateWorld`), Menus and UI flow, Rendering, Main loop, test hook `window.__dd`.

## Conventions
- Internal resolution 320x176, 16px tiles, 60 steps/second fixed timestep. Frame counts are in steps.
- 3D view: game logic stays 2D. Only the level tiles and back wall are 3D; actors, effects, lights and HUD are still drawn on the 2D canvas, which lines up with the z = 0 plane. Something drawn on the back wall in 2D must go through `V3.pt(x, y)` (see torches). View choice saved in localStorage `dd_view`.
- Enemies only deal damage through attacks (no contact damage). New attacks: add a def `{ wind, act, rec, dmg, parry, unblock, red, box, start, during, end, next, cd }` and call `startAtk`.
- Telegraphs: white flash = blockable, red flash (`red: true`, `unblock: true`) = must roll.
- Level ops: `[char, col, row, count, height]`. Chars: `#` wall, `=` ledge, `T` torch, `c` XP shard, `p` potion, `G` chest, mob letters r b t a s e w h k J.
  Bonfire (col 4) and exit door are added automatically.
- Jump reach: about 42 to 46 px. Keep ledges 32 px (2 tiles) apart vertically.
- Save key in localStorage: `dd2`. New save fields get defaults in `loadSave` so old saves keep working; bump the key only if that is not possible.
- Text in the game uses the bitmap font: uppercase letters, digits and `! : . + - ' , / ? %` only.
- Never use em dashes in code comments, UI text or docs.
- Mobile matters: every feature needs a touch path (on-screen buttons or tapping `uiRects`).

## Publishing
Bump `VERSION` (top of the script, shown as a watermark on screen) in every PR that changes the game.
The game is also published as a claude.ai artifact (single file). Re-publish `index.html` after changes.
The title music is the only external file (`docs/music/dungeon_music_preview.mp3`); the game must keep working without it.
