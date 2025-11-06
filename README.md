# Basic Morning Checklist

A simple, free habit-tracking app that displays a morning routine checklist to help with discipline and habit formation. Launches automatically when you log into your Mac.

## Features

- ✅ Clean, modern web interface
- 🌅 Automatically opens at login
- 📊 Progress tracking
- ⏰ Wake time tracking with lateness calculation
- 💾 Persistent data storage
- 🔔 macOS notifications
- 🆓 Completely free - no API costs

## Morning Routine Checklist

1. Wake up at 06:00 (with time tracking)
2. Take morning medications
3. Put on sunscreen
4. Walk outside for 15 minutes
5. Take a cold shower and brush teeth
6. Exercise properly
7. Have a protein-filled breakfast
8. Start work between 08:30 and 09:00

## Installation

### 1. Test the App

```bash
cd ~/code/PurpleKaz81/basic_morning_checklist
python3 daily_checklist.py
```

This will open your checklist in the browser.

### 2. Set Up Auto-Launch at Login

Create the LaunchAgent file:

```bash
cp com.user.morningchecklist.plist ~/Library/LaunchAgents/
```

Load the LaunchAgent:

```bash
launchctl load ~/Library/LaunchAgents/com.user.morningchecklist.plist
```

The checklist will now open automatically when you log in to your Mac.

## Usage

### View Checklist
```bash
python3 daily_checklist.py
```
Opens the checklist in your browser.

### Check Status in Terminal
```bash
python3 daily_checklist.py list
```

### Mark Item as Complete
```bash
python3 daily_checklist.py complete <item_number>
```
Example: `python3 daily_checklist.py complete 2`

### Set Wake Time
```bash
python3 daily_checklist.py waketime HH:MM
```
Example: `python3 daily_checklist.py waketime 06:30`

### Regenerate HTML
```bash
python3 daily_checklist.py generate
```

## How It Works

- **Data Storage**: `checklist.json` stores your progress
- **Auto-Reset**: Completion status resets daily
- **Wake Time**: Special tracking for question 1 - if you answer "no" to waking up at 6:00, enter your actual wake time to see how late you were
- **Browser Interface**: Beautiful, interactive HTML checklist
- **Progress Bar**: Visual feedback on daily completion

## Uninstall

To stop auto-launch:

```bash
launchctl unload ~/Library/LaunchAgents/com.user.morningchecklist.plist
rm ~/Library/LaunchAgents/com.user.morningchecklist.plist
```

## Files

- `daily_checklist.py` - Main application script
- `checklist.json` - Data storage
- `checklist.html` - Generated HTML interface (auto-created)
- `com.user.morningchecklist.plist` - LaunchAgent configuration

## Requirements

- macOS
- Python 3.7+
- No external dependencies!

## License

MIT License - Feel free to modify and use as you wish!
