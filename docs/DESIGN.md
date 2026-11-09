# Design

## Pillars
- Patience wins. Every enemy telegraphs, then leaves an opening.
- One area, one lesson. Each area introduces a single enemy mechanic.
- Readable on a phone. 320x176 pixel canvas, big touch buttons.

## Combat
- Stamina: light, heavy, roll, jump (8) and blocked hits drain it. Regen starts about 0.75 s after an attack, slower while blocking. No stamina, no jump.
- Pace (V13): combat is slow and deliberate. Player wind-up x1.35 and recovery x1.3 on every weapon (`PACE`), enemy wind-up and recovery x1.15. Hitstop 5 / 8 / 12 frames (light / heavy / crit). Stagger 24 frames.
- Light attack: tap. Heavy: hold 14 frames. Attacks commit: a buffered action only cuts in for the last quarter of the recovery.
- Combo: a light swing chained out of that late window builds a 3 hit string. Each link winds up 15% faster and hits 15% harder (up to +30%). A heavy resets it.
- Block: front hits only. Chip damage = dmg x (1 - absorb). Stamina cost = dmg x (100 - stability) / 28. Empty stamina = guard break (50 frame stagger).
- Parry: block raised within the shield's parry window (5 to 11 frames) when a parryable hit lands. Enemy staggers 80 frames; next hit is a riposte for 3x damage.
- Roll: 18 stamina, i-frames depend on armor weight (light / mid / heavy).
- Poise: enemies stagger when poise damage exceeds their poise.
- Fireball: learned for 600 XP at a bonfire (MAGIC) or free by beating the Jarl. 30 stamina, flies straight, 34 damage (scales with STR), 20 poise damage. Shieldbearers block it from the front, glowing wisps ignore it.
- Charge: hold FIRE. Full charge takes 60 steps and up to 12 more stamina; walk slowly while charging, roll cancels. Charge c (0 to 1) gives size 6 to 12 px, damage x(1 + 1.5c), speed 3.4 + c, poise 20 x(1 + 2c), burn 40 x(1 + c). A tap throws a plain fireball.
- Magic skills (bonfire, MAGIC, paid in XP): EMBER (3 ranks, +25% damage each), KINDLE (3, full charge 12 steps sooner each), FOCUS (3, -15% stamina each), INFERNO (2, a full charge bursts for half damage in 30 / 42 px), TWIN FLAME (1, a full charge throws three fireballs at 70% damage). Saved in `CH.sk`.
- Flasks: 3 (4 after the Jarl). Heal 45% max HP, slow to drink. Potions refill one flask, or heal 35% when full.
- Movement: walk about 47 px/s with slow start and stop. Turning in the air is not possible and air steering is weak, so jumps commit. Heavier gravity (0.34) and a stronger jump (5.6) keep the same reach (about 39 px tap, 46 px held) with less hang time. Landing slows you for 4 frames, a long fall for 14.

## Enemies (area: lesson)
1. Crypt Rat: telegraphed lunge then long recovery. Space and punish.
2. Bone Bat: screech, then dive, then dazed on the floor. Roll the dive.
3. Skeleton Thrall: 3-hit parryable combo, long recovery after the third.
4. Skull Archer: aimed arrows, backsteps, kicks when cornered. Shield up and walk in.
5. Grave Spider: drops when you pass under, web spit stops your roll.
6. Ember Slime: hop slam, fire patches go through block, splits in two on death.
7. Torch Wisp: invulnerable while glowing, dash, then dims and can be hit.
8. Draugr Shambler: parryable swipe and a red unblockable slam.
9. Shieldbearer: blocks all frontal light hits, turns slowly. Heavy breaks guard; parry the bash.
10. Draugr Jarl: 380 HP. Two-hit combo, red charge into the wall (stuns him), frost waves, leaps onto ledges. Phase 2 at 50%: faster, double waves, summons two thralls.

