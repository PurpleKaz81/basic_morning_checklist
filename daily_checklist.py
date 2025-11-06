#!/usr/bin/env python3
"""
Daily Morning Routine Checklist
A habit-tracking app that helps with discipline and habit formation
"""

import json
import os
import sys
import subprocess
from datetime import datetime, time as dt_time
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
CHECKLIST_FILE = SCRIPT_DIR / "checklist.json"
HTML_FILE = SCRIPT_DIR / "checklist.html"
TARGET_WAKE_TIME = dt_time(6, 0)  # 6:00 AM


def load_checklist():
    """Load checklist from JSON file"""
    if not CHECKLIST_FILE.exists():
        return {"items": [], "last_reset": str(datetime.now().date())}

    with open(CHECKLIST_FILE, "r") as f:
        return json.load(f)


def save_checklist(data):
    """Save checklist to JSON file"""
    with open(CHECKLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)


def reset_if_needed(data):
    """Reset completion status if it's a new day"""
    today = str(datetime.now().date())
    if data.get("last_reset") != today:
        for item in data["items"]:
            if item["completed_today"]:
                item["last_completed"] = today
            item["completed_today"] = False
            # Reset wake time tracking
            if item["id"] == 1:
                item["actual_wake_time"] = None
                item["minutes_late"] = None
        data["last_reset"] = today
        save_checklist(data)
    return data


def calculate_minutes_late(wake_time_str):
    """Calculate how many minutes late the user woke up"""
    try:
        # Parse time in format HH:MM
        wake_time = datetime.strptime(wake_time_str, "%H:%M").time()
        target = datetime.combine(datetime.now().date(), TARGET_WAKE_TIME)
        actual = datetime.combine(datetime.now().date(), wake_time)

        diff = actual - target
        minutes = int(diff.total_seconds() / 60)
        return minutes if minutes > 0 else 0
    except:
        return None


