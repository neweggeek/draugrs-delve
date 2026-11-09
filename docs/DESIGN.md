# Design

## Pillars
- Patience wins. Every enemy telegraphs, then leaves an opening.
- One area, one lesson. Each area introduces a single enemy mechanic.
- Readable on a phone. 320x176 pixel canvas, big touch buttons.

## Combat
- Stamina: light, heavy, roll and blocked hits drain it. Regen starts about 0.6 s after the last action, slower while blocking.
- Light attack: tap. Heavy: hold 14 frames. Attacks commit; late recovery can be cancelled into another action.
- Block: front hits only. Chip damage = dmg x (1 - absorb). Stamina cost = dmg x (100 - stability) / 28. Empty stamina = guard break (50 frame stagger).
- Parry: block raised within the shield's parry window (5 to 11 frames) when a parryable hit lands. Enemy staggers 80 frames; next hit is a riposte for 3x damage.
- Roll: 18 stamina, i-frames depend on armor weight (light / mid / heavy).
- Poise: enemies stagger when poise damage exceeds their poise.
- Fireball: unlocked by beating the Jarl. 30 stamina, 24 frame cast, flies straight, 34 damage (scales with STR), 20 poise damage. Shieldbearers block it from the front, glowing wisps ignore it.
- Flasks: 3 (4 after the Jarl). Heal 45% max HP, slow to drink. Potions refill one flask, or heal 35% when full.
- Movement: walk about 57 px/s, jump about 42 to 46 px.

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
- Deeper floors: wider, more mobs, mixed bodies, enemy HP +3.5 and damage +1.8 per floor past 10.
- Odd generated floors run right to left (bonfire on the right, exit on the left).
- Every 10th floor is a Jarl hall with a traited Jarl. The first Jarl gives the win screen and fireball, later ones lead on.
- Generated mobs never spawn in a dip or next to a pillar (they used to get stuck).

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
- Walking enemies step with a two-frame leg cycle; idle ones breathe.
- The hero also breaks into pixels on death. Areas fade in from black on load and respawn.
- Hero kicks up dust on jump, landing and roll.
- Below 25% HP: red screen edges throb with a heartbeat sound.

## Music
- Title: "dungeon_music_preview.mp3" streamed from `docs/music`. Falls back to generated music if the file is missing (single-file artifact).
- Areas: generated live. Seeded chord walk per area (key, mode, tempo, filter), a motif that mutates each phrase, drone, pad, bells, drips, echo.
- Boss: "The Jarl Rises" chiptune. Win: "Dungeon Complete" sting.
- Footsteps vary with armor weight.

## Inventory and loot
- Five slots: weapon, shield, armor, ring, amulet. Shield, ring and amulet can be left empty.
- Inventory (I key, BAG button, or pause and bonfire menus): worn gear on top, bag grid below, cooking parts at the bottom. Pick an item to wear it, pick a worn ring, amulet or shield to take it off. Gear can be changed anywhere.
- Stats screen (pause and bonfire menus): base stat, green gear bonus, total, then derived numbers.
- Rarity: COMMON (beige), RARE (blue), EPIC (purple), LEGENDARY (gold). Drops glow with a beam in their color, bigger for better rarity.
- Drops: chance = 10% + enemy XP / 600 (elites +50%). Rarity roll: 2% legendary, 10% epic, 28% rare, rest common, shifted toward better by 1 point per floor (cap 25) and 30 for elites. Only gear you do not own yet drops. Summons, split slimes and the Jarl do not roll.
- Loot pool: Bone Sword, Iron Ring, Bone Ring, Wolf Tooth (common); Bearded Axe, Round Shield, Wolf Pelt, Serpent Ring, Raven Charm (rare); Rune Blade, Frostfang, Bone Targe, Raven Leather, Ember Ring, Rune Stone (epic); Skullsplitter, Rune Mail, Allfather Ring, Thor's Hammer (legendary).
- Chest gear is rare or epic and never drops from monsters.

## Clarity
- A controls screen opens when a new game starts (keyboard or touch version) and from the pause menu (CONTROLS).
- Touch: MENU button at the top pauses (resume, inventory, stats, controls, quit). Gamepad: Start pauses, Select opens the bag.
- Title floor picker: A D one floor, Shift + A D ten floors (<< >> on touch, LB RB on a pad).
- The game saves when the tab is hidden or closed, so XP is not lost.

## Not built yet
NPCs or shops, settings menu, gear upgrades (the loot pool is all found by about floor 25), touch drop-down through ledges.
