"""XP calculation, leveling, and streak logic for the writing portal."""
import math
from datetime import date, datetime, timedelta
from app import db
from app.models import User, WritingSession, DailyLog

WORDS_PER_XP = 10       # 10 words = 1 XP
CHAPTER_XP = 500         # Completing a chapter
CHARACTER_XP = 100       # Creating a character
LORE_XP = 75             # Creating a lore note
TASK_XP = 25             # Completing a TODO task
STREAK_DAILY_XP = 50     # Base XP per streak day
STREAK_MIN_WORDS = 444   # Minimum words to maintain streak

# Streak multipliers from Warrior Dashboard
STREAK_MULTIPLIERS = {
    7: 1.5,    # 1.5x XP at 7 day streak
    30: 2.0,   # 2.0x XP at 30 day streak
    90: 2.5,   # 2.5x XP at 90 day streak
    365: 3.0,  # 3.0x XP at 365 day streak
}

TITLES = [
    (0, '🌱 Новичок', '#8bc34a'),
    (3, '✍️ Ученик пера', '#4caf50'),
    (6, '📝 Рассказчик', '#2196f3'),
    (10, '📖 Писатель', '#9c27b0'),
    (15, '⚔️ Мастер слова', '#ff9800'),
    (21, '🏆 Хранитель историй', '#f44336'),
    (30, '👑 Властелин страниц', '#ffd700'),
    (50, '🌟 Легенда пера', '#e040fb'),
    (75, '💫 Бессмертный автор', '#00e5ff'),
]


def calculate_xp_from_words(word_count):
    """Convert word count to base XP."""
    return max(0, word_count // WORDS_PER_XP)


def get_streak_multiplier(streak_days):
    """Get the XP multiplier for the current streak length."""
    mult = 1.0
    for threshold, multiplier in sorted(STREAK_MULTIPLIERS.items()):
        if streak_days >= threshold:
            mult = multiplier
    return mult


def calculate_streak_xp(streak_days):
    """Calculate streak XP with multiplier."""
    base = STREAK_DAILY_XP
    mult = get_streak_multiplier(streak_days)
    return int(base * mult)


def award_session_xp(user, words_written, duration_minutes=0):
    """Calculate and award XP for a writing session."""
    stat_points_gained = 0

    # Base XP from words
    words_xp = calculate_xp_from_words(words_written)

    # Streak multiplier
    streak_bonus = calculate_streak_xp(user.current_streak)

    # Intellect bonus: +1% XP per point
    intellect_bonus = 1.0 + (user.intellect * 0.01)

    total_xp = int((words_xp + streak_bonus) * intellect_bonus)

    # Calculate coins earned
    coins_earned = max(1, words_written // 100)

    # Check for level up before awarding
    old_level = user.calculate_level()

    user.xp += total_xp
    user.coins += coins_earned
    user.total_words_written += words_written
    user.total_sessions += 1

    # Check level up
    new_level = user.calculate_level()
    leveled_up = new_level > old_level

    if leveled_up:
        # Award stat points on level up
        stat_points_gained = (new_level - old_level)
        user.stat_points += stat_points_gained
        # Restore HP on level up
        user.hp = min(100, user.hp + 20)

    db.session.commit()

    return {
        'xp_earned': total_xp,
        'words_xp': words_xp,
        'streak_bonus': streak_bonus,
        'intellect_bonus': int(intellect_bonus * 100) - 100,
        'coins_earned': coins_earned,
        'leveled_up': leveled_up,
        'old_level': old_level,
        'new_level': new_level,
        'total_xp': user.xp,
        'stat_points_gained': stat_points_gained,
    }


def update_streak(user, words_written):
    """Update the user's streak based on today's writing."""
    today = date.today()

    if words_written < STREAK_MIN_WORDS:
        # Not enough words to maintain streak
        if user.last_write_date and user.last_write_date < today:
            # Missed a day - check if stempo can save it
            if user.stempos > 0:
                user.stempos -= 1
                # Streak preserved via stempo
                return {'streak_maintained': True, 'stempo_used': True, 'streak': user.current_streak}
            else:
                # Streak broken
                user.current_streak = 0

        return {'streak_maintained': False, 'stempo_used': False, 'streak': user.current_streak}

    # Update streak
    if user.last_write_date:
        delta = (today - user.last_write_date).days
        if delta == 1:
            # Consecutive day
            user.current_streak += 1
        elif delta == 0:
            # Same day, no change
            pass
        else:
            # Gap - check stempo
            stempos_needed = delta - 1
            if user.stempos >= stempos_needed:
                user.stempos -= stempos_needed
                user.current_streak += 1
            else:
                user.current_streak = 1
    else:
        user.current_streak = 1

    user.last_write_date = today

    # Update longest streak
    if user.current_streak > user.longest_streak:
        user.longest_streak = user.current_streak

    # HP maintenance - if writing enough, restore HP
    user.hp = min(100, user.hp + 5)

    db.session.commit()

    return {
        'streak_maintained': True,
        'stempo_used': False,
        'streak': user.current_streak,
        'longest_streak': user.longest_streak,
    }


def process_session_end(user, words_written, duration_minutes=0, content=''):
    """Process a complete writing session end-to-end."""
    # Create session record
    session = WritingSession(
        user_id=user.id,
        words_written=words_written,
        duration_minutes=duration_minutes,
        content=content,
        completed=True,
    )
    db.session.add(session)

    # Award XP
    xp_result = award_session_xp(user, words_written, duration_minutes)

    # Update streak
    streak_result = update_streak(user, words_written)

    # Fill in XP and coins on the session record
    session.xp_earned = xp_result['xp_earned']
    session.coins_earned = xp_result['coins_earned']

    # Update daily log
    today_date = date.today()
    daily_log = DailyLog.query.filter_by(user_id=user.id, date=today_date).first()
    if not daily_log:
        daily_log = DailyLog(user_id=user.id, date=today_date)
        db.session.add(daily_log)

    daily_log.words_written += words_written
    daily_log.sessions_count += 1
    daily_log.xp_earned += xp_result['xp_earned']
    daily_log.streak_maintained = streak_result['streak_maintained']
    daily_log.goals_completed += 1

    db.session.commit()

    return {
        'session': session,
        'xp': xp_result,
        'streak': streak_result,
        'daily': daily_log,
    }


def check_hp_decay(user):
    """Apply HP decay if user missed writing yesterday."""
    today = date.today()
    if user.last_write_date:
        delta = (today - user.last_write_date).days
        if delta > 1:
            # Lost days = HP loss
            lost_days = delta - 1
            hp_loss = min(10 * lost_days, 50)  # Max 50% HP loss
            user.hp = max(0, user.hp - hp_loss)
            db.session.commit()

    if user.hp <= 0:
        # Streak broken by HP hitting 0
        user.current_streak = 0
        user.hp = 20  # Reset to minimum
        db.session.commit()
        return {'hp_broken': True, 'streak_reset': True}

    return {'hp_broken': False, 'streak_reset': False}