def generate_html(data):
    """Generate interactive HTML checklist"""
    items_html = ""

    for item in data["items"]:
        checked = "checked" if item["completed_today"] else ""
        completed_class = "completed" if item["completed_today"] else ""

        # Special handling for wake time question
        wake_time_section = ""
        if item["id"] == 1:
            # Show only the question and a clock initially. User enters time; warning shows only if later than 06:00.
            wake_time_val = item.get("actual_wake_time", "") or ""
            late_display = (
                "block"
                if item.get("minutes_late") and item.get("minutes_late") > 0
                else "none"
            )
            late_text = ""
            if item.get("minutes_late") and item.get("minutes_late") > 0:
                minutes = item["minutes_late"]
                if minutes < 60:
                    late_text = f"⏰ {minutes} minute{'s' if minutes!=1 else ''} late"
                else:
                    hours = minutes // 60
                    mins = minutes % 60
                    late_text = (
                        f"⏰ {hours} hour{'s' if hours>1 else ''}"
                        + (f" {mins} min" if mins > 0 else "")
                        + " late"
                    )
            wake_time_section = f"""
                <div id="wake-time-input" style="display:block; margin-top:10px; margin-left:0;">
                    <label for="wake-time">At what time did you wake up?</label>
                    <input type="time" id="wake-time" value="{wake_time_val}">
                    <button id="wake-submit">Submit</button>
                </div>
                <div id="late-result" style="display: {late_display}; margin-top:10px; font-weight:bold; color:#e74c3c;">
                    {late_text}
                </div>
            """

        items_html += f"""
        <div class="checklist-item {completed_class}" data-id="{item['id']}">
            <label class="checkbox-container">
                <input type="checkbox" {checked} onchange="toggleItem({item['id']})">
                <span class="checkmark"></span>
            </label>
            <span class="task-text">{item['task']}</span>
            {wake_time_section}
        </div>
        """

    total = len(data["items"])
    completed = sum(1 for item in data["items"] if item["completed_today"])
    progress_percent = (completed / total * 100) if total > 0 else 0

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morning Routine Checklist</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}

        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 32px;
        }}

        .date {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 16px;
        }}

        .progress-bar {{
            background: #ecf0f1;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 30px;
            position: relative;
        }}

        .progress-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            width: {progress_percent}%;
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }}

        .progress-text {{
            position: absolute;
            width: 100%;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            color: {'white' if progress_percent > 30 else '#2c3e50'};
        }}

        .checklist-item {{
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 12px;
            display: flex;
            align-items: flex-start;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}

        .checklist-item:hover {{
            border-color: #667eea;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }}

        .checklist-item.completed {{
            background: #d4edda;
            border-color: #28a745;
        }}

        .checkbox-container {{
            position: relative;
            cursor: pointer;
            user-select: none;
            margin-right: 15px;
            flex-shrink: 0;
        }}

        .checkbox-container input {{
            position: absolute;
            opacity: 0;
            cursor: pointer;
        }}

        .checkmark {{
            display: block;
            height: 24px;
            width: 24px;
            background-color: white;
            border: 2px solid #667eea;
            border-radius: 6px;
            transition: all 0.2s ease;
        }}

        .checkbox-container:hover .checkmark {{
            background-color: #f0f0f0;
        }}

        .checkbox-container input:checked ~ .checkmark {{
            background-color: #667eea;
            border-color: #667eea;
        }}

        .checkmark:after {{
            content: "";
            position: absolute;
            display: none;
            left: 7px;
            top: 3px;
            width: 6px;
            height: 11px;
            border: solid white;
            border-width: 0 2px 2px 0;
            transform: rotate(45deg);
        }}

        .checkbox-container input:checked ~ .checkmark:after {{
            display: block;
        }}

        .task-text {{
            flex: 1;
            color: #2c3e50;
            font-size: 16px;
            line-height: 1.5;
        }}

        .completed .task-text {{
            color: #28a745;
        }}

        #wake-time-input {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #667eea;
        }}

        #wake-time-input label {{
            display: block;
            margin-bottom: 8px;
            color: #2c3e50;
            font-weight: 500;
        }}

        #wake-time-input input[type="time"] {{
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            margin-right: 10px;
        }}

        #wake-time-input button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background 0.2s;
        }}

        #wake-time-input button:hover {{
            background: #5568d3;
        }}

        #late-result {{
            padding: 12px;
            border-radius: 8px;
            background: #fff3cd;
            border: 2px solid #ffc107;
        }}

        .refresh-note {{
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌅 Morning Routine</h1>
        <div class="date">{datetime.now().strftime('%A, %B %d, %Y')}</div>

        <div class="progress-bar">
            <div class="progress-fill"></div>
            <div class="progress-text">{completed} of {total} completed</div>
        </div>

        <div class="checklist">
            {items_html}
        </div>

        <div class="refresh-note">
            Refresh the page to see updated status
        </div>
    </div>

    <script>
        const WAKE_TARGET = '06:00';
        const STORAGE_KEY = 'morningChecklistState';
        const TODAY = '{datetime.now().date()}';

        function startClock() {{
            const el = document.getElementById('wake-clock');
            if (!el) return;
            function tick() {{
                const now = new Date();
                const hh = String(now.getHours()).padStart(2,'0');
                const mm = String(now.getMinutes()).padStart(2,'0');
                el.textContent = `${{hh}}:${{mm}}`;
            }}
            tick();
            setInterval(tick, 1000);
        }}

        function compareTimes(t1, t2) {{
            const [h1,m1] = t1.split(':').map(Number);
            const [h2,m2] = t2.split(':').map(Number);
            return (h1*60 + m1) - (h2*60 + m2);
        }}

        function loadState() {{
            try {{
                const raw = localStorage.getItem(STORAGE_KEY + '_' + TODAY);
                return raw ? JSON.parse(raw) : {{ items: {{}}, wakeTime: null }};
            }} catch (e) {{
                return {{ items: {{}}, wakeTime: null }};
            }}
        }}

        function saveState(state) {{
            localStorage.setItem(STORAGE_KEY + '_' + TODAY, JSON.stringify(state));
        }}

        function onCheckboxChange(id, checkbox, itemEl) {{
            const state = loadState();
            state.items = state.items || {{}};
            state.items[id] = checkbox.checked;
            if (checkbox.checked) itemEl.classList.add('completed'); else itemEl.classList.remove('completed');
            saveState(state);
            updateProgress();
        }}

        function submitWakeTime() {{
            const wakeInput = document.getElementById('wake-time');
            const wakeTime = wakeInput && wakeInput.value;
            if (!wakeTime) {{ alert('Please enter a wake time'); return; }}
            const state = loadState();
            state.wakeTime = wakeTime;
            saveState(state);
            const diff = compareTimes(wakeTime, WAKE_TARGET);
            const lateEl = document.getElementById('late-result');
            if (diff > 0) {{
                lateEl.style.display = 'block';
                lateEl.textContent = `⏰ ${{diff}} minute${{diff!==1? 's' : ''}} late`;
                lateEl.style.color = '#721c24';
                lateEl.style.background = '#f8d7da';
                lateEl.style.borderColor = '#f5c6cb';
            }} else {{
                lateEl.style.display = 'none';
                // if on time or early, mark item 1 completed
                const item1 = document.querySelector('.checklist-item[data-id="1"]');
                if (item1) {{
                    const cb = item1.querySelector('input[type="checkbox"]');
                    if (cb) {{ cb.checked = true; item1.classList.add('completed'); state.items = state.items || {{}}; state.items['1'] = true; saveState(state); updateProgress(); }}
                }}
            }}
        }}

        function updateProgress() {{
            const items = document.querySelectorAll('.checklist-item');
            const total = items.length;
            let completed = 0;
            items.forEach(item => {{ if (item.classList.contains('completed')) completed++; }});
            const fill = document.querySelector('.progress-fill');
            const text = document.querySelector('.progress-text');
            const percent = total ? Math.round((completed/total)*100) : 0;
            if (fill) fill.style.width = percent + '%';
            if (text) text.textContent = `${{completed}} of ${{total}} completed`;
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            startClock();
            const state = loadState();
            // restore wake time late display
            if (state.wakeTime) {{
                const diff = compareTimes(state.wakeTime, WAKE_TARGET);
                const lateEl = document.getElementById('late-result');
                if (diff > 0) {{ lateEl.style.display = 'block'; lateEl.textContent = `⏰ ${{diff}} minute${{diff!==1? 's' : ''}} late`; }}
                const wakeInput = document.getElementById('wake-time'); if (wakeInput) wakeInput.value = state.wakeTime;
            }}

            // wire checkboxes
            const items = document.querySelectorAll('.checklist-item');
            items.forEach(item => {{
                const id = item.getAttribute('data-id');
                const checkbox = item.querySelector('input[type="checkbox"]');
                if (!checkbox) return;
                if (state.items && state.items[id]) {{ checkbox.checked = true; item.classList.add('completed'); }}
                checkbox.addEventListener('change', () => onCheckboxChange(id, checkbox, item));
            }});

            const btn = document.getElementById('wake-submit');
            if (btn) btn.addEventListener('click', submitWakeTime);
            updateProgress();
        }});
    </script>
</body>
</html>
    """

    with open(HTML_FILE, "w") as f:
        f.write(html_content)


def send_notification(title, message):
    """Send macOS notification"""
    script = f"""
    display notification "{message}" with title "{title}"
    """
    subprocess.run(["osascript", "-e", script], capture_output=True)


def open_browser():
    """Open the HTML file in default browser"""
    subprocess.run(["open", str(HTML_FILE)])


def complete_item(data, item_id):
    """Mark an item as complete"""
    for item in data["items"]:
        if item["id"] == item_id:
            item["completed_today"] = True
            save_checklist(data)
            return True
    return False


def set_wake_time(data, wake_time_str):
    """Set wake time for item 1 and calculate lateness"""
    for item in data["items"]:
        if item["id"] == 1:
            item["actual_wake_time"] = wake_time_str
            item["minutes_late"] = calculate_minutes_late(wake_time_str)
            save_checklist(data)
            return True
    return False


def show_list():
    """Show checklist in terminal"""
    data = load_checklist()
    data = reset_if_needed(data)

    print("\n🌅 Morning Routine Checklist")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}\n")

    for item in data["items"]:
        status = "✅" if item["completed_today"] else "⬜"
        print(f"{status} {item['id']}. {item['task']}")

        if item["id"] == 1 and item.get("actual_wake_time"):
            minutes = item.get("minutes_late", 0)
            if minutes == 0:
                print(f"   ✅ On time!")
            elif minutes < 60:
                print(f"   ⏰ {minutes} minutes late")
            else:
                hours = minutes // 60
                mins = minutes % 60
                print(
                    f"   ⏰ {hours} hour{'s' if hours > 1 else ''}"
                    + (f" {mins} min" if mins > 0 else "")
                    + " late"
                )

    completed = sum(1 for item in data["items"] if item["completed_today"])
    total = len(data["items"])
    print(f"\n📊 Progress: {completed}/{total} completed\n")


def main():
    """Main entry point"""
    data = load_checklist()
    data = reset_if_needed(data)

    if len(sys.argv) == 1:
        # No arguments: generate HTML and open browser
        generate_html(data)
        open_browser()
        send_notification("Morning Routine", "Your daily checklist is ready!")

    elif sys.argv[1] == "list":
        # Show in terminal
        show_list()

    elif sys.argv[1] == "complete" and len(sys.argv) == 3:
        # Complete an item
        try:
            item_id = int(sys.argv[2])
            if complete_item(data, item_id):
                generate_html(data)
                print(f"✅ Item {item_id} marked as complete!")
            else:
                print(f"❌ Item {item_id} not found")
        except ValueError:
            print("❌ Invalid item ID")

    elif sys.argv[1] == "waketime" and len(sys.argv) == 3:
        # Set wake time
        wake_time = sys.argv[2]
        if set_wake_time(data, wake_time):
            generate_html(data)
            print(f"⏰ Wake time set to {wake_time}")
        else:
            print("❌ Could not set wake time")

    elif sys.argv[1] == "generate":
        # Just generate HTML without opening
        generate_html(data)
        print("✅ HTML generated")

    else:
        print("Usage:")
        print("  python3 daily_checklist.py              - Show checklist in browser")
        print("  python3 daily_checklist.py list         - Show checklist in terminal")
        print("  python3 daily_checklist.py complete <id> - Mark item as complete")
        print("  python3 daily_checklist.py waketime HH:MM - Set wake time")


if __name__ == "__main__":
    main()
