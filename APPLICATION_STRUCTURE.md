# Voice Clone Lab M3 — Application Files Structure

**All source code files for Apple Silicon M3 installation**

## 📦 Application Files

### Core Modules

**`config.py`** (200 lines)
- Device auto-detection for Metal/CUDA/CPU
- Configuration dataclasses for project, ASR, and training
- Automatic device selection on startup
- Memory and compute type optimization
- Key functions:
  - `_get_default_device()` - Detects Metal, CUDA, or CPU
  - `_get_default_compute_type()` - Selects float32 (Metal) or float16 (CUDA)
  - `ProjectConfig`, `ASRConfig`, `TrainingConfig` - Configuration objects

**`system.py`** (240 lines)
- System detection and health checks
- Metal availability verification
- CUDA detection for NVIDIA GPUs
- Disk space monitoring
- Installation hints
- Key functions:
  - `check_metal_availability()` - Checks Metal (MPS) support
  - `check_cuda_availability()` - Checks CUDA GPU
  - `run_system_check()` - Comprehensive system diagnostic
  - `get_device_summary()` - Human-readable device info

**`transcribe.py`** (200 lines)
- Speech-to-text using Whisper or faster-whisper
- CPU-safe transcription (loads on CPU, not Metal)
- Batch transcription support
- Metal/CUDA/CPU compatibility
- Key functions:
  - `get_transcriber()` - Returns transcription function
  - `transcribe_file()` - Single file transcription
  - `transcribe_batch()` - Multiple file transcription

**`prepare_data.py`** (250 lines)
- Audio tokenization for training (CPU-only for Metal safety)
- Loads tokenizer on CPU with device_map="cpu"
- Avoids HuggingFace CUDA initialization
- Per-speaker audio code generation
- Key functions:
  - `get_audio_codes()` - Tokenize audio codes
  - `prepare_speaker_data()` - Prepare all audio for speaker
  - CLI: `python prepare_data.py --speaker-dir <path>`

### Web UI

**`enhanced_ui.py`** (600+ lines)
- Complete Gradio-based web interface
- 6 main tabs:
  1. System: Health check, speaker management
  2. Audio Pipeline: Extract, clean, transcribe, review
  3. Training: Prepare, train with batch tuning
  4. Generate: Text-to-speech and PDF synthesis
  5. Speaker Info: Statistics and status
  6. Help & Docs: Guidance and troubleshooting
- Real-time output logging
- Error handling and user feedback
- PDF extraction with page range selection
- VCLManager class for operation orchestration

**Run:** `python enhanced_ui.py` → Access at `http://127.0.0.1:7860`

### Installation & Setup

**`install.sh`** (Bash script)
- Automated installation for M3 Macs
- Creates virtual environment at ~/.venv/vcl
- Installs PyTorch with Metal support
- Verifies Metal availability
- Installs all dependencies
- Creates data directories
- Runs system check

**Usage:**
```bash
chmod +x install.sh
./install.sh
```

**`requirements.txt`** (50+ lines)
- All Python dependencies
- PyTorch (must be before other packages)
- Audio processing (librosa, soundfile)
- Speech recognition (whisper, faster-whisper)
- ML utilities (transformers, huggingface-hub)
- Web UI (gradio)
- PDF processing (pypdf, pdfplumber)

**`setup.py`** (60 lines)
- Python package setup configuration
- Installs as `voice-clone-lab-m3` package
- Console script entry points
- Package metadata and classifiers

## 📚 Documentation Files

**`QUICK_START_M3_UPDATED.md`**
- 5-minute quick start guide
- Copy-paste installation
- Full pipeline walkthrough
- Real timings from M3 testing
- Quick troubleshooting

**`INSTALL_MACOS_UPDATED.md`**
- 15-minute detailed installation
- Step-by-step explanations
- Batch size tuning by chip
- Comprehensive troubleshooting
- Storage management

**`README_UPDATED.md`**
- Project overview
- Quick facts and requirements
- Performance benchmarks
- Usage examples
- Comparison tables

**`MACOS_CONVERSION_SUMMARY_UPDATED.md`**
- Technical deep-dive
- Code changes explained
- Device detection logic
- Audio quality requirements
- Lessons learned

**`DOCUMENTATION_GUIDE.md`**
- Meta-guide for choosing docs
- Critical path checklist
- Common issues & fixes
- File overview

**`ENHANCED_UI_GUIDE.md`**
- Web UI user guide
- Tab-by-tab walkthrough
- Keyboard shortcuts
- Troubleshooting
- Customization

**`PDF_TO_SPEECH_GUIDE.md`**
- PDF-to-speech workflow
- Multiple methods (CLI, Python, Bash)
- Handling large PDFs
- Text cleanup tips
- Batch processing scripts

## 🏗️ Directory Structure

