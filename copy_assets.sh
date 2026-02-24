#!/usr/bin/env bash
# Copy audio samples and figures into demo/ for GitHub Pages hosting.
# Run from the repository root: bash demo/copy_assets.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEMO_DIR="$REPO_ROOT/demo"
SAMPLES_DIR="$REPO_ROOT/baselines/samples"
FIGURES_DIR="$REPO_ROOT/paper_works"

# Audio directories to copy (source_dir -> dest_dir)
AUDIO_DIRS=(
    "clean:clean"
    "noisy:noisy"
    "dublonet_12.5ms:lacosenet_12.5ms"
    "dublonet_25.0ms:lacosenet_25.0ms"
    "dublonet_50.0ms:lacosenet_50.0ms"
    "dublonet_75.0ms:lacosenet_75.0ms"
    "dublonet_200.0ms:lacosenet_200.0ms"
    "deepfilternet3:deepfilternet3"
    "mpsenet:mpsenet"
)

for mapping in "${AUDIO_DIRS[@]}"; do
    src="${mapping%%:*}"
    dst="${mapping##*:}"
    mkdir -p "$DEMO_DIR/audio/$dst"
    cp "$SAMPLES_DIR/$src/"*.wav "$DEMO_DIR/audio/$dst/"
    echo "Copied $src -> audio/$dst/ ($(ls "$DEMO_DIR/audio/$dst/"*.wav | wc -l) files)"
done

# Figures
mkdir -p "$DEMO_DIR/figures"
cp "$FIGURES_DIR/interspeech2026/figures/figure1.png" "$DEMO_DIR/figures/"
cp "$FIGURES_DIR/figures/latency_vs_pesq.png" "$DEMO_DIR/figures/"
echo "Copied figures ($(ls "$DEMO_DIR/figures/"*.png | wc -l) files)"

echo "Done. Total audio files: $(find "$DEMO_DIR/audio" -name '*.wav' | wc -l)"

# Generate spectrograms
echo "Generating spectrograms..."
python3 "$DEMO_DIR/generate_spectrograms.py"
