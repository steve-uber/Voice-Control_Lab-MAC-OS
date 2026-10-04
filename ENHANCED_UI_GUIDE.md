# Enhanced Web UI for Voice Clone Lab

**Complete, modern web interface with all new features and improved UX**

## Features

✅ **System Management**
- Real-time system health check
- Metal GPU status verification
- Speaker list & management

✅ **Complete Pipeline**
- Audio upload & extraction
- Transcript review & correction
- Audio preparation (prepare_data)
- Model training with batch size tuning
- Speech generation from text or PDF

✅ **PDF Integration**
- PDF file upload
- Page range selection
- Automatic text extraction
- Direct PDF-to-speech synthesis

✅ **Speaker Management**
- View all speakers
- Detailed speaker information
- Training status tracking
- Dataset statistics

✅ **Modern UI**
- Clean, intuitive interface
- Responsive design
- Real-time feedback
- Error handling

## Installation

### Step 1: Copy the UI File

```bash
# Navigate to your Voice Clone Lab folder
cd voice_clone_lab_macos

# Copy the enhanced UI
cp /path/to/enhanced_ui.py .
```

Or download it directly:
```bash
curl -o enhanced_ui.py https://your-url/enhanced_ui.py
```

### Step 2: Install Dependencies (if needed)

```bash
# Activate venv
source ~/.venv/vcl/bin/activate

# Ensure Gradio is installed
pip install gradio
```

### Step 3: Run the UI

```bash
# From the voice_clone_lab_macos directory
python enhanced_ui.py

# OR run with Gradio directly
gradio enhanced_ui.py
```

**Access at:** `http://127.0.0.1:7860`

## Usage Guide

### Tab 1: 🔧 System

Check that everything is working:
- Click "Run System Check"
- Verify "Metal (MPS) Available" appears in output
- Review any warnings

Manage speakers:
- Click "Refresh Speaker List" to see all trained speakers
- Shows ✅ Trained or ⏳ Training required status

### Tab 2: 🎙️ Audio Pipeline

**Step 1: Run Pipeline**
1. Enter a speaker name (e.g., "myvoice")
2. Upload your audio file (5-15 min recommended)
3. Click "Run Pipeline"
4. Wait for extraction, cleaning, splitting, and transcription

**Step 2: Review Transcripts (Optional)**
1. Select speaker from dropdown
2. Click "Open Review Mode"
3. This opens your default text editor with transcript file
4. Fix any errors in the transcript
5. Click "Apply Changes" to save

**Note:** Reviews happen outside the UI. Edit the file and return to apply.

### Tab 3: 🚂 Training

**Prepare Audio Codes**
1. Select speaker from dropdown
2. Click "Prepare Audio"
3. Wait for tokenization (5-10 min)
4. Proceed to training once complete

**Train Model**
1. Select speaker
2. Adjust batch size:
   - M3 8-core: **2** (default, safe)
   - M3 Pro: **4**
   - M3 Max: **8+**
3. Set epochs (default 5 is good, use 3 for faster testing)
4. Click "Start Training"
5. **⚠️ Training takes 40-60 minutes** — don't close the browser

**Monitor Training:**
- Watch the output log for "Loss: X.XX" values
- Loss should **decrease steadily** each epoch
- If loss becomes NaN → you don't have enough audio data

### Tab 4: 🔊 Generate Speech

**From Text**
1. Select your trained speaker
2. Enter text in the textbox (any length)
3. Click "Generate Speech"
4. Audio appears in the player

**From PDF**
1. Select your trained speaker
2. Upload a PDF file
3. (Optional) Set page range:
   - Start Page: first page to extract
   - End Page: last page to extract (leave empty for all)
4. Click "Convert PDF to Speech"
5. Audio appears in the player

**Tips:**
- For long PDFs (20+ pages), use page ranges
- Very long text (10,000+ characters) takes several minutes
- Audio quality matches your training data quality

### Tab 5: 📊 Speaker Info

View details about any speaker:
1. Select speaker from dropdown
2. Click "Get Info"
3. See dataset stats and training status

**Information shown:**
- Number of audio clips
- Total duration in minutes
- Min/Max/Mean clip durations
- Whether trained checkpoint exists
- Checkpoint file size

### Tab 6: ❓ Help & Docs

- Quick start guide
- Critical requirements checklist
- Training tips
- Troubleshooting section
- Links to full documentation

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Run command | Click button or press Enter |
| Stop generation | Close browser tab (careful!) |
| Refresh UI | Press F5 |

## Tips & Best Practices

### Audio Upload
- ✅ Use clear, natural speech
- ✅ Clean, quiet room (SNR > 15 dB)
- ✅ 5-15 minutes of audio
- ❌ Avoid heavy background noise
- ❌ Don't use highly compressed formats

