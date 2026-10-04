"""Transcription module with Metal compatibility."""

from pathlib import Path
from typing import Callable, Optional
import torch


def get_transcriber(
    backend: str = "whisper",
    model_name: str = "base",
    language: Optional[str] = None,
) -> Callable:
    """
    Get transcriber function with Metal (MPS) compatibility.

    Args:
        backend: "whisper" or "faster-whisper"
        model_name: Model size (tiny, base, small, medium, large)
        language: Language code or None for auto-detect

    Returns:
        Transcriber function that takes Path and returns text

    Note:
        - Whisper model is loaded on CPU (more stable than Metal)
        - Uses fp16=False (float32 only) for Metal/CPU compatibility
        - Transcription speed: ~1 sec per 10 sec audio on CPU
    """

    if backend == "whisper":
        import whisper

        print(f"📢 Loading Whisper model '{model_name}' on CPU (stable, float32)...")

        # Load model on CPU (more stable than moving to Metal)
        model = whisper.load_model(model_name, device="cpu")

        def transcribe(path: Path) -> str:
            """Transcribe audio file to text."""
            print(f"   Transcribing: {path.name}")

            # Use fp16=False on Metal/CPU (only float32 supported)
            result = model.transcribe(
                str(path),
                language=language or None,
                fp16=False,  # Metal doesn't support fp16 well
                verbose=False,
            )

            text = str(result.get("text", "")).strip()
            print(f"   ✅ Transcribed {len(text)} characters")
            return text

        return transcribe

    elif backend == "faster-whisper":
        from faster_whisper import WhisperModel

        print(f"📢 Loading faster-whisper model '{model_name}' on CPU...")

        # Determine compute type based on device
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            compute_type = "float32"  # Metal: use float32
            device = "cpu"  # Load on CPU
        elif torch.cuda.is_available():
            compute_type = "float16"  # CUDA: use float16
            device = "cuda"
        else:
            compute_type = "float32"  # CPU: use float32
            device = "cpu"

        print(f"   Device: {device}, Compute: {compute_type}")

        model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

        def transcribe(path: Path) -> str:
            """Transcribe audio file to text."""
            print(f"   Transcribing: {path.name}")

            segments, info = model.transcribe(
                str(path),
                language=language or None,
                beam_size=5,
            )

            text = " ".join(segment.text for segment in segments).strip()
            print(f"   ✅ Transcribed {len(text)} characters")
            return text

        return transcribe

    else:
        raise ValueError(f"Unknown backend: {backend}")


def transcribe_file(
    audio_path: Path,
    backend: str = "whisper",
    model_name: str = "base",
    language: Optional[str] = None,
) -> str:
    """
    Transcribe a single audio file.

    Args:
        audio_path: Path to audio file
        backend: Transcription backend
        model_name: Model size
        language: Language code

    Returns:
        Transcribed text
    """
    transcriber = get_transcriber(backend, model_name, language)
    return transcriber(audio_path)


def transcribe_batch(
    audio_paths: list,
    backend: str = "whisper",
    model_name: str = "base",
    language: Optional[str] = None,
) -> dict:
    """
    Transcribe multiple audio files.

    Args:
        audio_paths: List of paths to audio files
        backend: Transcription backend
        model_name: Model size
        language: Language code

    Returns:
        Dict mapping file paths to transcripts
    """
    print(f"📢 Transcribing {len(audio_paths)} files...")

    transcriber = get_transcriber(backend, model_name, language)
    results = {}

    for i, path in enumerate(audio_paths, 1):
        print(f"\n[{i}/{len(audio_paths)}] {path.name}")
        try:
            results[str(path)] = transcriber(Path(path))
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[str(path)] = None

    print(f"\n✅ Transcribed {len([v for v in results.values() if v])} / {len(audio_paths)} files")
    return results


if __name__ == "__main__":
    # Example usage
    from pathlib import Path

    audio_file = Path("test_audio.wav")
    if audio_file.exists():
        text = transcribe_file(audio_file)
        print(f"\n{text}")
    else:
        print("No test audio file found")
