#!/bin/bash

# OmniWordlist Pro - Local Quick Install
# Run from the project directory: ./quick-install.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}   🦀 ${YELLOW}OmniWordlist Pro${NC} - Quick Local Setup     ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════╝${NC}"
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

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

main() {
    print_header
    
    # Check if we're in the right directory
    if [ ! -f "Cargo.toml" ]; then
        print_error "Cargo.toml not found. Run this from the project root directory!"
        exit 1
    fi
    
    print_step "Checking Rust toolchain..."
    if ! command -v cargo &> /dev/null; then
        print_error "Rust/Cargo not installed. Visit https://rustup.rs"
        exit 1
    fi
    print_success "Rust is ready ($(rustc --version))"
    echo ""
    
    print_step "Building OmniWordlist Pro (release mode)..."
    echo -e "${CYAN}📦 First build takes 5-15 minutes (compiling dependencies)${NC}"
    echo -e "${CYAN}💡 Watching compilation progress:${NC}"
    echo ""
    
    # Start time for progress tracking
    START_TIME=$(date +%s)
    CRATE_COUNT=0
    
    # Run cargo with verbose output to show each crate being compiled
    if cargo build --release -v 2>&1 | while read -r line; do
        # Show which crate is being compiled
        if echo "$line" | grep -q "Compiling"; then
            CRATE_COUNT=$((CRATE_COUNT + 1))
            crate_info=$(echo "$line" | sed 's/.*Compiling \([^ ]*\).*/\1/')
            echo -e "${CYAN}  ⚙️  Compiling${NC} $crate_info"
        fi
        
        # Show dependency resolution
        if echo "$line" | grep -q "Resolving\|Updating"; then
            echo -e "${YELLOW}  🔗 ${NC}$(echo "$line" | sed 's/.*Resolving //' | sed 's/.*Updating //')"
        fi
        
        # Show when running tests
        if echo "$line" | grep -q "Running\|test"; then
            echo -e "${GREEN}  ✓ ${NC}Tests running..."
        fi
        
        # Show final status
        if echo "$line" | grep -q "Finished"; then
            ELAPSED=$(( $(date +%s) - START_TIME ))
            echo ""
            echo -e "${GREEN}  ✓ Finished in ${ELAPSED} seconds${NC}"
        fi
    done; then
        true
    else
        print_error "Build failed! Here's what went wrong:"
        echo ""
        echo -e "${YELLOW}Running build again to show error details:${NC}"
        echo ""
        cargo build --release 2>&1 | tail -50
        return 1
    fi
    echo ""
    
    # Check binary
    if [ ! -f "target/release/omni" ]; then
        print_error "Binary not created!"
        exit 1
    fi
    print_success "Binary ready at: ./target/release/omni"
    echo ""
    
    print_step "Setting up 'owpro' alias..."
    
    SHELL_RC="$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    ALIAS_CMD="alias owpro='$(pwd)/target/release/omni'"
    
    if grep -q "alias owpro=" "$SHELL_RC" 2>/dev/null; then
        print_info "Alias already exists in $SHELL_RC"
    else
        echo "" >> "$SHELL_RC"
        echo "# OmniWordlist Pro" >> "$SHELL_RC"
        echo "$ALIAS_CMD" >> "$SHELL_RC"
        print_success "Added alias to $SHELL_RC"
    fi
    echo ""
    
    print_step "Updating current shell..."
    eval "$ALIAS_CMD"
    export owpro="$(pwd)/target/release/omni"
    print_success "Alias is active now!"
    echo ""
    
    # Verify
    if owpro --version &>/dev/null || $("$(pwd)/target/release/omni" --version) &>/dev/null; then
        print_success "Verification passed!"
    fi
    echo ""
    
    # Show help
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Setup Complete! 🎉${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}You can now use:${NC}"
    echo ""
    echo -e "  ${CYAN}owpro info${NC}                                 # Show version"
    echo -e "  ${CYAN}owpro list-presets${NC}                        # List presets"
    echo -e "  ${CYAN}owpro preview --preset pentest_default${NC}    # Preview"
    echo -e "  ${CYAN}owpro run --min 3 --max 5 --charset abc${NC}   # Generate"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo ""
    echo -e "  ${CYAN}owpro run --preset pentest_default -o pentest.txt${NC}"
    echo -e "  ${CYAN}owpro run --charset 'abc123' --min 5 --max 10 --compress gzip -o out.gz${NC}"
    echo -e "  ${CYAN}owpro fields --categories${NC}"
    echo -e "  ${CYAN}owpro tui${NC}                                  # Launch interactive UI"
    echo ""
    
    # Check if alias is actually available
    if ! command -v owpro &>/dev/null; then
        echo -e "${YELLOW}⚠  To use 'owpro' command, reload your shell:${NC}"
        echo ""
        echo -e "  ${CYAN}source ~/.bashrc${NC}"
        echo ""
        echo -e "${YELLOW}Or use the full path:${NC}"
        echo ""
        echo -e "  ${CYAN}$(pwd)/target/release/omni [command]${NC}"
        echo ""
    fi
    
    echo -e "${BLUE}Documentation: https://github.com/AaryanBansal-dev/OmniWordlistPro${NC}"
    echo ""
}

main
