from datetime import date

WAKE_TARGET = '06:00'


def calculate_minutes_late(actual_time):
    if not actual_time:
        return 0
    h, m = map(int, actual_time.split(':'))
    ah = int(WAKE_TARGET.split(':')[0])
    am = int(WAKE_TARGET.split(':')[1])
    return max(0, (h * 60 + m) - (ah * 60 + am))


def reset_if_needed(data):
    today = date.today().isoformat()
    if data.get('last_reset') != today:
        # reset today's completion flags
        for item in data.get('items', []):
            item['completed_today'] = False
        data['last_reset'] = today
    return data


def set_wake_time(data, wake_time):
    # set the wake time on item 1 if exists
    items = data.get('items') or []
    if not items:
        return False
    item = items[0]
    item['actual_wake_time'] = wake_time
    item['minutes_late'] = calculate_minutes_late(wake_time)
    # optionally mark completed
    item['completed_today'] = True
    return True