### Training
- Start with batch_size=2 on M3 base
- Watch for "Loss: X.XX" decreasing
- If memory error: lower batch_size
- If NaN loss: you need more audio data (5+ min minimum)

### Generation
- Test with short phrases first
- For PDFs, extract a chapter first
- Very long texts may take hours
- Quality depends 100% on training audio quality

### Disk Space
- Check before training: `df -h /`
- Need at least 10 GB free
- If full: `rm -rf ~/.cache/huggingface/`

## Troubleshooting

### Issue: "Metal not available" in System Check

```bash
# Reinstall PyTorch
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Verify
python -c "import torch; print(torch.backends.mps.is_available())"
```

### Issue: "vcl command not found"

Make sure the venv is activated:
```bash
source ~/.venv/vcl/bin/activate
```

### Issue: Training produces NaN loss

Your audio is too short or too noisy. Record 5-15 minutes of clean speech.

### Issue: Generation fails with "No space left on device"

Free up disk space:
```bash
rm -rf ~/.cache/huggingface/
```

### Issue: PDF extraction is empty or garbled

- Try a different PDF
- Use `pdftotext` directly to test:
  ```bash
  pdftotext your_document.pdf output.txt
  cat output.txt
  ```
- For scanned PDFs (images), use an online OCR tool first

### Issue: UI is slow or unresponsive

- Close other applications
- Check disk space (df -h)
- Restart the UI: `python enhanced_ui.py`

### Issue: Audio playback doesn't work

- Make sure you have a speaker/headphones connected
- Try playing the file directly: `open outputs/generated/speaker/test.wav`
- Check file exists: `ls outputs/generated/speaker/`

## Advanced: Integration with Existing Installation

If you have Voice Clone Lab already installed:

1. Copy `enhanced_ui.py` to the root of `voice_clone_lab_macos`
2. Run it: `python enhanced_ui.py`
3. The UI automatically uses your existing speakers, checkpoints, and data

No configuration needed—it just works with your setup!

## Comparison: Default UI vs Enhanced UI

| Feature | Default `vcl ui` | Enhanced UI |
|---------|------------------|-------------|
| System Check | ✅ | ✅ Better |
| Audio Pipeline | ✅ | ✅ Clearer flow |
| Transcript Review | ✅ | ✅ Same |
| Training | ✅ | ✅ Better monitoring |
| Text Generation | ✅ | ✅ Same |
| PDF Support | ❌ | ✅ Full |
| Speaker Management | Basic | ✅ Detailed |
| Error Handling | Basic | ✅ Clear messages |
| Modern Design | No | ✅ Yes |

## Running Both UIs

You can run both at the same time on different ports:

```bash
# Terminal 1: Default UI on port 7860
vcl ui

# Terminal 2: Enhanced UI on port 7861
python enhanced_ui.py --server.port 7861
```

Then access:
- Default: `http://127.0.0.1:7860`
- Enhanced: `http://127.0.0.1:7861`

## Performance Tips

### For Slow Machines
- Close other applications during training
- Use batch_size=1 instead of 2
- Disable browser extensions
- Use Chrome instead of Safari for better performance

### For Fast Processing
- Use batch_size=4+ on M3 Pro/Max
- Generate in batches (don't refresh between calls)
- Keep PDF pages < 20 per batch

## Customization

Want to modify the UI? The file is `enhanced_ui.py`:

```python
# Change title
gr.Markdown("# Your Custom Title")

# Change colors/theme
theme=gr.themes.Soft()  # or Dark(), Default()

# Add/remove tabs
with gr.Tab("New Tab"):
    # Add content here
```

Then restart: `python enhanced_ui.py`

## Keyboard Input

The UI accepts all text formats:
- Plain text
- Multiple paragraphs (use newlines)
- Special characters (automatically handled)
- Very long text (no limit, but may take hours to synthesize)

## Batch Processing

To process multiple speakers/texts:

1. Text generation: Repeat for each text
2. PDF conversion: Upload each PDF separately
3. Training: Train one speaker at a time (UI handles one speaker at a time)

## Storage & Cleanup

Generated audio files are stored in:
```
outputs/generated/{speaker_name}/
```

To clean up old generations:
```bash
rm -rf outputs/generated/old_speaker/
```

## Next Steps

1. **Run System Check** (Tab 1) — Verify everything works
2. **Upload Audio** (Tab 2) — Create your first speaker
3. **Prepare & Train** (Tab 3) — Train your voice (1-2 hours)
4. **Generate Speech** (Tab 4) — Create audio!

---

**Ready? Start the UI and follow the tabs!** 🎤

For CLI commands, see QUICK_START_M3_UPDATED.md
For PDF details, see PDF_TO_SPEECH_GUIDE.md
