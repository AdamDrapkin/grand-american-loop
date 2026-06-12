#!/bin/bash
set -e

# Write .env from Codespaces secrets
echo "GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}" > .env
echo "SCRAPE_CREATORS_API_KEY=${SCRAPE_CREATORS_API_KEY}" >> .env
echo ".env written from Codespaces secrets"

# Install Node.js for Claude Code
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - 2>/dev/null
sudo apt-get install -y nodejs 2>/dev/null

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code 2>/dev/null && echo "Claude Code installed — run: claude" || echo "Claude Code install failed (authenticate manually after setup)"

echo ""
echo "Grand American Loop — Codespace ready"
echo "  Build viewer:     cd pre-california && python3 ../build.py"
echo "  Claude Code:      claude"
echo ""
