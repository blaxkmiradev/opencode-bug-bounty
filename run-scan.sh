#!/bin/bash
# Bug Hunter Toolkit - Quick Scanner Launcher (Linux/macOS)
# Usage: ./run-scan.sh [tool] [target]

TOOL="${1:-full}"
TARGET="${2:-localhost}"

TOOLS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/tools/python"

echo "[Running $TOOL on $TARGET]..."

case "$TOOL" in
    full)
        python3 "$TOOLS_DIR/full_scan.py" "$TARGET"
        ;;
    quick)
        python3 "$TOOLS_DIR/fast_scanner.py" "$TARGET"
        ;;
    rce)
        python3 "$TOOLS_DIR/rce_scanner.py" "$TARGET"
        ;;
    ssrf)
        python3 "$TOOLS_DIR/ssrf_scanner.py" "$TARGET"
        ;;
    xss)
        python3 "$TOOLS_DIR/xss_scanner.py" "$TARGET"
        ;;
    sqli)
        python3 "$TOOLS_DIR/sqli_scanner.py" "$TARGET"
        ;;
    web)
        python3 "$TOOLS_DIR/web_scanner.py" "$TARGET"
        ;;
    wp)
        python3 "$TOOLS_DIR/wp_scanner.py" "$TARGET"
        ;;
    waf)
        python3 "$TOOLS_DIR/waf_detector.py" "$TARGET"
        ;;
    headers)
        python3 "$TOOLS_DIR/header_analyzer.py" "$TARGET"
        ;;
    *)
        python3 "$TOOLS_DIR/$TOOL.py" "$TARGET"
        ;;
esac

echo
echo "[Done]"