## Every mob has a rule (strategy)
- Crypt Rat: PACK. A rat near another rat winds up and recovers fast; alone it is slow. A hurt rat squeals and wakes rats nearby. Lure one away.
- Bone Bat: EVASIVE. Melee misses it in the air. Roll the dive, hit it while dazed, or burn it.
- Skeleton Thrall: REASSEMBLES. The first death leaves a bone pile that rises at half HP after about 4 s. Light hits bounce; a heavy or a fireball crushes it.
- Skull Archer: block late (parry timing) to reflect an arrow back for heavy damage.
- Grave Spider: below 45% HP it climbs its thread and heals up to 80%. Finish it fast.
- Ember Slime: fire feeds it (fireball heals it).
- Torch Wisp: cannot be hurt while glowing.
- Draugr Shambler: does not flinch while winding up (no poise damage). Hits during the recovery after its red slam do double damage.
- Shieldbearer: blocks frontal light hits. Heavy breaks the guard.
- Green Slime (g): poison hop and poison puddles. Heals quickly when not hit for under 2 s. Kill it in one push.
- Blue Slime (u): ice skin. Light hits do a quarter damage and no poise; heavy hits do 1.25x and double poise; fire 1.5x. Lands on ice that freezes your feet (slow, no roll).
- Red Slime (v): quick double hops. Below 35% HP it swells for 80 frames (red flash, cannot be hurt) and bursts for 30 damage around it. Roll away.
- Spider Warrior (W): two-slash parryable combo, pounce from range, and a counter STANCE. A frontal hit on the stance triggers a red riposte; a hit from behind does double, a fireball breaks it.
- Spider Queen (Q): mini boss on floors 17, 27, 37 and so on. Lays two eggs (hatch into spiderlings). While any egg lives she takes a quarter damage. Web fan (block), parryable bite, red leg sweep along the floor (jump or roll).

## Mob movement
- Walking mobs hop walls one or two tiles high (so they leave dips), jump up to a ledge you stand on, and step down when you are below them. The Jarl keeps his own leap.

## Floors
- 100 floors. 1 to 10 are hand built (one lesson each, Jarl on 10). 11 to 100 are generated from a seed, so each floor is the same every visit.
- Areas are long: hand built areas are about 82 tiles (a mirrored second half), generated floors 70 to 110 tiles. Mob count scales with width.
- Rest shrine: in the middle of every area but boss halls. A safe zone 7 tiles wide marked by standing stones: no damage, monsters are pushed out, shots fizzle, HP slowly refills, calm music plays. Resting there is a bonfire (level up, cook, refill, monsters return) and you wake there after death until you rest at the bonfire again (`CH.cp`).
- Deeper floors: wider, more mobs, mixed bodies, enemy HP +3.5 and damage +1.8 per floor past 10.
- Odd generated floors run right to left (bonfire on the right, exit on the left).
- Every 10th floor is a Jarl hall with a traited Jarl. The first Jarl gives the win screen and fireball, later ones lead on.
- Generated mobs never spawn in a dip or next to a pillar (they used to get stuck).
- Spike traps (`^`): iron plates with steel points on the floor. Stepping on them costs 12% max HP + 4, staggers you and throws you up. Rolling does not help: jump over. One tile wide, two tiles past floor 30. In areas 3, 6, 8 and on generated floors.

## Ending and New Game+
- Floor 100's Jarl shows the ending: hero, play time, deaths, gear found.
- Any button then starts New Game+ at floor 1: keep level, gear and fireball; chests refill; floors lock again.
- Each NG+ cycle: foe HP and XP x(1 + 0.6 NG), foe damage x(1 + 0.4 NG). Shown as NG+N on the banner and title.

## Mix-and-match monsters
- Any body can carry traits. First trait tints the sprite; the name shows above it.
- IRON: tough, hard to stagger. SWIFT: short wind-up and recovery. GIANT: big, hits hard. EMBER: leaves fire where it dies. FROST: hits drain stamina even on block. CURSED: heals when it hits you.
- ELITE (floor 15 and down, about 1 in 10): gold, always two more traits, drops 3 parts and a flask. Loot goes through `dropTable(e)`.

## Cooking
- Kills drop parts: MEAT (rats, bats, spiders), BONE (thralls, archers, shambler, shieldbearers), JELLY (slimes), ASH (wisps).
- Bonfire, COOK: one meal at a time, lasts until you die. Roast (2 meat): max HP x1.3. Broth (2 bone): damage taken x0.75. Ember jelly (jelly + meat): stamina regen x1.5. Ash bread (ash + bone): damage x1.25.

