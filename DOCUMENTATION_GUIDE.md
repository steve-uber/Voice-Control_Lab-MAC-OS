# Voice Clone Lab macOS — Updated Documentation Guide

**Real-world tested conversion of Voice Clone Lab for Apple Silicon M3 Macs (Updated 2026-09-24)**

## What's Changed in This Update

✅ **Real-world testing completed** on M3 Mac with full training pipeline
✅ **All fixes documented** (prepare_data.py CPU-only, audio requirements, disk space management)
✅ **Actual performance numbers** from M3 testing (not estimates)
✅ **Critical learnings** about audio quality, batch sizing, and troubleshooting
✅ **Production-ready** error handling and recovery steps

## Which File Should I Read?

### 👉 **Starting Out?** → Read `QUICK_START_M3_UPDATED.md` (5 min)

Copy-paste installation + training guide with:
- Installation commands
- Full pipeline walkthrough
- Actual timings from M3 testing
- Quick troubleshooting

**Start here if:** You want to get running fast with real-world guidance.

---

### 👉 **Need Complete Setup?** → Read `INSTALL_MACOS_UPDATED.md` (15 min)

Detailed step-by-step with:
- System prerequisites & verification
- Why each step matters
- Batch size tuning by chip
- Comprehensive troubleshooting
- Storage & cleanup guidance

**Start here if:** You want detailed explanations and deep troubleshooting.

---

### 👉 **Project Overview?** → Read `README_UPDATED.md` (5 min)

High-level overview with:
- What changed from original
- Quick facts & critical requirements
- Real-world performance benchmarks
- Usage examples
- Development info

**Start here if:** You want to understand the project and capabilities.

---

### 👉 **Technical Deep-Dive?** → Read `MACOS_CONVERSION_SUMMARY_UPDATED.md` (10 min)

For developers/technical folks:
- Exact code changes & why
- Device detection logic
- Audio quality requirements (with real numbers)
- Loss progression patterns
- Lessons learned from testing

**Start here if:** You're integrating this or building on it.

---

## The Critical Path (You'll Want to Know This)

```
1. Installation (QUICK_START)
   ↓
2. Record 5-15 minutes of YOUR VOICE (most important!)
   ↓
3. vcl run --speaker me --input recording.wav --force
   ↓
4. vcl transcribe --speaker me --review (proofread)
   ↓
5. vcl prepare --speaker me
   ↓
6. vcl train --speaker me --batch-size 2
   ↓
7. vcl generate --speaker me --text "Your text here"
   ↓
✅ Done! You now have a voice clone.

Total time: ~90 minutes (mostly training)
```

## Critical Requirements (DO NOT SKIP)

| Requirement | Why | Consequence of Not Meeting |
|---|---|---|
| **5+ minutes of clean audio** | Model needs enough data to learn | Training produces NaN loss |
| **SNR > 15 dB** | Noise becomes part of trained voice | Generated voice sounds noisy/bad |
| **10+ GB free disk** | Models + checkpoints take space | "No space left on device" error |
| **PyTorch with Metal support** | Without it, no GPU acceleration | Training is 100× slower |

## Real-World Timings (M3 8-core, 10 min audio)

| Step | Time | Device |
|---|---|---|
| vcl run (extract/clean/split/transcribe) | 10 min | CPU |
| vcl transcribe --review | 5 min | Manual |
| vcl prepare | 8 min | CPU |
| vcl train (5 epochs, batch=2) | 50 min | Metal GPU |
| vcl generate | 3–5 sec | Metal GPU |
| **Total** | **~90 minutes** | - |

## Common Issues & Fixes

### Training produces NaN loss
→ You don't have 5+ minutes of audio. Record more.

### Metal not detected
→ Reinstall PyTorch with exact command in QUICK_START

### Out of memory (OOM)
→ Lower batch-size to 1, or reduce epochs to 3

### No space left on device
→ Run `rm -rf ~/.cache/huggingface/` to free space

### Transcription fails
→ Ensure audio is properly formatted: `brew install ffmpeg`

See INSTALL_MACOS_UPDATED.md for comprehensive troubleshooting.

## File Overview

### `QUICK_START_M3_UPDATED.md` (5 min read)
- **Purpose**: Get running fast
- **Audience**: Anyone wanting quick setup
- **Contains**: Copy-paste installation, full pipeline, quick troubleshooting
- **Best for**: Your first voice clone

### `INSTALL_MACOS_UPDATED.md` (15 min read)
- **Purpose**: Complete detailed setup
- **Audience**: Users who need detailed explanations
- **Contains**: Step-by-step with rationale, batch size tuning, comprehensive troubleshooting
- **Best for**: Detailed setup & troubleshooting reference

