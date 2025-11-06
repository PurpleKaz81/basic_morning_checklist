const WAKE_TARGET = '06:00';

document.addEventListener('DOMContentLoaded', () => {
  bindCheckboxes();
  bindWakeSubmit();
  bindSuggest0600();
  updateProgress();
});

function bindCheckboxes() {
  document.querySelectorAll('.task-checkbox').forEach(cb => {
      cb.addEventListener('change', (e) => {
        const { id } = cb.dataset;
        const checked = cb.checked;
        // toggle visual state immediately
        const itemEl = cb.closest('.checklist-item');
        if (itemEl) {
          if (checked) itemEl.classList.add('completed'); else itemEl.classList.remove('completed');
        }
        // call API to mark complete
        fetch('/api/complete', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: Number(id), completed: checked })
        }).then(r => r.json()).then(() => updateProgress()).catch(console.error);
      });
  });
}

function bindWakeSubmit() {
  const btn = document.getElementById('wake-submit');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const wakeTime = document.getElementById('wake-time').value;
    if (!wakeTime) { alert('Please enter a wake time'); return; }
    fetch('/api/waketime', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ wake_time: wakeTime })
    }).then(r => r.json()).then(res => {
      if (res.ok) {
        const lateEl = document.getElementById('late-result');
        if (res.minutes_late && res.minutes_late > 0) {
          lateEl.style.display = 'block';
          lateEl.textContent = `⏰ ${res.minutes_late} minute${res.minutes_late !== 1 ? 's' : ''} late`;
        } else {
          lateEl.style.display = 'none';
        }
        updateProgress();
      }
    }).catch(console.error);
  });
}

function bindSuggest0600() {
  const btn = document.getElementById('wake-fill-06');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const input = document.getElementById('wake-time');
    input.value = WAKE_TARGET;
  });
}

function updateProgress() {
  const total = document.querySelectorAll('.checklist-item').length;
  const completed = document.querySelectorAll('.checklist-item.completed, .task-checkbox:checked').length;
  const pct = Math.round((completed / total) * 100);
  const fill = document.getElementById('progress-fill');
  const text = document.getElementById('progress-text');
  if (fill) fill.style.width = pct + '%';
  if (text) text.textContent = `${completed} of ${total} completed`;
}
