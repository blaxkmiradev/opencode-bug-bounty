#!/bin/bash
# Bug Hunter Toolkit - Linux/macOS Setup
# Run: chmod +x setup-linux.sh && ./setup-linux.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "  Bug Hunter Toolkit - Setup (Linux/macOS)"
echo -e "${GREEN}========================================${NC}"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python not found! Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1)
echo -e "${GREEN}[+] Python ${PYTHON_VERSION} found${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OPENCODE_TOOLS="$HOME/.opencode/tools"

# Create symbolic link
if [ ! -d "$OPENCODE_TOOLS" ]; then
    echo -e "${YELLOW}[*] Creating OpenCode tools folder...${NC}"
    mkdir -p "$OPENCODE_TOOLS"
    ln -sf "$SCRIPT_DIR/tools" "$OPENCODE_TOOLS/tools"
fi

echo -e "${GREEN}[+] Tools linked to: $OPENCODE_TOOLS${NC}"

# Add to PATH (shell config)
SHELL_RC="$HOME/.bashrc"
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
fi

# Check if already added
if ! grep -q "bug-hunter" "$SHELL_RC" 2>/dev/null; then
    echo '' >> "$SHELL_RC"
    echo '# Bug Hunter Toolkit' >> "$SHELL_RC"
    echo "export PATH=\"$OPENCODE_TOOLS/tools/python:\$OPENCODE_TOOLS/tools/bug-hunter:\$PATH\"" >> "$SHELL_RC"
    echo -e "${GREEN}[+] PATH updated in $SHELL_RC${NC}"
fi

echo -e "${GREEN}[+] Setup complete!${NC}"

# Test tools
echo
echo -e "${GREEN}========================================${NC}"
echo -e "  Testing Tools..."
echo -e "${GREEN}========================================${NC}"

python3 "$SCRIPT_DIR/tools/python/full_scan.py" --help >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] All tools ready!${NC}"
else
    echo -e "${RED}[!] Tool test failed${NC}"
fi

echo
echo -e "${GREEN}========================================${NC}"
echo -e "  Usage Examples:"
echo -e "${GREEN}========================================${NC}"
echo "python3 tools/python/full_scan.py target.com"
echo "python3 tools/python/rce_scanner.py target.com"
echo "python3 tools/python/ssrf_scanner.py https://target.com"
echo "python3 tools/python/waf_detector.py target.com"
echo
echo -e "${YELLOW}Run: source ~/.bashrc${NC} to apply PATH changes"