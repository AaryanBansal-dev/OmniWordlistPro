#!/bin/bash

# OmniWordlist Pro - Verbose Installation Script with Real-Time Progress
# This version shows detailed progress during the build process
# Usage: ./install-verbose.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Spinner characters
SPINNER=( '⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏' )
SPINNER_IDX=0

# Progress variables
BUILD_START_TIME=""
LAST_CRATE=""
CRATE_LIST=()

print_header() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  🦀 ${YELLOW}OmniWordlist Pro${NC} - Verbose Installation Script   ${BLUE}║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo ""
    echo -e "${YELLOW}▶${NC} $1"
}

print_substep() {
    echo -e "${CYAN}  └─${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

spinner() {
    local pid=$1
    local msg=$2
    
    while kill -0 $pid 2>/dev/null; do
        echo -ne "\r${SPINNER[$SPINNER_IDX]} $msg"
        SPINNER_IDX=$(( (SPINNER_IDX + 1) % ${#SPINNER[@]} ))
        sleep 0.1
    done
    echo -ne "\r✓ $msg\n"
}

check_rust() {
    print_step "Checking Rust installation..."
    
    if ! command -v rustc &> /dev/null; then
        print_warning "Rust is not installed. Installing now..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source "$HOME/.cargo/env"
        print_success "Rust installed successfully!"
    else
        RUST_VERSION=$(rustc --version)
        print_success "Rust is installed: $RUST_VERSION"
        
        CARGO_VERSION=$(cargo --version)
        print_substep "Cargo: $CARGO_VERSION"
    fi
}

clone_repo() {
    print_step "Setting up repository..."
    
    INSTALL_DIR="${HOME}/.local/share/omniwordlist-pro"
    
    if [ -d "$INSTALL_DIR" ]; then
        print_info "Directory already exists at $INSTALL_DIR"
        print_substep "Updating from remote..."
        cd "$INSTALL_DIR"
        git pull origin main 2>/dev/null || print_warning "Could not update (may be offline)"
    else
        print_info "Cloning repository..."
        mkdir -p "$(dirname "$INSTALL_DIR")"
        git clone --progress https://github.com/AaryanBansal-dev/OmniWordlistPro.git "$INSTALL_DIR" 2>&1 | while read -r line; do
            if echo "$line" | grep -q "Receiving\|Resolving"; then
                echo -e "${CYAN}  $line${NC}"
            fi
        done || {
            print_error "Failed to clone repository. Check your internet connection."
            exit 1
        }
        cd "$INSTALL_DIR"
    fi
    
    print_success "Repository ready at: $INSTALL_DIR"
}

build_binary() {
    print_step "Building OmniWordlist Pro (Release Mode)"
    echo ""
    echo -e "${YELLOW}This may take 5-15 minutes on first build${NC}"
    echo -e "${YELLOW}(Dependencies are compiled once, subsequent builds are faster)${NC}"
    echo ""
    echo -e "${CYAN}Compilation Progress:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    BUILD_START_TIME=$(date +%s)
    local temp_file=$(mktemp)
    local crate_count=0
    local crate_display_count=0
    
    # Run cargo build with verbose output, capture to file and display
    (cargo build --release -v 2>&1) > "$temp_file" &
    local cargo_pid=$!
    
    # Monitor the build output in real-time
    while kill -0 $cargo_pid 2>/dev/null; do
        # Read new lines
        while IFS= read -r line; do
            # Display compile actions
            if echo "$line" | grep -q "Compiling"; then
                crate_name=$(echo "$line" | sed 's/.*Compiling \([^ ]*\).*/\1/' | cut -d' ' -f1)
                crate_display_count=$((crate_display_count + 1))
                
                # Show crate with alternating colors
                if [ $((crate_display_count % 2)) -eq 0 ]; then
                    echo -e "${MAGENTA}  ⚙️  Compiling:${NC} $crate_name"
                else
                    echo -e "${CYAN}  ⚙️  Compiling:${NC} $crate_name"
                fi
                
                CRATE_LIST+=("$crate_name")
                crate_count=$((crate_count + 1))
                
                # Show progress every 5 crates
                if [ $((crate_count % 5)) -eq 0 ]; then
                    ELAPSED=$(( $(date +%s) - BUILD_START_TIME ))
                    echo -e "${BLUE}     (${crate_count} crates compiled in ${ELAPSED}s)${NC}"
                fi
            fi
            
            # Show dependency resolution
            if echo "$line" | grep -q "Resolving"; then
                echo -e "${YELLOW}  🔗 Resolving dependencies...${NC}"
            fi
            
            # Show if downloading packages
            if echo "$line" | grep -q "Downloading"; then
                pkg=$(echo "$line" | sed 's/.*Downloading //' | cut -d' ' -f1-2)
                echo -e "${BLUE}  ↓ Downloading: ${NC}$pkg"
            fi
            
            # Show linking
            if echo "$line" | grep -q "Linking"; then
                echo -e "${GREEN}  🔗 Linking binary...${NC}"
            fi
            
        done < "$temp_file"
        sleep 0.5
    done
    
    # Wait for the process to finish and get exit code
    wait $cargo_pid
    local build_exit_code=$?
    
    # Show final statistics
    ELAPSED=$(( $(date +%s) - BUILD_START_TIME ))
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ $build_exit_code -ne 0 ]; then
        print_error "Build failed!"
        echo ""
        echo -e "${YELLOW}Last 50 lines of build output:${NC}"
        echo ""
        tail -50 "$temp_file" | sed 's/^/  /'
        rm "$temp_file"
        return 1
    fi
    
    print_success "Build completed in ${ELAPSED} seconds!"
    print_substep "Compiled ${crate_count} crates"
    
    # Verify binary
    if [ ! -f "target/release/omni" ]; then
        print_error "Binary file not found after build!"
        rm "$temp_file"
        return 1
    fi
    
    # Show binary info
    BINARY_SIZE=$(du -h "target/release/omni" | cut -f1)
    print_success "Binary created: target/release/omni (${BINARY_SIZE})"
    
    rm "$temp_file"
}

install_global() {
    print_step "Installing global command..."
    
    BINARY_SOURCE="target/release/omni"
    INSTALL_PATH="/usr/local/bin/owpro"
    
    if [ ! -f "$BINARY_SOURCE" ]; then
        print_error "Source binary not found: $BINARY_SOURCE"
        return 1
    fi
    
    print_info "Binary source: $BINARY_SOURCE"
    print_info "Target location: $INSTALL_PATH"
    
    if [ -w "/usr/local/bin" ]; then
        # No sudo needed
        cp "$BINARY_SOURCE" "$INSTALL_PATH"
        chmod +x "$INSTALL_PATH"
        print_success "Installed to /usr/local/bin/owpro (no sudo required)"
    else
        # Need sudo
        print_info "Need elevated privileges to install to /usr/local/bin"
        
        if sudo -n true 2>/dev/null; then
            # sudo available without password
            sudo cp "$BINARY_SOURCE" "$INSTALL_PATH"
            sudo chmod +x "$INSTALL_PATH"
            print_success "Installed to /usr/local/bin/owpro (with sudo)"
        else
            # Fallback: Try to use sudo with prompt
            if sudo -p "  Enter password for sudo: " cp "$BINARY_SOURCE" "$INSTALL_PATH" && \
               sudo chmod +x "$INSTALL_PATH"; then
                print_success "Installed to /usr/local/bin/owpro"
            else
                print_error "Failed to install globally (permission denied)"
                echo ""
                print_info "Fallback: Use local binary instead"
                echo -e "${YELLOW}  $(pwd)/$BINARY_SOURCE run --help${NC}"
                return 1
            fi
        fi
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    # Test if owpro command works
    if command -v owpro &> /dev/null; then
        OWPRO_VERSION=$(owpro --version 2>/dev/null || echo "unknown")
        print_success "owpro command is available"
        print_substep "Version: $OWPRO_VERSION"
    else
        print_warning "owpro command not yet in PATH"
        print_info "You may need to reload your shell:"
        echo -e "${CYAN}    source ~/.bashrc${NC}"
    fi
}

show_completion() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}  ✅ ${YELLOW}Installation Complete!${NC}                            ${GREEN}║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${CYAN}Quick Start Commands:${NC}"
    echo ""
    echo -e "  ${YELLOW}owpro info${NC}                    # Show version & features"
    echo -e "  ${YELLOW}owpro list-presets${NC}             # List available presets"
    echo -e "  ${YELLOW}owpro preview --preset pentest_default --sample-size 50${NC}"
    echo ""
    
    echo -e "${CYAN}Usage Examples:${NC}"
    echo ""
    echo -e "  # Generate basic wordlist"
    echo -e "  ${YELLOW}owpro run --min 3 --max 5 --charset abc -o output.txt${NC}"
    echo ""
    echo -e "  # Pentesting wordlist"
    echo -e "  ${YELLOW}owpro run --preset pentest_default -o pentest.txt${NC}"
    echo ""
    echo -e "  # Compressed output (gzip)"
    echo -e "  ${YELLOW}owpro run --charset 'abc123' --min 5 --max 10 --compress gzip -o out.gz${NC}"
    echo ""
    echo -e "  # JSON format"
    echo -e "  ${YELLOW}owpro run --charset 'abc' --min 3 --max 4 --format jsonl -o out.jsonl${NC}"
    echo ""
    
    echo -e "${CYAN}Browse Fields & Presets:${NC}"
    echo ""
    echo -e "  ${YELLOW}owpro fields --categories${NC}      # List all field categories"
    echo -e "  ${YELLOW}owpro show-preset pentest_default${NC}  # Show preset details"
    echo -e "  ${YELLOW}owpro tui${NC}                      # Interactive TUI (experimental)"
    echo ""
    
    echo -e "${CYAN}Documentation:${NC}"
    echo "  📚 https://github.com/AaryanBansal-dev/OmniWordlistPro"
    echo ""
    
    echo -e "${CYAN}Get Help:${NC}"
    echo -e "  ${YELLOW}owpro --help${NC}                   # Show all commands"
    echo -e "  ${YELLOW}owpro run --help${NC}               # Help for 'run' command"
    echo ""
}

# Main execution
main() {
    print_header
    
    check_rust
    echo ""
    
    clone_repo
    echo ""
    
    build_binary
    if [ $? -ne 0 ]; then
        print_error "Build failed. Cannot continue."
        exit 1
    fi
    echo ""
    
    install_global
    echo ""
    
    verify_installation
    echo ""
    
    show_completion
}

# Run main
main
