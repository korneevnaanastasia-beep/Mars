from flask import Blueprint, request, jsonify
from app import db
from app.models import User, WritingSession, DailyLog
from app.services import process_session_end, check_hp_decay
from datetime import date

api_bp = Blueprint('api', __name__)


@api_bp.route('/session/end', methods=['POST'])
def end_session():
    """End a writing session and award XP."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user = User.query.first()
    if not user:
        return jsonify({'error': 'No user found'}), 404

    words_written = data.get('words', 0)
    duration_minutes = data.get('duration', 0)
    content = data.get('content', '')

    if words_written <= 0:
        return jsonify({'error': 'No words written'}), 400

    result = process_session_end(user, words_written, duration_minutes, content)

    return jsonify({
        'success': True,
        'words': words_written,
        'duration': duration_minutes,
        'xp_earned': result['xp']['xp_earned'],
        'coins_earned': result['xp']['coins_earned'],
        'leveled_up': result['xp']['leveled_up'],
        'new_level': result['xp']['new_level'],
        'current_streak': result['streak']['streak'],
        'user': user.to_dict(),
    })


@api_bp.route('/user/stats', methods=['GET'])
def get_user_stats():
    """Get current user stats."""
    user = User.query.first()
    if not user:
        return jsonify({'error': 'No user found'}), 404

    # Check HP decay
    check_hp_decay(user)

    # Get today's stats
    today_log = DailyLog.query.filter_by(user_id=user.id, date=date.today()).first()

    return jsonify({
        'user': user.to_dict(),
        'today_words': today_log.words_written if today_log else 0,
        'today_sessions': today_log.sessions_count if today_log else 0,
    })


@api_bp.route('/session/save', methods=['POST'])
def save_session():
    """Auto-save a session in progress."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user = User.query.first()
    if not user:
        return jsonify({'error': 'No user found'}), 404

    words_written = data.get('words', 0)
    content = data.get('content', '')
    duration_minutes = data.get('duration', 0)

    # Save or update current session
    session = WritingSession(
        user_id=user.id,
        words_written=words_written,
        duration_minutes=duration_minutes,
        content=content,
        completed=False,
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({'success': True, 'session_id': session.id})


@api_bp.route('/streak/repair', methods=['POST'])
def repair_streak():
    """Use a stempo to repair the streak."""
    user = User.query.first()
    if not user:
        return jsonify({'error': 'No user found'}), 404

    if user.stempos <= 0:
        return jsonify({'error': 'No stempos available'}), 400

    user.stempos -= 1
    user.current_streak = max(1, user.current_streak)
    db.session.commit()

    return jsonify({
        'success': True,
        'stempos_left': user.stempos,
        'current_streak': user.current_streak,
    })
