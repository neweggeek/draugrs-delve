import random, math, os
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
PAL = {
    'k': (20, 12, 16), 'w': (232, 220, 192), 'g': (168, 152, 120), 'r': (200, 64, 42),
    'o': (240, 128, 48), 'y': (248, 208, 72), 'b': (110, 200, 232), 'B': (46, 106, 154),
    't': (79, 179, 154), 'T': (42, 110, 96), 'p': (122, 74, 154), 'n': (106, 64, 40),
    'N': (62, 36, 24), 's': (138, 150, 168), 'S': (74, 82, 96), 'G': (106, 138, 90),
    'e': (127, 240, 255), 'm': (122, 106, 106), 'M': (74, 62, 64), 'f': (216, 154, 138),
}

S = {}
S['rat'] = """
................
................
................
................
................
................
................
................
.........kkk....
...kkkkkkmmmk...
..kmmmmmmmmmrkk.
.kmmMmmmmmmmmmfk
kfkmMMmmmmmmmkk.
k..kMMkkkMMk....
....kk...kk.....
................"""
S['bat'] = """
................
................
................
k......kk......k
kk....kwwk....kk
kgk..kwwwwk..kgk
kggkkwrwwrwkkggk
kgggkwwwwwwkgggk
.kggggwwwwggggk.
..kkggkwwkggkk..
....kk.kk.kk....
................
................
................
................
................"""
S['thrall'] = """
.....kkkkk......
....kwwwwwk.....
....kwrwrwk.....
....kwwwwwk.....
.....kwkwk......
......kwk.......
....kkwwwkk..s..
...kwkwgwkwk.s..
...kw.kwk.kwks..
......kwk...kn..
.....kgggk......
.....kw.wk......
.....kw.wk......
.....kw.wk......
....kkk.kkk.....
................"""
S['archer'] = """
.....kkkkk......
....kpppppk.....
...kpkwwwkpk....
...kpwrwrwpk.k..
...kpkwwwkpkkwk.
....kkwkwkk.kwk.
....kwwwwwk.k.kn
...kwkwgwkwkk..n
..kw.kwgwk.wkn.n
.....kwgwk..k..n
.....kgggk..kwk.
.....kw.wk...kk.
.....kw.wk......
....kkk.kkk.....
................
................"""
S['spider'] = """
.......k........
.......k........
.......k........
.......k........
....k..k..k.....
.k..kkkkkkk..k..
..kkMMMMMMMkk...
...kMrMMMrMk....
.kkkMMMMMMMkkk..
k..kMMMMMMMk..k.
..k.kMMMMMk.k...
.k...kkkkk...k..
k.............k.
................
................
................"""
S['slime'] = """
................
................
................
.......yy.......
......kook......
.....kooook.....
....koyooook....
...kooyoooook...
..koooooooooook.
..kooykoooykook.
..koooooooooook.
..krooooooooork.
...krrrrrrrrrk..
....kkkkkkkkk...
................
................"""
S['wisp'] = """
.......y........
......yo........
......oyo.......
.....oyyo.......
....ooyyyo......
....oyyyyyo.....
...ooykyykoo....
...oyywyywyo....
...oyyyyyyyo....
...ooyykkyoo....
....oooyyooo....
.....rooooor....
......rrorr.....
.......r.r......
........r.......
................"""
S['shambler'] = """
.....kkkkkk.....
....kGGGGGGk....
....kGeGGeGk....
....kGGGGGGk....
....kkGkkGkk....
...kSSkGGkSSk...
..kSSSSGGSSSSk..
..kGkSSSSSSkGk..
..kGkNNNNNNkGk..
..kGkSSSSSSkGk..
...k.kSSSSk.k...
.....kNkkNk.....
.....kNk.kNk....
.....kNk.kNk....
....kkkk.kkkk...
................"""
S['shield'] = """
.....kkkkk......
....kSSSSSk.....
....kGeGeGk.....
....kGGGGGk.....
.....kGGGk......
...kkSSSSSkk....
..kGSSSSkkkkk...
..kGSSSkbBBBbk..
..kGSSkbBByBBbk.
...kSSkbByyyBbk.
...kNNkbBByBBbk.
...kNNkkbBBBbk..
...kN.k.kkkkk...
...kN..kNk......
..kkk..kkkk.....
................"""
S['jarl'] = """
..y.....y.....y.....
..yk...kyk...ky.....
..ykkkkkykkkkky.....
..kyyyyyyyyyyyk.....
..kGGGGGGGGGGGk.....
..kGeeGGGGGeeGk.....
..kGGGGGGGGGGGk...bb
..kGGkkkkkkkGGk..bBb
...kGwkwkwkwGk..bBBb
....kGGGGGGGk....kb.
..kkrSSSSSSSrkk..kn.
.krrSSSSSSSSSrrk.kn.
krrkSSSyySSSSkrrkkn.
krkGkSSSSSSSkGkrkn..
krkGkNNNNNNNkGkrkn..
krkGkSSSSSSSkGkrk...
krk.kSSSSSSSk.krk...
.kk..kNNkNNk...kk...
.....kNNkNNk........
.....kNNkNNk........
....kkkkkkkkk......."""
S['knight'] = """
.....kkkkk......
....kssssskk....
....ksSkkkSk....
....kskffffk....
....ksfkfkfk....
.....kffffk.....
....kBBBBBBk....
...kfkBbbBkfk...
...kfkBbbBkfks..
...kkkBBBBkkks..
....kNNNNNNk.s..
....kBBkkBBk.n..
....kBk..kBk....
....kNk..kNk....
...kkkk..kkkk...
................"""
S['coin'] = """
..kkkk..
.kyyyyk.
kyyooyyk
kyoyyyok
kyoyyyok
kyyooyyk
.kyyyyk.
..kkkk.."""
S['potion'] = """
..kkkk..
...kk...
..kwwk..
.krrrrk.
krrwrrrk
krrrrrrk
.krrrrk.
..kkkk.."""
S['heart'] = """
.kk.kk.
krrkrrk
krwrrrk
krrrrrk
.krrrk.
..krk..
...k..."""
S['sword'] = """
....k.......................
...kyk.kkkkkkkkkkkkkkkkkkk..
kSrrkyebtttttttttttttttttttk
...kyk.kTTTTTTTTTTTTTTTTTTk.
....k...kkkkkkkkkkkkkkkkkk.."""
S['flame'] = """
...y...
..yo...
..oyo..
.oyyo..
.oyyyo.
oyywyo.
oyyyyo.
.oooo..
..rr..."""