### `README_UPDATED.md` (5 min read)
- **Purpose**: Project overview
- **Audience**: Anyone curious about capabilities
- **Contains**: What changed, quick facts, performance benchmarks, examples
- **Best for**: Understanding the project

### `MACOS_CONVERSION_SUMMARY_UPDATED.md` (10 min read)
- **Purpose**: Technical deep-dive
- **Audience**: Developers, technical users
- **Contains**: Code changes, device detection logic, audio requirements, lessons learned
- **Best for**: Integration, understanding internals, extending the project

### `DOCUMENTATION_GUIDE.md` (This file)
- **Purpose**: Help you pick the right docs
- **Audience**: Everyone
- **Contains**: Which file to read, critical path, common issues, file overview

## What's Different from Original Documentation

| Aspect | Original | Updated |
|---|---|---|
| **Real-world tested?** | Theoretical | ✅ Tested on M3 |
| **Audio requirements** | Vague | ✅ Clear (5+ min, SNR > 15 dB) |
| **Actual timings** | Estimates | ✅ Real M3 timings (50 min training) |
| **prepare_data.py fix** | Not documented | ✅ CPU-only solution documented |
| **Troubleshooting** | Limited | ✅ Comprehensive (8 sections) |
| **Batch size guidance** | Not mentioned | ✅ Detailed by chip variant |
| **Disk space management** | Not mentioned | ✅ Cleanup commands & monitoring |
| **NaN loss explanation** | Not addressed | ✅ Root cause & solution |

## Getting Help

1. **Quick question?** → Check QUICK_START_M3_UPDATED.md troubleshooting
2. **Stuck on setup?** → See INSTALL_MACOS_UPDATED.md Step-by-Step
3. **Technical question?** → Read MACOS_CONVERSION_SUMMARY_UPDATED.md
4. **General overview?** → Start with README_UPDATED.md

## Audio Quality Testing

If you're curious why audio quality matters so much:

**Test case 1:** Prince Charles speech (9.98 min)
- Audio quality: SNR 10.1 dB (noisy)
- After VAD filtering: Only 7.65 sec accepted (0.13 min)
- Training result: NaN loss
- Conclusion: **Audio quality matters more than duration**

**Test case 2:** Clean voice memo (5–15 min)
- Audio quality: SNR > 20 dB (clean)
- After VAD filtering: 5–15 min accepted
- Training result: ✅ Normal loss descent
- Conclusion: **Clean audio is essential**

## Next Steps

1. **Pick a doc** based on your needs (see "Which File Should I Read?" above)
2. **Record 5–15 minutes of your voice** (this is critical!)
3. **Follow the pipeline** in QUICK_START_M3_UPDATED.md
4. **Refer to INSTALL_MACOS_UPDATED.md** if you hit issues
5. **Use your trained voice** to synthesize text, PDFs, or anything

## Files Included

```
📦 Updated Documentation Package

├── QUICK_START_M3_UPDATED.md (👈 START HERE)
│   └── Quick setup & pipeline guide
│
├── INSTALL_MACOS_UPDATED.md
│   └── Detailed step-by-step setup & troubleshooting
│
├── README_UPDATED.md
│   └── Project overview & capabilities
│
├── MACOS_CONVERSION_SUMMARY_UPDATED.md
│   └── Technical deep-dive for developers
│
├── DOCUMENTATION_GUIDE.md (this file)
│   └── Helps you pick the right docs
│
└── voice_clone_lab_macos.tar.gz
    └── Full fork source code (extract & use)
```

## Version Info

| Aspect | Detail |
|---|---|
| **Fork version** | Updated 2026-09-24 |
| **Base project** | [tetsuo-ai/voice_clone_lab](https://github.com/tetsuo-ai/voice_clone_lab) |
| **Target chip** | Apple Silicon M1/M2/M3 |
| **GPU** | Metal (MPS) acceleration |
| **Status** | Production-ready, real-world tested |

---

## TL;DR — Just Want to Clone Your Voice?

1. Extract: `tar -xzf voice_clone_lab_macos.tar.gz && cd voice_clone_lab_macos`
2. Read: `QUICK_START_M3_UPDATED.md` (5 min)
3. Do: Install + Record voice + Run pipeline
4. Enjoy: Your cloned voice ✨

**For help:** Check the docs in this order:
1. QUICK_START → Quick troubleshooting
2. INSTALL_MACOS → Detailed setup
3. README → Project info
4. MACOS_CONVERSION → Technical details

---

**Ready? 🎤 Start with `QUICK_START_M3_UPDATED.md`!**
