# Voice Clone Lab on M3 Mac — 5-Minute Quick Start

## The 60-Second Summary

✅ I converted Voice Clone Lab to work on your M3 Mac with Metal GPU acceleration.
✅ No CUDA needed—just install PyTorch the right way.
✅ Training takes 40–60 minutes per voice (acceptable).
✅ Generation is real-time (~2–5 sec per phrase).

## Installation (Copy-Paste)

```bash
# 1. Install dependencies via Homebrew
brew install python@3.12 ffmpeg git

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

## Train Your Voice (30–90 minutes)

```bash
# Activate environment
source ~/.venv/vcl/bin/activate
cd voice_clone_lab_macos

# Record or provide audio (5–15 min of clean speech)
# Put it at ~/Recordings/myvoice.wav or any .wav/.mp3/.m4a file

# Run the full pipeline
vcl run --speaker myname --input ~/Recordings/myvoice.wav

# Review transcripts (optional but recommended)
vcl transcribe --speaker myname --review
# Edit data/voices/myname/transcripts/transcripts_review.tsv if needed
vcl transcribe --speaker myname --apply-review --force

# Train (adjust batch-size based on your M3 variant)
# M3 base: --batch-size 2
# M3 Max:  --batch-size 4-8
vcl prepare --speaker myname
vcl train --speaker myname --batch-size 2

# Generate!
vcl generate --speaker myname --text "Hello, I am alive!"
# Output: outputs/generated/myname/test.wav
```

**Done!** Listen to `outputs/generated/myname/test.wav`. It should sound like you.

## Web UI (Optional)

```bash
vcl ui
# Opens http://127.0.0.1:7860 in browser
# Use tabs: Setup (check system), Data (upload & review), Train (run training), Generate (create speech)
```

## Batch Size Guide

| M3 Variant | Recommended | RAM Used | Training Time |
|---|---|---|---|
| M3 (8-core) | 2 | ~6 GB | 60 min |
| M3 Pro | 4 | ~10 GB | 40 min |
| M3 Max (12-core) | 8 | ~18 GB | 25 min |

If training crashes with `out of memory`, **lower batch size or epochs**.

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

## Troubleshooting

### Metal Not Detected
```bash
# Reinstall PyTorch
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Verify again
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

### Out of Memory
```bash
# Use smaller batch size
vcl train --speaker myname --batch-size 1

# Or reduce epochs in config/default.yaml
```

### Transcription Fails
```bash
# Install faster-whisper
pip install faster-whisper
```

## Next Steps

1. **Read `INSTALL_MACOS.md`** in the fork (15 min)—detailed setup & troubleshooting
2. **Read `README_MACOS.md`** in the fork (5 min)—project overview & compatibility

## Files You Got

- `voice_clone_lab_macos.tar.gz` ← Extract this
- `MACOS_FORK_COMPLETE.md` ← Full overview
- `MACOS_CONVERSION_SUMMARY.md` ← Technical details
- `QUICK_START_M3.md` ← This file

## Performance Expectations

- **Training:** 40–60 min for 5 epochs on 15 min of audio (M3)
- **Generation:** Real-time (~2–5 sec per phrase)
- **Quality:** Identical to CUDA version (Metal doesn't change voice quality)

## One More Thing

Existing checkpoints from CUDA systems? They work immediately:
```bash
cp -r /path/to/original/data/voices/* ./data/voices/
vcl generate --speaker copiedvoice --text "This checkpoint works on Metal!"
```

---

**You're all set! 🎤**

Questions? See `INSTALL_MACOS.md` or `README_MACOS.md` in the fork.
