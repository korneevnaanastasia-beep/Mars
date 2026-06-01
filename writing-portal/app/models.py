from app import db
from datetime import datetime, date
import uuid

def generate_id():
    return str(uuid.uuid4())[:8]

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    name = db.Column(db.String(100), default='Писатель')
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=100)
    strength = db.Column(db.Integer, default=1)
    endurance = db.Column(db.Integer, default=1)
    intellect = db.Column(db.Integer, default=1)
    luck = db.Column(db.Integer, default=1)
    stat_points = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    crystals = db.Column(db.Integer, default=0)
    stempos = db.Column(db.Integer, default=3)
    total_words_written = db.Column(db.Integer, default=0)
    total_sessions = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_write_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sessions = db.relationship('WritingSession', backref='user', lazy=True)
    daily_logs = db.relationship('DailyLog', backref='user', lazy=True)
    
    def calculate_level(self):
        """Calculate level from XP: level² × 100 XP per level"""
        import math
        return max(1, math.floor(math.sqrt(self.xp / 100)))
    
    def xp_for_next_level(self):
        import math
        next_lvl = self.calculate_level() + 1
        return next_lvl * next_lvl * 100
    
    def xp_in_current_level(self):
        import math
        current_lvl = self.calculate_level()
        xp_at_current = current_lvl * current_lvl * 100
        return self.xp - max(0, xp_at_current)
    
    def xp_needed_in_level(self):
        current_lvl = self.calculate_level()
        next_lvl = current_lvl + 1
        return (next_lvl * next_lvl * 100) - (current_lvl * current_lvl * 100)
    
    def xp_percent(self):
        needed = self.xp_needed_in_level()
        if needed <= 0:
            return 100
        return min(100, int((self.xp_in_current_level() / needed) * 100))
    
    def get_title(self):
        titles = [
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
        lvl = self.calculate_level()
        result = titles[0]
        for t in titles:
            if lvl >= t[0]:
                result = t
        return result
    
    def to_dict(self):
        title = self.get_title()
        return {
            'id': self.id,
            'name': self.name,
            'level': self.calculate_level(),
            'xp': self.xp,
            'xp_percent': self.xp_percent(),
            'xp_in_level': self.xp_in_current_level(),
            'xp_needed': self.xp_needed_in_level(),
            'title': title[0],
            'title_icon': title[1].split(' ')[0] if ' ' in title[1] else '',
            'title_name': title[1],
            'title_color': title[2],
            'hp': self.hp,
            'strength': self.strength,
            'endurance': self.endurance,
            'intellect': self.intellect,
            'luck': self.luck,
            'stat_points': self.stat_points,
            'coins': self.coins,
            'crystals': self.crystals,
            'stempos': self.stempos,
            'total_words': self.total_words_written,
            'total_sessions': self.total_sessions,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_write_date': str(self.last_write_date) if self.last_write_date else None,
        }

class WritingSession(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    user_id = db.Column(db.String(8), db.ForeignKey('users.id'), nullable=False)
    words_written = db.Column(db.Integer, default=0)
    duration_minutes = db.Column(db.Integer, default=0)
    xp_earned = db.Column(db.Integer, default=0)
    coins_earned = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, default='')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DailyLog(db.Model):
    __tablename__ = 'daily_log'
    
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    user_id = db.Column(db.String(8), db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    words_written = db.Column(db.Integer, default=0)
    sessions_count = db.Column(db.Integer, default=0)
    xp_earned = db.Column(db.Integer, default=0)
    streak_maintained = db.Column(db.Boolean, default=False)
    goals_completed = db.Column(db.Integer, default=0)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'date'),)

class Streak(db.Model):
    __tablename__ = 'streaks'
    
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    user_id = db.Column(db.String(8), db.ForeignKey('users.id'), nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.Date, nullable=True)
    streak_frozen_days = db.Column(db.Integer, default=0)  # Stempo-frozen days count
