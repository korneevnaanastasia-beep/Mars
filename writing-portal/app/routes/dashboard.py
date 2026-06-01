from flask import Blueprint, render_template
from app.models import User
from app.services import STREAK_MIN_WORDS

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    user = User.query.first()
    if not user:
        return 'No user found', 404

    # Get today's stats
    from datetime import date
    from app.models import DailyLog
    today_log = DailyLog.query.filter_by(user_id=user.id, date=date.today()).first()

    # Get recent sessions
    from app.models import WritingSession
    recent_sessions = WritingSession.query.filter_by(user_id=user.id).order_by(
        WritingSession.created_at.desc()).limit(5).all()

    # Get weekly stats
    from datetime import timedelta
    week_ago = date.today()
    week_start = week_ago - timedelta(days=6)
    week_logs = DailyLog.query.filter(
        DailyLog.user_id == user.id,
        DailyLog.date >= week_start,
        DailyLog.date <= week_ago
    ).order_by(DailyLog.date).all()

    week_words = sum(log.words_written for log in week_logs)
    week_active_days = sum(1 for log in week_logs if log.words_written >= STREAK_MIN_WORDS)

    return render_template('dashboard.html',
        user=user,
        today_log=today_log,
        recent_sessions=recent_sessions,
        week_words=week_words,
        week_active_days=week_active_days,
        streak_min_words=STREAK_MIN_WORDS,
    )
