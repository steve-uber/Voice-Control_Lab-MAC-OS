"""Configuration module with Apple Silicon Metal auto-detection."""

import torch
from dataclasses import dataclass, field
from typing import Optional


def _get_default_device() -> str:
    """Auto-detect Metal (MPS) on Apple Silicon, CUDA on NVIDIA, CPU fallback."""
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda:0"
    return "cpu"


def _get_default_asr_device() -> str:
    """ASR-specific device selection (same logic, for Whisper/faster-whisper)."""
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda:0"
    return "cpu"


def _get_default_compute_type() -> str:
    """Compute type: float32 for Metal (fp16 unsupported), float16 for CUDA."""
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "float32"  # Metal doesn't support fp16 well
    if torch.cuda.is_available():
        return "float16"  # CUDA prefers half-precision
    return "float32"  # CPU fallback


@dataclass
class ProjectConfig:
    """Main project configuration with Metal auto-detection."""
    device: str = field(default_factory=_get_default_device)
    checkpoint_dir: str = "outputs/checkpoints"
    data_dir: str = "data"
    output_dir: str = "outputs"
    sample_rate: int = 24000

    def __post_init__(self):
        """Validate device after initialization."""
        print(f"🎯 Using device: {self.device}")
        if self.device == "mps":
            print("   Metal (MPS) acceleration enabled for Apple Silicon")
        elif self.device.startswith("cuda"):
            print("   CUDA GPU acceleration enabled")
        else:
            print("   CPU mode (slow, fallback only)")


@dataclass
class ASRConfig:
    """ASR (Automatic Speech Recognition) configuration."""
    device: str = field(default_factory=_get_default_asr_device)
    compute_type: str = field(default_factory=_get_default_compute_type)
    model: str = "base"  # tiny, base, small, medium, large
    language: Optional[str] = None  # Auto-detect if None

    def __post_init__(self):
        """Validate ASR config after initialization."""
        print(f"📢 ASR Config: device={self.device}, compute_type={self.compute_type}, model={self.model}")


@dataclass
class TrainingConfig:
    """Training configuration with Metal-safe defaults."""
    batch_size: int = 2  # Safe default for M3 base; increase on Pro/Max
    learning_rate: float = 1e-4
    epochs: int = 5
    device: str = field(default_factory=_get_default_device)
    compute_type: str = field(default_factory=_get_default_compute_type)

    def __post_init__(self):
        """Warn on unsafe batch sizes."""
        if self.device == "mps" and self.batch_size > 4:
            print(f"⚠️  Warning: batch_size={self.batch_size} may cause OOM on M3 base (safe limit: 2-4)")
        print(f"🚂 Training: batch_size={self.batch_size}, epochs={self.epochs}, device={self.device}")


# Create global config instances
project_config = ProjectConfig()
asr_config = ASRConfig()
training_config = TrainingConfig()
