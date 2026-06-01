from flask import Blueprint, render_template
from app.models import User
from app.services import TITLES

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
def profile():
    user = User.query.first()
    if not user:
        return 'No user found', 404

    # Get all-time stats
    from app.models import WritingSession, DailyLog
    total_sessions = WritingSession.query.filter_by(user_id=user.id).count()
    total_days = DailyLog.query.filter_by(user_id=user.id).count()
    active_days = DailyLog.query.filter(
        DailyLog.user_id == user.id,
        DailyLog.streak_maintained == True
    ).count()

    # Get weekly chart data
    from datetime import date, timedelta
    week_data = []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        log = DailyLog.query.filter_by(user_id=user.id, date=d).first()
        week_data.append({
            'day': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'][d.weekday()],
            'words': log.words_written if log else 0,
            'active': log.streak_maintained if log else False,
        })

    return render_template('profile.html',
        user=user,
        titles=TITLES,
        total_sessions=total_sessions,
        total_days=total_days,
        active_days=active_days,
        week_data=week_data,
    )