## Character
- Classes: Knight (sword, wooden shield, chain), Berserker (greataxe, no shield, hide), Rogue (twin daggers, buckler, leather).
- Stats: VIT, END, STR, DEX. Each stat = level-up points + bonus from worn gear (`stat(k)`).
- HP = 30 + VIT x 7. Stamina = 40 + END x 6. Damage x (1 + (STR - 10) x 0.07). Crit chance = 3% + (DEX - 10) x 2%, capped at 40%, crit deals 1.5x.
- Class DEX: Knight 10, Berserker 8, Rogue 13.
- Level cost = 60 + 25 L + 3 L squared XP.
- Chest gear: Bat-Wing Cloak (area 2), Thrall Blade (3), Iron Kite Shield (5), Ember Daggers (6), Forge Axe (7), Draugr Mail (8). Boss: Sword of the Draugr.

## View
- 3D by default: tiles extruded in depth, back wall far behind, off-axis camera above the action so floors and ledge tops show. Sprites stay flat pixel art at z = 0. V or the 2D / 3D button switches to the flat view.

## Feel
- Hits: hitstop, screen shake, sparks, damage numbers. Enemies flash white on hit.
- Enemies squash on wind-up, stretch on the strike, squash on landing and when hit.
- Dead enemies break into their own sprite pixels, which bounce on the floor.
- Look follows the concept art (`docs/concept/`): cold mossy stone, deep arches with portcullises, pillars, hanging chains, stone slab ledges.
- Monsters, items and the hero body are painted from shapes (`RIG`, `pEll`/`pLimb`/`pPoly`) with shaded color ramps and dark outlines. Each monster has idle, walk (4 frames), wind-up, strike, recovery and hurt frames; the hero has a posed walk cycle, cape and class head (knight helm, horned berserker, hooded rogue).
- The hero also breaks into pixels on death. Areas fade in from black on load and respawn.
- Hero kicks up dust on jump, landing and roll.
- Below 25% HP: red screen edges throb with a heartbeat sound.

## Music
- Title: "dungeon_music_preview.mp3" streamed from `docs/music`. Falls back to generated music if the file is missing (single-file artifact).
- Areas: generated live. Seeded chord walk per area (key, mode, tempo, filter), a motif that mutates each phrase, drone, pad, bells, drips, echo.
- 16 area themes. When awake monsters are near, a fight layer (war drums and a low pulse) joins the area music.
- Rest shrine: "Shrine Lullaby" (F major, 72 BPM, harp arps and a slow hymn).
- Boss: "The Jarl Rises" chiptune. Win: "Dungeon Complete" sting.
- Footsteps vary with armor weight.

## Inventory and loot
- Five slots: weapon, shield, armor, ring, amulet. Shield, ring and amulet can be left empty.
- Inventory (I key, BAG button, or pause and bonfire menus): worn gear on top, bag grid below, cooking parts at the bottom. Gear can be changed anywhere.
- Bag input, the same everywhere: click or tap an item to see its info. Click or tap it again, right click it, press Enter (pad A) or ACTIONS for the action menu: EQUIP (or TAKE OFF for a ring, amulet or shield), COMBINE, SALVAGE, CANCEL. Actions that can not be used stay greyed with the reason. Esc / B / right click outside closes it.
- Stats screen (pause and bonfire menus): base stat, green gear bonus, total, then derived numbers.
- Rarity: COMMON (beige), RARE (blue), EPIC (purple), LEGENDARY (gold). Drops glow with a beam in their color, bigger for better rarity.
- Drops: chance = 10% + enemy XP / 600 (elites +50%). Rarity roll: 2% legendary, 10% epic, 28% rare, rest common, shifted toward better by 1 point per floor (cap 25) and 30 for elites. New gear drops first; once every item of a rarity is found, copies drop (fodder for combine or salvage). Summons, split slimes and the Jarl do not roll.
- Loot pool: Bone Sword, Iron Ring, Bone Ring, Wolf Tooth (common); Bearded Axe, Round Shield, Wolf Pelt, Serpent Ring, Raven Charm (rare); Rune Blade, Frostfang, Bone Targe, Raven Leather, Ember Ring, Rune Stone (epic); Skullsplitter, Rune Mail, Allfather Ring, Thor's Hammer (legendary).
- Chest gear is rare or epic and never drops from monsters.
- Hover an item (mouse) for a tooltip: stats, gear bonus, status effects, weight, compare with worn (green better, red worse), salvage value. The panel under the grid shows the same for the picked item. A yellow dot marks gear found since you last looked. The grid scrolls (arrows, wheel, side buttons).

