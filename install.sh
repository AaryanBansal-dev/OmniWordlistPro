#!/bin/bash

# OmniWordlist Pro - Automatic Installation Script
# Usage: curl -fsSL https://raw.githubusercontent.com/AaryanBansal-dev/OmniWordlistPro/main/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  🦀 ${YELLOW}OmniWordlist Pro${NC} - Installation Script         ${BLUE}║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${YELLOW}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

check_rust() {
    if ! command -v rustc &> /dev/null; then
        print_error "Rust is not installed!"
        echo ""
        echo -e "${YELLOW}Installing Rust...${NC}"
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
        print_success "Rust installed successfully!"
    else
        print_success "Rust is installed ($(rustc --version | cut -d' ' -f2))"
    fi
}

clone_repo() {
    INSTALL_DIR="${HOME}/.local/share/omniwordlist-pro"
    
    if [ -d "$INSTALL_DIR" ]; then
        print_step "Directory already exists, updating..."
        cd "$INSTALL_DIR"
        git pull origin main 2>/dev/null || true
    else
        print_step "Cloning OmniWordlist Pro repository..."
        mkdir -p "$(dirname "$INSTALL_DIR")"
        git clone https://github.com/AaryanBansal-dev/OmniWordlistPro.git "$INSTALL_DIR" 2>/dev/null || {
            print_error "Failed to clone repository. Check your internet connection."
            exit 1
        }
        cd "$INSTALL_DIR"
    fi
    
    print_success "Repository ready at: $INSTALL_DIR"
}

build_binary() {
    print_step "Building OmniWordlist Pro (this may take 2-5 minutes)..."
    
    if cargo build --release 2>&1 | grep -E "error|warning: unused" > /tmp/cargo_build.log; then
        print_error "Build had warnings/errors. Check /tmp/cargo_build.log"
        return 1
    fi
    
    if [ ! -f "target/release/omni" ]; then
        print_error "Binary not found after build!"
        return 1
    fi
    
    print_success "Binary built successfully!"
}

install_global() {
    print_step "Installing 'owpro' command globally..."
    
    BINARY_SOURCE="$(cd "$(dirname "$INSTALL_DIR")"; pwd)/omniwordlist-pro/target/release/omni"
    INSTALL_PATH="/usr/local/bin/owpro"
    
    if [ -w "/usr/local/bin" ]; then
        # No sudo needed
        cp "$BINARY_SOURCE" "$INSTALL_PATH"
        chmod +x "$INSTALL_PATH"
        print_success "Installed to /usr/local/bin/owpro (no sudo needed)"
    else
        # Need sudo
        if sudo -n true 2>/dev/null; then
            # sudo available without password
            sudo cp "$BINARY_SOURCE" "$INSTALL_PATH"
            sudo chmod +x "$INSTALL_PATH"
            print_success "Installed to /usr/local/bin/owpro (with sudo)"
        else
            # Fallback: Try to use sudo with prompt
            sudo -p "Enter password for sudo: " cp "$BINARY_SOURCE" "$INSTALL_PATH" && \
            sudo chmod +x "$INSTALL_PATH" && \
            print_success "Installed to /usr/local/bin/owpro" || {
                print_error "Failed to install globally (permission denied)"
                echo ""
                echo -e "${YELLOW}Fallback: Add to ~/.bashrc manually:${NC}"
                echo "export PATH=\"$INSTALL_DIR/target/release:\$PATH\""
                return 1
            }
        fi
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    if ! command -v owpro &> /dev/null; then
        # Try with full path if PATH hasn't been updated
        if [ ! -f "/usr/local/bin/owpro" ]; then
            print_error "Installation verification failed!"
            echo ""
            echo -e "${YELLOW}Try reloading your shell:${NC}"
            echo "source ~/.bashrc"
            return 1
        fi
    fi
    
    print_success "Installation verified!"
}

show_help() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Installation Complete! 🎉${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo ""
    echo -e "  ${YELLOW}owpro info${NC}                    # Show version & features"
    echo -e "  ${YELLOW}owpro list-presets${NC}             # List available presets"
    echo -e "  ${YELLOW}owpro preview --preset pentest_default --sample-size 50${NC}"
    echo -e "  ${YELLOW}owpro run --min 3 --max 5 --charset abc -o out.txt${NC}"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo ""
    echo -e "  # Generate pentest wordlist"
    echo -e "  ${YELLOW}owpro run --preset pentest_default -o pentest.txt${NC}"
    echo ""
    echo -e "  # Preview with meme pack"
    echo -e "  ${YELLOW}owpro preview --preset meme_humor_pack --sample-size 100${NC}"
    echo ""
    echo -e "  # Compressed output"
    echo -e "  ${YELLOW}owpro run --charset 'abc123' --min 5 --max 10 --compress gzip -o wordlist.gz${NC}"
    echo ""
    echo -e "  # List all fields"
    echo -e "  ${YELLOW}owpro fields --categories${NC}"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  📚 https://github.com/AaryanBansal-dev/OmniWordlistPro#readme"
    echo ""
    echo -e "${BLUE}Updates:${NC}"
    echo "  To update: ${YELLOW}curl -fsSL https://raw.githubusercontent.com/AaryanBansal-dev/OmniWordlistPro/main/install.sh | bash${NC}"
    echo ""
}

# Main execution
main() {
    print_header
    
    print_step "Checking prerequisites..."
    check_rust
    echo ""
    
    print_step "Cloning/updating repository..."
    clone_repo
    echo ""
    
    print_step "Building binary (release mode)..."
    build_binary
    echo ""
    
    print_step "Installing globally..."
    install_global
    echo ""
    
    print_step "Verifying installation..."
    verify_installation
    echo ""
    
    show_help
}

# Run main
main
