"""Headless smoke test for Draugr's Delve.

Run:  pip install playwright && python -m playwright install chromium
      python tests/smoke_test.py            (uses Playwright's Chromium)
      CHROME=/usr/bin/google-chrome python tests/smoke_test.py

Every check prints PASS or FAIL. Exit code 1 if anything fails.
Uses the window.__dd test hook and the page's global lexical bindings (MAP, SPAWNS, startAtk, ...).
"""
import asyncio, os, sys, pathlib
from playwright.async_api import async_playwright

URL = pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").as_uri()
fails = []

def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))
    if not ok: fails.append(name)

async def main():
    async with async_playwright() as p:
        kw = {"args": ["--autoplay-policy=no-user-gesture-required"]}
        if os.environ.get("CHROME"): kw["executable_path"] = os.environ["CHROME"]
        b = await p.chromium.launch(**kw)
        pg = await b.new_page(viewport={"width": 960, "height": 528})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        ev = pg.evaluate
        await pg.goto(URL); await pg.wait_for_timeout(400)
        check("title screen", await ev("__dd.state") == "title")
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(200)
        check("class select", await ev("__dd.state") == "class")
        await pg.wait_for_timeout(600)
        check("title music plays from mp3", await ev("Music.cur === TITLE_SONG && titleOk && !titleEl.paused && titleEl.currentTime > 0"))
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(400)
        check("new game starts area 1", await ev("[__dd.state, __dd.levelIdx]") == ["play", 0])
        check("title music stops in game", await ev("titleEl.paused && !!Music.cur.gen"))

        # core actions
        await ev("for (const e of __dd.enemies) e.dead = true")
        await pg.keyboard.press("KeyJ"); await pg.wait_for_timeout(100)
        check("light attack", await ev("__dd.P.state === 'atk' && !__dd.P.heavy"))
        await pg.wait_for_timeout(700)
        await pg.keyboard.down("KeyJ"); await pg.wait_for_timeout(400); await pg.keyboard.up("KeyJ"); await pg.wait_for_timeout(50)
        check("heavy attack (hold)", await ev("__dd.P.state === 'atk' && __dd.P.heavy"))
        await pg.wait_for_timeout(1500)
        await pg.keyboard.press("KeyL"); await pg.wait_for_timeout(80)
        check("roll gives i-frames", await ev("__dd.P.state === 'roll' && __dd.P.iframes > 0"))
        await pg.wait_for_timeout(700)
        await pg.keyboard.down("KeyK"); await pg.wait_for_timeout(150)
        check("block", await ev("__dd.P.blocking"))
        await pg.keyboard.up("KeyK")
        await ev("__dd.P.hp = 30"); await pg.keyboard.press("KeyQ"); await pg.wait_for_timeout(1200)
        check("flask heals", await ev("__dd.P.hp > 30 && __dd.P.flasks === 2"))

        # jump clears a 32px ledge even on a tap
        await ev("__dd.tp(4*16, 130); window.__minY = 999; const L=()=>{ window.__minY = Math.min(window.__minY, __dd.P.y); requestAnimationFrame(L)}; L();")
        await pg.wait_for_timeout(300); await pg.keyboard.press("Space"); await pg.wait_for_timeout(900)
        h = 130 - await ev("window.__minY")
        check("tap jump clears ledge", h > 34, f"{round(h)}px")

        # bonfire, level up, equipment
        await ev("__dd.newGame('knight',0); __dd.CH.xp = 1000"); await pg.wait_for_timeout(200)
        await pg.keyboard.press("KeyE"); await pg.wait_for_timeout(100)
        check("rest opens bonfire menu", await ev("__dd.state === 'menu' && __dd.menu.kind === 'bonfire'"))
        for k in ["Enter", "Enter"]: await pg.keyboard.press(k); await pg.wait_for_timeout(50)
        check("level up spends XP", await ev("__dd.CH.lvl === 2 && __dd.CH.vit === 11"))
        await pg.keyboard.press("Escape"); await pg.keyboard.press("Escape"); await pg.wait_for_timeout(80)
        check("leave menu", await ev("__dd.state") == "play")

        # parry a thrall, then riposte
        await ev("__dd.newGame('knight',2)"); await pg.wait_for_timeout(200)
        await ev("""(()=>{ window.__T = __dd.enemies.find(e => e.y > 120); const t = window.__T; __dd.tp(t.x - 24, 130); __dd.P.face = 1;
          const loop = () => { const e = window.__T; if (!e || e.dead) return;
            if (e.st === 'wind' && e.t2 <= 4 && !window.__blk) { window.__blk = true; dispatchEvent(new KeyboardEvent('keydown', {code:'KeyK'})); }
            if (e.parried && window.__blk === true) { window.__blk = 'done'; window.__parry = true; dispatchEvent(new KeyboardEvent('keyup', {code:'KeyK'}));
              dispatchEvent(new KeyboardEvent('keydown', {code:'KeyJ'})); setTimeout(()=>dispatchEvent(new KeyboardEvent('keyup', {code:'KeyJ'})), 60); }
            requestAnimationFrame(loop); }; loop(); })()""")
        await pg.wait_for_timeout(2800)
        check("parry", await ev("!!window.__parry"))
        check("riposte does big damage", await ev("window.__T.dead || window.__T.hp <= 20"), str(await ev("window.__T.hp")))

        # enemy mechanics
        await ev("__dd.newGame('berserker',8)"); await pg.wait_for_timeout(200)
        await ev("const k=__dd.enemies[0]; k.face=-1; k.cd=9999; k.agro=true; __dd.tp(k.x - 20, 130); __dd.P.face=1; __dd.P.hp=9999")
        await pg.wait_for_timeout(200); await ev("__dd.enemies[0].cd=9999")
        await pg.keyboard.down("KeyJ"); await pg.wait_for_timeout(350); await pg.keyboard.up("KeyJ"); await pg.wait_for_timeout(700)
        check("heavy breaks shieldbearer guard", await ev("__dd.enemies[0].st") == "gbrk")
        await ev("__dd.newGame('knight',7)"); await pg.wait_for_timeout(200)
        await ev("const h=__dd.enemies[0]; __dd.tp(h.x - 22, 130); __dd.P.face=1; __dd.P.hp=100; startAtk(h, SH_SLAM)")
        await pg.keyboard.down("KeyK"); await pg.wait_for_timeout(1200); await pg.keyboard.up("KeyK")
        check("red slam ignores block", await ev("__dd.P.hp < 100"))
        await ev("__dd.newGame('knight',5)"); await pg.wait_for_timeout(200)
        await ev("killEnemy(__dd.enemies[0])"); await pg.wait_for_timeout(50)
        check("slime splits", await ev("__dd.enemies.filter(e=>e.small).length") == 2)

        # chest, potion, death drop
        await ev("__dd.newGame('knight',1)"); await pg.wait_for_timeout(200)
        await ev("__dd.tp(SPAWNS.chest.x - 2, SPAWNS.chest.y - 8)"); await pg.wait_for_timeout(400)
        await pg.keyboard.press("KeyE"); await pg.wait_for_timeout(150)
        check("chest gives gear", await ev("__dd.CH.inv.includes('cloak')"))
        await ev("__dd.P.hp = 40; const pk = pickups.find(p=>p.kind==='flask'); __dd.tp(pk.x, pk.y - 2)"); await pg.wait_for_timeout(300)
        check("potion picks up at full flasks", await ev("__dd.P.hp > 40"))
        await ev("__dd.newGame('knight',0); __dd.CH.xp = 123"); await pg.wait_for_timeout(200)
        await ev("__dd.tp(300, 100); __dd.P.hp = 1"); await pg.wait_for_timeout(300)
        await ev("resolveHit({x: __dd.P.x + 20, w: 4}, {dmg: 50})"); await pg.wait_for_timeout(3000)
        check("death drops XP", await ev("__dd.CH.xp === 0 && __dd.CH.drop && __dd.CH.drop.xp === 123"))
        await ev("__dd.tp(__dd.CH.drop.x, __dd.CH.drop.y - 6)"); await pg.wait_for_timeout(400)
        check("XP recovered", await ev("__dd.CH.xp === 123 && !__dd.CH.drop"))

        # music
        check("area music is generated", await ev("!!(Music.cur && Music.cur.gen)"))

        # fireball: locked until the Jarl is beaten, then hits enemies
        await ev("__dd.newGame('knight',0); for (const e of __dd.enemies) e.dead = true; __dd.tp(300, 100)"); await pg.wait_for_timeout(500)
        await pg.keyboard.press("KeyF"); await pg.wait_for_timeout(300)
        check("fireball locked before the Jarl", await ev("__dd.P.state !== 'cast' && !__dd.projs.some(p => p.mine)"))
        await ev("""__dd.CH.beat = true; __dd.P.hp = 9999; __dd.P.face = 1; window.__fb = false;
          const t = makeEnemy('t', 0, 0); t.x = __dd.P.x + 50; t.y = __dd.P.y + __dd.P.h - t.h; t.cd = 999; __dd.enemies.push(t); window.__tgt = t;
          const L = () => { if (__dd.projs.some(p => p.kind === 'fireball')) window.__fb = true; requestAnimationFrame(L); }; L();""")
        await pg.keyboard.press("KeyF"); await pg.wait_for_timeout(700)
        check("fireball casts after the Jarl", await ev("window.__fb"))
        check("fireball damages enemy", await ev("window.__tgt.hp < window.__tgt.maxhp"), str(await ev("[window.__tgt.hp, window.__tgt.maxhp]")))

        # boss: leap to ledge, then kill for the win screen
        await ev("__dd.newGame('knight',9)"); await pg.wait_for_timeout(200)
        await ev("__dd.tp(ARENA_X + 60, 130); __dd.P.hp = 9999"); await pg.wait_for_timeout(2200)
        # land on the ledge first, then let the boss choose (it only leaps once you stand up there)
        await ev("__dd.tp(15*16, 65); __dd.P.hp = 9999; __dd.boss.atk = null; __dd.boss.st = 'idle'; __dd.boss.cd = 999"); await pg.wait_for_timeout(250)
        await ev("__dd.P.hp = 9999; __dd.boss.atk = null; __dd.boss.st = 'idle'; __dd.boss.cd = 0; window.__leap = false; const L=()=>{ if (__dd.boss.atk === J_LEAP) window.__leap = true; requestAnimationFrame(L)}; L();")
        await pg.wait_for_timeout(2500)
        check("boss leaps after you on a ledge", await ev("window.__leap"))
        await ev("killEnemy(__dd.boss)"); await pg.wait_for_timeout(2600)
        check("win screen and legendary sword", await ev("__dd.state === 'win' && __dd.CH.inv.includes('draugr')"))

        # 3D view: WebGL level under the 2D layer, V toggles 2D and back
        if await ev("V3.ok"):
            await ev("localStorage.removeItem('dd_view')")
            check("3D view on by default", await ev("V3.on && document.body.classList.contains('v3d')"))
            await pg.keyboard.press("KeyV"); await pg.wait_for_timeout(100)
            check("V switches to 2D", await ev("!V3.on && getComputedStyle(document.getElementById('g3')).display === 'none'"))
            await pg.click("#view"); await pg.wait_for_timeout(100)
            check("view button switches back to 3D", await ev("V3.on"))
        else:
            print("SKIP 3D checks (no WebGL in this browser)")

        # hero is drawn from parts: every class, weapon, shield and armor paints pixels
        n = await ev("""(() => { let ok = 0, tot = 0; const W = Object.keys(ITEMS).filter(k => ITEMS[k].slot === 'w'), Sh = Object.keys(ITEMS).filter(k => ITEMS[k].slot === 's'), A = Object.keys(ITEMS).filter(k => ITEMS[k].slot === 'a');
          for (const cls of CLASS_KEYS) for (const w of W) for (const s of Sh) for (const a of A) { tot++; paintHero({ cls, w, s, a, legs: 'walk1', A: -60, block: s !== 'none' });
            const d = hb.getImageData(0, 0, 48, 40).data; let px = 0; for (let i = 3; i < d.length; i += 4) if (d[i]) px++; if (px > 120) ok++; } return ok === tot; })()""")
        check("hero paints with every gear combo", n)
        # juice: death shatters into sprite pixels, squash and stretch, low HP heartbeat
        n = await ev("(() => { const e = makeEnemy('t', 10, 5); const before = particles.length; shatter(e); return particles.length - before; })()")
        check("dead enemy shatters into its pixels", n > 40, f"{n} pixels")
        sq = await ev("(() => { const e = makeEnemy('t', 10, 5); startAtk(e, { wind: 20, act: 10, rec: 10 }); e.t2 = 5; const a = enemyScale(e); e.st = 'act'; e.t2 = 10; const b = enemyScale(e); e.st = 'idle'; e.flash = 0; e.land = 0; const c = enemyScale(e); return [a[0] > 1 && a[1] < 1, b[0] < 1 && b[1] > 1, c[0] === 1 && c[1] === 1]; })()")
        check("enemy squash on wind-up, stretch on strike", sq == [True, True, True], str(sq))
        check("low HP heartbeat", await ev("(() => { const s = P.state, h = P.hp; P.state = 'free'; P.hp = 1; const a = lowHP(); P.hp = maxHP(); const b = lowHP(); P.state = s; P.hp = h; return a && !b; })()"))
        check("no page errors", not errs, "; ".join(errs[:3]))
        await b.close()

asyncio.run(main())
print(f"\n{'ALL PASSED' if not fails else str(len(fails)) + ' FAILED: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
