"""Cuts authentic recitations into one clip per dua (and per line) for the app.

Sources
  - Hisn al-Muslim audio (hisnmuslim.com), one file per dhikr
  - Sheikh Mishary Rashid Alafasy, murattal (quranicaudio.com), cut with the
    word-level timings published by Quran.com (api.qurancdn.com)

Run with a Python that has PyAV:  python scripts/make-audio.py <src_dir> <out_dir> <plan.json>
plan.json maps clip name -> list of pieces; a piece is
  {"file": "h16.mp3", "from": 0.42, "to": 3.10}            (seconds)
  {"quran": "2:158", "words": [1, 6]}                       (word range, inclusive)
Clips are mono AAC (.m4a), 64 kbps, with short fades so cuts never click.
"""
import json, sys, os
import av
import numpy as np

SR = 44100
PAD = 0.0        # cuts already land in the silence between words
FADE = 0.025

src_dir, out_dir, plan_path = sys.argv[1:4]
os.makedirs(out_dir, exist_ok=True)
plan = json.load(open(plan_path))

_cache = {}
def load(path):
    """Decode a file to mono float32 at SR (cached)."""
    if path in _cache:
        return _cache[path]
    c = av.open(path)
    rs = av.AudioResampler(format="flt", layout="mono", rate=SR)
    chunks = []
    for frame in c.decode(audio=0):
        for f in rs.resample(frame):
            chunks.append(f.to_ndarray().reshape(-1))
    for f in rs.resample(None):
        chunks.append(f.to_ndarray().reshape(-1))
    c.close()
    _cache[path] = np.concatenate(chunks)
    return _cache[path]

_timings = {}
def quran_range(key, w0, w1):
    sura, ayah = key.split(":")
    if sura not in _timings:
        _timings[sura] = json.load(open(os.path.join(src_dir, f"q{sura}.json")))["audio_files"][0]["verse_timings"]
    vt = next(v for v in _timings[sura] if v["verse_key"] == key)
    segs = {s[0]: (s[1], s[2]) for s in vt["segments"] if len(s) >= 3}
    if w1 == -1:
        w1 = max(segs)
    if w0 < 0:
        w0 = max(segs) + 1 + w0
    return os.path.join(src_dir, f"q{sura}.mp3"), segs[w0][0] / 1000, segs[w1][1] / 1000

FR = 0.02  # analysis frame, seconds
_rms = {}
def frames(path):
    """Per-frame loudness and a silence threshold for the file."""
    if path not in _rms:
        x = load(path); n = int(FR * SR); k = len(x) // n
        r = np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(axis=1))
        _rms[path] = (r, 0.10 * np.percentile(r, 95))
    return _rms[path]

def _quietest(path, t0, t1):
    """Time of the quietest moment (smoothed over 60 ms) between t0 and t1: the gap between two words."""
    r, _ = frames(path)
    i0, i1 = max(1, int(t0 / FR)), min(len(r) - 2, int(t1 / FR))
    if i1 <= i0:
        return t0
    sm = np.convolve(r, np.ones(3) / 3, mode="same")
    return (i0 + int(np.argmin(sm[i0:i1]))) * FR

def snap_start(path, a):
    return _quietest(path, a - 0.5, a + 0.25)

def snap_end(path, b):
    return _quietest(path, b - 0.25, b + 0.35)

def piece_audio(p):
    if "quran" in p:
        path, a, b = quran_range(p["quran"], *p["words"])
        a, b = snap_start(path, a), snap_end(path, b)
    else:
        path, a, b = os.path.join(src_dir, p["file"]), p["from"], p["to"]
        if b < 0: b = len(load(path)) / SR + b
        if not p.get("exact_from"): a = snap_start(path, a)   # exact_from: start was placed by hand
        b = snap_end(path, b)
    x = load(path)
    a = max(0, a - PAD); b = min(len(x) / SR, b + PAD + p.get("tail", 0))
    y = x[int(a * SR):int(b * SR)].copy()
    n = int(FADE * SR)
    if len(y) > 2 * n:
        y[:n] *= np.linspace(0, 1, n); y[-n:] *= np.linspace(1, 0, n)
    return y

def write(name, y):
    path = os.path.join(out_dir, name + ".m4a")
    c = av.open(path, "w", format="mp4")
    s = c.add_stream("aac", rate=SR); s.layout = "mono"; s.bit_rate = 64000
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    step = 1024
    for i in range(0, len(pcm), step):
        fr = av.AudioFrame.from_ndarray(pcm[i:i + step].reshape(1, -1), format="s16", layout="mono")
        fr.sample_rate = SR
        for pkt in s.encode(fr):
            c.mux(pkt)
    for pkt in s.encode(None):
        c.mux(pkt)
    c.close()
    return len(y) / SR

gap = np.zeros(int(0.35 * SR), dtype=np.float32)
for name, pieces in plan.items():
    parts = []
    for i, p in enumerate(pieces):
        if i: parts.append(gap)
        parts.append(piece_audio(p))
    dur = write(name, np.concatenate(parts))
    print(f"{name:22s} {dur:5.2f}s")
