#!/usr/bin/env python3
"""
Enhanced Web UI for Voice Clone Lab - macOS Edition
Complete interface for all training and generation features
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
import gradio as gr
from typing import Optional, Tuple
import shutil

class VCLManager:
    """Manage Voice Clone Lab operations."""

    def __init__(self):
        self.project_root = Path.cwd()
        self.data_dir = self.project_root / "data" / "voices"
        self.output_dir = self.project_root / "outputs"
        self.checkpoint_dir = self.output_dir / "checkpoints"

    def get_speakers(self) -> list:
        """Get list of trained speakers."""
        if not self.data_dir.exists():
            return []
        return [d.name for d in self.data_dir.iterdir() if d.is_dir()]

    def get_checkpoints(self) -> dict:
        """Get list of trained checkpoints."""
        checkpoints = {}
        if self.checkpoint_dir.exists():
            for speaker_dir in self.checkpoint_dir.iterdir():
                if speaker_dir.is_dir():
                    model_file = speaker_dir / "model.safetensors"
                    if model_file.exists():
                        checkpoints[speaker_dir.name] = {
                            "path": str(speaker_dir),
                            "exists": True
                        }
        return checkpoints

    def check_system(self) -> dict:
        """Run vcl check and return results."""
        try:
            result = subprocess.run(
                ["vcl", "check"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "status": "success",
                "output": result.stdout,
                "errors": result.stderr
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "errors": str(e)
            }

    def run_vcl_command(self, cmd: list, timeout: int = 3600) -> Tuple[bool, str]:
        """Run a vcl command and return success status and output."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            success = result.returncode == 0
            output = result.stdout + result.stderr
            return success, output
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout} seconds"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def extract_pdf_text(self, pdf_path: str, start_page: int = 1, end_page: Optional[int] = None) -> Tuple[bool, str]:
        """Extract text from PDF."""
        try:
            import subprocess
            cmd = ["pdftotext"]

            if start_page > 1 or end_page:
                cmd.extend(["-f", str(start_page)])
                if end_page:
                    cmd.extend(["-l", str(end_page)])

            cmd.extend([pdf_path, "-"])

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, f"Error extracting PDF: {str(e)}"

# Initialize manager
vcl = VCLManager()

# ============================================================================
# GRADIO INTERFACE FUNCTIONS
# ============================================================================

def check_system_status():
    """Check system and return status."""
    result = vcl.check_system()

    if result["status"] == "success":
        return f"✅ System Check Passed\n\n{result['output']}"
    else:
        return f"❌ System Check Failed\n\n{result['errors']}"

def run_pipeline(speaker_name: str, audio_file) -> str:
    """Run full vcl run pipeline."""
    if not speaker_name:
        return "❌ Error: Speaker name is required"

    if audio_file is None:
        return "❌ Error: Audio file is required"

    # Get audio file path
    audio_path = audio_file if isinstance(audio_file, str) else audio_file.name

    cmd = ["vcl", "run", "--speaker", speaker_name, "--input", audio_path, "--force"]
    success, output = vcl.run_vcl_command(cmd, timeout=600)

    if success:
        return f"✅ Pipeline completed successfully\n\n{output}"
    else:
        return f"❌ Pipeline failed\n\n{output}"

def review_transcripts(speaker_name: str) -> str:
    """Review transcripts for a speaker."""
    if not speaker_name:
        return "❌ Error: Speaker name is required"

    cmd = ["vcl", "transcribe", "--speaker", speaker_name, "--review"]
    success, output = vcl.run_vcl_command(cmd, timeout=300)

    if success:
        return f"✅ Review mode opened\n\n{output}\n\nEdit the transcripts file and return to apply changes."
    else:
        return f"❌ Failed to open review mode\n\n{output}"

def apply_transcript_review(speaker_name: str) -> str:
    """Apply reviewed transcripts."""
    if not speaker_name:
        return "❌ Error: Speaker name is required"

    cmd = ["vcl", "transcribe", "--speaker", speaker_name, "--apply-review", "--force"]
    success, output = vcl.run_vcl_command(cmd, timeout=300)

    if success:
        return f"✅ Transcript review applied\n\n{output}"
    else:
        return f"❌ Failed to apply review\n\n{output}"

def prepare_audio(speaker_name: str) -> str:
    """Prepare audio codes for training."""
    if not speaker_name:
        return "❌ Error: Speaker name is required"

    cmd = ["vcl", "prepare", "--speaker", speaker_name]
    success, output = vcl.run_vcl_command(cmd, timeout=600)

    if success:
        return f"✅ Audio preparation completed\n\n{output}"
    else:
        return f"❌ Audio preparation failed\n\n{output}"

