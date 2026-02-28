#!/bin/bash

echo "🛡️  Initializing Context Guard..."

# 1. Create a hidden directory for the tool
INSTALL_DIR="$HOME/.context-guard"
mkdir -p "$INSTALL_DIR"

# 2. Create a virtual environment (so we don't mess with system python)
if [ ! -d "$INSTALL_DIR/venv" ]; then
    echo "📦 Creating isolated environment..."
    python3 -m venv "$INSTALL_DIR/venv"
fi

# 3. Download the latest scanner
echo "⬇️  Downloading scanner..."
curl -sSL https://context-guard-six.vercel.app/context_guard.py -o "$INSTALL_DIR/context_guard.py"

# 4. Install dependencies into the venv
echo "🔧 Installing dependencies (tiktoken)..."
"$INSTALL_DIR/venv/bin/pip" install -q tiktoken

# 5. Run the scanner
echo "🚀 Running scan on current directory..."
echo ""
"$INSTALL_DIR/venv/bin/python3" "$INSTALL_DIR/context_guard.py" .

echo ""
echo "✅ Done. To run again, use:"
echo "   $INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/context_guard.py ."
