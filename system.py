"""System detection and health checks for Metal/CUDA/CPU devices."""

import platform
import torch
import subprocess
from typing import Dict, List


def get_system_info() -> Dict[str, str]:
    """Get system information."""
    return {
        "platform": platform.system(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
    }


def check_metal_availability() -> Dict[str, bool]:
    """Check Metal (MPS) availability on Apple Silicon."""
    info = {
        "is_apple": platform.system() == "Darwin",
        "is_apple_silicon": "arm64" in platform.processor() or "arm" in platform.processor(),
        "torch_has_mps": hasattr(torch.backends, "mps"),
        "mps_available": False,
        "mps_built": False,
    }

    if info["torch_has_mps"]:
        info["mps_built"] = torch.backends.mps.is_built()
        info["mps_available"] = torch.backends.mps.is_available()

    return info


def check_cuda_availability() -> Dict[str, bool]:
    """Check CUDA availability on NVIDIA GPUs."""
    return {
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda,
        "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def get_device_summary() -> str:
    """Get human-readable device summary."""
    metal = check_metal_availability()
    cuda = check_cuda_availability()

    if metal["mps_available"]:
        return "✅ Metal (MPS) Available — Apple Silicon GPU acceleration enabled"
    elif cuda["cuda_available"]:
        return f"✅ CUDA Available — {cuda['device_name']} GPU acceleration enabled"
    else:
        return "⚠️  CPU Mode — No GPU acceleration (training will be slow)"


def run_system_check() -> Dict:
    """Run comprehensive system check."""
    print("\n" + "="*60)
    print("🔧 VOICE CLONE LAB SYSTEM CHECK")
    print("="*60 + "\n")

    # System info
    sys_info = get_system_info()
    print("📊 System Information:")
    print(f"   Platform: {sys_info['platform']}")
    print(f"   Processor: {sys_info['processor']}")
    print(f"   Python: {sys_info['python_version']}")
    print(f"   PyTorch: {sys_info['torch_version']}\n")

    # Metal check
    metal = check_metal_availability()
    print("🍎 Apple Silicon Check:")
    print(f"   macOS: {metal['is_apple']}")
    print(f"   Apple Silicon: {metal['is_apple_silicon']}")
    print(f"   PyTorch has MPS: {metal['torch_has_mps']}")
    print(f"   MPS Built: {metal['mps_built']}")
    print(f"   MPS Available: {metal['mps_available']}\n")

    if metal["mps_available"]:
        print("   ✅ Metal GPU acceleration is ready!\n")
    elif metal['is_apple'] and not metal['mps_available']:
        print("   ⚠️  Metal not available. Fix:")
        print("      pip uninstall torch torchvision torchaudio -y")
        print("      pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu\n")

    # CUDA check
    cuda = check_cuda_availability()
    print("🔌 NVIDIA GPU Check:")
    print(f"   CUDA Available: {cuda['cuda_available']}")
    if cuda['cuda_available']:
        print(f"   CUDA Version: {cuda['cuda_version']}")
        print(f"   Devices: {cuda['device_count']}")
        print(f"   Device: {cuda['device_name']}\n")
        print("   ✅ CUDA is available\n")
    else:
        print("   (No NVIDIA GPU)\n")

    # Device summary
    print("🎯 Selected Device:")
    print(f"   {get_device_summary()}\n")

    # Disk space check
    print("💾 Disk Space:")
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        lines = result.stdout.split("\n")
        if len(lines) > 1:
            parts = lines[1].split()
            print(f"   Total: {parts[1]}")
            print(f"   Used: {parts[2]}")
            print(f"   Available: {parts[3]}")
            if len(parts) > 4:
                print(f"   Usage: {parts[4]}\n")
    except Exception as e:
        print(f"   (Could not check: {e})\n")

    # Model cache check
    print("📦 Model Cache:")
    try:
        result = subprocess.run(["du", "-sh", f"{torch.hub.get_dir()}"], capture_output=True, text=True)
        if result.returncode == 0:
            size = result.stdout.split()[0]
            print(f"   Cache size: {size}\n")
    except Exception as e:
        print(f"   (Could not check: {e})\n")

    print("="*60)
    print("✅ System check complete!\n")

    return {
        "system": sys_info,
        "metal": metal,
        "cuda": cuda,
        "device_summary": get_device_summary(),
    }


def get_install_hint() -> str:
    """Get installation hint based on platform."""
    system = platform.system()

    if system == "Darwin":
        return "macOS detected. Use: brew install poppler"
    elif system == "Linux":
        return "Linux detected. Use: apt-get install poppler-utils"
    else:
        return "Windows detected. Use: choco install poppler"


if __name__ == "__main__":
    run_system_check()