def train_model(speaker_name: str, batch_size: int, epochs: int) -> str:
    """Train voice model."""
    if not speaker_name:
        return "❌ Error: Speaker name is required"

    if batch_size < 1:
        return "❌ Error: Batch size must be >= 1"

    if epochs < 1:
        return "❌ Error: Epochs must be >= 1"

    cmd = [
        "vcl", "train",
        "--speaker", speaker_name,
        "--batch-size", str(batch_size),
        "--epochs", str(epochs)
    ]
    success, output = vcl.run_vcl_command(cmd, timeout=3600)

    if success:
        return f"✅ Training completed successfully\n\n{output}"
    else:
        return f"❌ Training failed\n\n{output}"

def generate_speech(speaker_name: str, text: str) -> Tuple[str, Optional[str]]:
    """Generate speech from text."""
    if not speaker_name:
        return "❌ Error: Speaker name is required", None

    if not text or text.strip() == "":
        return "❌ Error: Text is required", None

    cmd = [
        "vcl", "generate",
        "--speaker", speaker_name,
        "--text", text
    ]
    success, output = vcl.run_vcl_command(cmd, timeout=300)

    if success:
        # Find generated audio file
        audio_path = vcl.output_dir / "generated" / speaker_name / "test.wav"
        if audio_path.exists():
            return f"✅ Speech generated successfully\n\n{output}", str(audio_path)
        else:
            return f"✅ Command succeeded but audio file not found\n\n{output}", None
    else:
        return f"❌ Generation failed\n\n{output}", None

def generate_from_pdf(speaker_name: str, pdf_file, start_page: int = 1, end_page: Optional[int] = None) -> Tuple[str, Optional[str]]:
    """Generate speech from PDF."""
    if not speaker_name:
        return "❌ Error: Speaker name is required", None

    if pdf_file is None:
        return "❌ Error: PDF file is required", None

    pdf_path = pdf_file if isinstance(pdf_file, str) else pdf_file.name

    # Extract text from PDF
    success, text = vcl.extract_pdf_text(pdf_path, start_page, end_page)

    if not success:
        return f"❌ Failed to extract text from PDF\n\n{text}", None

    if not text.strip():
        return "❌ Error: PDF extraction produced empty text", None

    # Warn if text is very long
    if len(text) > 10000:
        text_preview = text[:500] + "..."
        full_msg = f"⚠️  Warning: Extracted {len(text)} characters\n\nPreview:\n{text_preview}\n\nThis may take several minutes to synthesize. Proceeding..."
    else:
        full_msg = f"📄 Extracted {len(text)} characters from PDF\n\nGenerating speech..."

    # Generate speech
    result, audio_path = generate_speech(speaker_name, text)

    return full_msg + "\n\n" + result, audio_path

def list_speakers() -> str:
    """List all speakers and their status."""
    speakers = vcl.get_speakers()
    checkpoints = vcl.get_checkpoints()

    if not speakers:
        return "No speakers found. Run the pipeline to create your first speaker."

    info = "📊 Available Speakers:\n\n"
    for speaker in speakers:
        is_trained = speaker in checkpoints
        status = "✅ Trained" if is_trained else "⏳ Training required"
        info += f"• {speaker} - {status}\n"

    return info

def get_speaker_info(speaker_name: str) -> str:
    """Get detailed info about a speaker."""
    if not speaker_name:
        return "❌ Error: Speaker name is required"

    speaker_dir = vcl.data_dir / speaker_name
    if not speaker_dir.exists():
        return f"❌ Speaker '{speaker_name}' not found"

    info = f"📋 Speaker: {speaker_name}\n\n"

    # Check dataset stats
    stats_file = speaker_dir / "dataset" / "dataset_stats.json"
    if stats_file.exists():
        try:
            with open(stats_file) as f:
                stats = json.load(f)
                info += "Dataset Statistics:\n"
                info += f"  • Clips: {stats.get('clips', 'N/A')}\n"
                info += f"  • Duration: {stats.get('duration_minutes', 'N/A')} minutes\n"
                info += f"  • Min/Max/Mean: {stats.get('duration_min', 'N/A')}s / {stats.get('duration_max', 'N/A')}s / {stats.get('duration_mean', 'N/A')}s\n"
        except:
            info += "Dataset Statistics: (Unable to read)\n"

    # Check checkpoint
    checkpoint_dir = vcl.checkpoint_dir / speaker_name
    if checkpoint_dir.exists():
        info += "\n✅ Trained Checkpoint Found\n"
        model_file = checkpoint_dir / "model.safetensors"
        if model_file.exists():
            size_mb = model_file.stat().st_size / (1024 * 1024)
            info += f"  • Model size: {size_mb:.1f} MB\n"
    else:
        info += "\n⏳ No trained checkpoint yet\n"

    return info

