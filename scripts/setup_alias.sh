#!/bin/bash
#
# Setup script for YouTube Archive alias
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YTARCHIVE_PATH="$SCRIPT_DIR/ytarchive"

# Detect shell
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "Unsupported shell. Please manually add the alias to your shell configuration:"
    echo "alias ytarchive='$YTARCHIVE_PATH'"
    exit 1
fi

# Check if alias already exists
if grep -q "alias ytarchive=" "$SHELL_RC" 2>/dev/null; then
    echo "ytarchive alias already exists in $SHELL_RC"
else
    echo "Adding ytarchive alias to $SHELL_RC"
    echo "" >> "$SHELL_RC"
    echo "# YouTube Archive Tool" >> "$SHELL_RC"
    echo "alias ytarchive='$YTARCHIVE_PATH'" >> "$SHELL_RC"
    echo "Alias added successfully!"
fi

echo ""
echo "To use the alias immediately, run:"
echo "  source $SHELL_RC"
echo ""
echo "Then you can archive videos with:"
echo "  ytarchive \"https://www.youtube.com/watch?v=VIDEO_ID\""