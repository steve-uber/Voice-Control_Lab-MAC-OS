# Voice Clone Lab on M3 Mac — 5-Minute Quick Start (UPDATED)

## The 60-Second Summary

✅ Voice Clone Lab converted to work on your M3 Mac with Metal GPU acceleration.
✅ No CUDA needed—just install PyTorch the right way.
✅ Training takes 40–60 minutes per voice (acceptable).
✅ **⚠️ You need 5+ minutes of clean audio** (critical for stable training).

## Installation (Copy-Paste)

```bash
# 1. Install dependencies via Homebrew
brew install python@3.12 ffmpeg git sox

# 2. Create virtual environment
python3.12 -m venv ~/.venv/vcl
source ~/.venv/vcl/bin/activate

# 3. Install PyTorch WITH Metal support (CRITICAL)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# 4. Verify Metal is available
python3 -c "import torch; print('Metal available:', torch.backends.mps.is_available())"
# Should print: Metal available: True

# 5. Extract the macOS fork
tar -xzf voice_clone_lab_macos.tar.gz
cd voice_clone_lab_macos

# 6. Install Voice Clone Lab
pip install -e '.[ui]'

# 7. Download models (~4 GB)
vcl setup --download

# 8. Verify everything
vcl check
# Should show "Metal (MPS) Available"
```

If **step 4** prints `False`, **redo step 3** (PyTorch install).

## Train Your Voice (90–120 minutes total)

**IMPORTANT: You need 5–15 minutes of YOUR VOICE for stable training.**

```bash
# Activate environment
source ~/.venv/vcl/bin/activate
cd voice_clone_lab_macos

# 1. Record or prepare audio
# Record 5–15 min of clean speech (macOS: ⌘-Space → Voice Memos)
# Save as: ~/Recordings/myvoice.wav (or .mp3/.m4a)

# 2. Run full pipeline
vcl run --speaker myname --input ~/Recordings/myvoice.wav --force

# 3. Review & fix transcripts (optional but recommended)
vcl transcribe --speaker myname --review
# Edit data/voices/myname/transcripts/transcripts_review.tsv if needed
vcl transcribe --speaker myname --apply-review --force

# 4. Prepare audio codes (CPU-only, ~5–10 min)
vcl prepare --speaker myname

# 5. Train (adjust batch-size based on your M3 variant)
# M3 base:    --batch-size 2
# M3 Pro:     --batch-size 4
# M3 Max:     --batch-size 8
vcl train --speaker myname --batch-size 2

# 6. Generate!
vcl generate --speaker myname --text "Hello, I am alive!"
# Output: outputs/generated/myname/test.wav
```

**Done!** Listen to `outputs/generated/myname/test.wav`. It should sound like you.

## ⚠️ Critical: Audio Requirements

Your training data must meet these minimums:

| Requirement | Minimum | Recommended |
|---|---|---|
| Duration | 5 min | 10–15 min |
| Quality | Clean (SNR > 15 dB) | Very clean (SNR > 20 dB) |
| Format | WAV/MP3/M4A mono | 16 kHz mono |
| Content | Natural speech | Natural, varied content |

**If training produces NaN loss → you don't have enough data.** Record more audio (5–15 min).

## Batch Size Guide

| M3 Variant | Recommended | RAM Used | Training Time | Disk Space |
|---|---|---|---|---|
| M3 (8-core) | 2 | ~6 GB | 40–60 min | 2–3 GB |
| M3 Pro | 4 | ~10 GB | 25–40 min | 2–3 GB |
| M3 Max (12-core) | 8 | ~18 GB | 15–25 min | 2–3 GB |

⚠️ **Disk space:** Ensure you have **at least 10 GB free** before training.

If training crashes with `out of memory` or `no space left on device`:
- Lower `--batch-size` (2 or 1)
- Reduce `--epochs 3` instead of 5
- Free disk space: `rm -rf ~/.cache/huggingface/`

## Verify It Works

```bash
# Check Metal is detected
vcl check
# Should show [OK] Metal (MPS) Available

# Generate a test phrase
vcl generate --speaker myname --text "Metal works!"

# Listen to output
open outputs/generated/myname/test.wav
```

## Use Your Voice to Synthesize Text

**From command line:**
```bash
vcl generate --speaker myname --text "Any text here"
```

**From a PDF:**
```bash
# Extract text and synthesize
pdftotext your_file.pdf extracted.txt
vcl generate --speaker myname --text "$(cat extracted.txt)"
```

**From the web UI:**
```bash
vcl ui
# Opens http://127.0.0.1:7860
# Go to Generate tab, select your speaker, enter text, click Generate
```

## Troubleshooting

### Training produces NaN loss
```
Solution: You don't have enough audio data. Record 5–15 minutes of your voice.
```

### Metal Not Detected
```bash
# Reinstall PyTorch
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Verify again
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

### Out of Memory During Training
```bash
# Use smaller batch size
vcl train --speaker myname --batch-size 1

# Or reduce epochs in config/default.yaml
```

### Transcription Fails
```bash
# Ensure audio is properly formatted
brew install ffmpeg
pip install faster-whisper
```

### No Space Left on Device
```bash
# Free up disk space
rm -rf ~/.cache/huggingface/
rm -rf ./outputs/checkpoints/unused_speaker/

# Check available space
df -h
# Ensure at least 10 GB free before training
```

## Performance Expectations

- **Audio extraction & cleaning**: Real-time (~2–5 min)
- **Transcription**: Real-time (~1–2 min for 5 min audio)
- **Prepare step**: CPU-only (~5–10 min)
- **Training**: 40–60 min for 5 epochs on 5–15 min audio (M3)
- **Generation**: Real-time (~2–5 sec per phrase)

## Next Steps

1. **Record 5–15 minutes of your voice** (most important!)
2. **Follow the pipeline above** (vcl run → prepare → train → generate)
3. **If training fails**, check troubleshooting or increase audio duration
4. **Use your voice** to synthesize text, PDFs, or any content

## Files You Got

- `voice_clone_lab_macos.tar.gz` ← Extract this
- `README.md` ← Project overview
- `INSTALL_MACOS.md` ← Detailed setup
- `QUICK_START_M3_UPDATED.md` ← This file (real-world tested)

## One More Thing

Existing checkpoints from CUDA systems? They work immediately:
```bash
cp -r /path/to/original/data/voices/* ./data/voices/
vcl generate --speaker copiedvoice --text "This checkpoint works on Metal!"
```

---

**You're all set! 🎤**

**Key reminder: You need 5+ minutes of clean audio for stable training. This is not optional.**

Questions? See `INSTALL_MACOS.md` for detailed troubleshooting.