```
voice_clone_lab_macos/
├── Application Code
│   ├── config.py          [Device auto-detection]
│   ├── system.py          [System checks & health]
│   ├── transcribe.py      [Speech recognition]
│   ├── prepare_data.py    [Audio tokenization (CPU)]
│   └── enhanced_ui.py     [Web UI (Gradio)]
│
├── Installation
│   ├── install.sh         [Automated setup script]
│   ├── requirements.txt   [Python dependencies]
│   └── setup.py           [Package configuration]
│
├── Documentation
│   ├── QUICK_START_M3_UPDATED.md
│   ├── INSTALL_MACOS_UPDATED.md
│   ├── README_UPDATED.md
│   ├── MACOS_CONVERSION_SUMMARY_UPDATED.md
│   ├── DOCUMENTATION_GUIDE.md
│   ├── ENHANCED_UI_GUIDE.md
│   └── PDF_TO_SPEECH_GUIDE.md
│
├── Data (created during setup)
│   └── speakers/          [Speaker audio files]
│
└── Outputs (created during training)
    ├── checkpoints/       [Trained model checkpoints]
    └── generated/         [Generated audio files]
```

## 🚀 Installation Steps

### 1. Download & Extract
```bash
# Download voice_clone_lab_macos.tar.gz
tar -xzf voice_clone_lab_macos.tar.gz
cd voice_clone_lab_macos
```

### 2. Run Installation Script
```bash
chmod +x install.sh
./install.sh
```

This will:
- Create virtual environment at `~/.venv/vcl`
- Install PyTorch with Metal support
- Verify Metal availability
- Install all dependencies
- Create data directories
- Run system check

### 3. Activate Virtual Environment
```bash
source ~/.venv/vcl/bin/activate
```

### 4. Start Using
```bash
# Web UI
python enhanced_ui.py
# Access: http://127.0.0.1:7860

# Or CLI
vcl run --speaker myname --input recording.wav
vcl transcribe --speaker myname --review
vcl prepare --speaker myname
vcl train --speaker myname --batch-size 2
vcl generate --speaker myname --text "Hello world"
```

## 🔧 File Dependencies

```
enhanced_ui.py
├── config.py        (Device auto-detection)
├── system.py        (System checks)
├── transcribe.py    (Transcription)
├── prepare_data.py  (Audio tokenization)
└── gradio           (Web UI framework)

CLI (vcl commands)
├── config.py        (Device auto-detection)
├── transcribe.py    (Transcription)
├── prepare_data.py  (Audio tokenization)
└── PyTorch/Metal    (Training backend)
```

## 🎯 Key Features

✅ **Automatic Device Detection**
- Detects Metal (MPS) on Apple Silicon
- Falls back to CUDA on NVIDIA
- Falls back to CPU if needed

✅ **Metal Safety**
- Float32 compute (Metal-safe)
- CPU-only tokenization (no device conflicts)
- CPU-safe transcription

✅ **Complete Pipeline**
- Audio upload & extraction
- Transcript review & correction
- Audio preparation (tokenization)
- Model training with batch size tuning
- Speech generation from text or PDF

✅ **PDF Integration**
- PDF upload and text extraction
- Page range selection
- Direct PDF-to-speech synthesis

✅ **Modern Web UI**
- 6-tab Gradio interface
- Real-time logging
- Error handling
- Speaker management

## ⚠️ Critical Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Audio duration | 5 min | 10-15 min |
| Audio quality (SNR) | 10 dB | 20+ dB |
| Disk space | 10 GB | 20+ GB |
| PyTorch | Metal-compiled | Latest nightly |

## 📝 File Sizes (Approximate)

| File | Size |
|---|---|
| config.py | 4 KB |
| system.py | 6 KB |
| transcribe.py | 5 KB |
| prepare_data.py | 7 KB |
| enhanced_ui.py | 25 KB |
| install.sh | 2 KB |
| requirements.txt | 2 KB |
| setup.py | 2 KB |

**Total application code: ~50 KB** (highly portable)

## 🔍 Verification

After installation, verify everything works:

```bash
# Activate venv
source ~/.venv/vcl/bin/activate

# Check system
python system.py

# Start UI
python enhanced_ui.py

# Or test CLI
vcl check
```

Expected output:
```
✅ Metal (MPS) Available — Apple Silicon GPU acceleration enabled
```

## 🆘 Troubleshooting

### Metal not detected
```bash
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

### Virtual environment not activating
```bash
source ~/.venv/vcl/bin/activate
which python  # Should show ~/.venv/vcl/bin/python
```

### Disk space issues
```bash
rm -rf ~/.cache/huggingface/
df -h /
```

## 📦 Next: Getting Voice Clone Lab Source

These application files are the modified/new modules for Voice Clone Lab. You'll also need:
- The full Voice Clone Lab source code repository
- Or contact the Voice Clone Lab project for the base code
- These files replace/extend the original implementations with Metal support

---

**Status:** Production-ready, real-world tested on M3 Macs

**For full setup guide:** See `QUICK_START_M3_UPDATED.md`