## Weight
- Every item has a weight in KG (rings and amulets 1, daggers 2, mail 15). Everything in the bag counts, worn or not.
- Carry limit = 30 + 3 x STR (60 at STR 10). Over it you are OVERLOADED: walk at 65%, slow short roll (26 frames, i-frames 3 to 11), roll costs 27 stamina, stamina regen x0.6. The HUD and bag say so.
- Fix it by salvaging, combining, or levelling STR (gear STR counts too).

## Crafting
- Salvage (action menu, or X / pad Y): asks YES / NO, then breaks one copy into rune dust: 3 / 8 / 20 / 50 by rarity. Copies share one upgrade level, so only the last copy adds +4 per upgrade level. Your only worn weapon or armor can not be salvaged (equip another first); a worn ring, amulet or shield must be taken off first.
- Combine (action menu, or C / pad X) opens its own screen: the item to upgrade on top, every item that can melt into it below (same slot, never your only worn copy). Picking one previews the result (new level, stats before and after, weight saved, a red warning if the fodder is upgraded or rarer). Pick it again or press COMBINE: it always works and shows a SUCCESS card. Gain is +1, plus half the melted item's upgrades when it is a different item, up to +10.
- Upgrade +N: weapon damage x(1 + 0.08N), shield block +1% and stability +3 per level, armor defense +1.2% per level, ring and amulet stats +1 every 2 levels, other gear bonuses +1 every 3 levels, status buildup x(1 + 0.08N).
- Rune altar on floors 3, 6, 9, ... (not boss halls), next to the bonfire. Craft a random item of a chosen rarity for 15 / 40 / 100 / 250 dust (unowned first), or temper worn weapon or armor for 30 + 25 x level x (rarity + 1) dust.
- Dust also comes from kills (25% chance, elites and Jarls always, more on deep floors) and from chests that have nothing left to give.

## Durability
- Weapon, shield and armor wear down. Weapon: 1 per hit landed (1.5 heavy). Shield: 1 + damage / 25 per block. Armor: 1 per hit taken.
- Hits to wear out, by rarity: weapon 220 / 300 / 400 / 550, shield 90 / 130 / 180 / 250, armor 70 / 100 / 140 / 200. Rings and amulets never wear.
- Under 30% the item is DAMAGED (stats x0.85). At 0% it is BROKEN (attack, block, stability or defense x0.5). It is not lost.
- The HUD warns, bag cells show a bar (red ! when broken), the tooltip shows the percent.
- Bonfire REPAIR fixes everything you carry: (missing % x (rarity + 1) / 8) dust per item, rounded up. Short on dust, each missing dust costs 4 XP.
- Combine, temper and picking up a fresh copy also restore an item.

## Status effects
- Four effects, same rules for the hero and monsters. Hits fill a meter to 100; the meter drains slowly. When it fills:
  BLEED bursts for 20% max HP on the hero (25% on monsters, 8% on Jarls); POISON ticks 2% max HP every half second for 6 s;
  BURN ticks 2.5% every quarter second for 2.5 s; FROST slows for 3.3 s (hero walks at 60% with half stamina regen, monsters act a third slower).
- Blocking still fills meters, scaled by what the shield lets through. Elites fill 50% faster. A flask cures poison and burn.
- Monsters: rats, bats, thralls, archers, shield knights and the Jarl bleed you; spiders and shamblers poison; ember slimes and wisps burn; Jarl frost waves freeze. Frost and ember traits add frost or burn.
- Monster resist: skeletons resist bleed 50%, slimes are immune to burn, wisps to bleed, poison and burn, frost and ember traits to their own element, Jarls at least 50% to all.
- Gear: weapons and some rings put meters on monsters (Bone Sword bleed, Rune Blade frost, Forge Axe burn, Serpent Ring poison, ...). Armor and trinkets resist (Wolf Pelt bleed 40%, Raven Leather poison 40%, Rune Mail frost 40%, Thor's Hammer burn 40%, ...). Fireball adds burn. The stats screen sums it up.

## Clarity
- A controls screen opens when a new game starts (keyboard or touch version) and from the pause menu (CONTROLS).
- Touch: MENU button at the top pauses (resume, inventory, stats, controls, quit). Gamepad: Start pauses, Select opens the bag.
- Title floor picker: A D one floor, Shift + A D ten floors (<< >> on touch, LB RB on a pad).
- The game saves when the tab is hidden or closed, so XP is not lost.
- Touch: the USE button turns into DROP on a one-way ledge.

## Not built yet
NPCs or shops, settings menu.
