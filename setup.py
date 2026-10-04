"""Setup script for Voice Clone Lab on Apple Silicon Macs."""

from setuptools import setup, find_packages
from pathlib import Path

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = [
    line.strip()
    for line in requirements_path.read_text().split("\n")
    if line.strip() and not line.startswith("#")
]

setup(
    name="voice-clone-lab-m3",
    version="1.0.0",
    description="Voice Clone Lab - Apple Silicon M3 Edition",
    long_description="Full training and generation support for Voice Clone Lab on Apple Silicon Macs with Metal GPU acceleration",
    author="Voice Clone Lab Contributors",
    author_email="",
    url="https://github.com/tetsuo-ai/voice_clone_lab",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "vcl=voice_clone_lab.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS 12",
        "Operating System :: MacOS :: MacOS 13",
        "Operating System :: MacOS :: MacOS 14",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="voice-clone speech-synthesis text-to-speech metal gpu apple-silicon m3",
)
