# Lab 001 sound: riser into the landing frame, a tick on every flicker cut, a sub hit on the land, then air.
import numpy as np, wave, sys
SR = 48000; DUR = 5.0
cuts = [1.1, 1.5, 1.7666667, 1.9666667, 2.1, 2.2]; land = 2.2
t = np.arange(int(SR * DUR)) / SR
out = np.zeros_like(t)
rng = np.random.default_rng(1)
# riser: exponential sweep 180 -> 1400 Hz + band noise, gain rising 0 -> 1 from 0.5 s to the land, cut dead at the land
m = (t >= 0.5) & (t < land)
x = (t[m] - 0.5) / (land - 0.5)
f = 180 * (1400 / 180) ** x
ph = 2 * np.pi * np.cumsum(f) / SR
noise = rng.standard_normal(m.sum())
noise = np.convolve(noise, np.ones(8) / 8, mode="same")
out[m] += (0.25 * np.sin(ph) + 0.18 * noise) * x ** 2.2
# ticks on each flicker cut (short filtered click)
for c in cuts[:-1]:
    i = int(c * SR); n = int(0.025 * SR)
    out[i:i + n] += 0.35 * rng.standard_normal(n) * np.exp(-np.arange(n) / (0.004 * SR))
# the hit: sub sine with a pitch drop + a noise transient, long decay
i = int(land * SR); n = int(1.6 * SR); tt = np.arange(n) / SR
fh = 30 + 70 * np.exp(-tt / 0.06)
hit = 0.9 * np.sin(2 * np.pi * np.cumsum(fh) / SR) * np.exp(-tt / 0.45)
hit[:int(0.02 * SR)] += 0.5 * rng.standard_normal(int(0.02 * SR)) * np.exp(-np.arange(int(0.02 * SR)) / 200)
out[i:i + n] += hit[:len(out) - i]
out = np.tanh(out * 1.2) * 0.8
pcm = (out * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