def grid(name):
    rows = [r for r in S[name].strip('\n').split('\n')]
    w = max(len(r) for r in rows)
    return [r.ljust(w, '.') for r in rows]


def sprite_img(name, flip=False):
    g = grid(name)
    h, w = len(g), len(g[0])
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = im.load()
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c in PAL:
                px[x, y] = PAL[c] + (255,)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


def save_scaled(im, fn, scale):
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(os.path.join(OUT, fn))


# individual sprites, mobs face left (toward the player)
for n in ['rat', 'bat', 'thrall', 'archer', 'spider', 'slime', 'wisp', 'shambler', 'shield', 'jarl', 'knight']:
    flip = n in ('rat', 'thrall', 'archer', 'shambler', 'shield', 'jarl')
    save_scaled(sprite_img(n, flip=flip), f'{n}.png', 8)
for n in ['coin', 'potion', 'heart', 'flame']:
    save_scaled(sprite_img(n), f'{n}.png', 8)
save_scaled(sprite_img('sword'), 'sword.png', 6)

# ---------- key art scene, 320x180 ----------
random.seed(7)
W, H = 320, 180
FLOOR = 150
base = np.zeros((H, W, 3), dtype=np.float32)
base[:] = (18, 12, 16)
bricks = [(58, 34, 38), (67, 39, 42), (77, 44, 44), (46, 28, 32), (52, 30, 30)]
mortar = (24, 15, 18)
for row in range(0, FLOOR // 8 + 1):
    y0 = row * 8
    off = 0 if row % 2 == 0 else -8
    x = off
    while x < W:
        bw = 16
        col = np.array(random.choice(bricks), dtype=np.float32)
        y1, x1 = min(y0 + 8, FLOOR), min(x + bw, W)
        xs = max(x, 0)
        if y0 < FLOOR and xs < x1:
            base[y0:y1, xs:x1] = mortar
            base[y0 + 1:y1, xs + 1:x1] = col
            # chips and highlights
            for _ in range(2):
                cx, cy = random.randint(xs + 1, x1 - 1), random.randint(y0 + 1, max(y0 + 1, y1 - 1))
                if cy < FLOOR and cx < W:
                    base[cy, cx] = col * 1.25
        x += bw

# arches (dark recesses)
def arch(cx, top, half, bottom):
    for y in range(top, bottom):
        for x in range(cx - half, cx + half):
            dy = y - (top + half)
            if y < top + half and (x - cx) ** 2 + dy ** 2 > half ** 2:
                continue
            if 0 <= x < W:
                base[y, x] = base[y, x] * 0.28 + np.array((6, 4, 6)) * 0.72
for cx in (120, 240):
    arch(cx, 40, 22, FLOOR)

# floor
for y in range(FLOOR, H):
    for x in range(W):
        base[y, x] = (40, 26, 28) if (x // 12 + (y - FLOOR) // 6) % 2 else (48, 30, 30)
base[FLOOR, :] = (96, 58, 46)
base[FLOOR + 1, :] = (70, 42, 36)
for _ in range(70):
    x, y = random.randint(0, W - 3), random.randint(FLOOR + 3, H - 2)
    base[y, x:x + random.randint(1, 3)] = random.choice([(110, 60, 40), (30, 18, 20), (140, 70, 40)])

# ledge for archer
LX0, LX1, LY = 262, 318, 112
base[LY:LY + 6, LX0:LX1] = (72, 44, 40)
base[LY, LX0:LX1] = (120, 72, 52)
base[LY + 6, LX0:LX1] = (20, 12, 16)

# lighting from torches
torches = [(60, 66), (180, 66), (300, 66)]
yy, xx = np.mgrid[0:H, 0:W]
light = np.full((H, W), 0.35, dtype=np.float32)
for tx, ty in torches:
    d = np.sqrt((xx - tx) ** 2 + ((yy - ty) * 1.15) ** 2)
    light += np.clip(1.25 - d / 70.0, 0, None)
# vignette
vx = np.abs(xx - W / 2) / (W / 2)
vy = np.abs(yy - H / 2) / (H / 2)
light *= np.clip(1.15 - 0.45 * (vx ** 2 + vy ** 2), 0.3, 1.2)
# posterize light into bands with ordered dither for a pixel feel
bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
dith = bayer[yy % 4, xx % 4]
steps = 5
lq = np.floor(light * steps + dith) / steps
ember = np.array((255, 110, 40), dtype=np.float32)
img = base * lq[..., None] + ember * np.clip(lq - 1.0, 0, None)[..., None] * 0.35
img = np.clip(img, 0, 255).astype(np.uint8)
scene = Image.fromarray(img, 'RGB').convert('RGBA')

def paste(name, x, y, flip=False):
    sp = sprite_img(name, flip=flip)
    scene.alpha_composite(sp, (x, y))

# sconces + flames
for tx, ty in torches:
    for y in range(ty + 6, ty + 30):
        scene.putpixel((tx, y), (62, 36, 24, 255))
        scene.putpixel((tx + 1, y), (106, 64, 40, 255))
    for x in range(tx - 3, tx + 5):
        scene.putpixel((x, ty + 8), (74, 82, 96, 255))
    paste('flame', tx - 3, ty - 3)

# characters
paste('knight', 34, FLOOR - 15)
# sword slash arc in front of the knight
for a in range(-60, 61, 6):
    r = 13
    px_ = int(34 + 12 + r * math.cos(math.radians(a)))
    py_ = int(FLOOR - 9 + r * math.sin(math.radians(a)))
    if 0 <= px_ < W and 0 <= py_ < H:
        scene.putpixel((px_, py_), (240, 240, 220, 255))
        if px_ - 1 >= 0:
            scene.putpixel((px_ - 1, py_), (110, 200, 232, 255))
paste('rat', 70, FLOOR - 15, flip=True)
paste('thrall', 142, FLOOR - 15, flip=True)
paste('bat', 104, 60)
paste('slime', 206, FLOOR - 14)
paste('wisp', 190, 92)
paste('archer', 286, LY - 14, flip=True)
# arrow in flight
for x in range(244, 258):
    scene.putpixel((x, LY - 6), (232, 220, 192, 255))
scene.putpixel((243, LY - 7), (200, 200, 210, 255)); scene.putpixel((243, LY - 5), (200, 200, 210, 255))
for y in range(0, 34):
    scene.putpixel((157, y), (90, 80, 84, 255))
paste('spider', 150, 30)
paste('coin', 92, 118)
paste('coin', 102, 112)
paste('potion', 240, FLOOR - 8)

# HUD: hearts + coin counter in tiny pixel digits
DIG = {'0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111',
       '4': '101101111001001', '5': '111100111001111', '6': '111100111101111', '7': '111001001001001',
       '8': '111101111101111', '9': '111101111001111', 'x': '000101010101000'}
def text(s, x, y, col=(248, 236, 210, 255)):
    for ch in s:
        pat = DIG[ch]
        for i, bit in enumerate(pat):
            if bit == '1':
                scene.putpixel((x + i % 3, y + i // 3), col)
        x += 4
hud = Image.new('RGBA', (96, 14), (12, 8, 10, 190))
scene.alpha_composite(hud, (4, 4))
for i in range(5):
    sp = sprite_img('heart')
    if i >= 4:
        sp = Image.eval(sp, lambda v: v)  # placeholder for empty heart
        sp = sp.convert('LA').convert('RGBA')
    scene.alpha_composite(sp, (8 + i * 9, 7))
scene.alpha_composite(sprite_img('coin'), (60, 7))
text('x364', 70, 9)

save_scaled(scene, 'keyart.png', 4)
print(sorted(os.listdir(OUT)))
