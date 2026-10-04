# Voice Clone Lab: PDF to Speech Guide

**Convert PDFs to speech using your trained voice clone**

This guide shows you how to extract text from PDF files and synthesize them into audio using your trained Voice Clone Lab checkpoint.

## Quick Start (Copy-Paste)

```bash
# Activate venv
source ~/.venv/vcl/bin/activate
cd voice_clone_lab_macos

# Extract text from PDF (requires pdftotext)
pdftotext your_document.pdf extracted_text.txt

# Generate speech from extracted text
vcl generate --speaker myname --text "$(cat extracted_text.txt)" --output output.wav

# Listen to result
open output.wav
```

Done! Your PDF is now speech.

## Setup: Install PDF Tools

### Option 1: Using Homebrew (Recommended)

```bash
brew install poppler
```

This installs `pdftotext` (command-line tool) needed for extraction.

### Option 2: Using pip (Python)

```bash
# Activate your venv
source ~/.venv/vcl/bin/activate

# Install pypdf library
pip install pypdf
```

Both methods work; Homebrew is simpler.

## Method 1: Command-Line (pdftotext)

### Simple Extraction

```bash
# Extract text from PDF to file
pdftotext your_document.pdf extracted_text.txt

# View extracted text
cat extracted_text.txt

# Generate speech
vcl generate --speaker myname --text "$(cat extracted_text.txt)" --output speech.wav
```

### Extract Specific Pages

```bash
# Extract only pages 1-5
pdftotext -f 1 -l 5 your_document.pdf extracted_text.txt

# -f = first page
# -l = last page
```

### Handle Complex PDFs

```bash
# Preserve layout (better for formatted text)
pdftotext -layout your_document.pdf extracted_text.txt

# Preserve column structure
pdftotext -layout -column your_document.pdf extracted_text.txt
```

## Method 2: Python Script (More Control)

Create a file called `pdf_to_speech.py`:

```python
#!/usr/bin/env python3
"""Convert PDF to speech using Voice Clone Lab."""

import sys
import subprocess
from pathlib import Path

def extract_pdf_with_pypdf(pdf_path):
    """Extract text using pypdf library."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("ERROR: pypdf not installed. Run: pip install pypdf")
        return None
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page_num, page in enumerate(reader.pages, 1):
            text += f"\n--- Page {page_num} ---\n"
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"ERROR reading PDF: {e}")
        return None

def extract_pdf_with_pdftotext(pdf_path):
    """Extract text using pdftotext command-line tool."""
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        print("ERROR: pdftotext not found. Install with: brew install poppler")
        return None
    except subprocess.CalledProcessError as e:
        print(f"ERROR running pdftotext: {e}")
        return None

def generate_speech(text, speaker, output_file):
    """Generate speech using vcl generate."""
    try:
        subprocess.run(
            ["vcl", "generate", "--speaker", speaker, "--text", text, "--output", output_file],
            check=True
        )
        print(f"✅ Speech saved to: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Generation failed: {e}")
        return False
    except FileNotFoundError:
        print("ERROR: vcl command not found. Activate venv: source ~/.venv/vcl/bin/activate")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python pdf_to_speech.py <pdf_file> <speaker_name> [output_file]")
        print("\nExample:")
        print("  python pdf_to_speech.py document.pdf myname output.wav")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    speaker = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else f"outputs/generated/{speaker}/from_pdf.wav"
    
    # Verify PDF exists
    if not Path(pdf_file).exists():
        print(f"ERROR: PDF file not found: {pdf_file}")
        sys.exit(1)
    
    print(f"📄 Extracting text from: {pdf_file}")
    
    # Try pypdf first, fallback to pdftotext
    text = extract_pdf_with_pypdf(pdf_file)
    if text is None:
        text = extract_pdf_with_pdftotext(pdf_file)
    
    if text is None:
        print("❌ Failed to extract text from PDF")
        sys.exit(1)
    
    # Clean up text
    text = text.strip()
    char_count = len(text)
    print(f"✅ Extracted {char_count} characters from {len(text.split())} words")
    
    # Warn if text is very long
    if char_count > 10000:
        print(f"\n⚠️  WARNING: Text is {char_count} characters (very long)")
        print("   This may take several minutes to synthesize.")
        print("   Consider splitting into smaller chunks.")
        response = input("\nContinue? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    print(f"\n🎤 Generating speech with speaker: {speaker}")
    
    # Generate speech
    if generate_speech(text, speaker, output_file):
        print(f"\n✅ Done! Listen to: {output_file}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
# Make executable
chmod +x pdf_to_speech.py

# Use it
python pdf_to_speech.py document.pdf myname output.wav
```

## Handling Large PDFs

### Problem: PDF is too long to synthesize at once

