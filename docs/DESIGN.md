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

## Character
- Classes: Knight (sword, wooden shield, chain), Berserker (greataxe, no shield, hide), Rogue (twin daggers, buckler, leather).
- HP = 30 + VIT x 7. Stamina = 40 + END x 6. Damage x (1 + (STR - 10) x 0.07).
- Level cost = 60 + 25 L + 3 L squared XP.
- Chest gear: Bat-Wing Cloak (area 2), Thrall Blade (3), Iron Kite Shield (5), Ember Daggers (6), Forge Axe (7), Draugr Mail (8). Boss: Sword of the Draugr.

## View
- 3D by default: tiles extruded in depth, back wall far behind, off-axis camera above the action so floors and ledge tops show. Sprites stay flat pixel art at z = 0. V or the 2D / 3D button switches to the flat view.

## Music
- Title: "dungeon_music_preview.mp3" streamed from `docs/music`. Falls back to generated music if the file is missing (single-file artifact).
- Areas: generated live. Seeded chord walk per area (key, mode, tempo, filter), a motif that mutates each phrase, drone, pad, bells, drips, echo.
- Boss: "The Jarl Rises" chiptune. Win: "Dungeon Complete" sting.
- Footsteps vary with armor weight.

## Not built yet
More dungeons, NPCs or shops, settings menu.
