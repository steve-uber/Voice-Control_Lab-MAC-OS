"""Prepare audio data for training - CPU ONLY (Metal-safe tokenization)."""

import argparse
import os
from pathlib import Path
from typing import List
import torch
import json


def get_audio_codes(tokenizer_path: str, audio_codes: List[int], speaker_name: str) -> List[int]:
    """
    Encode audio codes using tokenizer (CPU-only for Metal compatibility).

    Args:
        tokenizer_path: Path to tokenizer model
        audio_codes: Raw audio codes to tokenize
        speaker_name: Speaker name for logging

    Returns:
        Encoded audio codes
    """
    print(f"🎤 Preparing audio codes for speaker: {speaker_name}")
    print(f"   Tokenizer path: {tokenizer_path}")
    print(f"   Input codes: {len(audio_codes)} items")

    try:
        from transformers import AutoTokenizer
    except ImportError:
        print("❌ transformers not installed. Run: pip install transformers")
        return audio_codes

    try:
        # Load tokenizer on CPU only (avoids HuggingFace CUDA checks)
        print("   Loading tokenizer (CPU-only)...")
        tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_path,
            device_map="cpu",  # CPU-only load
            trust_remote_code=True,
        )

        # Encode on CPU (tokenization is lightweight, no GPU needed)
        print("   Encoding audio codes (CPU)...")
        encoded = tokenizer.encode(audio_codes, return_tensors="pt")

        # Convert to list
        result = encoded[0].tolist()

        print(f"   ✅ Encoded {len(result)} codes")
        return result

    except Exception as e:
        print(f"   ⚠️  Tokenization error: {e}")
        print("   Falling back to raw audio codes")
        return audio_codes


def prepare_speaker_data(
    speaker_dir: Path,
    tokenizer_path: str,
    output_dir: Path,
    device: str = "cpu",  # Always CPU for tokenization
) -> dict:
    """
    Prepare all audio for a speaker.

    Args:
        speaker_dir: Directory with speaker's audio files
        tokenizer_path: Path to tokenizer model
        output_dir: Output directory for prepared data
        device: Device (ignored - always uses CPU)

    Returns:
        Preparation summary
    """
    speaker_name = speaker_dir.name
    print(f"\n{'='*60}")
    print(f"📦 Preparing data for speaker: {speaker_name}")
    print(f"{'='*60}")

    # Find audio files
    audio_files = list(speaker_dir.glob("*.wav"))
    print(f"   Found {len(audio_files)} audio files")

    if not audio_files:
        print("   ❌ No audio files found")
        return {"success": False, "speaker": speaker_name}

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each audio file
    prepared_files = []
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n   [{i}/{len(audio_files)}] {audio_file.name}")

        try:
            # Load audio
            import librosa
            audio, sr = librosa.load(str(audio_file), sr=24000)

            # Simple tokenization: just quantize to 8-bit
            # (Real tokenization would use the Qwen3-TTS tokenizer)
            codes = ((audio + 1) / 2 * 255).astype('int32').tolist()

            # Save codes
            output_file = output_dir / f"{audio_file.stem}_codes.pt"
            torch.save(torch.tensor(codes), str(output_file))

            prepared_files.append(str(output_file))
            print(f"      ✅ Prepared ({len(codes)} codes)")

        except Exception as e:
            print(f"      ❌ Error: {e}")

    # Save summary
    summary = {
        "speaker": speaker_name,
        "total_files": len(audio_files),
        "prepared_files": len(prepared_files),
        "output_dir": str(output_dir),
        "prepared_files_list": prepared_files,
    }

    summary_file = output_dir / "summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ Preparation complete")
    print(f"   Prepared files: {len(prepared_files)}/{len(audio_files)}")
    print(f"   Output directory: {output_dir}")
    print(f"{'='*60}\n")

    return summary


def main():
    """CLI interface for data preparation."""
    parser = argparse.ArgumentParser(
        description="Prepare audio data for Voice Clone Lab training (CPU-only)"
    )

    parser.add_argument(
        "--speaker-dir",
        type=Path,
        required=True,
        help="Directory containing speaker's audio files"
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: speaker_dir/prepared)"
    )

    parser.add_argument(
        "--tokenizer-path",
        type=str,
        default="Qwen/Qwen3-TTS",
        help="Path to tokenizer model (default: Qwen/Qwen3-TTS)"
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device (CPU-only, this argument is ignored)"
    )

    args = parser.parse_args()

    # Set output directory
    output_dir = args.output_dir or args.speaker_dir / "prepared"

    # Validate
    if not args.speaker_dir.exists():
        print(f"❌ Speaker directory not found: {args.speaker_dir}")
        return

    # Prepare
    summary = prepare_speaker_data(
        args.speaker_dir,
        args.tokenizer_path,
        output_dir,
        device="cpu",  # Always CPU
    )

    if summary.get("success") is False:
        exit(1)


if __name__ == "__main__":
    main()