**Solution 1: Extract specific pages only**

```bash
# Extract only pages 1-10
pdftotext -f 1 -l 10 large_document.pdf chapter1.txt

# Generate speech
vcl generate --speaker myname --text "$(cat chapter1.txt)" --output chapter1.wav

# Repeat for other page ranges
pdftotext -f 11 -l 20 large_document.pdf chapter2.txt
vcl generate --speaker myname --text "$(cat chapter2.txt)" --output chapter2.wav
```

### Solution 2: Split text into chunks (Python)

Create `split_pdf_speech.py`:

```python
#!/usr/bin/env python3
"""Split large PDF text into chunks for synthesis."""

import sys
import subprocess
from pathlib import Path

def extract_pdf(pdf_path):
    """Extract text from PDF."""
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        print("ERROR: pdftotext not found. Install: brew install poppler")
        sys.exit(1)

def split_text_into_chunks(text, max_length=5000):
    """Split text into chunks at sentence boundaries."""
    sentences = text.replace(".", ".\n").replace("!", "!\n").replace("?", "?\n").split("\n")
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += " " + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_speech(text, speaker, output_file):
    """Generate speech using vcl generate."""
    subprocess.run(
        ["vcl", "generate", "--speaker", speaker, "--text", text, "--output", output_file],
        check=True
    )

def main():
    if len(sys.argv) < 3:
        print("Usage: python split_pdf_speech.py <pdf_file> <speaker_name>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    speaker = sys.argv[2]
    max_chunk = int(sys.argv[3]) if len(sys.argv) > 3 else 5000  # chars per chunk
    
    print(f"📄 Extracting text from: {pdf_file}")
    text = extract_pdf(pdf_file)
    
    print(f"✂️  Splitting into chunks ({max_chunk} chars max)")
    chunks = split_text_into_chunks(text, max_chunk)
    
    print(f"📊 Split into {len(chunks)} chunks")
    
    # Generate speech for each chunk
    for i, chunk in enumerate(chunks, 1):
        output_file = f"outputs/generated/{speaker}/chunk_{i:03d}.wav"
        print(f"\n[{i}/{len(chunks)}] Generating: {output_file}")
        print(f"    ({len(chunk)} chars)")
        
        try:
            generate_speech(chunk, speaker, output_file)
            print(f"    ✅ Done")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
    
    print(f"\n✅ All chunks generated!")
    print(f"   Output files: outputs/generated/{speaker}/chunk_*.wav")
    print(f"\nTo combine into single audio file:")
    print(f"   ffmpeg -i 'concat:chunk_001.wav|chunk_002.wav|chunk_003.wav' -c copy output.wav")

if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python split_pdf_speech.py large_document.pdf myname

# Then combine chunks if needed
ffmpeg -i 'concat:outputs/generated/myname/chunk_001.wav|outputs/generated/myname/chunk_002.wav' \
       -c copy outputs/generated/myname/full_book.wav
```

## Practical Examples

### Example 1: Simple Article

```bash
# Extract from article PDF
pdftotext article.pdf article.txt

# Generate speech
vcl generate --speaker me --text "$(cat article.txt)" --output article_speech.wav

# Listen
open article_speech.wav
```

### Example 2: Book Chapter

```bash
# Extract pages 45-67 of book (one chapter)
pdftotext -f 45 -l 67 mybookn.pdf chapter.txt

# Generate speech
vcl generate --speaker me --text "$(cat chapter.txt)" --output chapter.wav
```

### Example 3: Academic Paper with Cleanup

```bash
# Extract text
pdftotext paper.pdf text.txt

# Clean up (remove extra whitespace, page numbers)
sed 's/^[0-9]*$//' text.txt | tr -s '\n' | tr -s ' ' > cleaned.txt

# Generate speech
vcl generate --speaker me --text "$(cat cleaned.txt)" --output paper_audio.wav
```

## Text Cleanup Tips

PDFs often have formatting artifacts. Clean them up before synthesis:

### Remove extra whitespace
```bash
tr -s ' ' < text.txt > cleaned.txt  # Remove multiple spaces
```

### Remove page numbers
```bash
sed '/^[0-9]\+$/d' text.txt > cleaned.txt  # Remove lines with only numbers
```

### Remove headers/footers
```bash
# Remove first and last line of each "page"
sed '/^---$/d' text.txt > cleaned.txt
```

### Replace special characters
```bash
# Replace common artifacts
sed 's/—/-/g' text.txt |  # Em-dashes to hyphens
sed 's/[""]/"/g' |        # Smart quotes to straight quotes
sed 's/…/.../g' > cleaned.txt  # Ellipses
```

## Combining All Steps (Bash Script)

Create `pdf2speech.sh`:

