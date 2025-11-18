#!/bin/bash

# OmniWordlist Pro - Python Installation Script
# Run from the project directory: ./install.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  🐍 ${YELLOW}OmniWordlist Pro${NC} - Python Setup  ${CYAN}║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════╝${NC}"
echo ""

# Check if omni.py exists
if [ ! -f "omni.py" ]; then
    echo -e "${RED}✗${NC} omni.py not found!"
    echo -e "${YELLOW}ℹ${NC} Please run this from the project root directory"
    exit 1
fi

# Check Python
echo -e "${YELLOW}▶${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 not found!"
    echo -e "${YELLOW}ℹ${NC} Install from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} $PYTHON_VERSION found"

# Install dependencies
echo -e "${YELLOW}▶${NC} Installing dependencies..."
if pip3 install click rich 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Dependencies installed (click, rich)"
else
    echo -e "${YELLOW}ℹ${NC} Could not install dependencies system-wide"
    echo -e "${YELLOW}ℹ${NC} Try: pip3 install --user click rich"
fi

# Make executable
chmod +x omni.py
echo -e "${GREEN}✓${NC} Made omni.py executable"

# Test
if python3 omni.py --version &> /dev/null; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}   Installation Complete! 🎉         ${GREEN}║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Quick Start:${NC}"
    echo -e "  python3 omni.py --help"
    echo -e "  python3 omni.py info"
    echo -e "  python3 omni.py list-presets"
    echo ""
    echo -e "${CYAN}Optional: Add to PATH${NC}"
    echo -e "  sudo ln -s \$(pwd)/omni.py /usr/local/bin/omni"
    echo ""
else
    echo -e "${RED}✗${NC} Installation test failed"
    exit 1
fi
