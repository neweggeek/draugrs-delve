"""Tiny NES-style chiptune renderer: 2 pulse, triangle, noise. Original compositions."""
import numpy as np, wave, subprocess, os

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
        'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def midi(n):
    name, octv = n[:-1], int(n[-1])
    return 12 * (octv + 1) + NOTE[name]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pulse(f, n, duty, vib=0.0):
    t = np.arange(n) / SR
    if vib:
        # vibrato fades in after 150 ms, like a held synth lead
        depth = np.clip((t - 0.15) / 0.2, 0, 1) * vib
        ph = np.cumsum(f * (1 + depth * np.sin(2 * np.pi * 5.5 * t))) / SR
    else:
        ph = f * t
    return np.where((ph % 1.0) < duty, 1.0, -1.0)


def tri(f, n):
    ph = (f * np.arange(n) / SR) % 1.0
    v = 1 - 4 * np.abs(ph - 0.5)
    return np.round(v * 7.5) / 7.5  # 4-bit stepped, NES style


_lfsr_cache = {}
def noise(n, short=False):
    key = (n, short)
    if key not in _lfsr_cache:
        reg, out, tap = 1, np.empty(n), 6 if short else 1
        rate = 4  # samples per LFSR step
        for i in range(0, n, rate):
            fb = (reg & 1) ^ ((reg >> tap) & 1)
            reg = (reg >> 1) | (fb << 14)
            out[i:i + rate] = 1.0 if reg & 1 else -1.0
        _lfsr_cache[key] = out[:n]
    return _lfsr_cache[key]


def env(n, a=0.004, d=0.12, s=0.6, r=0.03):
    e = np.full(n, s)
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n)
    e[:na] = np.linspace(0, 1, na, endpoint=False)
    k = min(nd, max(0, n - na))
    e[na:na + k] = np.linspace(1, s, k, endpoint=False)
    nr = min(nr, n)
    e[n - nr:] *= np.linspace(1, 0, nr)
    return e