```bash
#!/bin/bash
# PDF to Speech Converter
# Usage: ./pdf2speech.sh document.pdf speaker_name

if [ $# -lt 2 ]; then
    echo "Usage: $0 <pdf_file> <speaker_name>"
    exit 1
fi

PDF="$1"
SPEAKER="$2"
TXT="${PDF%.pdf}.txt"
OUT="outputs/generated/$SPEAKER/${PDF%.pdf}_speech.wav"

# Activate venv
source ~/.venv/vcl/bin/activate
cd voice_clone_lab_macos

echo "📄 Extracting text from: $PDF"
pdftotext "$PDF" "$TXT"

echo "🧹 Cleaning text..."
# Remove extra whitespace and page numbers
sed 's/^[0-9]*$//' "$TXT" | tr -s ' ' > "${TXT%.txt}_clean.txt"

echo "🎤 Generating speech..."
vcl generate --speaker "$SPEAKER" --text "$(cat ${TXT%.txt}_clean.txt)" --output "$OUT"

echo "✅ Done! Audio saved to: $OUT"
open "$OUT"
```

**Use it:**

```bash
chmod +x pdf2speech.sh
./pdf2speech.sh document.pdf myname
```

## Troubleshooting

### Issue: pdftotext: command not found

```bash
# Install Homebrew and poppler
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install poppler
```

### Issue: PDF extraction produces garbled text

```bash
# Try with layout preservation
pdftotext -layout your_document.pdf extracted.txt

# If that doesn't work, try alternative tools
# Install with: pip install pdfminer.six
```

### Issue: Audio is too short/long or cuts off

```bash
# vcl generate has no text length limit, but very long text takes time
# For > 10,000 characters, use chunk splitting (see above)

# Monitor while generating
vcl generate --speaker myname --text "$(cat text.txt)" --output output.wav
# Generation happens in real-time; watch the progress
```

### Issue: Text extraction has OCR artifacts (scanned PDFs)

```bash
# For scanned PDFs (images), you need OCR
# Install tesseract
brew install tesseract

# Extract with OCR
pdftotext -ocr your_scanned_document.pdf extracted.txt
# Note: This may not work in all versions; consider using online OCR tools instead
```

## Performance Expectations

| PDF Size | Extraction Time | Synthesis Time | Total |
|---|---|---|---|
| 5 pages (~2,000 chars) | < 1 sec | 5–10 min | 5–10 min |
| 20 pages (~8,000 chars) | < 1 sec | 15–20 min | 15–20 min |
| 50 pages (~20,000 chars) | 1–2 sec | 45–60 min | 45–60 min |

**Note:** Synthesis time depends on text length and your M3 variant. Generation is real-time (no waiting between phrases).

## Advanced: Batch Process Multiple PDFs

Create `batch_pdf2speech.sh`:

```bash
#!/bin/bash
# Batch convert multiple PDFs

SPEAKER="${1:-myname}"  # Default speaker is "myname"
DIRECTORY="${2:-.}"     # Default directory is current

echo "🎯 Processing all PDFs in: $DIRECTORY"
echo "🎤 Using speaker: $SPEAKER"

source ~/.venv/vcl/bin/activate
cd voice_clone_lab_macos

for pdf in "$DIRECTORY"/*.pdf; do
    if [ -f "$pdf" ]; then
        basename=$(basename "$pdf" .pdf)
        echo ""
        echo "📄 Processing: $basename"
        
        # Extract
        pdftotext "$pdf" /tmp/temp.txt
        
        # Generate
        vcl generate --speaker "$SPEAKER" \
                     --text "$(cat /tmp/temp.txt)" \
                     --output "outputs/generated/$SPEAKER/${basename}_speech.wav"
        
        echo "✅ $basename done"
    fi
done

echo ""
echo "🎉 All PDFs processed!"
```

**Use:**

```bash
chmod +x batch_pdf2speech.sh

# Process all PDFs in current directory
./batch_pdf2speech.sh myname

# Process all PDFs in specific directory
./batch_pdf2speech.sh myname ~/Documents/PDFs/
```

## Tips & Best Practices

1. **Always clean extracted text** — Remove page numbers, headers, footers
2. **Test with short PDFs first** — Verify extraction quality before batch processing
3. **Monitor disk space** — Synthesis creates WAV files (~1 MB per 1 min audio)
4. **Split large PDFs** — 20+ pages should be split into chapters
5. **Verify speaker name** — Make sure trained voice checkpoint exists: `ls ./outputs/checkpoints/`
6. **Check quality** — Always listen to first generated audio before batch processing

---

**Ready to convert PDFs to speech? Pick a method above and start synthesizing! 🎤**

For issues, see the Troubleshooting section or refer back to the main installation guide.
