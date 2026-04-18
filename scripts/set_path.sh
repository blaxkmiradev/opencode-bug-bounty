#!/usr/bin/env bash
# Add Bug Hunter to PATH
# Usage: source set_path.sh

export BUGHUNTER_ROOT="/path/to/bug-hunter"
export PATH="$PATH:$BUGHUNTER_ROOT/tools/python:$BUGHUNTER_ROOT/scripts"

echo "Bug Hunter added to PATH"
echo "Run: run_tool <target> <tool>"
echo ""
echo "Available tools:"
echo "  run_tool target.com quick-scan"
echo "  run_tool target.com full-scan"
echo "  run_tool target.com xss"
echo "  run_tool target.com headers"