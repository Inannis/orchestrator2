"""Instruments for a sound you cannot hear: turn a WAV into a picture and a plain reading of what is measurable in it.
usage: python listen.py <file.wav> [out.png]
Writes a PNG (waveform, spectrogram with the strongest pitch traced, loudness) and prints duration, loudness, onsets,
the pitches that sound longest as note names, and the intervals between successive ones. This is measurement, not hearing:
it cannot say whether something is pleasant, only what frequencies, when, and how loud."""
import sys, numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def note(f):
    if f <= 0: return "-"
    m = 69 + 12 * np.log2(f / 440.0); r = int(round(m))
    return f"{NAMES[r % 12]}{r // 12 - 1}{'' if abs(m - r) < 0.2 else ('+' if m > r else '-')}"
INTERVALS = {0: "unison", 1: "minor 2nd", 2: "major 2nd", 3: "minor 3rd", 4: "major 3rd", 5: "4th", 6: "tritone", 7: "5th",
             8: "minor 6th", 9: "major 6th", 10: "minor 7th", 11: "major 7th", 12: "octave"}

path = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else path.rsplit(".", 1)[0] + "-listen.png"
sr, x = wavfile.read(path)
x = x.astype(np.float64)
if x.ndim > 1: x = x.mean(axis=1)
peak_int = {np.dtype("int16"): 32768, np.dtype("int32"): 2 ** 31, np.dtype("uint8"): 128}
x = x / (np.max(np.abs(x)) or 1) if np.max(np.abs(x)) > 1.5 else x
dur = len(x) / sr
nper = min(4096, max(256, 2 ** int(np.log2(sr * 0.05))))
f, t, S = signal.stft(x, sr, nperseg=nper, noverlap=nper * 3 // 4)
mag = np.abs(S); db = 20 * np.log10(mag + 1e-9)
rms = np.sqrt(np.mean(mag ** 2, axis=0)); rms_db = 20 * np.log10(rms + 1e-9)
voiced = rms_db > rms_db.max() - 35
pitch = np.where(voiced, f[np.argmax(mag, axis=0)], 0.0)
flux = np.maximum(0, np.diff(mag, axis=1)).sum(axis=0)
onsets = t[1:][signal.find_peaks(flux, height=flux.mean() + 2 * flux.std(), distance=max(1, int(0.08 / (t[1] - t[0]))))[0]] if len(flux) > 3 else []

# pitch runs: consecutive frames on the same semitone
runs, cur, start = [], None, 0
semis = [int(round(69 + 12 * np.log2(p / 440))) if p > 0 else None for p in pitch]
for i, s in enumerate(semis + [None]):
    if s != cur:
        if cur is not None: runs.append((cur, t[start], t[i - 1] - t[start] + (t[1] - t[0])))
        cur, start = s, i
runs = [r for r in runs if r[2] >= 0.06]
seq = [r[0] for r in runs]

fig, ax = plt.subplots(3, 1, figsize=(11, 8), sharex=True, gridspec_kw={"height_ratios": [1, 3, 1]})
ax[0].plot(np.arange(len(x)) / sr, x, lw=0.4, color="k"); ax[0].set_ylabel("wave")
hi = min(f[-1], max(2000, (pitch.max() if pitch.max() > 0 else 1000) * 4))
ax[1].pcolormesh(t, f, db, shading="auto", cmap="magma", vmin=db.max() - 80, vmax=db.max()); ax[1].set_ylim(0, hi)
ax[1].plot(t, np.where(pitch > 0, pitch, np.nan), color="cyan", lw=1); ax[1].set_ylabel("Hz")
for r in runs[:40]: ax[1].text(r[1], 440 * 2 ** ((r[0] - 69) / 12), note(440 * 2 ** ((r[0] - 69) / 12)), color="w", fontsize=7)
ax[2].plot(t, rms_db, color="k"); ax[2].set_ylabel("dB"); ax[2].set_xlabel("seconds")
for o in onsets: ax[2].axvline(o, color="r", lw=0.5)
fig.suptitle(path.replace("\\", "/").split("/")[-1]); fig.tight_layout(); fig.savefig(out, dpi=110)

print(f"file: {path}\nduration: {dur:.2f} s, sample rate {sr} Hz")
print(f"peak level: {20*np.log10(np.max(np.abs(x))+1e-9):.1f} dBFS; loudness range over time: {rms_db[voiced].min() if voiced.any() else 0:.0f} to {rms_db.max():.0f} dB (relative)")
print(f"silence: {100*(1-voiced.mean()):.0f}% of the time; onsets detected: {len(onsets)}" + (f", mean gap {np.diff(onsets).mean():.2f} s" if len(onsets) > 2 else ""))
if runs:
    print("pitches in order (note, start s, length s): " + "; ".join(f"{note(440*2**((s-69)/12))} {a:.2f} {l:.2f}" for s, a, l in runs[:30]) + (" ..." if len(runs) > 30 else ""))
    iv = [abs(b - a) for a, b in zip(seq, seq[1:])]
    if iv: print("intervals between successive pitches: " + ", ".join(INTERVALS.get(i % 12 if i > 12 else i, f"{i} semitones") for i in iv[:30]))
    print(f"range: {note(440*2**((min(seq)-69)/12))} to {note(440*2**((max(seq)-69)/12))}")
else:
    print("no stable pitch found (noise, speech, or very short events)")
print(f"picture: {out}")
