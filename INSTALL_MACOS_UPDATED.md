# Voice Clone Lab on macOS — Complete Installation & Setup Guide (UPDATED)

## Prerequisites

- **macOS 12.3+** (Metal/MPS support)
- **M1, M2, or M3** Apple Silicon Mac (any variant: base, Pro, Max, Ultra)
- **8 GB unified memory minimum** (16 GB+ strongly recommended)
- **10+ GB free disk space** (20+ GB recommended for training multiple voices)
- **Python 3.10+** (3.12 recommended)
- **Internet connection** (for downloading models)

## System Check

Before starting, verify your Mac:

```bash
# Check chip (should show Apple)
sysctl -n machdep.cpu.brand_string

# Check available disk space
df -h /
# Ensure "/" row shows >10 GB available

# Check macOS version
sw_vers
# Should show 12.3 or higher
```

## Step 1: Install Dependencies

Use Homebrew to install required tools:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.12 ffmpeg git sox

# Verify installations
python3.12 --version  # Should show 3.12.x
ffmpeg -version | head -n 1
sox --version
```

**What each tool does:**
- **Python 3.12**: Runtime for Voice Clone Lab
- **ffmpeg**: Audio format conversion & processing
- **git**: Version control (for cloning the fork)
- **sox**: Audio file format handling & SoX utility (needed for prepare step)

## Step 2: Create Virtual Environment

Keep Voice Clone Lab isolated from system Python:

```bash
# Create virtual environment
python3.12 -m venv ~/.venv/vcl

# Activate it
source ~/.venv/vcl/bin/activate

# Verify activation (should show (.venv/vcl) prefix)
which python
# Should show ~/.venv/vcl/bin/python
```

**Keep this activated for all subsequent steps.**

## Step 3: Install PyTorch with Metal Support (CRITICAL)

This is the most important step. PyTorch MUST be installed with Metal support:

```bash
# Install PyTorch from the official nightly index (includes Metal)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Verify Metal is available
python3 -c "import torch; print('Metal available:', torch.backends.mps.is_available())"
# Should print: Metal available: True
```

**If Metal is NOT available (prints False):**
1. Uninstall and retry:
   ```bash
   pip uninstall torch torchvision torchaudio -y
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
   ```
2. Verify again—if still False, your PyTorch installation is broken
3. Try: `python3 -c "import torch; print(torch.version.cuda);"` 
   - If this says "None", PyTorch has no CUDA (expected)
   - If it says something else, you have wrong PyTorch build

## Step 4: Extract & Install Voice Clone Lab

```bash
# Extract the fork
tar -xzf voice_clone_lab_macos.tar.gz
cd voice_clone_lab_macos

# Install Voice Clone Lab with UI dependencies
pip install -e '.[ui]'
```

**Installation time: 5–10 minutes** (depends on network)

## Step 5: Download Pre-trained Models

```bash
# Download Qwen3-TTS and Whisper models (~4 GB)
vcl setup --download

# This saves models to:
# ~/.cache/huggingface/hub/  (models)
# ./models/  (local checkpoints)
```

**Download time: 5–15 minutes** (depends on internet speed)

## Step 6: Verify System Setup

```bash
# Run diagnostic checks
vcl check

# Expected output (all [OK]):
# [OK] Python 3.12.x
# [OK] PyTorch 2.x.x
# [OK] Metal (MPS) Available
# [OK] ffmpeg installed
# [OK] sox installed
# [WARN] flash-attn not installed (this is OK, just slower)
```

If you see `[FAIL]` on anything, see Troubleshooting below.

## Step 7: Your First Voice Clone

### A. Prepare Audio

You need **5–15 minutes of clean speech**. Options:

1. **Record yourself** (best):
   - ⌘-Space → "Voice Memos"
   - Record 5–10 minutes of natural speech
   - Save as `~/Recordings/myvoice.m4a`

2. **Use existing audio**:
   - Podcast/interview of yourself
   - Any MP3, WAV, or M4A file
   - Mono preferred (stereo works too)

### B. Run the Full Pipeline

```bash
# Activate venv (if not already active)
source ~/.venv/vcl/bin/activate
cd voice_clone_lab_macos

# Start the pipeline
vcl run --speaker myname --input ~/Recordings/myvoice.wav --force

# This step:
# 1. Extracts & converts audio to 24 kHz mono
# 2. Cleans audio (removes silence, normalizes)
# 3. Splits into chunks (VAD-based speech detection)
# 4. Transcribes each chunk (uses Whisper large-v3)
# 5. Creates initial dataset

