from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
    basedir = Path(__file__).resolve().parent.parent
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(basedir / 'data' / 'portal.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ensure data directory exists
    (basedir / 'data').mkdir(exist_ok=True)
    
    # Init db
    db.init_app(app)
    
    # Register routes
    from app.routes.dashboard import dashboard_bp
    from app.routes.editor import editor_bp
    from app.routes.profile import profile_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(editor_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        from app.models import User, WritingSession, DailyLog, Streak
        db.create_all()
        # Create default user if not exists
        if not User.query.first():
            default_user = User(name='Писатель')
            db.session.add(default_user)
            db.session.commit()
    
    return app