class Song:
    def __init__(self, bpm, bars, beats_per_bar=4):
        self.spb = 60.0 / bpm
        self.len = int(round(bars * beats_per_bar * self.spb * SR))
        self.buf = np.zeros(self.len + SR * 2)

    def s(self, beat):
        return int(round(beat * self.spb * SR))

    def add(self, start_beat, sig, vol):
        i = self.s(start_beat)
        self.buf[i:i + len(sig)] += sig * vol

    def melody(self, start_beat, notes, duty, vol, vib=0.0, gate=0.92, echo=0.0, sustain=0.65):
        b = start_beat
        for n, d in notes:
            if n != 'r':
                ln = self.s(d * gate)
                sig = pulse(hz(midi(n)), ln, duty, vib) * env(ln, s=sustain)
                self.add(b, sig, vol)
                if echo:
                    self.add(b + 0.75, sig, vol * echo)
            b += d
        return b

    def tri_line(self, start_beat, notes, vol, gate=0.85):
        b = start_beat
        for n, d in notes:
            if n != 'r':
                ln = self.s(d * gate)
                self.add(b, tri(hz(midi(n)), ln) * env(ln, d=0.05, s=0.9, r=0.01), vol)
            b += d

    def kick(self, beat, vol=0.55):
        n = int(0.11 * SR)
        f = np.linspace(170, 45, n)
        ph = np.cumsum(f) / SR % 1.0
        v = np.round((1 - 4 * np.abs(ph - 0.5)) * 7.5) / 7.5
        self.add(beat, v * np.linspace(1, 0, n) ** 1.5, vol)

    def snare(self, beat, vol=0.32):
        n = int(0.14 * SR)
        e = np.exp(-np.arange(n) / (0.04 * SR))
        self.add(beat, noise(n) * e, vol)
        m = int(0.05 * SR)
        self.add(beat, tri(190, m) * np.linspace(1, 0, m), vol * 0.8)

    def hat(self, beat, vol=0.10, open_=False):
        n = int((0.09 if open_ else 0.03) * SR)
        e = np.exp(-np.arange(n) / ((0.03 if open_ else 0.008) * SR))
        self.add(beat, noise(n, short=True) * e, vol)

    def save(self, name, tail=0.0):
        n = self.len + int(tail * SR)
        x = self.buf[:n].copy()
        x /= max(1e-9, np.max(np.abs(x))) / 0.89
        pcm = (x * 32767).astype(np.int16)
        wav = os.path.join(OUT, name + '.wav')
        with wave.open(wav, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
        mp3 = os.path.join(OUT, name + '.mp3')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-codec:a', 'libmp3lame', '-b:a', '160k', mp3], check=True)
        os.remove(wav)
        return mp3


CH = {  # chord tones for arps and bass
    'Dm': ['D', 'F', 'A'], 'Bb': ['Bb', 'D', 'F'], 'F': ['F', 'A', 'C'], 'C': ['C', 'E', 'G'],
    'Gm': ['G', 'Bb', 'D'], 'A': ['A', 'C#', 'E'], 'Em': ['E', 'G', 'B'], 'D': ['D', 'F#', 'A'],
    'B': ['B', 'D#', 'F#'], 'Am': ['A', 'C', 'E'], 'G': ['G', 'B', 'D'],
}


def arp_bar(chord, octv, pattern=(0, 1, 2, 3, 2, 1, 0, 1), step=0.5):
    r, t, f = CH[chord]
    rm = midi(r + str(octv))
    tones = [rm, rm + (midi(t + str(octv)) - rm) % 12, rm + (midi(f + str(octv)) - rm) % 12, rm + 12]
    out = []
    names = {v: k for k, v in NOTE.items() if len(k) == 1 or '#' in k}
    for i in range(int(4 / step)):
        m = tones[pattern[i % len(pattern)]]
        out.append((names[m % 12] + str(m // 12 - 1), step))
    return out


def bass_bar(chord, octv, gallop=False):
    r = CH[chord][0]
    lo, hi = r + str(octv), r + str(octv + 1)
    if gallop:
        return [(lo, 0.5), (lo, 0.25), (lo, 0.25)] * 4
    return [(lo, 0.5), (hi, 0.5)] * 4


# ---------------- Track 1: "Torchlit Delve" (dungeon loop) ----------------
def delve():
    intro = ['Dm', 'Bb', 'F', 'C']
    A = ['Dm', 'Bb', 'F', 'C', 'Dm', 'Bb', 'Gm', 'A']
    B = ['Bb', 'C', 'Dm', 'Dm', 'Bb', 'C', 'A', 'A']
    prog = intro + A + B + A
    leadA = [('D5', 1), ('F5', .5), ('A5', .5), ('G5', 1), ('F5', 1),
             ('D5', 1.5), ('C5', .5), ('Bb4', 1), ('D5', 1),
             ('C5', 1), ('F5', 1), ('A5', 1.5), ('G5', .5),
             ('G5', 2), ('E5', 1), ('C5', 1),
             ('D5', .5), ('E5', .5), ('F5', 1), ('A5', 1), ('D6', 1),
             ('C6', 1), ('Bb5', .5), ('A5', .5), ('F5', 2),
             ('G5', 1), ('Bb5', 1), ('D6', 1), ('C6', .5), ('Bb5', .5),
             ('A5', 2), ('C#6', 1), ('E6', 1)]
    leadB = [('F5', 1), ('Bb5', 1), ('D6', 2),
             ('E6', 1.5), ('D6', .5), ('C6', 1), ('G5', 1),
             ('A5', 1), ('D6', 1), ('F6', 2),
             ('E6', .5), ('D6', .5), ('C6', .5), ('A5', .5), ('D6', 2),
             ('F6', 1), ('E6', .5), ('D6', .5), ('Bb5', 2),
             ('C6', 1), ('E6', 1), ('G6', 1), ('E6', 1),
             ('E6', 1), ('C#6', 1), ('A5', 1), ('E5', 1),
             ('A5', 3), ('r', 1)]
    s = Song(120, len(prog))
    for i, c in enumerate(prog):
        b = i * 4
        duty = 0.125 if i >= 20 else 0.25
        s.melody(b, arp_bar(c, 4, step=0.25, pattern=(0, 1, 2, 3, 2, 1, 2, 3)), duty, 0.09, gate=0.7, sustain=0.4)
        s.tri_line(b, bass_bar(c, 2), 0.30)
        if i >= 4:
            for q in range(4):
                if q in (0, 2):
                    s.kick(b + q)
                else:
                    s.snare(b + q)
                s.hat(b + q + 0.5)
            if i >= 20:
                s.kick(b + 2.5, 0.4)
                for q in range(4):
                    s.hat(b + q + 0.25, 0.06); s.hat(b + q + 0.75, 0.06)
        else:
            s.hat(b + 2, 0.08, open_=True)
    s.melody(16, leadA, 0.5, 0.15, vib=0.012, echo=0.35)
    s.melody(48, leadB, 0.5, 0.15, vib=0.012, echo=0.35)
    s.melody(80, leadA, 0.25, 0.15, vib=0.012, echo=0.35)
    return s.save('01_torchlit_delve_loop')


# ---------------- Track 2: "The Jarl Rises" (boss) ----------------
def jarl():
    A = ['Em', 'Em', 'C', 'D', 'Em', 'Em', 'C', 'B']
    B = ['Am', 'C', 'Em', 'B', 'Am', 'C', 'Em', 'B']
    prog = ['Em', 'Em'] + A + B + A
    leadA = [('E5', .5), ('F5', .5), ('E5', .5), ('B4', .5), ('E5', 1), ('G5', 1),
             ('F#5', .5), ('E5', .5), ('D5', .5), ('E5', .5), ('B4', 2),
             ('C5', .5), ('E5', .5), ('G5', .5), ('C6', .5), ('B5', 1), ('G5', 1),
             ('A5', 1), ('F#5', 1), ('D5', 1), ('F#5', 1),
             ('E6', 1), ('D6', .5), ('B5', .5), ('G5', 1), ('E5', 1),
             ('F5', .5), ('G5', .5), ('F5', .5), ('E5', .5), ('B4', 2),
             ('C6', 1), ('B5', .5), ('A5', .5), ('G5', 1), ('E5', 1),
             ('D#5', 1), ('F#5', 1), ('B5', 2)]
    leadB = [('A5', 2), ('C6', 2),
             ('E6', 2), ('D6', 1), ('C6', 1),
             ('B5', 3), ('G5', 1),
             ('F#5', 2), ('D#6', 2),
             ('E6', 1), ('C6', 1), ('A5', 2),
             ('G6', 1), ('E6', 1), ('C6', 2),
             ('B5', 1), ('E6', 1), ('G6', 1), ('B6', 1),
             ('A6', 1), ('F#6', 1), ('D#6', 2)]
    s = Song(150, len(prog))
    for i, c in enumerate(prog):
        b = i * 4
        s.tri_line(b, bass_bar(c, 2, gallop=True), 0.32, gate=0.7)
        s.melody(b, arp_bar(c, 4, step=0.25, pattern=(0, 2, 1, 3, 0, 2, 1, 2)), 0.125, 0.07, gate=0.6, sustain=0.35)
        for q in range(4):
            s.kick(b + q, 0.5)
            if q in (1, 3):
                s.snare(b + q, 0.34)
            s.hat(b + q + 0.5, 0.09)
        if i < 2:
            s.snare(b + 3.5, 0.25); s.snare(b + 3.75, 0.3)
    s.melody(8, leadA, 0.25, 0.16, vib=0.015, echo=0.3)
    s.melody(40, leadB, 0.5, 0.16, vib=0.015, echo=0.3)
    s.melody(72, leadA, 0.125, 0.17, vib=0.015, echo=0.3)
    return s.save('02_the_jarl_rises_boss')


# ---------------- Track 3: "Dungeon Complete" (victory sting) ----------------
def victory():
    s = Song(140, 3)
    lead = [('D5', .25), ('F#5', .25), ('A5', .25), ('D6', .25), ('A5', .25), ('D6', .25), ('F#6', .25), ('A6', .25),
            ('G6', .5), ('F#6', .5), ('E6', .5), ('G6', .5),
            ('F#6', .75), ('E6', .25), ('D6', .5), ('A5', .5), ('D6', 2)]
    harm = [('r', 2), ('B5', .5), ('A5', .5), ('C#6', .5), ('E6', .5), ('D6', .75), ('C#6', .25), ('A5', .5), ('F#5', .5), ('A5', 2)]
    s.melody(0, lead, 0.5, 0.17, vib=0.012, echo=0.3, gate=0.95)
    s.melody(0, harm, 0.25, 0.10, gate=0.95)
    s.tri_line(0, [('D3', 1), ('D3', 1), ('G2', 1), ('A2', 1), ('D2', 4), ('r', 4)], 0.34, gate=0.95)
    for q in range(4):
        s.kick(q, 0.45); s.hat(q + 0.5, 0.08)
    s.snare(1); s.snare(3); s.snare(3.5, 0.25); s.snare(3.75, 0.3)
    s.kick(4, 0.55); s.hat(4, 0.12, open_=True)
    return s.save('03_dungeon_complete_sting', tail=0.6)


if __name__ == '__main__':
    for f in (delve, jarl, victory):
        p = f()
        print(p, os.path.getsize(p))