# ============================================================================
# BUILD GRADIO INTERFACE
# ============================================================================

def build_interface():
    """Build the Gradio interface."""

    speakers = vcl.get_speakers()

    with gr.Blocks(title="Voice Clone Lab - macOS", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎤 Voice Clone Lab - Enhanced Web UI")
        gr.Markdown("Complete interface for voice cloning on Apple Silicon Macs")

        # ====================================================================
        # TAB 1: SYSTEM STATUS
        # ====================================================================
        with gr.Tab("🔧 System"):
            gr.Markdown("### System Status & Health Check")

            col1, col2 = gr.Group(), gr.Group()

            with gr.Group():
                check_btn = gr.Button("Run System Check", size="lg", variant="primary")
                status_output = gr.Textbox(label="Status", lines=15, interactive=False)

            def handle_check():
                return check_system_status()

            check_btn.click(handle_check, outputs=status_output)

            gr.Markdown("### Speaker Management")
            with gr.Group():
                speakers_output = gr.Textbox(label="Available Speakers", lines=10, interactive=False)
                refresh_btn = gr.Button("Refresh Speaker List")

                def refresh_speakers():
                    return list_speakers()

                refresh_btn.click(refresh_speakers, outputs=speakers_output)

        # ====================================================================
        # TAB 2: AUDIO PIPELINE
        # ====================================================================
        with gr.Tab("🎙️ Audio Pipeline"):
            gr.Markdown("### Step 1: Extract, Clean & Transcribe Audio")
            gr.Markdown("Upload your audio file and create a new speaker")

            with gr.Group():
                speaker_input = gr.Textbox(label="Speaker Name", placeholder="e.g., 'myvoice'")
                audio_input = gr.Audio(label="Audio File (5-15 min recommended)", type="filepath")
                run_btn = gr.Button("Run Pipeline", size="lg", variant="primary")
                run_output = gr.Textbox(label="Output", lines=20, interactive=False)

            run_btn.click(run_pipeline, inputs=[speaker_input, audio_input], outputs=run_output)

            gr.Markdown("### Step 2: Review Transcripts (Optional)")
            gr.Markdown("Proofread and fix any transcription errors")

            with gr.Group():
                speaker_review = gr.Dropdown(
                    choices=speakers,
                    label="Select Speaker",
                    interactive=True
                )
                gr.Button("Refresh Speakers").click(
                    lambda: gr.Dropdown(choices=vcl.get_speakers()),
                    outputs=speaker_review
                )

                review_btn = gr.Button("Open Review Mode")
                review_output = gr.Textbox(label="Output", lines=10, interactive=False)

                apply_btn = gr.Button("Apply Changes")
                apply_output = gr.Textbox(label="Output", lines=5, interactive=False)

            review_btn.click(review_transcripts, inputs=speaker_review, outputs=review_output)
            apply_btn.click(apply_transcript_review, inputs=speaker_review, outputs=apply_output)

        # ====================================================================
        # TAB 3: TRAINING
        # ====================================================================
        with gr.Tab("🚂 Training"):
            gr.Markdown("### Prepare Audio Codes")
            gr.Markdown("Convert audio to token codes (required before training)")

            with gr.Group():
                speaker_prep = gr.Dropdown(
                    choices=speakers,
                    label="Select Speaker",
                    interactive=True
                )
                prepare_btn = gr.Button("Prepare Audio", size="lg", variant="primary")
                prepare_output = gr.Textbox(label="Output", lines=15, interactive=False)

            prepare_btn.click(prepare_audio, inputs=speaker_prep, outputs=prepare_output)

            gr.Markdown("### Train Voice Model")
            gr.Markdown("⚠️  Training takes 40-60 minutes on M3. Ensure you have 10+ GB free disk space.")

            with gr.Group():
                speaker_train = gr.Dropdown(
                    choices=speakers,
                    label="Select Speaker",
                    interactive=True
                )

                with gr.Row():
                    batch_size = gr.Slider(
                        label="Batch Size",
                        minimum=1,
                        maximum=16,
                        step=1,
                        value=2,
                        info="M3 base: 2 | M3 Pro: 4 | M3 Max: 8"
                    )
                    epochs = gr.Slider(
                        label="Epochs",
                        minimum=1,
                        maximum=10,
                        step=1,
                        value=5,
                        info="More epochs = better quality but slower"
                    )

                train_btn = gr.Button("Start Training", size="lg", variant="primary")
                train_output = gr.Textbox(label="Training Output", lines=20, interactive=False)

            train_btn.click(
                train_model,
                inputs=[speaker_train, batch_size, epochs],
                outputs=train_output
            )

        # ====================================================================
        # TAB 4: GENERATION
        # ====================================================================
        with gr.Tab("🔊 Generate Speech"):
            gr.Markdown("### Generate from Text")

            with gr.Group():
                speaker_gen = gr.Dropdown(
                    choices=speakers,
                    label="Select Speaker",
                    interactive=True
                )
                text_input = gr.Textbox(
                    label="Text to Synthesize",
                    placeholder="Enter text here...",
                    lines=5
                )
                gen_btn = gr.Button("Generate Speech", size="lg", variant="primary")

                with gr.Row():
                    gen_output = gr.Textbox(label="Status", lines=10, interactive=False)
                    audio_output = gr.Audio(label="Generated Audio", type="filepath")

            gen_btn.click(
                generate_speech,
                inputs=[speaker_gen, text_input],
                outputs=[gen_output, audio_output]
            )

            gr.Markdown("### Generate from PDF")
            gr.Markdown("Upload a PDF and convert it to speech")

            with gr.Group():
                speaker_pdf = gr.Dropdown(
                    choices=speakers,
                    label="Select Speaker",
                    interactive=True
                )
                pdf_input = gr.File(label="PDF File", file_types=[".pdf"])

                with gr.Row():
                    start_page = gr.Number(
                        label="Start Page",
                        value=1,
                        precision=0,
                        info="First page to extract"
                    )
                    end_page = gr.Number(
                        label="End Page (optional)",
                        value=None,
                        precision=0,
                        info="Leave empty for all pages"
                    )

                pdf_btn = gr.Button("Convert PDF to Speech", size="lg", variant="primary")

                with gr.Row():
                    pdf_output = gr.Textbox(label="Status", lines=10, interactive=False)
                    pdf_audio = gr.Audio(label="Generated Audio", type="filepath")

            pdf_btn.click(
                generate_from_pdf,
                inputs=[speaker_pdf, pdf_input, start_page, end_page],
                outputs=[pdf_output, pdf_audio]
            )

        # ====================================================================
        # TAB 5: SPEAKER INFO
        # ====================================================================
        with gr.Tab("📊 Speaker Info"):
            gr.Markdown("### Get Speaker Details")

            with gr.Group():
                speaker_info_select = gr.Dropdown(
                    choices=speakers,
                    label="Select Speaker",
                    interactive=True
                )
                info_btn = gr.Button("Get Info")
                info_output = gr.Textbox(label="Speaker Information", lines=20, interactive=False)

            info_btn.click(
                get_speaker_info,
                inputs=speaker_info_select,
                outputs=info_output
            )

        # ====================================================================
        # TAB 6: HELP & DOCS
        # ====================================================================
        with gr.Tab("❓ Help & Docs"):
            gr.Markdown("""
            # Voice Clone Lab - Enhanced UI Help

            ## Quick Start
            1. **System Check** - Verify Metal GPU is available
            2. **Audio Pipeline** - Upload your voice (5-15 min recommended)
            3. **Review** - Fix any transcription errors (optional)
            4. **Prepare** - Encode audio to codes
            5. **Train** - Fine-tune the model (40-60 minutes)
            6. **Generate** - Create speech from text or PDF

            ## Critical Requirements
            - **Audio duration**: 5-15 minutes minimum
            - **Audio quality**: Clean, SNR > 15 dB (no heavy background noise)
            - **Disk space**: 10+ GB free before training
            - **Batch size**: M3 base=2, M3 Pro=4, M3 Max=8

            ## Training Tips
            - Start with batch_size=2 on M3 base
            - If OOM: lower batch_size or epochs
            - Loss should decrease steadily (if NaN → not enough audio data)
            - Monitor disk space during training

            ## PDF Conversion
            - Supports any PDF file
            - Extracts text and synthesizes to speech
            - Select page range for large documents
            - Very long PDFs may take hours

            ## Troubleshooting

            ### Metal not detected
            Reinstall PyTorch:
            ```bash
            pip uninstall torch torchvision torchaudio -y
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
            ```

            ### Training produces NaN loss
            You don't have enough audio data. Record 5+ minutes of clean speech.

            ### Out of memory
            Lower batch_size to 1, or reduce epochs to 3.

            ### No space left on device
            Free space:
            ```bash
            rm -rf ~/.cache/huggingface/
            ```

            ## Documentation
            See the included guides:
            - `QUICK_START_M3_UPDATED.md` - Fast setup
            - `INSTALL_MACOS_UPDATED.md` - Detailed guide
            - `PDF_TO_SPEECH_GUIDE.md` - PDF conversion
            """)

    return interface

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🎤 Launching Voice Clone Lab Enhanced Web UI...")
    print("📍 Opening at http://127.0.0.1:7860")

    interface = build_interface()
    interface.launch(share=False, show_error=True)
