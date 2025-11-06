from flask import Blueprint, render_template, jsonify, request
from . import models, logic

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    data = models.load_checklist()
    data = logic.reset_if_needed(data)
    return render_template('checklist.html', data=data)


@bp.route('/api/list')
def api_list():
    data = models.load_checklist()
    return jsonify(data)


@bp.route('/api/complete', methods=['POST'])
def api_complete():
    payload = request.json or {}
    item_id = int(payload.get('id', 0))
    data = models.load_checklist()
    for item in data['items']:
        if item['id'] == item_id:
            item['completed_today'] = True
            models.save_checklist(data)
            return jsonify({'ok': True})
    return jsonify({'ok': False}), 404


@bp.route('/api/waketime', methods=['POST'])
def api_waketime():
    payload = request.json or {}
    wake_time = payload.get('wake_time')
    data = models.load_checklist()
    if logic.set_wake_time(data, wake_time):
        return jsonify({'ok': True, 'minutes_late': data['items'][0].get('minutes_late')})
    return jsonify({'ok': False}), 400