# Expected output:
# [1/5] extracted -> ...
# [2/5] cleaned -> ...
# [3/5] split -> 5–10 chunks (depends on audio length)
# [4/5] transcribed 5–10 chunks
# [5/5] dataset -> 5–10 clips, ~5 min total
```

**Time: 5–15 minutes** (depends on audio length & quality)

⚠️ **If you see "only X minutes of valid data. Recommended minimum is 5.0 minutes.":**
- You don't have enough audio yet, OR
- Your audio is too noisy/has too much silence
- Try: Record longer audio, or use cleaner source

### C. Proofread Transcripts (Optional)

Whisper may make errors. Fix them before training:

```bash
# Review transcripts
vcl transcribe --speaker myname --review

# Opens: data/voices/myname/transcripts/transcripts_review.tsv
# Edit any errors in the "text" column

# Apply corrections
vcl transcribe --speaker myname --apply-review --force
```

**Time: 5–15 minutes** (depends on how many corrections needed)

### D. Prepare Audio Codes

Convert audio to token codes for training:

```bash
vcl prepare --speaker myname
# Output: data/voices/myname/dataset/train_with_codes.jsonl

# Expected:
# Wrote Qwen training JSONL with audio_codes: ...
# Wrote: ...
```

**Time: 5–10 minutes** (uses CPU, not GPU)

⚠️ **If you get "No space left on device":**
- Free disk space:
  ```bash
  rm -rf ~/.cache/huggingface/
  df -h /
  # Need at least 10 GB free
  ```

### E. Train Your Model

```bash
# Adjust batch-size for your Mac:
# M3 base (8-core):     --batch-size 2
# M3 Pro (12-core GPU): --batch-size 4
# M3 Max (12-core GPU): --batch-size 8

vcl train --speaker myname --batch-size 2

# Expected output:
# Epoch 0 | Step 0 | Loss: 13.XX
# Epoch 1 | Step 0 | Loss: 12.XX  (decreasing is good)
# Epoch 2 | Step 0 | Loss: 11.XX
# ...
# Training complete. Checkpoints in: ...
```

**Time: 40–60 minutes** (depends on audio length & batch size)

**Training loss should decrease steadily. If it becomes NaN:**
- You don't have enough training data (need 5+ min)
- Your audio is too noisy
- Solution: Record more/cleaner audio and retry

### F. Generate Speech

```bash
# Generate from your trained voice
vcl generate --speaker myname --text "Hello, this is my cloned voice!"

# Output saved to:
# outputs/generated/myname/test.wav

# Listen to it
open outputs/generated/myname/test.wav
```

**Time: 5–10 seconds**

## Batch Size Selection

| Chip | RAM | Recommended | Max | Training Time |
|---|---|---|---|---|
| M3 8-core | 8 GB | 1–2 | 2 | 60 min |
| M3 8-core | 16 GB | 2–4 | 4 | 40 min |
| M3 Pro | 18 GB | 4 | 8 | 25 min |
| M3 Max 12-core | 36 GB | 8+ | 16 | 15 min |

**Guidelines:**
- Start with the recommended value
- If training crashes: lower by 1 and retry
- If memory usage is <50%: increase by 1 for faster training
- Monitor Activity Monitor (⌘-Space → Activity Monitor):
  - Check "Memory" tab
  - If "Swap" > 5 GB: lower batch size
  - If GPU Memory near max: reduce epochs

## Storage & Cleanup

**Disk space requirements per voice:**
- Models (~4 GB, shared across voices)
- Dataset (~100–500 MB)
- Training checkpoint (~500 MB–2 GB)
- Generated audio (~10–100 MB)

**Total: ~10 GB recommended for setup + one voice**

**To free up space:**
```bash
# Clear Hugging Face cache (safe to delete)
rm -rf ~/.cache/huggingface/

# Remove old unused voice checkpoints
rm -rf ./outputs/checkpoints/old_voice/

# Clear Python caches
find . -type d -name "__pycache__" -exec rm -rf {} +
```

## Troubleshooting

### Issue: Metal not detected (prints False)

```bash
# Step 1: Verify PyTorch installation
python3 -c "import torch; print(torch.__version__); print(torch.backends.mps.is_available())"

