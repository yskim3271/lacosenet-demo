#!/usr/bin/env python3
"""Generate spectrogram images for all demo audio samples.

Run from the repo root:
    python demo/generate_spectrograms.py
"""

import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DEMO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(DEMO_DIR, "audio")
OUT_DIR = os.path.join(DEMO_DIR, "spectrograms")

MODELS = [
    "clean", "noisy",
    "lacosenet_12.5ms", "lacosenet_25.0ms",
    "lacosenet_75.0ms", "lacosenet_200.0ms",
    "deepfilternet3", "mpsenet",
]

SAMPLES = ["p232_005", "p232_023", "p257_003", "p257_054"]

# STFT params (match the model: 25ms window, 6.25ms hop @ 16kHz)
NPERSEG = 400
NOVERLAP = 300  # nperseg - hop (400 - 100)
NFFT = 512

# Plot params
FREQ_MAX_HZ = 8000  # Nyquist for 16kHz
DB_RANGE = 60  # dB dynamic range
FIGSIZE = (5.0, 2.0)  # inches per spectrogram
DPI = 150


def make_spectrogram(wav_path: str, out_path: str) -> None:
    sr, data = wavfile.read(wav_path)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0

    f, t, Zxx = stft(data, fs=sr, nperseg=NPERSEG, noverlap=NOVERLAP, nfft=NFFT)

    mag = np.abs(Zxx)
    mag_db = 20 * np.log10(mag + 1e-8)
    vmax = mag_db.max()
    vmin = vmax - DB_RANGE

    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
    ax.pcolormesh(t, f, mag_db, vmin=vmin, vmax=vmax, cmap="magma",
                  shading="gouraud", rasterized=True)
    ax.set_ylim(0, FREQ_MAX_HZ)
    ax.set_xlim(t[0], t[-1])
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(out_path, dpi=DPI, bbox_inches="tight", pad_inches=0.02,
                facecolor="black")
    plt.close(fig)


def main():
    total = 0
    for sample in SAMPLES:
        sample_dir = os.path.join(OUT_DIR, sample)
        os.makedirs(sample_dir, exist_ok=True)
        for model in MODELS:
            wav_path = os.path.join(AUDIO_DIR, model, f"{sample}.wav")
            if not os.path.exists(wav_path):
                print(f"SKIP (not found): {wav_path}")
                continue
            out_path = os.path.join(sample_dir, f"{model}.png")
            make_spectrogram(wav_path, out_path)
            total += 1

    print(f"Generated {total} spectrograms in {OUT_DIR}")


if __name__ == "__main__":
    main()
