#!/bin/bash
# Setup script for Basic Morning Checklist

echo "🌅 Setting up Basic Morning Checklist..."

# Copy LaunchAgent to the correct location
echo "📋 Installing LaunchAgent..."
cp com.user.morningchecklist.plist ~/Library/LaunchAgents/

# Load the LaunchAgent
echo "🚀 Loading LaunchAgent..."
launchctl load ~/Library/LaunchAgents/com.user.morningchecklist.plist

echo ""
echo "✅ Setup complete!"
echo ""
echo "The checklist will now open automatically when you log in."
echo ""
echo "To test it now, run:"
echo "  python3 daily_checklist.py"
echo ""
echo "To view status in terminal:"
echo "  python3 daily_checklist.py list"
echo ""
echo "To uninstall:"
echo "  launchctl unload ~/Library/LaunchAgents/com.user.morningchecklist.plist"
echo "  rm ~/Library/LaunchAgents/com.user.morningchecklist.plist"