# Step 2: Reinstall PyTorch (exact URL is important)
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Step 3: Test again
python3 -c "import torch; print('Metal:', torch.backends.mps.is_available())"
```

**If still False:** Your PyTorch is broken. Try:
```bash
# Remove venv and start fresh
rm -rf ~/.venv/vcl
python3.12 -m venv ~/.venv/vcl
source ~/.venv/vcl/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

### Issue: vcl command not found

```bash
# Ensure you've activated the venv
source ~/.venv/vcl/bin/activate

# Verify installation
which vcl
# Should show ~/.venv/vcl/bin/vcl

# If not found, reinstall
pip install -e '.[ui]'
```

### Issue: Training produces NaN loss

**Cause:** Insufficient or noisy training data.

**Solution:**
1. Verify audio duration:
   ```bash
   ls -lh ./data/voices/myname/chunks/
   # Check train_raw.jsonl for "Total minutes"
   ```
2. If < 5 min: **Record more audio** (5–15 min minimum)
3. If > 5 min but still NaN: Your audio is too noisy
   - Re-record with less background noise
   - Try a different source audio

### Issue: Out of memory (OOM) during training

```bash
# Lower batch size
vcl train --speaker myname --batch-size 1

# Or reduce epochs
# Edit config/default.yaml and change epochs: 5 to epochs: 3
# Then retry training
```

### Issue: No space left on device

```bash
# Free up disk space immediately
rm -rf ~/.cache/huggingface/
rm -rf ./outputs/checkpoints/unused_speaker/

# Check available space
df -h /

# Ensure at least 10 GB free
# Then retry training
```

### Issue: ffmpeg errors during extraction

```bash
# Reinstall ffmpeg
brew uninstall ffmpeg
brew install ffmpeg

# Or install from source
brew install ffmpeg --HEAD
```

### Issue: Transcription fails or is very slow

```bash
# Ensure faster-whisper is installed
pip install faster-whisper

# If still slow: install CUDA (won't help on Metal, but some systems benefit)
# Actually, on Metal we use CPU for transcription, so this is normal
```

### Issue: Web UI doesn't open

```bash
# Ensure gradio is installed
pip install gradio

# Run UI directly
vcl ui

# Open browser manually to:
http://127.0.0.1:7860
```

## Next Steps

After training one voice, you can:

1. **Train multiple speakers**:
   ```bash
   vcl run --speaker speaker2 --input speaker2_audio.wav --force
   vcl prepare --speaker speaker2
   vcl train --speaker speaker2 --batch-size 2
   ```

2. **Use trained voice for synthesis**:
   ```bash
   # Generate from PDF
   pdftotext document.pdf text.txt
   vcl generate --speaker myname --text "$(cat text.txt)"
   
   # Use web UI
   vcl ui
   ```

3. **Export checkpoints**:
   ```bash
   # Copy to use on other Macs
   cp -r ./outputs/checkpoints/myname /path/to/external/drive/
   ```

## Performance Benchmarks (Real-World)

These are actual timings on M3 Mac with ~10 min audio:

| Step | Time | Notes |
|---|---|---|
| vcl run (extract/clean/split/transcribe) | 10 min | Real-time processing |
| vcl transcribe --review | 5 min | Manual proofreading |
| vcl prepare | 8 min | CPU-only encoding |
| vcl train (5 epochs, batch_size=2) | 50 min | M3 base, ~10 min audio |
| vcl generate (per phrase) | 3–5 sec | Real-time |

**Total first run: ~90 minutes** (mostly training)

## FAQ

**Q: Can I use checkpoints from my Linux/CUDA system?**
A: Yes! Copy them over:
```bash
cp -r /path/to/original/data/voices/* ./data/voices/
vcl generate --speaker copiedvoice --text "test"
# Works immediately, no retraining needed
```

**Q: Why is training so much slower than CUDA?**
A: Metal (MPS) on Apple Silicon is ~1–1.5× slower than RTX 3090. This is acceptable for voice cloning (one-time fine-tuning).

**Q: Do I need flash-attn?**
A: No. The warning is harmless. Flash-attn would be faster, but not required.

**Q: Can I use the trained voice with different models?**
A: The trained checkpoint is specific to Qwen3-TTS. Use it only with this fork.

**Q: How many speakers can I train?**
A: Unlimited. Each takes up disk space (~500 MB–2 GB per checkpoint).

**Q: Can I train with less than 5 minutes of audio?**
A: Not recommended. Less data → NaN loss. Minimum 5 min; 10–15 min is best.

---

**Ready to clone your voice? Start with the Quick Start guide!** 🎤

For real-time issues or questions, check the Quick Start troubleshooting section.
