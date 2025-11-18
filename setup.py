from setuptools import setup, find_packages
import shutil
from pathlib import Path

# Copy omni.py to make it available as a script
scripts = []
if Path("omni.py").exists():
    scripts.append("omni.py")

setup(
    name="omniwordlist",
    version="1.1.0",
    description="Enterprise-grade ultra-customizable wordlist generation platform - Pure Python",
    author="Aaryan Bansal",
    license="MIT",
    packages=find_packages(),
    scripts=scripts,
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "omni=omniwordlist.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
