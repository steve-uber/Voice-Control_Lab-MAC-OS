#!/bin/bash
# Voice Clone Lab Installation Script for Apple Silicon M3 Macs
# Updated 2026-09-24

set -e  # Exit on error

echo "🎤 Voice Clone Lab - Apple Silicon M3 Installation"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is for macOS only${NC}"
    exit 1
fi

# Check if Apple Silicon
if ! [[ $(uname -m) == "arm64" ]]; then
    echo -e "${YELLOW}⚠️  This is not an Apple Silicon Mac (arm64)${NC}"
    echo "   This script is optimized for M1/M2/M3 Macs"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo -e "${GREEN}✓ Creating virtual environment...${NC}"
VENV_PATH="$HOME/.venv/vcl"

if [ -d "$VENV_PATH" ]; then
    echo "   Virtual environment already exists at $VENV_PATH"
    read -p "   Replace it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_PATH"
    else
        echo "   Using existing virtual environment"
    fi
fi

if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
fi

# Activate venv
source "$VENV_PATH/bin/activate"
echo -e "   ✅ Virtual environment activated: $VENV_PATH"

# Upgrade pip
echo -e "\n${GREEN}✓ Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install PyTorch with Metal support (CRITICAL!)
echo -e "\n${GREEN}✓ Installing PyTorch with Metal support...${NC}"
echo "   This is the most important step for GPU acceleration"
pip install --index-url https://download.pytorch.org/whl/nightly/cpu torch torchvision torchaudio

# Verify Metal support
echo -e "\n${GREEN}✓ Verifying Metal support...${NC}"
python3 << 'EOF'
import torch

if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    print("   ✅ Metal (MPS) is available - GPU acceleration enabled!")
else:
    print("   ❌ Metal (MPS) is NOT available")
    print("   Try reinstalling PyTorch:")
    print("   pip uninstall torch torchvision torchaudio -y")
    print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Metal verification failed${NC}"
    exit 1
fi

# Install other dependencies
echo -e "\n${GREEN}✓ Installing other dependencies...${NC}"
pip install --break-system-packages -r requirements.txt

# Install system tools
echo -e "\n${GREEN}✓ Installing system tools (poppler for PDF extraction)...${NC}"
if command -v brew &> /dev/null; then
    brew install poppler ffmpeg
else
    echo "   ⚠️  Homebrew not found - install with:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "   Then run: brew install poppler ffmpeg"
fi

# Create data directories
echo -e "\n${GREEN}✓ Creating data directories...${NC}"
mkdir -p data/speakers
mkdir -p outputs/checkpoints
mkdir -p outputs/generated
echo -e "   ✅ Created: data/speakers/, outputs/checkpoints/, outputs/generated/"

# Run system check
echo -e "\n${GREEN}✓ Running system check...${NC}"
python3 system.py

echo -e "\n${GREEN}=================================================="
echo "✅ Installation complete!"
echo "==================================================${NC}"

echo ""
echo "📚 Next steps:"
echo ""
echo "1. Activate virtual environment in new terminal:"
echo "   source ~/.venv/vcl/bin/activate"
echo ""
echo "2. Record 5-15 minutes of clear, clean audio (critical!)"
echo ""
echo "3. Follow the quick start guide:"
echo "   cat QUICK_START_M3_UPDATED.md"
echo ""
echo "4. Start with the web UI:"
echo "   python enhanced_ui.py"
echo ""
echo "   Or use CLI:"
echo "   vcl run --speaker myname --input recording.wav"
echo ""
